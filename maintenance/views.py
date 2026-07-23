from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

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

        queryset = MaintenanceRequest.objects.select_related(
            "property",
            "created_by",
        ).all()

        if user.is_staff:
            return queryset

        return queryset.filter(created_by=user) 
     
    def get_serializer_class(self):
        if self.action == "list":
            return MaintenanceRequestListSerializer

        if self.action in ["create", "update", "partial_update"]:
            return MaintenanceRequestCreateUpdateSerializer

        return MaintenanceRequestDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


    @action(
        detail=True,
        methods=["patch"],
        url_path="status",
        permission_classes=[permissions.IsAdminUser],
    )
    def update_status(self, request, pk=None):
        maintenance_request = self.get_object()

        new_status = request.data.get("status")

        valid_statuses = [
            MaintenanceRequest.Status.OPEN,
            MaintenanceRequest.Status.IN_PROGRESS,
            MaintenanceRequest.Status.RESOLVED,
            MaintenanceRequest.Status.CLOSED,
        ]

        if new_status not in valid_statuses:
            return Response(
                {"detail": "Invalid status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        maintenance_request.status = new_status
        maintenance_request.save(update_fields=["status", "updated_at"])

        serializer = self.get_serializer(maintenance_request)
        return Response(serializer.data)


class RequestCommentViewSet(viewsets.ModelViewSet):
    serializer_class = RequestCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = RequestComment.objects.select_related(
            "request",
            "author",
            "request__created_by",
        ).all()

        if user.is_staff:
            return queryset

        return queryset.filter(request__created_by=user)

    def perform_create(self, serializer):
        maintenance_request = serializer.validated_data["request"]

        if not self.request.user.is_staff and maintenance_request.created_by != self.request.user:
            raise PermissionDenied("You can only comment on your own requests.")

        serializer.save(author=self.request.user)