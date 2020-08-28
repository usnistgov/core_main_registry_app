""" Handle refinement signals
"""
from logging import getLogger

from billiard.exceptions import SoftTimeLimitExceeded

from core_main_app.components.template.models import Template
from core_main_registry_app.tasks import init_refinement_task
from signals_utils.signals.mongo import connector, signals

logger = getLogger(__name__)


def init():
    """Connect to template object events."""
    connector.connect(post_save_template, signals.post_save, sender=Template)


def post_save_template(sender, document, **kwargs):
    """Method executed after saving of a Template object.
    Args:
        sender:
        document: template object.
        **kwargs:
    """
    try:
        # start asynchronous task
        if kwargs["created"]:
            init_refinement_task.delay(str(document.id))
    except (TimeoutError, SoftTimeLimitExceeded) as ex:
        logger.error("Timeout while generating refinements: {0}".format(str(ex)))
    except Exception as ex:
        logger.error("Error happened while generating refinements: {0}".format(str(ex)))
