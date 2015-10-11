# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffer', '0002_auto_20151010_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='filesize',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
