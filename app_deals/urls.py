from django.urls import path
from app_deals.views import *

urlpatterns = [
    # Пути templates - html:
    path('', DealsUploadPage.as_view(), name='upload_deals_html'),
    path('get_deals', deals_get_page, name='get_deals_html'),
    
    # Пути API
    path('api/v1/upload_csv', DealAPIList.as_view(), name='upload_deals_api'),
    path('api/v1/deallist', DealAPIView.as_view()),
    path('api/v1/deallistget', DealAPIView.as_view()),
]