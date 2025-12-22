from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from app.models import Customer, Product

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding data...")

        self.seed_customers(10)
        self.seed_products(5)

        self.stdout.write(self.style.SUCCESS("✅ Seeding completed"))

    def seed_customers(self, count):
        customers = []

        for _ in range(count):
            customers.append(
                Customer(
                    name=fake.name(),
                    email=fake.unique.email(),
                    phone=fake.phone_number()
                )
            )

        Customer.objects.bulk_create(customers)
        self.stdout.write(f"✔ Created {count} customers")

    def seed_products(self, count):
        products = []

        for _ in range(count):
            products.append(
                Product(
                    name=fake.word(),
                    price=fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                )
            )

        Product.objects.bulk_create(products)
        self.stdout.write(f"✔ Created {count} products")
