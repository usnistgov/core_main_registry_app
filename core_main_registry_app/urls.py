""" Url router for the core main registry app
"""
from django.conf.urls import url, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core_main_app.components.data import api as data_api
from core_main_app.utils.rendering import render
from core_main_app.views.common import ajax as common_ajax, views as common_views
from core_main_app.views.user import views as user_views, ajax as user_ajax
from core_main_registry_app.views.admin import ajax as admin_ajax
from core_main_registry_app.views.user import views as registry_user_views

schema_view = get_schema_view(
   openapi.Info(
      title="REST API",
      default_version='v1',
   ),
)

# FIXME: Check needed URLs for registry and remove the others.

urlpatterns = [
    url(r'^$', user_views.homepage, name='core_main_app_homepage'),

    url(r'^login', user_views.custom_login, name='core_main_app_login'),
    url(r'^logout', user_views.custom_logout, name='core_main_app_logout'),
    url(r'^locked', common_views.defender_error_page, name='core_main_app_locked'),

    url(r'^rest/', include('core_main_registry_app.rest.urls')),
    url(r'^data',  registry_user_views.RegistryViewData.as_view(), name='core_main_app_data_detail'),

    url(r'^template/versions/(?P<version_manager_id>\w+)', user_views.manage_template_versions,
        name='core_main_app_manage_template_versions'),

    url(r'^template/version/disable', common_ajax.disable_template_version_from_version_manager,
        name='core_main_app_disable_template_version'),
    url(r'^template/version/restore', common_ajax.restore_template_version_from_version_manager,
        name='core_main_app_restore_template_version'),
    url(r'^template/version/current', admin_ajax.set_current_template_version_from_version_manager,
        name='core_main_app_set_current_template_version'),

    url(r'^xslt$', common_views.XSLTView.as_view(), name='core_main_app_xslt'),
    url(r'^xslt/upload$', common_views.UploadXSLTView.as_view(), name='core_main_app_upload_xslt'),
    url(r'^template/xslt/(?P<template_id>\w+)',
        common_views.TemplateXSLRenderingView.as_view(
            rendering=render,
            template_name="core_main_app/common/templates_xslt/main.html",
            save_redirect="core_main_app_manage_template_versions"
        ),
        name='core_main_app_template_xslt'),

    url(r'^edit-rights/(?P<workspace_id>\w+)$', common_views.EditWorkspaceRights.as_view(),
        name='core_main_edit_rights_workspace'),

    url(r'^create-workspace', user_ajax.create_workspace, name='core_main_create_workspace'),
    url(r'^change-workspace', user_ajax.LoadFormChangeWorkspace.as_view(
        show_global_workspace=False
    ), name='core_main_change_workspace'),
    url(r'^assign-data-workspace',
        user_ajax.AssignView.as_view(api=data_api),
        name='core_main_assign_data_workspace'),
    url(r'^assign-workspace', user_ajax.AssignView.as_view(api=data_api), name='core_main_assign_workspace'),

    url(r'^add-user-form', user_ajax.load_add_user_form, name='core_main_edit_rights_users_form'),
    url(r'^add-user-right-to-workspace', user_ajax.add_user_right_to_workspace,
        name='core_main_add_user_right_to_workspace'),
    url(r'^switch-right', user_ajax.switch_right, name='core_main_switch_right'),
    url(r'^remove-rights', user_ajax.remove_user_or_group_rights, name='core_main_remove_rights'),
    url(r'^add-group-form', user_ajax.load_add_group_form, name='core_main_edit_rights_groups_form'),
    url(r'^add-group-right-to-workspace', user_ajax.add_group_right_to_workspace,
        name='core_main_add_group_right_to_workspace'),
    url(r'^docs/api$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_view'),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^password_reset/$', user_views.custom_reset_password, name='password_reset'),
    url(r'^password_reset/done/$', user_views.custom_password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.custom_password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', user_views.custom_password_reset_complete, name='password_reset_complete'),
]
