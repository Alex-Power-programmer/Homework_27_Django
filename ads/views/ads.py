import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView

from ads.serializers import AdSerializer
from avito import settings
from ads.models import Category, Ad, User


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by('-price')
        cat_id = request.GET.get('cat')
        if cat_id:
            self.queryset = self.queryset.filter(
                category_id__in=cat_id
            )

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(
                name__icontains=text
            )

        location_q = None
        locations = request.GET.get('location')
        if locations:
            self.queryset = self.queryset.filter(
                author__locations__name__icontains=locations
            )

        price_from = request.GET.get('price_from', 0)
        price_to = request.GET.get('price_to', 10000)
        if price_from:
            self.queryset = self.queryset.filter(
                price__gte=int(price_from)
            )
        if price_to:
            self.queryset = self.queryset.filter(
                price__lte=int(price_to)
            )

        return super().get(request, *args, **kwargs)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        }, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, pk=ad_data['author_id'])
        category = get_object_or_404(Category, pk=ad_data['category_id'])

        ad = Ad.objects.create(
            name=ad_data['name'],
            author=author,
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data["is_published"],
            category=category
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        }, safe=False, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data['name']
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.author = get_object_or_404(User, pk=ad_data['author_id'])
        self.object.category = get_object_or_404(Category, pk=ad_data['category_id'])

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image', None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, status=200)
