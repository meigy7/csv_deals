from django.urls import path
# from app_deals import views
from app_deals.views import DealsUploadPage

urlpatterns = [
    path('', DealsUploadPage.as_view(), name='upload_deals'),
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),
]