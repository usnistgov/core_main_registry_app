""" Custom admin site for the Custom Resource model
"""
from django.contrib import admin


class CustomResourceAdmin(admin.ModelAdmin):
    """CustomResourceAdmin"""

    readonly_fields = [
        "template",
        "name_in_schema",
        "title",
        "type",
        "role_choice",
        "role_type",
    ]
    exclude = ["slug"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Custom Resources"""
        return False
