from django.db import models
from django.utils import timezone


class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated_at = models.DateTimeField(default=timezone.now)
    api_token = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.last_updated_at = timezone.now()
        super().save(*args, **kwargs)


class Document(models.Model):
    id = models.BigAutoField(primary_key=True)
    openID = models.IntegerField()
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated_at = models.DateTimeField(default=timezone.now)
    companyID = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    externalID = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.last_updated_at = timezone.now()
        super().save(*args, **kwargs)


class Signer(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    externalID = models.CharField(max_length=255, null=True, blank=True)
    documentID = models.ForeignKey('Document', on_delete=models.CASCADE, null=True, blank=True)
