"""
URL configuration for carwash_management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def root_redirect(request):
    return redirect('accounts:dashboard')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('carwash/', include('carwash.urls')),
    path('attendance/', include('attendance.urls')),
    path('requests/', include('requests.urls')),
    path('reports/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
