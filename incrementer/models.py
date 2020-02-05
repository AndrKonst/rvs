from django.db import models


class Num(models.Model):
    num = models.PositiveIntegerField(primary_key=True)

class Error_log(models.Model):
    err = models.CharField(max_length=7)
    date_time = models.DateTimeField(auto_now_add=True, db_index=True)
    number = models.ForeignKey(Num, on_delete=models.CASCADE)