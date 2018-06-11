"""Url router for the REST API
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import core_main_app.rest.xsl_transformation.views as xslTransformationList_view
from core_main_app.rest.data import views as data_views
from core_main_app.rest.template import views as template_views
from core_main_app.rest.template_version_manager import views as template_version_manager_views
from core_main_app.rest.workspace import views as workspace_views
from core_main_registry_app.rest.data import views as registry_data_views

urlpatterns = [
    url(r'^template-version-manager/global/$',
        template_version_manager_views.GlobalTemplateVersionManagerList.as_view(),
        name='core_main_app_rest_template_version_manager_global_list'),

    url(r'^template-version-manager/(?P<pk>\w+)/$',
        template_version_manager_views.TemplateVersionManagerDetail.as_view(),
        name='core_main_app_rest_template_version_manager_detail'),

    url(r'^template-version-manager/(?P<pk>\w+)/version/$',
        template_version_manager_views.TemplateVersion.as_view(),
        name='core_main_app_rest_template_version'),

    url(r'^template/version/(?P<pk>\w+)/current/$',
        template_version_manager_views.CurrentTemplateVersion.as_view(),
        name='core_main_app_rest_template_version_current'),

    url(r'^template/version/(?P<pk>\w+)/disable/$',
        template_version_manager_views.DisableTemplateVersion.as_view(),
        name='core_main_app_rest_template_version_disable'),

    url(r'^template/version/(?P<pk>\w+)/restore/$',
        template_version_manager_views.RestoreTemplateVersion.as_view(),
        name='core_main_app_rest_template_version_restore'),

    url(r'^template/(?P<pk>\w+)/download/$', template_views.TemplateDownload.as_view(),
        name='core_main_app_rest_template_download'),

    url(r'^template/(?P<pk>\w+)/$', template_views.TemplateDetail.as_view(),
        name='core_main_app_rest_template_detail'),

    url(r'^data/$', data_views.DataList.as_view(),
        name='core_main_app_rest_data_list'),

    url(r'^data/download/(?P<pk>\w+)/$', data_views.DataDownload.as_view(),
        name='core_main_app_rest_data_download'),

    url(r'^data/get-full$', data_views.get_by_id_with_template_info,
        name='core_main_app_rest_data_get_by_id_with_template_info'),

    url(r'^data/query/keyword/$', data_views.ExecuteLocalKeywordQueryView.as_view(),
        name='core_explore_common_local_query_keyword'),

    url(r'^data/query/$', data_views.ExecuteLocalQueryView.as_view(),
        name='core_explore_common_local_query'),

    url(r'^data/(?P<pk>\w+)/$', registry_data_views.DataDetailRegistry.as_view(),
        name='core_main_app_rest_data_detail'),

    url(r'^data/(?P<pk>\w+)/publish/$', registry_data_views.publish_data,
        name='core_main_app_rest_publish_data'),

    url(r'^data/(?P<pk>\w+)/assign/(?P<workspace_id>\w+)$', data_views.DataAssign.as_view(),
        name='core_main_app_rest_data_assign'),

    url(r'^xslt/$', xslTransformationList_view.XslTransformationList.as_view(),
        name='core_main_app_rest_xslt'),

    url(r'^xslt/transform/$', xslTransformationList_view.XslTransformationTransform.as_view(),
        name='core_main_app_rest_xslt_transform'),

    url(r'^xslt/(?P<pk>\w+)/$', xslTransformationList_view.XslTransformationDetail.as_view(),
        name='core_main_app_rest_xslt_detail'),

    url(r'^workspace/$', workspace_views.WorkspaceList.as_view(),
        name='core_main_app_rest_workspace_list'),

    url(r'^workspace/(?P<pk>\w+)/detail/$', workspace_views.WorkspaceDetail.as_view(),
        name='core_main_app_rest_workspace_detail'),

    url(r'^workspace/read_access', workspace_views.get_workspaces_with_read_access,
        name='core_main_app_rest_workspace_get_all_workspaces_with_read_access_by_user'),

    url(r'^workspace/write_access', workspace_views.get_workspaces_with_write_access,
        name='core_main_app_rest_workspace_get_all_workspaces_with_write_access_by_user'),

    url(r'^workspace/(?P<pk>\w+)/is_public/$', workspace_views.is_workspace_public,
        name='core_main_app_rest_workspace_is_public'),

    url(r'^workspace/(?P<pk>\w+)/list_user_can_read/$', workspace_views.get_list_user_can_read_workspace,
        name='core_main_app_rest_workspace_list_user_can_read'),

    url(r'^workspace/(?P<pk>\w+)/list_user_can_write/$', workspace_views.get_list_user_can_write_workspace,
        name='core_main_app_rest_workspace_list_user_can_write'),

    url(r'^workspace/(?P<pk>\w+)/list_user_can_access/$', workspace_views.get_list_user_can_access_workspace,
        name='core_main_app_rest_workspace_list_user_can_access'),

    url(r'^workspace/(?P<pk>\w+)/list_group_can_read/$', workspace_views.get_list_group_can_read_workspace,
        name='core_main_app_rest_workspace_list_group_can_read'),

    url(r'^workspace/(?P<pk>\w+)/list_group_can_write/$', workspace_views.get_list_group_can_write_workspace,
        name='core_main_app_rest_workspace_list_group_can_write'),

    url(r'^workspace/(?P<pk>\w+)/list_group_can_access/$', workspace_views.get_list_group_can_access_workspace,
        name='core_main_app_rest_workspace_list_group_can_access'),

    url(r'^workspace/(?P<pk>\w+)/add_read_right_to_user/(?P<user_id>\w+)/$',
        workspace_views.add_user_read_right_to_workspace,
        name='core_main_app_rest_workspace_add_user_read'),

    url(r'^workspace/(?P<pk>\w+)/add_write_right_to_user/(?P<user_id>\w+)/$',
        workspace_views.add_user_write_right_to_workspace,
        name='core_main_app_rest_workspace_add_user_write'),

    url(r'^workspace/(?P<pk>\w+)/add_read_right_to_group/(?P<group_id>\w+)/$',
        workspace_views.add_group_read_right_to_workspace,
        name='core_main_app_rest_workspace_add_group_read'),

    url(r'^workspace/(?P<pk>\w+)/add_write_right_to_group/(?P<group_id>\w+)/$',
        workspace_views.add_group_write_right_to_workspace,
        name='core_main_app_rest_workspace_add_group_write'),

    url(r'^workspace/(?P<pk>\w+)/remove_read_right_to_user/(?P<user_id>\w+)/$',
        workspace_views.remove_user_read_right_to_workspace,
        name='core_main_app_rest_workspace_remove_user_read'),

    url(r'^workspace/(?P<pk>\w+)/remove_write_right_to_user/(?P<user_id>\w+)/$',
        workspace_views.remove_user_write_right_to_workspace,
        name='core_main_app_rest_workspace_remove_user_write'),

    url(r'^workspace/(?P<pk>\w+)/remove_read_right_to_group/(?P<group_id>\w+)/$',
        workspace_views.remove_group_read_right_to_workspace,
        name='core_main_app_rest_workspace_remove_group_read'),

    url(r'^workspace/(?P<pk>\w+)/remove_write_right_to_group/(?P<group_id>\w+)/$',
        workspace_views.remove_group_write_right_to_workspace,
        name='core_main_app_rest_workspace_remove_group_write'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
