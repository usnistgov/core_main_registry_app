""" Registry tasks
"""
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from core_main_app.components.template import api as template_api
from core_main_registry_app.utils.refinement.refinement import init_refinements


@shared_task
def init_refinement_task(template_id):
    """ Asynchronous tasks init refinement

    Args:
        template_id:

    Returns:

    """
    template = template_api.get(template_id)
    init_refinements(template)
