# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ('-created',), 'get_latest_by': 'created'},
        ),
        migrations.AddField(
            model_name='dataset',
            name='datatype',
            field=models.CharField(default=b'csv', max_length=4, choices=[(b'csv', b'csv'), (b'json', b'json'), (b'xml', b'xml')]),
        ),
        migrations.AlterModelTable(
            name='dataset',
            table='datasets',
        ),
    ]
