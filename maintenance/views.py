from rest_framework import viewsets
# Create your views here.
from .models import Property
from . serializers import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
