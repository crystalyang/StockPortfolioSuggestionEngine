# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stockportfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticker', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=10)),
                ('exchange', models.CharField(max_length=10)),
                ('close', models.DecimalField(max_digits=8, decimal_places=2)),
                ('volume', models.DecimalField(max_digits=20, decimal_places=2)),
                ('strategy', models.CharField(max_length=20)),
            ],
        ),
    ]
