import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Categories, Ads


# Create your views here.


def index(request):
    return JsonResponse({"status": "Ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories_all = Categories.objects.all()

        search_text = request.GET.get('name', None)

        if search_text:
            categories_all = categories_all.filter(name=search_text)

        response = []
        for category in categories_all:
            response.append({
                "name": category.name
            })

        return JsonResponse(response, safe=False, status=200)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Categories(**category_data)

        category.save()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        }, safe=False, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):
    def get(self, request):
        ads_all = Ads.objects.all()

        response = []
        for ad in ads_all:
            response.append({
                "id": ad.Id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price
            })

        return JsonResponse(response, safe=False, status=200)

    def post(self, request):
        ads_data = json.loads(request.body)

        ads_new = Ads(**ads_data)

        ads_new.save()

        return JsonResponse({
            "name": ads_new.name,
            "author": ads_new.author,
            "price": ads_new.price,
            "description": ads_new.description,
            "address": ads_new.address,
            "is_published": ads_new.is_published
        }, safe=False, status=201)


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.Id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })
