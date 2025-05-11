import json
from pathlib import Path
from django.core.management.base import BaseCommand
from main.models import Food, Image

class Command(BaseCommand):
    help = 'Import foods from db.json'

    def handle(self, *args, **kwargs):
        file_path = Path('main/db.json')
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f'db.json not found at {file_path.resolve()}'))
            return

        with file_path.open(encoding='utf-8') as f:
            data = json.load(f)

        # بررسی نوع data و انتخاب لیست مناسب
        if isinstance(data, dict) and 'foods' in data:
            foods = data['foods']
        elif isinstance(data, list):
            foods = data
        else:
            self.stdout.write(self.style.ERROR('Invalid db.json structure: Expected a dict with "foods" key or a list'))
            return

        for item in foods:
            # نرمال‌سازی comments
            comments = [comment['txt'] if isinstance(comment, dict) else comment for comment in item['comments']]
            # پردازش تصویر
            image_path = item['image'].replace('/image/', 'images/')
            image_instance, created = Image.objects.get_or_create(
                image=image_path,
                defaults={'title': item['name']}
            )
            # ذخیره غذا
            Food.objects.update_or_create(
                id=item['id'],
                defaults={
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': item['quantity'],
                    'ingredients': item['ingredients'],
                    'image': image_instance,
                    'rating': float(item['rating']),
                    'comments': comments,
                    'type': item['type'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Foods imported successfully.'))