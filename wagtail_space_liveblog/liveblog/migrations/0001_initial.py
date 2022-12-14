# Generated by Django 4.0.3 on 2022-03-15 12:02

import django.db.models.deletion
import django.utils.timezone
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="LiveBlogPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "channel_id",
                    models.CharField(
                        blank=True, help_text="Channel ID", max_length=255, unique=True
                    ),
                ),
                (
                    "last_updated_at",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        help_text="Last update of this page",
                    ),
                ),
                (
                    "live_posts",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "live_post",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "message_id",
                                            wagtail.core.blocks.CharBlock(
                                                help_text="Message's ID"
                                            ),
                                        ),
                                        (
                                            "created",
                                            wagtail.core.blocks.DateTimeBlock(
                                                help_text="Date and time of message creation",
                                                required=False,
                                            ),
                                        ),
                                        (
                                            "modified",
                                            wagtail.core.blocks.DateTimeBlock(
                                                help_text="Date and time of last update",
                                                required=False,
                                            ),
                                        ),
                                        (
                                            "show",
                                            wagtail.core.blocks.BooleanBlock(
                                                default=True,
                                                help_text="Indicates if this message is shown/hidden",
                                                required=False,
                                            ),
                                        ),
                                        (
                                            "content",
                                            wagtail.core.blocks.StreamBlock(
                                                [
                                                    (
                                                        "text",
                                                        wagtail.core.blocks.RichTextBlock(
                                                            help_text="Text of the message"
                                                        ),
                                                    ),
                                                    (
                                                        "image",
                                                        wagtail.images.blocks.ImageChooserBlock(
                                                            help_text="Image of the message"
                                                        ),
                                                    ),
                                                    (
                                                        "embed",
                                                        wagtail.embeds.blocks.EmbedBlock(
                                                            help_text="URL of the embed message"
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        ),
                                        (
                                            "posted_by",
                                            wagtail.snippets.blocks.SnippetChooserBlock(
                                                "liveblog.Person", required=False
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ],
                        blank=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", models.Model),
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "slack_id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
    ]
