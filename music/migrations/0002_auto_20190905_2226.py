# Generated by Django 2.2.5 on 2019-09-05 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
