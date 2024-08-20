""""Discover rules for core main registry app
"""

import json
import logging
from os.path import join

from django.contrib.staticfiles import finders
from django.db.migrations.exceptions import BadMigrationError

from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.components.xsl_transformation import (
    api as xslt_transformation_api,
)
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.utils.file import read_file_content
from core_main_registry_app import settings as main_registry_settings
from core_main_registry_app.components.custom_resource import (
    api as custom_resource_api,
)
from core_main_registry_app.components.custom_resource.models import (
    CustomResource,
)
from core_main_registry_app.components.refinement.models import Refinement
from core_main_registry_app.system import api as registry_system_api
from core_main_registry_app.utils.refinement import refinement

logger = logging.getLogger(__name__)


def init_registry():
    """Initialize the registry.
       Add the registry template, refinements, and resources.

    Returns:
    """
    # Check if data were previously inserted
    if (
        TemplateVersionManager.objects.count() > 0
        or CustomResource.objects.count() > 0
        or Refinement.objects.count() > 0
        or XslTransformation.objects.filter(
            name=main_registry_settings.LIST_XSL_FILENAME
        ).count()
        > 0
        or XslTransformation.objects.filter(
            name=main_registry_settings.DETAIL_XSL_FILENAME
        ).count()
        > 0
    ):
        logger.warning("The database is not empty. Skipping migration.")
        return

    # Check if file settings are set
    if (
        not main_registry_settings.REGISTRY_XSD_FILENAME
        or not main_registry_settings.REGISTRY_XSD_FILEPATH
        or not main_registry_settings.CUSTOM_REGISTRY_FILE_PATH
        or not main_registry_settings.XSL_FOLDER_PATH
        or not main_registry_settings.LIST_XSL_FILENAME
        or not main_registry_settings.DETAIL_XSL_FILENAME
    ):
        raise BadMigrationError(
            "Please configure the REGISTRY_XSD_FILENAME, "
            "REGISTRY_XSD_FILEPATH, CUSTOM_REGISTRY_FILE_PATH, "
            "XSL_FOLDER_PATH, LIST_XSL_FILENAME and DETAIL_XSL_FILENAME "
            "settings in your project."
        )

    # Load files
    default_xsd_path = finders.find(
        main_registry_settings.REGISTRY_XSD_FILEPATH
    )
    list_xslt_path = finders.find(
        join(
            main_registry_settings.XSL_FOLDER_PATH,
            main_registry_settings.LIST_XSL_FILENAME,
        )
    )
    detail_xslt_path = finders.find(
        join(
            main_registry_settings.XSL_FOLDER_PATH,
            main_registry_settings.DETAIL_XSL_FILENAME,
        )
    )
    default_json_path = finders.find(
        main_registry_settings.CUSTOM_REGISTRY_FILE_PATH
    )
    if (
        not default_xsd_path
        or not list_xslt_path
        or not detail_xslt_path
        or not default_json_path
    ):
        raise BadMigrationError(
            "A file required for loading data was not found."
        )
    # Read files
    xsd_data = read_file_content(default_xsd_path)
    with open(default_json_path, encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    list_xsl_data = read_file_content(list_xslt_path)
    detail_xsl_data = read_file_content(detail_xslt_path)

    # Build list of custom resources from JSON file
    custom_resources = custom_resource_api.get_resources_from_dict(json_data)

    # Insert template
    tvm, current_template = registry_system_api.insert_registry_schema(
        main_registry_settings.REGISTRY_XSD_FILENAME, xsd_data
    )
    # Insert refinements
    refinement.init_refinements(current_template)
    # Insert custom resources
    for custom_resource in custom_resources:
        custom_resource.template = current_template
        custom_resource.save()

    # Save list and detail XSLT
    list_xslt = xslt_transformation_api.upsert(
        XslTransformation(
            name=main_registry_settings.LIST_XSL_FILENAME,
            filename=main_registry_settings.LIST_XSL_FILENAME,
            content=list_xsl_data,
        )
    )
    detail_xslt = xslt_transformation_api.upsert(
        XslTransformation(
            name=main_registry_settings.DETAIL_XSL_FILENAME,
            filename=main_registry_settings.DETAIL_XSL_FILENAME,
            content=detail_xsl_data,
        )
    )

    # Bind XSLT to template
    template_xsl_rendering_api.add_or_delete(
        template=current_template,
        list_xslt=list_xslt,
        default_detail_xslt=detail_xslt,
        list_detail_xslt=[detail_xslt],
    )
