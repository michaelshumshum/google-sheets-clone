# Generated by Django 4.0.4 on 2022-04-25 02:12

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataframe', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
