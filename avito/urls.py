from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ads.views.service import root
from ads.views import ads as ads_view
from ads.views import category as cat_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root),
    path('ad/', ads_view.AdListView.as_view()),
    path('ad/<int:pk>/', ads_view.AdDetailView.as_view()),
    path('ad/<int:pk>/create/', ads_view.AdCreateView.as_view()),

    path('cat/', cat_view.CategoryListView.as_view()),
    path('cat/<int:pk>/', cat_view.CategoryDetailView.as_view()),
    path('cat/create/', cat_view.CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', cat_view.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', cat_view.CategoryDeleteView.as_view()),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
