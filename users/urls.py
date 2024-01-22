from rest_framework.routers import SimpleRouter

from .views import  UserListViewSet


app_name = 'users'

router = SimpleRouter()
router.register(r'users', UserListViewSet, basename='users')

urlpatterns = router.urls
