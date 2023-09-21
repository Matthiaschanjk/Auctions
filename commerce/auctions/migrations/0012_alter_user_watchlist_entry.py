# Generated by Django 4.2.3 on 2023-09-20 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_user_watchlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_watchlist',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_entries', to='auctions.entries'),
        ),
    ]