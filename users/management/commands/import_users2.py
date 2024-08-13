import openpyxl
from django.core.management.base import BaseCommand, CommandError
from users.models import User
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Import users from an Excel file using bulk operations'

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

        new_users = []
        existing_users = []
        errors = []

        with transaction.atomic():
            for row in sheet.iter_rows(min_row=2, values_only=True):
                username, password, role, phone_number = row

                if not all([username, password, role, phone_number]):
                    errors.append(f"Skipping row with incomplete data: {row}")
                    continue

                try:
                    hashed_password = make_password(password)

                    try:
                        user = User.objects.get(username=username)
                        # Update existing user's fields
                        user.password = hashed_password
                        user.role = role
                        user.phone_number = phone_number
                        existing_users.append(user)
                    except User.DoesNotExist:
                        # Create a new user object
                        new_users.append(User(
                            username=username,
                            password=hashed_password,
                            role=role,
                            phone_number=phone_number,
                        ))

                except IntegrityError as e:
                    errors.append(f"Failed to process row {row}: {str(e)}")

            # Bulk create new users
            if new_users:
                User.objects.bulk_create(new_users)
                self.stdout.write(self.style.SUCCESS(f"Created {len(new_users)} users."))

            # Bulk update existing users
            if existing_users:
                User.objects.bulk_update(existing_users, ['password', 'role', 'phone_number'])
                self.stdout.write(self.style.SUCCESS(f"Updated {len(existing_users)} users."))

        if errors:
            self.stdout.write(self.style.ERROR("Some rows could not be processed:"))
            for error in errors:
                self.stdout.write(self.style.ERROR(error))

        self.stdout.write(self.style.SUCCESS("User import completed."))
