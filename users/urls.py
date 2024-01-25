from .api import users_router


app_name = 'users'

urlpatterns = users_router.urls
