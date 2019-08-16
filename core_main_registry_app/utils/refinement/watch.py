""" Handle refinement signals
"""
from core_main_app.components.template.models import Template
from core_main_registry_app.utils.refinement.refinement import init_refinements
from signals_utils.signals.mongo import connector, signals


def init():
    """ Connect to template object events.
    """
    connector.connect(post_save_template, signals.post_save, sender=Template)


def post_save_template(sender, document, **kwargs):
    """ Method executed after saving of a Template object.
    Args:
        sender:
        document: template object.
        **kwargs:
    """
    init_refinements(document)
