from django.db import models

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=100, null=True, blank=True)
  def __str__(self):
    return self.name

class Deal(models.Model):
  time_deal = models.DateTimeField(verbose_name="Время сделки")
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Юзер")
  gem = models.ForeignKey('Gem', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Камень")
  quantity = models.IntegerField(verbose_name="Количество")
  spent_money = models.FloatField(verbose_name="Сумма покупки")
  csv_file = models.ForeignKey('File_load', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Файл CSV")
  def __str__(self):
    return self.username.name
  
class Gem(models.Model):
  name = models.CharField(max_length=100, null=True, blank=True)
  def __str__(self):
    return self.name

class File_load(models.Model):
  csv_file = models.FileField(upload_to='deals', null=True, blank=True, verbose_name="Файл CSV")
  def __str__(self):
    return str(self.csv_file)