from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

        
class UserRequest(models.Model):
    requests = models.JSONField(default=dict)

    class Meta:
        verbose_name = "User request"
        verbose_name_plural = "User requests"

    def __str__(self):
        return (str(self.id))
