import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from apps.users.models import Profile
from apps.finders.models import PoliceStation, LegalCase, Helpline
from apps.legal_tools.models import LegalAct, Chapter, Section

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        # Clear old data
        User.objects.filter(is_superuser=False).delete()
        PoliceStation.objects.all().delete()
        LegalCase.objects.all().delete()
        Helpline.objects.all().delete()
        LegalAct.objects.all().delete() # This cascades to delete Chapters and Sections

        fake = Faker('en_IN') # Use Indian names/addresses

        self.stdout.write('Creating new data...')

        # --- 1. Create Dummy Lawyers ---
        specializations = ['Criminal Law', 'Civil Law', 'Corporate Law', 'Family Law', 'Property Law', 'Tax Law']
        locations = ['Delhi High Court', 'Mumbai High Court', 'Supreme Court', 'District Court, Pune', 'District Court, Bangalore']

        for _ in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f'{first_name.lower()}_{last_name.lower()}{random.randint(1, 99)}'
            email = f'{username}@fake-law.com'

            user = User.objects.create_user(
                username=username,
                password='password123',
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            # Update the profile created by the signal
            user.profile.user_type = 'LAWYER'
            user.profile.specialization = random.choice(specializations)
            user.profile.location = random.choice(locations)
            user.profile.experience_years = random.randint(2, 20)
            user.profile.phone_number = fake.phone_number()
            user.profile.save()

        self.stdout.write(self.style.SUCCESS('50 dummy lawyers created.'))

        # --- 2. Create Dummy Citizens ---
        for _ in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f'{first_name.lower()}{random.randint(1, 99)}'
            email = f'{username}@fake-mail.com'
            user = User.objects.create_user(
                username=username,
                password='password123',
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            # Profile is already set to 'CITIZEN' by default

        self.stdout.write(self.style.SUCCESS('50 dummy citizens created.'))

        # --- 3. Create Dummy Police Stations ---
        districts = ['South Delhi', 'North Delhi', 'East Delhi', 'West Delhi', 'Central Delhi']
        for _ in range(40):
            district = random.choice(districts)
            name = f'{district.split(" ")[0]} {fake.street_suffix()} Police Station'
            PoliceStation.objects.create(
                name=name,
                address=fake.address(),
                pincode=fake.postcode(),
                district=district,
                phone_number=fake.phone_number()
            )
        self.stdout.write(self.style.SUCCESS('40 dummy police stations created.'))

        # --- 4. Create Dummy Legal Cases ---
        categories = ['Property Dispute', 'Consumer Complaint', 'Contract Law', 'Theft', 'Assault']
        for _ in range(60):
            category = random.choice(categories)
            LegalCase.objects.create(
                title=f'Case of {category}: {fake.company()} vs. {fake.company()}',
                summary=fake.paragraph(nb_sentences=5),
                category=category
            )
        self.stdout.write(self.style.SUCCESS('60 dummy legal cases created.'))

        # --- 5. Create Dummy Helplines ---
        helplines = [
            {'name': 'National Emergency Response', 'phone': '112', 'cat': 'Emergency', 'desc': 'All-in-one emergency number.'},
            {'name': 'Police', 'phone': '100', 'cat': 'Emergency', 'desc': 'Police emergency services.'},
            {'name': 'Fire', 'phone': '101', 'cat': 'Emergency', 'desc': 'Fire department.'},
            {'name': 'Ambulance', 'phone': '102', 'cat': 'Medical', 'desc': 'Medical emergency services.'},
            {'name': 'Childline India', 'phone': '1098', 'cat': 'Child', 'desc': 'Helpline for children in distress.'},
            {'name': 'Women Helpline (Domestic Abuse)', 'phone': '181', 'cat': 'Women', 'desc': 'Helpline for women facing violence.'},
            {'name': 'National Consumer Helpline', 'phone': '1915', 'cat': 'Consumer', 'desc': 'For consumer complaints.'},
            {'name': 'Cyber Crime Helpline', 'phone': '1930', 'cat': 'Cybersecurity', 'desc': 'For reporting cyber fraud.'},
            {'name': 'Senior Citizen Helpline', 'phone': '14567', 'cat': 'General', 'desc': 'Helpline for senior citizens.'},
        ]

        for h in helplines:
            Helpline.objects.create(
                name=h['name'],
                phone_number=h['phone'],
                category=h['cat'],
                description=h['desc']
            )
        self.stdout.write(self.style.SUCCESS(f'{len(helplines)} dummy helplines created.'))

        # --- 6. Create Dummy Legal Acts ---
        self.stdout.write('Creating dummy legal acts...')

        # Act 1: BNS
        bns = LegalAct.objects.create(
            name="Bharatiya Nyaya Sanhita (BNS)",
            description="An Act to consolidate and amend the provisions in the Indian Penal Code.",
            category="Criminal"
        )

        ch_bns_1 = Chapter.objects.create(act=bns, chapter_number="1", title="Preliminary")
        Section.objects.create(chapter=ch_bns_1, section_number="1", title="Short title and commencement", content="This Act may be called the Bharatiya Nyaya Sanhita, 2023.")

        ch_bns_2 = Chapter.objects.create(act=bns, chapter_number="2", title="Of Punishments")
        Section.objects.create(chapter=ch_bns_2, section_number="4", title="Punishments", content="The punishments to which offenders are liable under this Sanhita are...")
        Section.objects.create(chapter=ch_bns_2, section_number="5", title="Community service", content="A new punishment added to the code.")

        ch_bns_6 = Chapter.objects.create(act=bns, chapter_number="6", title="Of Offences Affecting the Human Body")
        Section.objects.create(chapter=ch_bns_6, section_number="101", title="Culpable homicide", content="Whoever causes death by doing an act with the intention of causing death...")
        Section.objects.create(chapter=ch_bns_6, section_number="103", title="Murder", content="Culpable homicide is murder, if the act by which the death is caused is done...")
        Section.objects.create(chapter=ch_bns_6, section_number="124", title="Assault", content="Whoever makes any gesture, or any preparation, intending or knowing it to be likely...")

        ch_bns_17 = Chapter.objects.create(act=bns, chapter_number="17", title="Of Offences Against Property")
        Section.objects.create(chapter=ch_bns_17, section_number="301", title="Theft", content="Whoever, intending to take dishonestly any moveable property out of the possession of any person...")

        # Act 2: BNSS
        bnss = LegalAct.objects.create(
            name="Bharatiya Nagarik Suraksha Sanhita (BNSS)",
            description="An Act to consolidate and amend the law relating to Criminal Procedure.",
            category="Procedure"
        )
        ch_bnss_1 = Chapter.objects.create(act=bnss, chapter_number="1", title="Preliminary")
        Section.objects.create(chapter=ch_bnss_1, section_number="1", title="Short title and commencement", content="This Act may be called the Bharatiya Nagarik Suraksha Sanhita, 2023.")

        ch_bnss_12 = Chapter.objects.create(act=bnss, chapter_number="12", title="Information to the Police and their Powers to Investigate")
        Section.objects.create(chapter=ch_bnss_12, section_number="173", title="Information in cognizable cases (FIR)", content="Every information relating to the commission of a cognizable offence... shall be reduced to writing.")

        # Act 3: BSA
        bsa = LegalAct.objects.create(
            name="Bharatiya Sakshya Adhiniyam (BSA)",
            description="An Act to consolidate and provide for general rules and principles of evidence.",
            category="Evidence"
        )
        ch_bsa_1 = Chapter.objects.create(act=bsa, chapter_number="1", title="Preliminary")
        Section.objects.create(chapter=ch_bsa_1, section_number="1", title="Short title and commencement", content="This Act may be called the Bharatiya Sakshya Adhiniyam, 2023.")
        ch_bsa_2 = Chapter.objects.create(act=bsa, chapter_number="2", title="Of the Relevancy of Facts")
        Section.objects.create(chapter=ch_bsa_2, section_number="24", title="Admissions", content="An admission is a statement, oral or documentary or contained in electronic form...")

        self.stdout.write(self.style.SUCCESS('3 dummy legal acts with chapters/sections created.'))
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
