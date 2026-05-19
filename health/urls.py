from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, HealthRecordViewSet

router = DefaultRouter()
router.register('records', HealthRecordViewSet, basename='healthrecord')
router.register('clinics', ClinicViewSet, basename='clinic')

urlpatterns = router.urls
