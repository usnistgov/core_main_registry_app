""" Custom Resource model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.text import slugify

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE


class CustomResource(models.Model):
    """
    Custom resource object
    """

    template = models.ForeignKey(
        Template, blank=False, on_delete=models.CASCADE
    )
    name_in_schema = models.CharField(blank=True, max_length=200)
    title = models.CharField(blank=False, max_length=200)
    slug = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True, default=None, null=True)
    type = models.CharField(
        blank=False,
        max_length=200,
        choices=[
            (
                CUSTOM_RESOURCE_TYPE.RESOURCE.value,
                CUSTOM_RESOURCE_TYPE.RESOURCE.value,
            ),
            (CUSTOM_RESOURCE_TYPE.ALL.value, CUSTOM_RESOURCE_TYPE.ALL.value),
        ],
    )
    icon = models.CharField(blank=False, max_length=200)
    icon_color = models.CharField(
        blank=True, default=None, null=True, max_length=200
    )
    display_icon = models.BooleanField(
        blank=True,
        default=None,
        null=True,
    )
    role_choice = models.CharField(
        blank=True, default=None, null=True, max_length=200
    )
    role_type = models.CharField(
        blank=True, default=None, null=True, max_length=200
    )
    sort = models.PositiveIntegerField()
    refinements = models.JSONField(blank=True, default=list)

    class Meta:
        """Meta"""

        unique_together = (("title", "template"), ("sort", "template"))

    def save(self, *args, **kwargs):
        """save.

        Args:

        Returns:

        """
        # set refinements to default value before cleaning if not set
        if not self.refinements:
            self.refinements = list()
        # manually clean object to trigger choices validation
        self.full_clean()
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @staticmethod
    def get_all_by_template(template):
        """Get all custom resource by template.

        Args:
            template:

        Returns:

        """
        return CustomResource.objects.filter(template=template).all()

    @staticmethod
    def get_custom_resource_by_template_and_type(template, type_name):
        """Get custom resource by template and type.

        Args:
            template:
            type_name:

        Returns:

        """
        return CustomResource.objects.filter(
            template=template, type=type_name
        ).all()

    @staticmethod
    def get_custom_resource_by_template_and_slug(template, slug):
        """Get custom resource by template and slug.

        Args:
            template:
            slug:

        Returns:

        """
        try:
            return CustomResource.objects.get(template=template, slug=slug)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_role_for_current_template(template, role):
        """Get custom resource by role for current template.

        Args:
            template:
            role:

        Returns:

        """
        try:
            list_custom_resources = CustomResource.objects.filter(
                template=template, role_choice=role
            ).all()
            if len(list_custom_resources) == 0:
                raise exceptions.ModelError(
                    "Can't find the custom resource with the given role: "
                    + role
                )
            return list_custom_resources[0]

        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def delete_custom_resources_by_template(template):
        """Delete all custom resources related to a template.

        Args:
            template:
        Returns:
        """
        CustomResource.objects.filter(template=template).delete()

    def __str__(self):
        """Custom Resource object as string

        Returns:

        """
        return str(self.title)
