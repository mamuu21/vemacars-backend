
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("backend.vemacars.urls")),
    path("api/", include("backend.api.urls")),
    path("accounts/", include("backend.accounts.urls")),
    # path("snip/", include("backend.snip.urls"))
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
