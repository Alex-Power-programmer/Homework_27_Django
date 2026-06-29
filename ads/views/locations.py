from rest_framework.viewsets import ModelViewSet

from ads.models import Location
from ads.serializers import LocationsSerializer


class LocationsViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationsSerializer
