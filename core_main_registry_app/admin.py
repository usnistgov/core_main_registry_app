""" Url router for the administration site
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path, reverse_lazy
from django.views.generic.base import RedirectView

import core_main_app.components.web_page_login.api as login_page_api
from core_main_app.admin import core_admin_site
from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.utils.admin_site.view_only_admin import ViewOnlyAdmin
from core_main_app.utils.rendering import admin_render
from core_main_app.views.admin import views as admin_views, ajax as admin_ajax
from core_main_app.views.admin.views import WebPageView
from core_main_app.views.common import views as common_views
from core_main_registry_app.components.category.models import Category
from core_main_registry_app.components.custom_resource.admin_site import (
    CustomResourceAdmin,
)
from core_main_registry_app.components.custom_resource.models import (
    CustomResource,
)
from core_main_registry_app.components.refinement.models import Refinement
from core_main_registry_app.views.admin import views as registry_admin_views

# FIXME: Check needed URLs for registry and remove the others.

admin_urls = [
    re_path(
        r"^login/message/$",
        staff_member_required(
            WebPageView.as_view(
                api=login_page_api,
                get_redirect="core_main_app/admin/web_page/login_page.html",
                post_redirect="core-admin:core_main_app_login_page",
                web_page_type=WEB_PAGE_TYPES["login"],
            )
        ),
        name="core_main_app_login_page",
    ),
    re_path(
        r"^login",
        RedirectView.as_view(url=reverse_lazy("core_main_app_login")),
    ),
    re_path(
        r"^logout",
        RedirectView.as_view(url=reverse_lazy("core_main_app_logout")),
    ),
    re_path(
        r"^data",
        staff_member_required(
            common_views.ViewData.as_view(
                administration=True,
                template="core_main_registry_app/admin/data/view_data.html",
            )
        ),
        name="core_main_app_data_detail",
    ),
    re_path(
        r"^templates$",
        staff_member_required(
            registry_admin_views.ManageTemplatesRegistryView.as_view(
                template="core_main_registry_app/admin/templates/list.html",
            )
        ),
        name="core_main_registry_app_templates",
    ),
    re_path(
        r"^template/upload/(?P<version_manager_id>\w+)",
        admin_views.upload_template_version,
        name="core_main_app_upload_template_version",
    ),
    re_path(
        r"^template/versions/(?P<version_manager_id>\w+)",
        admin_views.manage_template_versions,
        name="core_main_app_manage_template_versions",
    ),
    re_path(
        r"^template/xslt/(?P<template_id>\w+)",
        staff_member_required(
            common_views.TemplateXSLRenderingView.as_view(
                rendering=admin_render,
                template_name="core_main_app/admin/templates_xslt/main.html",
                save_redirect="core-admin:core_main_app_manage_template_versions",
                back_to_url="core-admin:core_main_app_manage_template_versions",
            )
        ),
        name="core_main_app_template_xslt",
    ),
    re_path(
        r"^dashboard$", admin_views.admin_home, name="core_main_app_admin_home"
    ),
    re_path(
        r"^template/resolve-dependencies",
        admin_ajax.resolve_dependencies,
        name="core_main_app_resolve_dependencies",
    ),
    re_path(
        r"^xslt/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditXSLTView.as_view()),
        name="core_main_app_edit_xslt",
    ),
    re_path(
        r"^xslt$",
        staff_member_required(admin_views.XSLTView.as_view()),
        name="core_main_app_xslt",
    ),
    re_path(
        r"^xslt/upload$",
        staff_member_required(admin_views.UploadXSLTView.as_view()),
        name="core_main_app_upload_xslt",
    ),
    re_path(
        r"^xslt/(?P<pk>[\w-]+)/delete/$",
        staff_member_required(admin_ajax.DeleteXSLTView.as_view()),
        name="core_main_app_delete_xslt",
    ),
    re_path(
        r"^edit-rights/(?P<workspace_id>\w+)$",
        staff_member_required(
            common_views.EditWorkspaceRights.as_view(
                administration=True,
                template="core_main_app/admin/workspaces/edit_rights.html",
            )
        ),
        name="core_main_edit_rights_workspace",
    ),
    re_path(
        r"^custom-registry$",
        staff_member_required(registry_admin_views.CustomRegistry.as_view()),
        name="core_main_registry_app_custom_registry",
    ),
    re_path(
        r"^template/(?P<template_id>\w+)/custom-resource",
        staff_member_required(
            registry_admin_views.UploadCustomResource.as_view()
        ),
        name="core_main_registry_app_template_custom_resource",
    ),
]
admin.site.register(CustomResource, CustomResourceAdmin)
admin.site.register(Category, ViewOnlyAdmin)
admin.site.register(Refinement, ViewOnlyAdmin)
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
