from django.db import models

# Create your models here.


class Ads(models.Model):
    Id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=2000)
    author = models.CharField(max_length=2000)
    price = models.CharField(max_length=2000)
    description = models.CharField(max_length=3000)
    address = models.CharField(max_length=2000)
    is_published = models.CharField(max_length=2000)


class Categories(models.Model):
    STATUS = [
        ('draft', 'Черновик'),
        ('open', "Открыто"),
        ('closed', "Закрыто")
    ]

    id = models.IntegerField(primary_key=True)

    slug = models.SlugField(max_length=50, default='')
    name = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default='draft')
    created = models.DateField(auto_now_add=True)
