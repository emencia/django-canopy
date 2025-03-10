"""
URL Configuration for sandbox
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("canopy/", include("canopy.urls")),
    # Dummy homepage template
    path(
        "",
        TemplateView.as_view(template_name="homepage.html"),
        name="homepage",
    ),
]

# This is only needed when using runserver with settings "DEBUG" enabled
if settings.DEBUG:
    try:
        import debug_toolbar  # noqa: F401,F403
    except ImportError:
        pass
    else:
        urlpatterns.append(
            path("__debug__/", include("debug_toolbar.urls"))
        )

    urlpatterns = (
        urlpatterns
        + staticfiles_urlpatterns()
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
