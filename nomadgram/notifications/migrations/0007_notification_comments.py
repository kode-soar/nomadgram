# Generated by Django 2.0.13 on 2019-03-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20190314_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
