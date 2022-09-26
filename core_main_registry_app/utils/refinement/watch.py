""" Handle refinement signals
"""
from logging import getLogger

from billiard.exceptions import SoftTimeLimitExceeded
from django.db.models.signals import post_save

from core_main_app.components.template.models import Template
from core_main_registry_app.tasks import init_refinement_task

logger = getLogger(__name__)


def init():
    """Connect to template object events."""
    post_save.connect(post_save_template, sender=Template)


def post_save_template(sender, instance, **kwargs):
    """Method executed after saving of a Template object.
    Args:
        sender:
        instance: template object.
        **kwargs:
    """
    try:
        # start asynchronous task
        if kwargs["created"]:
            init_refinement_task.delay(str(instance.id))
    except (TimeoutError, SoftTimeLimitExceeded) as ex:
        logger.error("Timeout while generating refinements: %s ", str(ex))
    except Exception as ex:
        logger.error(
            "Error happened while generating refinements:  %s ", str(ex)
        )
