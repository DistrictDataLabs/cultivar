# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('dataset', models.FileField(upload_to=b'datasets')),
                ('dimensions', models.PositiveIntegerField(default=0)),
                ('length', models.PositiveIntegerField(default=0)),
                ('filesize', models.PositiveIntegerField(default=0)),
                ('signature', models.CharField(unique=True, max_length=44, blank=True)),
                ('datatype', models.CharField(default=b'csv', max_length=4, choices=[(b'csv', b'csv'), (b'json', b'json'), (b'xml', b'xml')])),
                ('delimiter', models.CharField(default=b',', max_length=1)),
                ('uploader', models.ForeignKey(related_name='datasets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
                'db_table': 'datasets',
                'get_latest_by': 'created',
            },
        ),
    ]
