"""
    Admin views
"""
from django.contrib.admin.views.decorators import staff_member_required

from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.utils.rendering import admin_render


@staff_member_required
def manage_templates(request):
    """View that allows template management.

    Args:
        request:

    Returns:

    """
    # get all current templates
    templates = template_version_manager_api.get_global_version_managers()

    context = {
        'object_name': 'Template',
        'available': [template for template in templates if not template.is_disabled],
        'disabled': [template for template in templates if template.is_disabled]
    }

    assets = {}
    modals = []

    return admin_render(request,
                        'core_main_app/admin/templates/list.html',
                        assets=assets,
                        context=context,
                        modals=modals)
