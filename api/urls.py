from api import views as views
from rest_framework.routers import DefaultRouter

app_name='api'

router=DefaultRouter()
router.register('reviews',views.ReviewModelViewSet,basename='review')
urlpatterns=router.urls
