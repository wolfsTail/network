from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentViewSet


app_name = 'main'

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = router.urls
