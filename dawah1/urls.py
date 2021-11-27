
from home import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('accounts.urls')),
    path('', include('channel.urls')),
    path('accounts/', include('allauth.urls')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
