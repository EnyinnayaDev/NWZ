from django.core.management.base import BaseCommand

from core.models import Service

SERVICES = [
    {
        'name': 'General Nutrition Consultation',
        'summary': 'A full assessment of your eating habits, lifestyle and health goals.',
        'description': (
            "A one-on-one session where Chizitere reviews your current diet, medical "
            "history and lifestyle, then builds a realistic nutrition plan you can "
            "actually stick to. Great as a first session for anyone new to NWZ."
        ),
        'duration_minutes': 45,
        'price': 15000,
        'icon': 'leaf',
        'order': 1,
    },
    {
        'name': 'Weight Management Program',
        'summary': 'Sustainable, personalised plans for healthy weight loss or gain.',
        'description': (
            "A structured program that pairs meal planning with realistic habit "
            "changes to help you reach and maintain a healthy weight — without "
            "extreme dieting."
        ),
        'duration_minutes': 60,
        'price': 25000,
        'icon': 'scale',
        'order': 2,
    },
    {
        'name': 'Diabetes & Chronic Disease Nutrition',
        'summary': 'Meal planning support for diabetes, hypertension and related conditions.',
        'description': (
            "Nutrition guidance tailored for managing diabetes, hypertension and "
            "other chronic conditions — focused on blood sugar control, heart health "
            "and working alongside your existing treatment plan."
        ),
        'duration_minutes': 60,
        'price': 25000,
        'icon': 'heart',
        'order': 3,
    },
    {
        'name': 'Maternal & Child Nutrition',
        'summary': 'Guidance for pregnancy, breastfeeding and early childhood feeding.',
        'description': (
            "Support for expecting and new mothers — covering pregnancy nutrition, "
            "breastfeeding, and safe, healthy weaning and feeding plans for infants "
            "and toddlers."
        ),
        'duration_minutes': 45,
        'price': 20000,
        'icon': 'baby',
        'order': 4,
    },
    {
        'name': 'Corporate Wellness Session',
        'summary': 'Nutrition talks and wellness check-ins for teams and organisations.',
        'description': (
            "A workplace wellness package — nutrition talks, group Q&A and optional "
            "individual check-ins to help teams build healthier habits."
        ),
        'duration_minutes': 90,
        'price': 60000,
        'icon': 'briefcase',
        'order': 5,
    },
    {
        'name': 'Follow-up / Progress Review',
        'summary': 'A shorter check-in to review progress and adjust your plan.',
        'description': (
            "For existing clients — a shorter session to review progress against "
            "your goals and fine-tune your nutrition plan."
        ),
        'duration_minutes': 30,
        'price': 10000,
        'icon': 'plate',
        'order': 6,
    },
]


class Command(BaseCommand):
    help = "Seed the database with NWZ's default service list."

    def handle(self, *args, **options):
        created_count = 0
        for data in SERVICES:
            _, created = Service.objects.get_or_create(
                name=data['name'], defaults=data
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(
            f"Seeded services: {created_count} created, "
            f"{len(SERVICES) - created_count} already existed."
        ))
