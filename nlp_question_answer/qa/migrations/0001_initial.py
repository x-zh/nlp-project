# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('title', models.TextField()),
                ('h1', models.TextField()),
                ('h2', models.TextField()),
                ('h3', models.TextField()),
                ('h4', models.TextField()),
                ('h5', models.TextField()),
                ('p', models.TextField()),
                ('div', models.TextField()),
                ('dt', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
