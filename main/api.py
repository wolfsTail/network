from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentViewSet, ReactionViewSet


main_router = SimpleRouter()
main_router.register(r'posts', PostViewSet, basename='posts')
main_router.register(r'comments', CommentViewSet, basename='comments')
main_router.register(r'reactions', ReactionViewSet, basename='reactions')