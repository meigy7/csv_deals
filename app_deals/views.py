# -*- coding: UTF-8 -*- 
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Deal, File_load, User, Gem
from .serializers import DealSerializer, File_loadSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.template import loader
import os, time
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Value
from django.db.models.functions import Concat
#
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
import pytz
import csv


# HTML Upload page
class DealsUploadPage(APIView):
    def get(self, request):
        template = loader.get_template('deals_list/file_upload.html')
        context = {}
        return HttpResponse(template.render(context, request))
    
# HTML Filter page
class DealsFilterPage(APIView):
    def get(self, request):
        template = loader.get_template('deals_list/get_deals.html')
        context = {}
        return HttpResponse(template.render(context, request))


# API post = Upload function; 
class UploadFileView(generics.CreateAPIView):
    serializer_class = File_loadSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        file_name = File_load.objects.order_by('-id').first()
        try:
            with open('media/'+str(file_name.csv_file), 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                next(reader, None)
                Deal.objects.bulk_create([
                    Deal(
                    time_deal=pytz.timezone('Asia/Krasnoyarsk').localize(datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')),
                    username=User.objects.get_or_create(name=row[0],defaults={'name':row[0]})[0],
                    gem=Gem.objects.get_or_create(name=row[1],defaults={'name':row[1]})[0],
                    quantity=row[3],
                    spent_money=row[2],
                    csv_file=file_name) for row in reader])
                f.close()
            return Response({'msg':'Файл был обработан без ошибок!', 'data':serializer.data}, status=status.HTTP_201_CREATED) 
        except Exception as e:
            return Response({'msg':'В процессе обработки файла произошла ошибка:', 'errors':[str(e), serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)



# API get = Filter function;
class DealGetView(generics.ListAPIView):
    serializer_class = DealSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        # num_clients=self.kwargs['pk']
        # name = self.request.query_params.get('term')
        num_clients=5
        gem_limit=2 
        top_clients = (
            self.model.objects
            .filter(csv_file=File_load.objects.order_by('-id').first())
            .values('username')
            .annotate(spent_money=Sum('spent_money'))
            .order_by('-spent_money')
            [:num_clients]
            )   
        print('top_clients', top_clients)
        
        count_distinct_users_for_gem = (
            self.model.objects    
            .values('gem')
            .filter(username__in=top_clients.values_list('username', flat=True))
            .annotate(qty_buy=Count(Concat('gem', 'username'), distinct=True))
            .filter(qty_buy__gte=gem_limit)
            )
        print('\ncount_distinct_users_for_gem:\n', count_distinct_users_for_gem)

        result = []
        for client in top_clients:
            gems = (
                self.model.objects
                .values_list('gem', flat=True)
                .filter(username=client['username'])
                .distinct()
                .filter(gem__in=count_distinct_users_for_gem.values_list('gem', flat=True))
            )
            client_data = {
                'username': client['username'],
                'spent_money': client['spent_money'],
                'gems': list(gems)
            }
            result.append(client_data)

        # q1 = self.model.objects.all().filter(csv_file=File_load.objects.order_by('-id').first()).values('username').annotate(spent_money=Sum('spent_money')).order_by('-spent_money')[:num_clients]
        # q2 = self.model.objects.all().values('gem').filter(username__in=top_clients.values_list('username', flat=True)).annotate(qty_buy=Count(Concat('gem', 'username'), distinct=True)).filter(qty_buy__gte=gem_limit)
        # result = q1 | q2
        print('result:\n', result)
        queryset = result
        return queryset








''' Вариант №2
def get_queryset(self):
    serializer = self.get_serializer(data=self.request.data)
    serializer.is_valid(raise_exception=True)
    # num_clients = self.kwargs['pk']
    num_clients = 5
    gem_limit = 2

    top_clients = (
        self.model.objects
        .filter(csv_file=File_load.objects.order_by('-id').first())
        .values('username')
        .annotate(spent_money=Sum('spent_money'))
        .order_by('-spent_money')
        [:num_clients]
    )

    print('top_clients', top_clients)

    count_distinct_users_for_gem = (
        self.model.objects    
        .values('gem')
        .filter(username__in=top_clients.values_list('username', flat=True))
        .annotate(qty_buy=Count(Concat('gem', 'username'), distinct=True))
        .filter(qty_buy__gte=gem_limit)
    )

    print('\ncount_distinct_users_for_gem:\n', count_distinct_users_for_gem)

    gems_query = (
        self.model.objects
        .values_list('gem', flat=True)
        .filter(username__in=top_clients.values_list('username', flat=True))
        .distinct()
        .filter(gem__in=count_distinct_users_for_gem.values('gem'))
    )

    result = (
        top_clients
        .annotate(gems=Concat(Value('['), Concat.Agg(gems_query), Value(']')))
        .values('username', 'spent_money', 'gems')
    )

    return QuerySet(model=self.model, query=result.query, using=self.model._db)

'''






# Класс фильтров
# class DealGetFilter(filters.FilterSet):
#     createdtimestamp = filters.BooleanFilter(
#         field_name='createdtimestamp', method='filter_a_week_from_date'
#     )

#     class Meta:
#         model = MeterLake
#         fields = ['createdtimestamp', 'siteid']

#     def filter_a_week_from_date(self, queryset, name, value):
#         lookup = f'{name}__gte'
#         dateformat = '%Y-%m-%d' # replace with expected value format.
#         # value may be serialized already, thus not needing to be parsed here.
#         value = datetime.strptime(value, dateformat) + timedelta(days=7)
#         return queryset.filter(**{lookup: value})



# filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # queryset = model.objects.all()
    
    # ordering_fields = ["created_at", "pr"]
    # filter_class = PmPFilter
    # fields = ("created_at", "pr", "li__pro__e")
    # filter_fields = fields
    # search_fields = fields
    

    # paginate_by = 100
    # def get_queryset(self):
    #     queryset = self.model.objects.all()
    #     return queryset
    # def get_context_data(self,**kwargs):
    #     context = super(CarList,self).get_context_data(**kwargs)
    #     context['picture'] = Picture.objects.filter(your_condition)
    #     return context












# num_clients=10
# gem_limit=3  
# top_clients = (
#     self.model.objects
#     .filter(csv_file=File_load.objects.order_by('-id').first())
#     .values('username')
#     .annotate(spent_money=Sum('spent_money'))
#     .order_by('-spent_money')
#     [:num_clients]
#     )
# queryset = self.model.objects.values('username').filter(csv_file=File_load.objects.order_by('-id').first())
# return queryset
# print('Point 1')
# count_distinct_users_for_gem = (
#     self.model.objects    
#     .values('gem')
#     .filter(username__in=top_clients.values_list('username', flat=True))
#     .annotate(qty_buy=Count(Concat('gem', 'username'), distinct=True))
#     .filter(qty_buy__gte=gem_limit)
#     )
# print('\ncount_distinct_users_for_gem:\n', count_distinct_users_for_gem)

# result = []
# for client in top_clients:
#     gems = (
#         self.model.objects
#         .values_list('gem', flat=True)
#         .filter(username=client['username'])
#         .distinct()
#         .filter(gem__in=count_distinct_users_for_gem.values_list('gem', flat=True))
#     )
#     client_data = {
#         'username': client['username'],
#         'spent_money': client['spent_money'],
#         'gems': list(gems)
#     }
#     result.append(client_data)
# print('result:\n', result)
# queryset = top_clients
# return queryset