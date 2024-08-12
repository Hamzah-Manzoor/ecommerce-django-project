import openpyxl
from django.core.management.base import BaseCommand, CommandError
from users.models import User
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Import users from an Excel file'

    def handle(self, *args, **kwargs):
        file_path = 'UberEats.xlsx'

        try:
            wb = openpyxl.load_workbook(file_path)
            sheet = wb['Users']
        except FileNotFoundError:
            raise CommandError(f"File '{file_path}' does not exist.")
        except KeyError:
            raise CommandError("The 'Users' sheet is not found in the Excel file.")

        self.stdout.write(self.style.SUCCESS(f"Processing '{file_path}'..."))

        errors = []
        with transaction.atomic():
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skipping the header row
                username, password, role, phone_number = row

                if not all([username, password, role, phone_number]):
                    errors.append(f"Skipping row with incomplete data: {row}")
                    continue

                try:
                    hashed_password = make_password(password)

                    user, created = User.objects.update_or_create(
                        username=username,
                        defaults={
                            'password': hashed_password,
                            'role': role,
                            'phone_number': phone_number,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Updated user: {username}"))

                except IntegrityError as e:
                    errors.append(f"Failed to process row {row}: {str(e)}")

        if errors:
            self.stdout.write(self.style.ERROR("Some rows could not be processed:"))
            for error in errors:
                self.stdout.write(self.style.ERROR(error))

        self.stdout.write(self.style.SUCCESS("User import completed."))
