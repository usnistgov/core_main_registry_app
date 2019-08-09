"""
    Admin ajax
"""
from django.http.response import HttpResponse, HttpResponseBadRequest

from core_main_registry_app.components.version_manager import api as version_manager_api
from core_main_app.components.template import api as template_api


def set_current_template_version_from_version_manager(request):
    """ Set the current version of a template.

    Args:
        request:

    Returns:

    """
    try:
        version_manager_api.set_current(template_api.get(request.GET['id']))
    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type='application/javascript')

    return HttpResponse(content_type='application/javascript')
