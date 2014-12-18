# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_paragraph'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='annotations',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
