# Generated by Django 4.1 on 2023-10-20 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_rename_myuploadfiles_uploadfilemodel"),
    ]

    operations = [
        migrations.RenameField(
            model_name="uploadfilemodel",
            old_name="myfiles",
            new_name="myfile",
        ),
    ]
