# Generated by Django 5.0.2 on 2024-03-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_queue', '0002_alter_patient_personal_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_gold',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
