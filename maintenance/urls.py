from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet

router = DefaultRouter()
router.register('property', PropertyViewSet, basename='property')

urlpatterns = router.urls