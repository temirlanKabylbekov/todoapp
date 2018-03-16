from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from todos.api.views import TodoViewSet

router = routers.SimpleRouter()
router.register(r'todos', TodoViewSet)

api_v1 = (
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/signup/', include('rest_auth.registration.urls')),

    url(r'^auth/token/$', obtain_jwt_token),
    url(r'^auth/token/refresh/$', refresh_jwt_token),

    url(r'^', include(router.urls)),
)

urlpatterns = [
    url(r'^api/v1/', include((api_v1, 'api'), namespace='v1')),
    url('admin/', admin.site.urls),
]


if settings.DEBUG:  # add django-debug-toolbar
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
