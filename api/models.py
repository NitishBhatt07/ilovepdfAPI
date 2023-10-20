from django.db import models


class uploadFileModel(models.Model):
    myfile = models.FileField()