# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coffer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='_description_rendered',
            field=models.TextField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='description',
            field=markupfield.fields.MarkupField(default=None, null=True, rendered_field=True, blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='description_markup_type',
            field=models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'html', 'HTML'), (b'plain', 'Plain'), (b'markdown', 'Markdown')]),
        ),
        migrations.AddField(
            model_name='dataset',
            name='title',
            field=models.CharField(default=None, max_length=128, null=True, blank=True),
        ),
    ]
