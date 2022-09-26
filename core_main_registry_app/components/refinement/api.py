""" Refinement API
"""

from core_main_registry_app.components.refinement.models import Refinement


def create_and_save(name, xsd_name, template_hash):
    """Create and save a refinement.

    Args:
        name:
        xsd_name:
        template_hash:

    Returns:

    """

    # Save refinement
    return Refinement.create_and_save(
        name=name, xsd_name=xsd_name, template_hash=template_hash
    )


def get_all():
    """Get all refinements.

    Returns: Refinement collection

    """
    return Refinement.get_all()


def get_all_filtered_by_template_hash(template_hash):
    """Get all refinements by template hash.

    Args:
        template_hash:

    Returns: Refinement collection

    """
    return Refinement.get_all_filtered_by_template_hash(
        template_hash=template_hash
    )


def check_refinements_already_exist_by_template_hash(template_hash):
    """Check if the refinements have already been generated for the template.

    Args:
        template_hash:

    Returns:
        Boolean: True/False

    """
    return Refinement.check_refinements_already_exist_by_template_hash(
        template_hash
    )


def get_by_template_hash_and_by_slug(template_hash, slug):
    """Get refinement by template hash and by slug.

    Args:
        template_hash:
        slug:

    Returns: Refinement collection

    """
    return Refinement.get_by_template_hash_and_by_slug(
        template_hash=template_hash, slug=slug
    )
