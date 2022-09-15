""" Apps file for setting core main registry app package when app is ready
"""
import sys

from django.apps import AppConfig


class InitApp(AppConfig):
    """Core main registry app application settings"""

    name = "core_main_registry_app"
    verbose_name = "Core Main Registry App"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "migrate" not in sys.argv:
            from core_main_registry_app import discover

            # Init registry
            discover.init_registry()
