from rest_framework import viewsets, permissions
# Create your views here.
from .models import Property, MaintenanceRequest
from . serializers import (
    MaintenanceRequestCreateUpdateSerializer,
    MaintenanceRequestDetailSerializer,
    MaintenanceRequestListSerializer,
    PropertySerializer,
)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return MaintenanceRequest.objects.all()

        return MaintenanceRequest.objects.filter(created_by=user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return MaintenanceRequestListSerializer

        if self.action in ["create", "update", "partial_update"]:
            return MaintenanceRequestCreateUpdateSerializer

        return MaintenanceRequestDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)