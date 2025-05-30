# Generated by Django 3.1.12 on 2025-02-26 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cnn_model',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False)),
                ('model_accuracy', models.CharField(max_length=10)),
                ('model_name', models.CharField(max_length=10)),
                ('model_executed', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'Cnn_model',
            },
        ),
        migrations.CreateModel(
            name='Comparison_graph',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False)),
                ('Cnn', models.CharField(max_length=10, null=True)),
                ('MobileNet', models.CharField(max_length=10, null=True)),
                ('Densenet', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'Comparisongraph',
            },
        ),
        migrations.CreateModel(
            name='Densenet_model',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False)),
                ('model_accuracy', models.CharField(max_length=10)),
                ('model_name', models.CharField(max_length=10)),
                ('model_executed', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'Densenet_model',
            },
        ),
        migrations.CreateModel(
            name='MobileNet_model',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False)),
                ('model_accuracy', models.CharField(max_length=10)),
                ('model_name', models.CharField(max_length=10)),
                ('model_executed', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'MobileNet_model',
            },
        ),
        migrations.CreateModel(
            name='Train_test_split_model',
            fields=[
                ('S_No', models.AutoField(primary_key=True, serialize=False)),
                ('Images_training', models.CharField(max_length=10, null=True)),
                ('Images_validation', models.CharField(max_length=10, null=True)),
                ('Images_testing', models.CharField(max_length=10, null=True)),
                ('Images_classes', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'Traintestsplit',
            },
        ),
    ]
