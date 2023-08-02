from django.db import models

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
  def __str__(self):
    return str(self.name)

class Gem(models.Model):
  name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
  def __str__(self):
    return str(self.name)
  
class File_load(models.Model):
  csv_file = models.FileField(upload_to='deals', null=True, blank=True, verbose_name="File CSV")
  def __str__(self):
    return str(self.csv_file)

class Deal(models.Model):
  time_deal = models.DateTimeField(verbose_name="Deal Time")
  username = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
  gem = models.ForeignKey('Gem', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Gem")
  quantity = models.PositiveIntegerField(verbose_name="Quantity")
  spent_money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sum buy")
  csv_file = models.ForeignKey('File_load', on_delete=models.CASCADE, null=True, blank=True, verbose_name="File CSV")
  def __str__(self):
    return f"{self.username} - {self.gem}"