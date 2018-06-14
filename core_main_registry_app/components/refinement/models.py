""" Refinement model
"""

from django.db import models
from django_extensions.db.fields import AutoSlugField


class Refinement(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(max_length=50, overwrite=True, populate_from='name')
    # Cannot use a ReferenceField to template: not same database. Use the template hash instead.
    template_hash = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all():
        """ Get all refinements.

        Returns: Refinement collection

        """
        return Refinement.objects.all()

    @staticmethod
    def get_all_filtered_by_template_hash(template_hash):
        """ Get all refinements by template hash.

        Args:
            template_hash:

        Returns: Refinement collection

        """
        return Refinement.objects.all().filter(template_hash=template_hash)

    @staticmethod
    def create_and_save(name, template_hash):
        """ Create and save a refinement.

        Args:
            name:
            template_hash:

        Returns:

        """
        return Refinement.objects.create(name=name, template_hash=template_hash)

    @staticmethod
    def check_refinements_already_exist_by_template_hash(template_hash):
        """ Check if the refinements have already been generated for the template.

        Args:
            template_hash:

        Returns:
            Boolean: True/False

        """
        return len(Refinement.get_all_filtered_by_template_hash(template_hash)) > 0
