from django.urls import path
from app_deals.views import *

urlpatterns = [
    # Пути templates - html:
    path('', DealsUploadPage.as_view(), name='upload_deals_html'),
    
    # Пути API
    path('api/v1/upload_csv', UploadFileView.as_view(), name='upload_deals_api'),
    # path('api/v1/get_top_clients/', DealGetView.as_view()),
    path('api/v1/get_top_clients/<int:pk>/<int:pt>/', DealGetView.as_view()),
]