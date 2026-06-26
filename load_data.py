import csv
import json
import os
import sys


# Добавляем текущую папку в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Homework_27.settings')

import django

django.setup()

from ads.models import Category, Ad
from users.models import User, Location


def load_categories():
    """Загрузка категорий"""
    json_path = os.path.join('datasets', 'category.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            print("⚠️ Файл category.json пуст")
            return 0

        inserted = 0
        for item in data:
            try:
                Category.objects.create(
                    name=item.get('name', '').strip()
                )
                inserted += 1
                print(f'✅ Загружена категория: {item.get("name", "без названия")[:30]}')
            except Exception as e:
                print(f'❌ Ошибка при загрузке категории ID {item.get("id", "unknown")}: {e}')

        print(f'\n✅ Загружено {inserted} категорий')
        return inserted

    except FileNotFoundError:
        print(f'❌ Файл {json_path} не найден')
        return 0
    except Exception as e:
        print(f'❌ Ошибка: {e}')
        return 0


def load_ads():
    """Загрузка объявлений"""
    json_path = os.path.join('datasets', 'ad.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            print("⚠️ Файл ad.json пуст")
            return 0

        inserted = 0
        for item in data:
            try:
                # Проверяем, существует ли категория
                category_id = int(item.get('category_id', 0))
                if category_id:
                    category = Category.objects.get(id=category_id)
                else:
                    category = None

                Ad.objects.create(
                    name=item.get('name', '').strip(),
                    author_id=int(item.get('author_id', '').strip()),
                    price=int(item.get('price', 0).strip()),
                    description=item.get('description', '').strip(),
                    is_published=item.get('is_published', False).title(),
                    image=item.get('image'),
                    category=category
                )
                inserted += 1
                print(f'✅ Загружено объявление: {item.get("name", "без названия")[:30]}')
            except Exception as e:
                print(f'❌ Ошибка при загрузке объявления ID {item.get("Id", "unknown")}: {e}')

        print(f'\n✅ Загружено {inserted} объявлений')
        return inserted

    except FileNotFoundError:
        print(f'❌ Файл {json_path} не найден')
        return 0
    except Exception as e:
        print(f'❌ Ошибка: {e}')
        return 0


def load_locations():
    """Загрузка локаций"""
    json_path = os.path.join('datasets', 'location.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            print("⚠️ Файл location.json пуст")
            return 0

        inserted = 0
        for item in data:
            try:
                Location.objects.create(
                    name=item.get('name', '').strip(),
                    lat=float(item.get('lat', 9.99)),
                    lng=float(item.get('lng', 9.99))
                )
                inserted += 1
                print(f'✅ Загружена локация: {item.get("name", "без названия")[:30]}')
            except Exception as e:
                print(f'❌ Ошибка при загрузке локации ID {item.get("id", "unknown")}: {e}')

        print(f'\n✅ Загружено {inserted} локаций')
        return inserted

    except FileNotFoundError:
        print(f'❌ Файл {json_path} не найден')
        return 0
    except Exception as e:
        print(f'❌ Ошибка: {e}')
        return 0


def load_users():
    """Загрузка пользователей"""
    json_path = os.path.join('datasets', 'user.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            print("⚠️ Файл user.json пуст")
            return 0

        inserted = 0
        for item in data:
            try:
                # Проверяем, существует ли локация
                location_id = int(item.get('location_id', 0))
                if location_id:
                    locations = Location.objects.get(id=location_id)
                else:
                    locations = None

                User.objects.create(
                    first_name=item.get('first_name', '').strip(),
                    last_name=item.get('last_name', 'last_name_default').strip(),
                    username=item.get('username', 'username_default').strip(),
                    password=item.get('password', '1'),
                    role=item.get('role', 'member'),
                    age=int(item.get('age', 18)),
                    location=locations
                )
                inserted += 1
                print(f'✅ Загружен пользователь: {item.get("username", "без имени")}')
            except Exception as e:
                print(f'❌ Ошибка при загрузке пользователя ID {item.get("id", "unknown")}: {e}')

        print(f'\n✅ Загружено {inserted} пользователей')
        return inserted

    except FileNotFoundError:
        print(f'❌ Файл {json_path} не найден')
        return 0
    except Exception as e:
        print(f'❌ Ошибка: {e}')
        return 0


def clear_database():
    """Очистка базы данных"""
    confirm = input("⚠️ Вы уверены, что хотите очистить все таблицы? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Очистка отменена")
        return False

    try:
        print("🗑️ Удаление всех данных...")
        Ad.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        Location.objects.all().delete()
        print("✅ База данных очищена")
        return True
    except Exception as e:
        print(f"❌ Ошибка при очистке: {e}")
        return False


def load_all_data():
    """Загрузка всех данных"""
    print("=" * 60)
    print("🚀 Начинаем загрузку данных в базу данных PostgreSQL")
    print("=" * 60)

    # Проверяем подключение к БД
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✅ Подключение к базе данных установлено")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return

    # Загружаем данные в правильном порядке
    print("\n📂 1. Загрузка локаций...")
    locations_count = load_locations()

    print("\n📂 2. Загрузка пользователей...")
    users_count = load_users()

    # print("\n📂 3. Загрузка категорий...")
    # categories_count = load_categories()

    # print("\n📂 4. Загрузка объявлений...")
    # ads_count = load_ads()

    # Итог
    print("\n" + "=" * 60)
    print("📊 ИТОГИ ЗАГРУЗКИ:")
    print(f"   Локации: {locations_count}")
    print(f"   Пользователи: {users_count}")
    # print(f"   Категории: {categories_count}")
    # print(f"   Объявления: {ads_count}")
    print("=" * 60)
    print("✅ Загрузка завершена!")


def convert_csv_to_json():
    """Конвертация CSV в JSON (если нужно)"""
    files = ['ad.csv', 'category.csv', 'user.csv', 'location.csv']

    for file_name in files:
        csv_path = os.path.join('datasets', file_name)
        json_path = os.path.join('datasets', file_name.replace('.csv', '.json'))

        if not os.path.exists(csv_path):
            print(f"⚠️ Файл {csv_path} не найден, пропускаем")
            continue

        try:
            with open(csv_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                data = list(reader)

            with open(json_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)

            print(f"✅ Конвертирован {file_name} -> {json_path}")
        except Exception as e:
            print(f"❌ Ошибка при конвертации {file_name}: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == '--clear':
            clear_database()
        elif sys.argv[1] == '--convert':
            convert_csv_to_json()
        elif sys.argv[1] == '--help':
            print("""
📋 ДОСТУПНЫЕ КОМАНДЫ:
    python load_data.py          - Загрузить все данные
    python load_data.py --clear  - Очистить базу данных перед загрузкой
    python load_data.py --convert - Конвертировать CSV в JSON
    python load_data.py --help   - Показать эту справку
            """)
        else:
            print(f"❌ Неизвестная команда: {sys.argv[1]}")
    else:
        load_all_data()


def csv_to_json():
    with open('datasets/user.csv', 'r', encoding='utf-8') as file:
        data = csv.DictReader(file)
        data = list(data)

    with open('datasets/user.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# csv_to_json()

