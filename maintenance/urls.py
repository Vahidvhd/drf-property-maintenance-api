from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, MaintenanceRequestViewSet

router = DefaultRouter()
router.register('property', PropertyViewSet, basename='property')
router.register('requests', MaintenanceRequestViewSet, basename='request')

urlpatterns = router.urls