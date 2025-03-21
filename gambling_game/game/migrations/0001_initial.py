# Generated by Django 5.1.6 on 2025-03-06 10:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_bet', models.DecimalField(decimal_places=2, max_digits=15)),
                ('original_bet', models.DecimalField(decimal_places=2, max_digits=15)),
                ('current_stage', models.IntegerField(default=1)),
                ('current_label', models.CharField(default='Poor', max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-started_at'],
            },
        ),
        migrations.CreateModel(
            name='GameStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_number', models.IntegerField(unique=True)),
                ('safe_doors', models.IntegerField(default=1)),
                ('mid_safe_doors', models.IntegerField(default=2)),
                ('not_safe_doors', models.IntegerField(default=1)),
                ('label_on_complete', models.CharField(default='Poor', max_length=20)),
            ],
            options={
                'ordering': ['stage_number'],
            },
        ),
        migrations.CreateModel(
            name='GameMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.IntegerField()),
                ('move_type', models.CharField(choices=[('SAFE', 'Safe'), ('MID_SAFE', 'Mid-Safe'), ('NOT_SAFE', 'Not Safe')], max_length=10)),
                ('outcome', models.CharField(choices=[('WIN', 'Win'), ('LOSS', 'Loss'), ('PARTIAL', 'Partial')], max_length=10)),
                ('bet_before', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bet_after', models.DecimalField(decimal_places=2, max_digits=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='game.gamesession')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PlayerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=100.0, max_digits=15)),
                ('highest_label', models.CharField(default='Poor', max_length=20)),
                ('games_played', models.IntegerField(default=0)),
                ('games_won', models.IntegerField(default=0)),
                ('total_bet', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('total_winnings', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gamesession',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.playerprofile'),
        ),
    ]
