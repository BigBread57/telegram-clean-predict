"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from server.url_components import (
    admin_urlpatterns,
    docs_urlpatterns,
    seo_urlpatterns,
)

api_url = [
    # path('api/', include((router.urls, 'api'))),
]

admin.autodiscover()

urlpatterns = [
    # Health checks:
    path('api-auth/', include('rest_framework.urls')),
    path('', include(api_url)),

    *admin_urlpatterns,
    *docs_urlpatterns,
    *seo_urlpatterns,
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = (
        [
            # URLs specific only to django-debug-toolbar:
            path('__debug__/', include(debug_toolbar.urls)),  # noqa: DJ05
        ] + urlpatterns +
        static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        ) + static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

    )
