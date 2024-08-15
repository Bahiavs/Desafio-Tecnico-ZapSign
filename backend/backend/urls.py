from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('documentapp/', include('documentapp.urls')),
    path('admin/', admin.site.urls),
]
