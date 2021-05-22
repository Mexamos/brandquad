from django.db import models


class DataLog(models.Model):
    ip = models.CharField(max_length=16)
    date = models.DateTimeField(db_index=True)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=200, db_index=True)
    response_status = models.IntegerField(db_index=True)
    response_size = models.IntegerField()
