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
from django.db.models import Sum, Count
from django.db.models.functions import Concat
import pytz
import csv


class DealAPIList(generics.ListCreateAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class DealsUploadPage(APIView):
    def get(self, request):
        template = loader.get_template('deals_list/file_upload.html')
        context = {}
        return HttpResponse(template.render(context, request))


class DealAPIView(APIView):
    def post(self, request):
        csv_file = request.data['deals']
        # print('csv_file:\n',csv_file)
        file_data = {'csv_file':csv_file}
        serializer = File_loadSerializer(data=file_data)
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
            return Response({'msg':'Файл был обработан без ошибок!', 'data':serializer.data}, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({'msg':'В процессе обработки файла произошла ошибка:', 'errors':[str(e), serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        model = Deal.objects.all()
        serializer = DealSerializer(model, many=True)
        return Response(serializer.data)



def deals_get_page(request):
    template = loader.get_template('deals_list/get_deals.html')
    context = {}
    def get_top_clients(num_clients, gem_limit):
        top_clients = (
            Deal.objects
            .values('username')
            .annotate(spent_money=Sum('spent_money'))
            .order_by('-spent_money')
            [:num_clients]
            )
        
        count_distinct_users_for_gem = (
            Deal.objects
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
        print('result:\n', result)
        return result
    top_clients = get_top_clients(5,2)
    print('Готово!')
    
    
    
    return HttpResponse(template.render(context, request))









# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Deal.objects.all()
#         serializer = DealSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = DealSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Deal.objects.get(pk=pk)
#     except Deal.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = DealSerializer(snippet)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = DealSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)




        # if request.form.get('type_action') == 'update_settings_binv5':
        #     if request.form.get("min_trade_turnover_binv5") != None:
        #         # db.query(ConfigSite).filter_by(name="min_trade_turnover_binv5").first().value = request.form["min_trade_turnover_binv5"]
        #         try:
        #             min_trade_turnover = float(
        #                 request.form["min_trade_turnover_binv5"])
        #             db.query(User).filter_by(id=current_user.id).first(
        #             ).min_trade_turnover_binv5 = request.form["min_trade_turnover_binv5"]
        #         except Exception as e:
        #             print('Минимальный торговый оборот задан в неправильном формате', e)




# class DealAPIView(generics.ListAPIView):
#     queryset = Deal.objects.all()
#     serializer_class = DealSerializer
