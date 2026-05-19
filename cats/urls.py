from rest_framework.routers import DefaultRouter
from .views import CatViewSet, AchievementViewSet

router = DefaultRouter()
router.register('cats', CatViewSet)
router.register('achievements', AchievementViewSet)

urlpatterns = router.urls
