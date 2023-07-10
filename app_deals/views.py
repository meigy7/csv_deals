# -*- coding: UTF-8 -*- 
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum, Count
from django.db.models.functions import Concat
from .models import Deal, File_load, User, Gem
from .serializers import *
#
from datetime import datetime
import pytz
import csv


# HTML Upload page
class DealsUploadPage(APIView):
    def get(self, request):
        template = loader.get_template('deals_list/file_upload.html')
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
    serializer_class = DealSerializer_top
    def get_queryset(self):
        num_clients = self.kwargs['pk']
        gem_limit = self.kwargs['pt']
        # num_clients, gem_limit=5, 2
        top_clients = (
            Deal.objects.all()
            .filter(csv_file=File_load.objects.order_by('-id').first())
            .values('username')
            .annotate(spent_money=Sum('spent_money'))
            .order_by('-spent_money')
            [:num_clients]
            )   
        print('top_clients', top_clients)
        
        count_distinct_users_for_gem = (
            Deal.objects.all()
            .values('gem')
            .filter(username__in=top_clients.values_list('username', flat=True))
            .annotate(qty_buy=Count(Concat('gem', 'username'), distinct=True))
            .filter(qty_buy__gte=gem_limit)
            )
        print('\ncount_distinct_users_for_gem:\n', count_distinct_users_for_gem)

        result = []
        for client in top_clients:
            gems = (
                Deal.objects
                .values_list('gem__name', flat=True)
                .filter(username=client['username'])
                .distinct()
                .filter(gem__in=count_distinct_users_for_gem.values_list('gem', flat=True))
            )
            client_data = {
                'username': str(User.objects.all().filter(id = client['username']).first()),
                'spent_money': client['spent_money'],
                'gems': list(gems)
            }
            result.append(client_data)
        print('result:\n', result)
        
        serializer = DealSerializer_top(data=result, many=True)
        print('serializer:\n', serializer)
        if serializer.is_valid():
            serialized_data = serializer.data
            print('Serializer is valid', serialized_data)
            return serialized_data
        else:
            return print('Error! Serializer is not valid', serializer.errors)