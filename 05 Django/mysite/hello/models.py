from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Data(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    data = models.CharField(max_length=200)

    def __str__(self):
        return self.data
