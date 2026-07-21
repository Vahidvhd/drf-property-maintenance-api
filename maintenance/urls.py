from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, MaintenanceRequestViewSet, RequestCommentViewSet

router = DefaultRouter()
router.register('properties', PropertyViewSet, basename='property')
router.register('requests', MaintenanceRequestViewSet, basename='request')
router.register("comments", RequestCommentViewSet, basename="comment")

urlpatterns = router.urls