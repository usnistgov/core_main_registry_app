""" Registry tasks
"""
from celery import shared_task

from core_main_app.system import api as system_api
from core_main_registry_app.utils.refinement.refinement import init_refinements


@shared_task
def init_refinement_task(template_id):
    """Asynchronous tasks init refinement

    Args:
        template_id:

    Returns:

    """
    template = system_api.get_template_by_id(template_id)
    init_refinements(template)
