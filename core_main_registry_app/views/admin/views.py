""" Admin views
"""
import logging

from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import escape as html_escape
from django.views.generic import View

from core_main_app.commons.exceptions import ModelError
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.utils.json_utils import load_json_string
from core_main_app.utils.rendering import admin_render
from core_main_app.views.common.ajax import EditTemplateVersionManagerView
from core_main_registry_app.components.custom_resource import (
    api as custom_resource_api,
)
from core_main_registry_app.components.template import (
    api as template_registry_api,
)
from core_main_registry_app.views.admin.forms import UploadCustomResourcesForm

logger = logging.getLogger("core_main_registry_app.views.admin.views")


class ManageTemplatesRegistryView(View):
    """Manage Templates view."""

    template = "core_main_registry_app/admin/templates/list.html"

    def get(self, request):
        """get request

        Args:
            request:

        Returns:
        """

        templates = template_version_manager_api.get_global_version_managers(
            request=request
        )
        # get all registry current template
        registry_template = (
            template_registry_api.get_current_registry_template(request)
        )
        context = {
            "object_name": "Template",
            "available": [
                template for template in templates if not template.is_disabled
            ],
            "disabled": [
                template for template in templates if template.is_disabled
            ],
            "registry_current_template": template_version_manager_api.get_by_id(
                registry_template.version_manager_id, request
            ),
            "available_template_block": "core_main_registry_app/admin/core_main_app/templates/list/available.html",
            "MULTIPLE_SCHEMAS": settings.ALLOW_MULTIPLE_SCHEMAS,
        }

        assets = {
            "js": [
                {
                    "path": "core_main_app/common/js/templates/list/restore.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/list/modals/disable.js",
                    "is_raw": False,
                },
                EditTemplateVersionManagerView.get_modal_js_path(),
            ],
        }
        if settings.ALLOW_MULTIPLE_SCHEMAS:
            assets["js"].extend(
                [
                    {
                        "path": "core_main_app/common/js/templates/sort.js",
                        "is_raw": True,
                    },
                    {
                        "path": "core_main_registry_app/admin/js/templates/sort.raw.js",
                        "is_raw": True,
                    },
                ]
            )

        modals = [
            "core_main_app/admin/templates/list/modals/disable.html",
            EditTemplateVersionManagerView.get_modal_html_path(),
        ]

        return admin_render(
            request,
            self.template,
            assets=assets,
            context=context,
            modals=modals,
        )


class UploadCustomResource(View):
    """Upload custom resource admin view."""

    form_class = UploadCustomResourcesForm
    template_name = "core_main_registry_app/admin/custom_registry/upload.html"
    object_name = "Custom Resources"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.context.update({"object_name": self.object_name})

    def get(self, request, *args, **kwargs):
        self.context.update({"upload_form": self.form_class()})
        return admin_render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        template_id = kwargs.pop("template_id")
        form = self.form_class(request.POST, request.FILES)
        self.context.update({"upload_form": form})

        if form.is_valid():
            return self._save_custom_resources(request, template_id)

        # Display error from the form
        return admin_render(request, self.template_name, context=self.context)

    def _save_custom_resources(self, request, template_id):
        """Saves a JSON Custom resource.

        Args:
            request: Request.
            template_id

        """
        try:
            # get the template
            template = template_api.get_by_id(template_id, request=request)

            # get the file from the form
            upload_file = request.FILES["json_file"].read().decode("utf-8")

            data = load_json_string(upload_file)
            custom_resource_api.replace_custom_resources_by_template(
                template, data
            )

            return HttpResponseRedirect(
                reverse("core-admin:core_main_registry_app_custom_registry")
            )
        except Exception as exception:
            self.context.update({"errors": html_escape(str(exception))})
            return admin_render(
                request, self.template_name, context=self.context
            )


class CustomRegistry(View):
    """Custom registry admin view."""

    def get(self, request, *args, **kwargs):
        """Get Custom Registry configuration page

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        data_context_list = []
        try:
            # get the current version
            current_registry_template = (
                template_registry_api.get_current_registry_template(request)
            )
            # for each template versions
            for version in current_registry_template.version_manager.versions:
                # get the template
                template = template_api.get_by_id(version, request=request)
                # get all the template's custom resources
                custom_resources = custom_resource_api.get_all_by_template(
                    template
                )
                # append to list for the context
                data_context_list.append(
                    {
                        "template_name": template.display_name,
                        "count": custom_resources.count(),
                        "template_id": str(template.id),
                        "is_current": current_registry_template
                        == str(template.id),
                    }
                )
        except ModelError as model_error:
            messages.add_message(request, messages.ERROR, str(model_error))

        modals = []

        assets = {
            "js": [],
        }

        context = {
            "objects": data_context_list,
            "object_name": "Custom Resources",
        }

        return admin_render(
            request,
            "core_main_registry_app/admin/custom_registry/list.html",
            modals=modals,
            assets=assets,
            context=context,
        )
