from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Barcha jadvallarni tozalaydi va ID'larni qayta tiklaydi."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Baza ma'lumotlari tozalanmoqda..."))

        with connection.cursor() as cursor:
            # Barcha jadvallarni olish
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                if table_name not in ['django_migrations']:  # Muhim jadvallarni o‘chirmaslik
                    try:
                        cursor.execute(f'TRUNCATE TABLE "{table_name}" CASCADE;')
                        self.stdout.write(self.style.SUCCESS(f'Toza qilindi: {table_name}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Xato: {table_name} - {e}"))

        self.stdout.write(self.style.SUCCESS("✅ Baza muvaffaqiyatli tozalandi!"))
