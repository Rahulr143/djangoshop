# Generated by Django 3.1.7 on 2021-04-09 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20210409_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Address',
            new_name='address',
        ),
    ]
