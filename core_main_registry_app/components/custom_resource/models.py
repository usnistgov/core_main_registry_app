""" Custom Resource model
"""

from django_mongoengine import fields, Document
from core_main_app.components.template.models import Template


class CustomResource(Document):
    """
    Custom resource model
    """

    template = fields.ReferenceField(Template, blank=False)
    name_in_schema = fields.StringField(blank=True) # Not sure if needed
    title = fields.StringField()
    url = fields.StringField(blank=True, unique_with='template')
    description = fields.StringField(blank=True)
    type = fields.StringField(blank=False)
    icon = fields.StringField(blank=False)
    icon_color = fields.StringField(blank=True)
    display_icon = fields.BooleanField(blank=True)
    role_choice = fields.StringField(blank=True)
    role_type = fields.StringField(blank=True)
    sort = fields.IntField(unique_with='template', min_value=0)

    @staticmethod
    def get_all_by_template(template):
        """ Get all custom resource by template.

        Args:
            template:

        Returns:

        """
        return CustomResource.objects(template=template).all()
