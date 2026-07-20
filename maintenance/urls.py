from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, MaintenanceRequestViewSet

router = DefaultRouter()
router.register('properties', PropertyViewSet, basename='property')
router.register('requests', MaintenanceRequestViewSet, basename='request')

urlpatterns = router.urls