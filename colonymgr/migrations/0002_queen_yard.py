# Generated by Django 2.1.4 on 2018-12-08 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('colonymgr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queen',
            name='yard',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='queens', to='colonymgr.Yard'),
        ),
    ]