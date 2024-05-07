# Generated by Django 4.2.11 on 2024-04-16 23:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

from ..choices import get_kind_choices, get_kind_default


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Controller",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=100, unique=True, verbose_name="title"),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Used to build the URL.",
                        max_length=100,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "version",
                    models.PositiveSmallIntegerField(default=1, verbose_name="version"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "last_update",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "verbose_name": "Form controller",
                "verbose_name_plural": "Form controllers",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Slot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=get_kind_choices(),
                        default=get_kind_default(),
                        max_length=50,
                        verbose_name="element type",
                    ),
                ),
                ("label", models.CharField(max_length=100, verbose_name="field label")),
                ("name", models.CharField(max_length=100, verbose_name="field name")),
                (
                    "required",
                    models.BooleanField(
                        blank=True, default=False, verbose_name="required"
                    ),
                ),
                ("position", models.IntegerField(default=0, verbose_name="position")),
                ("help_text", models.TextField(blank=True, verbose_name="help text")),
                (
                    "initial",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="initial"
                    ),
                ),
                (
                    "controller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="canopy.controller",
                    ),
                ),
            ],
            options={
                "verbose_name": "Form slot",
                "verbose_name_plural": "Form slots",
                "ordering": ["label"],
            },
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "version",
                    models.PositiveSmallIntegerField(default=1, verbose_name="version"),
                ),
                ("data", models.JSONField(null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "controller",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="canopy.controller",
                    ),
                ),
            ],
            options={
                "verbose_name": "Form entry",
                "verbose_name_plural": "Form entries",
                "ordering": ["-created"],
            },
        ),
        migrations.AddConstraint(
            model_name="slot",
            constraint=models.UniqueConstraint(
                fields=("controller", "label"), name="canopy_unique_slot_label"
            ),
        ),
        migrations.AddConstraint(
            model_name="slot",
            constraint=models.UniqueConstraint(
                fields=("controller", "name"), name="canopy_unique_slot_name"
            ),
        ),
    ]
