"""
    Admin views
"""
import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import escape as html_escape
from django.views.generic import View

from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.utils.rendering import admin_render
from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_registry_app.views.admin.forms import UploadCustomResourcesForm

logger = logging.getLogger("core_main_registry_app.views.admin.views")


@staff_member_required
def manage_templates(request):
    """View that allows template management.

    Args:
        request:

    Returns:

    """
    # get all current templates
    templates = template_version_manager_api.get_global_version_managers(
        request=request
    )

    context = {
        "object_name": "Template",
        "available": [template for template in templates if not template.is_disabled],
        "disabled": [template for template in templates if template.is_disabled],
    }

    assets = {}
    modals = []

    return admin_render(
        request,
        "core_main_app/admin/templates/list.html",
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
        """Saves an XSLT.

        Args:
            request: Request.
            template_id

        """
        try:
            # get the template
            template = template_api.get_by_id(template_id, request=request)

            # get the file from the form
            upload_file = request.FILES["json_file"].read().decode("utf-8")

            data = json.loads(upload_file)
            custom_resource_api.replace_custom_resources_by_template(template, data)

            return HttpResponseRedirect(
                reverse("core-admin:core_main_registry_app_custom_registry")
            )
        except Exception as exception:
            self.context.update({"errors": html_escape(str(exception))})
            return admin_render(request, self.template_name, context=self.context)


class CustomRegistry(View):
    """Custom registry admin view."""

    def get(self, request, *args, **kwargs):
        data_context_list = []
        global_template_version_manager = (
            template_version_manager_api.get_global_version_managers(request=request)
        )
        if len(global_template_version_manager) == 1:
            template_version_manager = list(global_template_version_manager)[0]
            # get the current version
            current_template_version = template_version_manager.current
            # for each template versions
            for version in template_version_manager.versions:
                # get the template
                template = template_api.get_by_id(version, request=request)
                # get all the template's custom resources
                custom_resources = custom_resource_api.get_all_by_template(template)
                # append to list for the context
                data_context_list.append(
                    {
                        "template_name": template.display_name,
                        "count": custom_resources.count(),
                        "template_id": str(template.id),
                        "is_current": current_template_version == str(template.id),
                    }
                )
        else:
            logger.error("We should only have one template.")

        modals = []

        assets = {
            "js": [],
        }

        context = {"objects": data_context_list, "object_name": "Custom Resources"}

        return admin_render(
            request,
            "core_main_registry_app/admin/custom_registry/list.html",
            modals=modals,
            assets=assets,
            context=context,
        )
