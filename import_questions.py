import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jamb_cbt.settings')
django.setup()

from exams.models import Subject, Question

with open('questions.csv', newline='', encoding='latin-1') as file:
    reader = csv.DictReader(file)

    for row in reader:
        subject, created = Subject.objects.get_or_create(name=row['subject'])

        Question.objects.create(
            subject=subject,
            question_text=row['Question'],
            option_a=row['Option A'],
            option_b=row['Option B'],
            option_c=row['Option C'],
            option_d=row['Option D'],
            correct_option=row['Answer'],
            year=row['Year']
        )

print("Questions imported successfully!")