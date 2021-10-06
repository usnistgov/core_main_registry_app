# Generated by Django 3.2 on 2021-12-03 14:32

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core_main_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Refinement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("xsd_name", models.CharField(default="", max_length=50)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, overwrite=True, populate_from="name"
                    ),
                ),
                ("template_hash", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, overwrite=True, populate_from="name"
                    ),
                ),
                ("path", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="core_main_registry_app.category",
                    ),
                ),
                (
                    "refinement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_main_registry_app.refinement",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="CustomResource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name_in_schema", models.CharField(blank=True, max_length=200)),
                ("title", models.CharField(max_length=200)),
                ("slug", models.CharField(blank=True, max_length=200)),
                ("description", models.TextField(blank=True, default=None, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("resource", "resource"), ("all", "all")],
                        max_length=200,
                    ),
                ),
                ("icon", models.CharField(max_length=200)),
                (
                    "icon_color",
                    models.CharField(
                        blank=True, default=None, max_length=200, null=True
                    ),
                ),
                (
                    "display_icon",
                    models.BooleanField(blank=True, default=None, null=True),
                ),
                (
                    "role_choice",
                    models.CharField(
                        blank=True, default=None, max_length=200, null=True
                    ),
                ),
                (
                    "role_type",
                    models.CharField(
                        blank=True, default=None, max_length=200, null=True
                    ),
                ),
                ("sort", models.PositiveIntegerField()),
                ("refinements", models.JSONField(blank=True, default=[])),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_main_app.template",
                    ),
                ),
            ],
            options={
                "unique_together": {("title", "template"), ("sort", "template")},
            },
        ),
    ]
