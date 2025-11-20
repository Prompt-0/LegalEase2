#
# NEW LOCATION: apps/core/management/commands/populate_db.py
#
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

# Import all models from all apps
from apps.users.models import Profile
from apps.finders.models import PoliceStation, LegalCase, Helpline
from apps.legal_tools.models import LegalAct, Chapter, Section
from apps.doc_generator.models import DocumentTemplate

class Command(BaseCommand):
    help = 'Populates the database with comprehensive dummy data for all apps'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')

        # Clear old data (User is handled separately)
        PoliceStation.objects.all().delete()
        LegalCase.objects.all().delete()
        Helpline.objects.all().delete()
        LegalAct.objects.all().delete() # This is now safe, as we repopulate
        DocumentTemplate.objects.all().delete()

        # Clear non-superuser users and their profiles
        User.objects.filter(is_superuser=False).delete()

        fake = Faker('en_IN') # Use Indian names and addresses

        self.stdout.write('Creating new data...')

        # --- 1. Create Users & Profiles (Citizens) ---
        self.stdout.write('Creating 5 dummy citizens...')
        for _ in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create_user(
                username=f"{first_name.lower()}_{last_name.lower()}",
                email=fake.email(),
                password='password123',
                first_name=first_name,
                last_name=last_name
            )
            # Profile is created automatically by the signal
            user.profile.user_type = 'CITIZEN'
            user.profile.save()

        # --- 2. Create Users & Profiles (Lawyers) ---
        self.stdout.write('Creating 5 dummy lawyers...')
        specializations = ['Criminal Law', 'Civil Law', 'Corporate Law', 'Family Law', 'Property Law']
        for spec in specializations:
            first_name = fake.first_name()
            last_name = fake.last_name()
            lawyer_user = User.objects.create_user(
                username=f"adv_{first_name.lower()}",
                email=fake.email(),
                password='password123',
                first_name=first_name,
                last_name=last_name
            )
            lawyer_user.profile.user_type = 'LAWYER'
            lawyer_user.profile.specialization = spec
            lawyer_user.profile.location = f"{fake.city()} High Court"
            lawyer_user.profile.experience_years = random.randint(3, 20)
            lawyer_user.profile.phone_number = fake.phone_number()
            lawyer_user.profile.save()

        # --- 3. Create Finders App Data ---
        self.stdout.write('Creating 15 police stations...')
        for _ in range(15):
            PoliceStation.objects.create(
                name=f"{fake.city()} {random.choice(['Main', 'East', 'West'])} Station",
                address=fake.street_address(),
                pincode=fake.postcode(),
                district=fake.city(), # Using city as district for simplicity
                phone_number=fake.phone_number()
            )

        self.stdout.write('Creating 10 legal cases...')
        case_categories = ['Theft', 'Property Dispute', 'Assault', 'Fraud', 'Consumer Complaint']
        for _ in range(10):
            LegalCase.objects.create(
                title=f"Case of {fake.word()} vs {fake.word()}",
                summary=fake.paragraph(nb_sentences=5),
                category=random.choice(case_categories)
            )

        self.stdout.write('Creating 5 helplines...')
        Helpline.objects.create(name="Police Emergency", phone_number="100", category="Emergency")
        Helpline.objects.create(name="Women Helpline", phone_number="1091", category="Women")
        Helpline.objects.create(name="Childline", phone_number="1098", category="Child")
        Helpline.objects.create(name="Cyber Crime", phone_number="1930", category="Cybercrime")
        Helpline.objects.create(name="Senior Citizen", phone_number="14567", category="General")

        # --- 4. Create Legal Tools App Data (FIX) ---
        self.stdout.write('Creating dummy legal acts (BNS)...')

        # Create an Act
        bns_act = LegalAct.objects.create(
            name="Bharatiya Nyaya Sanhita (BNS)",
            description="The new penal code of India.",
            category="Criminal"
        )

        # Create Chapters for the Act
        ch1 = Chapter.objects.create(act=bns_act, chapter_number="I", title="Preliminary")
        ch2 = Chapter.objects.create(act=bns_act, chapter_number="II", title="Of Punishments")

        # Create Sections for Chapter 1
        Section.objects.create(chapter=ch1, section_number="1", title="Short title and commencement", content="This Act may be called the Bharatiya Nyaya Sanhita...")
        Section.objects.create(chapter=ch1, section_number="2", title="Definitions", content="In this Sanhita, unless the context otherwise requires...")

        # Create Sections for Chapter 2
        Section.objects.create(chapter=ch2, section_number="4", title="Punishments", content="The punishments to which offenders are liable under the provisions of this Sanhita are...")
        Section.objects.create(chapter=ch2, section_number="5", title="Community Service", content="Community service shall be a punishment for petty offences...")

        self.stdout.write('Dummy legal acts, chapters, and sections created.')


        # --- 5. Create Document Templates ---
        self.stdout.write('Creating dummy document templates...')
        DocumentTemplate.objects.create(
            name="Legal Notice",
            description="Draft a formal legal notice to be sent by an advocate.",
            js_file_path="js/doc_templates/legal_notice.js",
            icon_class="fas fa-file-signature"
        )
        DocumentTemplate.objects.create(
            name="Rental Agreement",
            description="Create a basic residential lease agreement.",
            js_file_path="js/doc_templates/rental_agreement.js", # (You would need to create this JS file)
            icon_class="fas fa-file-contract"
        )
        self.stdout.write('2 dummy document templates created.')


        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
