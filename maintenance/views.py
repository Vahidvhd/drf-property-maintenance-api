from rest_framework import viewsets, permissions

from .models import Property, MaintenanceRequest, RequestComment
from .serializers import (
    PropertySerializer,
    MaintenanceRequestListSerializer,
    MaintenanceRequestDetailSerializer,
    MaintenanceRequestCreateUpdateSerializer,
    RequestCommentSerializer,
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


class RequestCommentViewSet(viewsets.ModelViewSet):
    queryset = RequestComment.objects.select_related("request", "author").all()
    serializer_class = RequestCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)