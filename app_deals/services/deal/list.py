from django import forms
from django.db.models import Sum, Count
from django.db.models.functions import Concat
from app_deals.models import Deal, File_load, User
from functools import lru_cache
from service_objects.services import Service
class TopDealListService(Service):
    """API service class for add photo"""
    top_clients = forms.IntegerField()
    min_limit_gem = forms.IntegerField()
    # custom_validations = ["validate_top_clients","validate_min_limit_gem"]


    def process(self):
        self.validate_top_clients()
        self.validate_min_limit_gem()
        # self.run_custom_validations()
        self.result = self._get_top_deals
        return self

    @property
    def _get_top_deals(self):
        top_clients = self._get_top_clients()
        count_distinct_users_for_gem = self._get_count_distinct_users_for_gem()
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
        return result
    
    @lru_cache
    def _get_top_clients(self):
        return Deal.objects.filter(
            csv_file=File_load.objects.order_by('-id').first()
            ).values('username').annotate(
            spent_money=Sum('spent_money')
            ).order_by('-spent_money')[:self.cleaned_data['top_clients']]
    
    def _get_count_distinct_users_for_gem(self):
      return Deal.objects.values('gem').filter(
          username__in=self._get_top_clients().values_list('username', flat=True)).annotate(
          qty_buy=Count(Concat('gem', 'username'), distinct=True)).filter(qty_buy__gte=self.cleaned_data['min_limit_gem'])


    def validate_top_clients(self):
        if type(self.cleaned_data['top_clients']) != int or self.cleaned_data['top_clients']<=0:
            raise Exception(f'Invalid top_clients value {self.cleaned_data["top_clients"]}')
    
    def validate_min_limit_gem(self):
        if type(self.cleaned_data['min_limit_gem']) != int or self.cleaned_data['min_limit_gem']<=0:
            raise Exception(f'Invalid min_limit_gem value {self.cleaned_data["min_limit_gem"]}')