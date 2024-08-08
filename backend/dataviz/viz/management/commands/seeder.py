import json
from django.core.management.base import BaseCommand
from django_seed import Seed
from datetime import datetime
from django.utils import timezone
from viz.models import InsightData

class Command(BaseCommand):
    help = 'Seed the database with sample data for InsightData'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, choices=['insert', 'delete'], help='Action to perform: insert or delete')

    def handle(self, *args, **options):
        action = options['action']

        if action == 'insert':
            self.insert_data()
        elif action == 'delete':
            self.delete_data()

    def insert_data(self):
        with open('jsondata.json', 'r', encoding='utf-8') as file:
            sample_data = json.load(file)

        seeder = Seed.seeder()

        for data in sample_data:
            if data.get('added'):
                added_naive = datetime.strptime(data.get('added'), "%B, %d %Y %H:%M:%S")
                added = timezone.make_aware(added_naive, timezone.get_current_timezone())
            else:
                added = None
            
            if data.get('published'):
                published_naive = datetime.strptime(data.get('published'), "%B, %d %Y %H:%M:%S")
                published = timezone.make_aware(published_naive, timezone.get_current_timezone())
            else:
                published = None
            
            intensity = int(data.get('intensity')) if data.get('intensity') else None
            relevance = int(data.get('relevance')) if data.get('relevance') else None
            likelihood = int(data.get('likelihood')) if data.get('likelihood') else None
            
            seeder.add_entity(InsightData, 1, {
                'end_year': data.get('end_year'),
                'intensity': intensity,
                'sector': data.get('sector'),
                'topic': data.get('topic'),
                'insight': data.get('insight'),
                'url': data.get('url'),
                'region': data.get('region'),
                'start_year': data.get('start_year'),
                'impact': data.get('impact'),
                'added': added,
                'published': published,
                'country': data.get('country'),
                'relevance': relevance,
                'pestle': data.get('pestle'),
                'source': data.get('source'),
                'title': data.get('title'),
                'likelihood': likelihood,
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS('Data insertion complete.'))

    def delete_data(self):
        InsightData.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Data deletion complete.'))
