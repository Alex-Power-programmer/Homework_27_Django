from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads.views.locations import LocationsViewSet
from ads.views.service import root
from ads.views import ads as ads_view
from ads.views import category as cat_view
from ads.views import users as users_view


router = routers.SimpleRouter()
router.register(r'location', LocationsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root),
    path('ad/', ads_view.AdListView.as_view()),
    path('ad/<int:pk>/', ads_view.AdDetailView.as_view()),
    path('ad/create/', ads_view.AdCreateView.as_view()),
    path('ad/<int:pk>/update/', ads_view.AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', ads_view.AdDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', ads_view.AdUploadImageView.as_view()),

    path('user/', users_view.UserListView.as_view()),
    path('user/<int:pk>/', users_view.UserDetailView.as_view()),
    path('user/create/', users_view.UserCreateView.as_view()),
    path('user/<int:pk>/update/', users_view.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', users_view.UserDeleteView.as_view()),

    path('cat/', cat_view.CategoryListView.as_view()),
    path('cat/<int:pk>/', cat_view.CategoryDetailView.as_view()),
    path('cat/create/', cat_view.CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', cat_view.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', cat_view.CategoryDeleteView.as_view()),

]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
