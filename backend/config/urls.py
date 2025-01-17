from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerSplitView

from application.access_control.api.views import (
    AuthenticateView,
    CreateUserAPITokenView,
    RevokeUserAPITokenView,
)
from application.commons.api.views import HealthView, VersionView
from application.commons.views import empty_view
from application.import_observations.api.views import (
    ApiImportObservationsById,
    ApiImportObservationsByName,
    FileUploadObservationsById,
    FileUploadObservationsByName,
)
from application.metrics.api.views import (
    ProductMetricsCurrentView,
    ProductMetricsExportCodeChartaView,
    ProductMetricsExportCsvView,
    ProductMetricsExportExcelView,
    ProductMetricsStatusView,
    ProductMetricsTimelineView,
)

urlpatterns = [
    path("", empty_view),
    path(
        "favicon.ico",
        RedirectView.as_view(
            url=staticfiles_storage.url("favicon.ico"), permanent=False
        ),
        name="favicon",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    path("api/status/version/", VersionView.as_view()),
    path("api/status/health/", HealthView.as_view()),
    path(
        "api/authentication/authenticate/",
        AuthenticateView.as_view(),
        name="authenticate",
    ),
    path(
        "api/authentication/create_user_api_token/",
        CreateUserAPITokenView.as_view(),
        name="create_user_api_token",
    ),
    path(
        "api/authentication/revoke_user_api_token/",
        RevokeUserAPITokenView.as_view(),
        name="revoke_user_api_token",
    ),
    path(
        "api/import/api_import_observations_by_name/",
        ApiImportObservationsByName.as_view(),
    ),
    path(
        "api/import/api_import_observations_by_id/", ApiImportObservationsById.as_view()
    ),
    path(
        "api/import/file_upload_observations_by_name/",
        FileUploadObservationsByName.as_view(),
    ),
    path(
        "api/import/file_upload_observations_by_id/",
        FileUploadObservationsById.as_view(),
    ),
    path("api/metrics/product_metrics_timeline/", ProductMetricsTimelineView.as_view()),
    path("api/metrics/product_metrics_current/", ProductMetricsCurrentView.as_view()),
    path("api/metrics/product_metrics_status/", ProductMetricsStatusView.as_view()),
    path("api/metrics/export_excel/", ProductMetricsExportExcelView.as_view()),
    path("api/metrics/export_csv/", ProductMetricsExportCsvView.as_view()),
    path(
        "api/metrics/export_codecharta/", ProductMetricsExportCodeChartaView.as_view()
    ),
    # OpenAPI 3
    path("api/oa3/schema/", SpectacularAPIView.as_view(), name="schema_oa3"),
    path(
        "api/oa3/swagger-ui",
        SpectacularSwaggerSplitView.as_view(url="/api/oa3/schema/?format=json"),
        name="swagger-ui_oa3",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
