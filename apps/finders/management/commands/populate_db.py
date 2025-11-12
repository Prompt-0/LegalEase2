import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from apps.users.models import Profile
from apps.finders.models import PoliceStation, LegalCase, Helpline
from apps.legal_tools.models import LegalAct, Chapter, Section
# --- NEW: Import doc generator model ---
from apps.doc_generator.models import DocumentTemplate

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        # Clear old data
        User.objects.filter(is_superuser=False).delete()
        PoliceStation.objects.all().delete()
        LegalCase.objects.all().delete()
        Helpline.objects.all().delete()
        LegalAct.objects.all().delete()
        DocumentTemplate.objects.all().delete() # <-- ADD THIS

        fake = Faker('en_IN')

        self.stdout.write('Creating new data...')

        # --- 1-6 ... (Keep all other sections: Lawyers, Citizens, etc.) ---

        # --- 7. NEW: Create Dummy Document Templates ---
        self.stdout.write('Creating dummy document templates...')
        DocumentTemplate.objects.create(
            name="Legal Notice",
            description="Draft a formal legal notice to be sent by an advocate.",
            js_file_path="js/doc_templates/legal_notice.js",
            icon_class="fas fa-file-signature"
        )
        # We can add more templates here in the future

        self.stdout.write(self.style.SUCCESS('1 dummy document template created.'))
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
