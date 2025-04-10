# Generated by Django 5.1.7 on 2025-03-29 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_alter_doctorschedule_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('confirmed', 'Confirmado'), ('cancelled', 'Candelada'), ('completed', 'Completada')], default='pending', max_length=10)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_doctor', to='users.doctorprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_patient', to='users.patientprofile')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('doctor', 'date', 'start_time'), name='unique_appointment')],
            },
        ),
    ]
