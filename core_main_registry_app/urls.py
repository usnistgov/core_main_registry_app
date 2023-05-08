""" Url router for the core main registry app
"""
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core_main_app.components.data import api as data_api
from core_main_app.utils.rendering import render
from core_main_app.utils.urls import get_auth_urls
from core_main_app.views.common import views as common_views
from core_main_app.views.user import views as user_views, ajax as user_ajax
from core_main_registry_app.settings import ENABLE_BLOB_ENDPOINTS

# FIXME: Check needed URLs for registry and remove the others.

urlpatterns = [
    re_path(r"^$", user_views.homepage, name="core_main_app_homepage"),
    re_path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    re_path(
        "docs/api/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger_view",
    ),
    re_path(
        r"^locked",
        common_views.defender_error_page,
        name="core_main_app_locked",
    ),
    re_path(r"^rest/", include("core_main_registry_app.rest.urls")),
    re_path(
        r"^data",
        common_views.ViewData.as_view(),
        name="core_main_app_data_detail",
    ),
    re_path(
        r"^template/versions/(?P<version_manager_id>\w+)",
        user_views.manage_template_versions,
        name="core_main_app_manage_template_versions",
    ),
    re_path(
        r"^template/xslt/(?P<template_id>\w+)",
        login_required(
            common_views.TemplateXSLRenderingView.as_view(
                rendering=render,
                template_name="core_main_app/common/templates_xslt/main.html",
                save_redirect="core_main_app_manage_template_versions",
            )
        ),
        name="core_main_app_template_xslt",
    ),
    re_path(
        r"^edit-rights/(?P<workspace_id>\w+)$",
        login_required(common_views.EditWorkspaceRights.as_view()),
        name="core_main_edit_rights_workspace",
    ),
    re_path(
        r"^change-workspace",
        login_required(
            user_ajax.LoadFormChangeWorkspace.as_view(
                show_global_workspace=False
            )
        ),
        name="core_main_change_workspace",
    ),
    re_path(
        r"^assign-data-workspace",
        login_required(user_ajax.AssignView.as_view(api=data_api)),
        name="core_main_assign_data_workspace",
    ),
    re_path(
        r"^assign-workspace",
        login_required(user_ajax.AssignView.as_view(api=data_api)),
        name="core_main_assign_workspace",
    ),
    re_path(
        r"^add-user-form",
        user_ajax.load_add_user_form,
        name="core_main_edit_rights_users_form",
    ),
    re_path(
        r"^add-user-right-to-workspace",
        user_ajax.add_user_right_to_workspace,
        name="core_main_add_user_right_to_workspace",
    ),
    re_path(
        r"^switch-right", user_ajax.switch_right, name="core_main_switch_right"
    ),
    re_path(
        r"^remove-rights",
        user_ajax.remove_user_or_group_rights,
        name="core_main_remove_rights",
    ),
    re_path(
        r"^add-group-form",
        user_ajax.load_add_group_form,
        name="core_main_edit_rights_groups_form",
    ),
    re_path(
        r"^add-group-right-to-workspace",
        user_ajax.add_group_right_to_workspace,
        name="core_main_add_group_right_to_workspace",
    ),
    re_path(r"^tz_detect/", include("tz_detect.urls")),
    re_path(
        r"^password_reset/$",
        user_views.custom_reset_password,
        name="password_reset",
    ),
    re_path(
        r"^password_reset/done/$",
        user_views.custom_password_reset_done,
        name="password_reset_done",
    ),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        user_views.custom_password_reset_confirm,
        name="password_reset_confirm",
    ),
    re_path(
        r"^reset/done/$",
        user_views.custom_password_reset_complete,
        name="password_reset_complete",
    ),
    re_path(
        r"^change-data-display",
        user_ajax.change_data_display,
        name="core_main_add_change_data_display",
    ),
    re_path(
        r"^xml-editor/data",
        login_required(
            common_views.DataContentEditor.as_view(),
        ),
        name="core_main_app_xml_text_editor_view",
    ),
]

urlpatterns.extend(get_auth_urls())

if ENABLE_BLOB_ENDPOINTS:
    from core_main_app.components.blob import api as blob_api

    urlpatterns.append(
        re_path(
            r"^assign-blob-workspace",
            user_ajax.AssignView.as_view(api=blob_api),
            name="core_main_assign_blob_workspace",
        )
    )
