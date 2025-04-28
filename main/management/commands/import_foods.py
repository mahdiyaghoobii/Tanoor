import json
from pathlib import Path
from django.core.management.base import BaseCommand
from main.models import Food, Image


class Command(BaseCommand):
    help = 'Import foods from db.json'

    def handle(self, *args, **kwargs):
        file_path = Path('main/db.json')  # مسیر صحیح فایل جیسون

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f'db.json not found at {file_path.resolve()}'))
            return

        with file_path.open(encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            # پیدا کردن یا ساختن تصویر
            image_path = item['image'].replace('/image/', 'images/')  # چون در media/images هستند
            image_instance, created = Image.objects.get_or_create(
                title=item['name'],  # یا هر عنوان مناسب دیگه
                defaults={'image': image_path}
            )

            # ساختن یا آپدیت غذ
            Food.objects.update_or_create(
                id=item['id'],
                defaults={
                    'name': item['name'],
                    'price': item['price'],
                    'stringPrice': item['stringPrice'],
                    'quantity': item['quantity'],
                    'ingredients': item['ingredients'],
                    'image': image_instance,
                    'rating': item['rating'],
                    'comments': item['comments'],
                    'type': item['type'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Foods imported successfully.'))
