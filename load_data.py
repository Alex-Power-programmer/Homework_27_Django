# load_data.py - поместите в корень проекта (рядом с manage.py)
import json
import os
import sys

# Добавляем текущую папку в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Homework_27.settings')

import django

django.setup()

from ads.models import Categories


def load_ads():
    json_path = os.path.join('datasets', 'categories.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            print("⚠️ Файл пуст")
            return

        inserted = 0
        for item in data:
            try:
                Categories.objects.create(
                    id=int(item['id']),
                    name=item['name'].strip(),
                )
                inserted += 1
                print(f'✅ Загружено: {item["name"][:30]}...')
            except Exception as e:
                print(f'❌ Ошибка при загрузке ID {item.get("Id", "unknown")}: {e}')

        print(f'\n✅ Успешно загружено {inserted} из {len(data)} записей')

    except FileNotFoundError:
        print(f'❌ Файл {json_path} не найден')
    except Exception as e:
        print(f'❌ Ошибка: {e}')


if __name__ == "__main__":
    load_ads()
