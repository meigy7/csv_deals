from django.urls import path
from app_deals.views import *

urlpatterns = [
    # Пути templates - html:
    path('', DealsUploadPage.as_view(), name='upload_deals_html'),
    path('get_deals', DealsFilterPage.as_view(), name='get_deals_html'),
    
    # Пути API
    path('api/v1/upload_csv', UploadFileView.as_view(), name='upload_deals_api'),
    # path('api/v1/get_top_clients/<int:pk>/', DealGetView.as_view()),
    path('api/v1/get_top_clients/', DealGetView.as_view()),
]