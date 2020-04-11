from django.contrib import admin
from django.urls import path, include
from gwrcApp import urls as gwrc_urls
from gwrcApp.views import AlarmViewSet
from rest_framework import routers


admin.site.site_header = "Administração GWRC-1.0"
admin.site.site_title = "GWRC-1.0"
admin.site.index_title = "Administração GWRC-1.0"

router = routers.DefaultRouter()
router.register('alarmes', AlarmViewSet)

urlpatterns = [
    path('alarms', include(router.urls)),
    path('', include(gwrc_urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
