""" Custom Resource model
"""

from django.utils.text import slugify
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE


class CustomResource(Document):
    """
    Custom resource model
    """

    template = fields.ReferenceField(Template, blank=False)
    name_in_schema = fields.StringField(blank=True)
    title = fields.StringField(unique_with="template")
    slug = fields.StringField()
    description = fields.StringField(blank=True)
    type = fields.StringField(
        blank=False,
        choices=(CUSTOM_RESOURCE_TYPE.RESOURCE.value, CUSTOM_RESOURCE_TYPE.ALL.value),
    )
    icon = fields.StringField(blank=False)
    icon_color = fields.StringField(blank=True)
    display_icon = fields.BooleanField(blank=True)
    role_choice = fields.StringField(blank=True)
    role_type = fields.StringField(blank=True)
    sort = fields.IntField(unique_with="template", min_value=0)
    refinements = fields.ListField(fields.StringField(), blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(CustomResource, self).save(*args, **kwargs)

    @staticmethod
    def get_all_by_template(template):
        """Get all custom resource by template.

        Args:
            template:

        Returns:

        """
        return CustomResource.objects(template=template).all()

    @staticmethod
    def get_custom_resource_by_template_and_type(template, type):
        """Get custom resource by template and type.

        Args:
            template:
            type:

        Returns:

        """
        return CustomResource.objects(template=template, type=type).all()

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
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
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
            list_custom_resources = CustomResource.objects(
                template=template, role_choice=role
            ).all()
            if len(list_custom_resources) > 0:
                return list_custom_resources[0]
            else:
                raise exceptions.ModelError(
                    "Can't find the custom resource with the given role: " + role
                )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def delete_custom_resources_by_template(template):
        """Delete all custom resources related to a template.

        Args:
            template:
        Returns:
        """
        CustomResource.objects(template=template).delete()
