import random

from src.gmail_client import Email

# Do not modify this file


class TestDataGenerator:
    def __init__(self):
        self.names = [
            "John Smith",
            "Emily Johnson",
            "Michael Brown",
            "Sarah Davis",
            "David Wilson",
            "Jessica Miller",
            "James Taylor",
            "Ashley Anderson",
            "Christopher Thomas",
            "Amanda Jackson",
            "Matthew White",
            "Jennifer Harris",
            "Joshua Martin",
            "Elizabeth Thompson",
            "Daniel Garcia",
            "Stephanie Martinez",
            "Anthony Robinson",
            "Michelle Clark",
            "Mark Rodriguez",
            "Lisa Lewis",
            "Steven Lee",
            "Karen Walker",
            "Paul Hall",
            "Betty Allen",
            "Edward Young",
            "Helen Hernandez",
            "Jason King",
            "Sandra Wright",
            "Ryan Lopez",
            "Donna Hill",
            "Kevin Scott",
            "Carol Green",
            "Brian Adams",
            "Ruth Baker",
            "George Gonzalez",
            "Sharon Nelson",
            "Eric Carter",
            "Maria Mitchell",
            "Stephen Perez",
            "Laura Roberts",
            "Andrew Turner",
            "Dorothy Phillips",
            "Kenneth Campbell",
            "Lisa Parker",
            "Joshua Evans",
            "Nancy Edwards",
            "Kevin Collins",
            "Betty Stewart",
            "Ronald Sanchez",
            "Helen Morris",
        ]

        self.companies = [
            "TechCorp",
            "InnovaSoft",
            "DataSystems",
            "CloudTech",
            "NextGen Solutions",
            "CodeCraft",
            "ByteWorks",
            "PixelPerfect",
            "WebWorks",
            "AppMasters",
            "DevSolutions",
            "TechFlow",
            "DigitalEdge",
            "SmartSystems",
            "ProCode",
        ]

        self.subject_templates = [
            "pseudo internship interest application",
            "Applying for pseudo internship position - great interest",
            "Interest in pseudo internship program",
            "pseudo internship application - very interested",
            "Looking for pseudo internship opportunity with interest",
            "pseudo internship interest inquiry",
            "Application: pseudo internship position interest",
            "Seeking pseudo internship role - high interest",
        ]

        self.invalid_subjects = [
            "Job application",
            "internship opportunity",
            "pseudo job posting",
            "interest in position",
            "Software engineer role",
            "Marketing internship interest",
            "Data analyst pseudo position",
        ]

        self.email_endings = [
            "Best regards,\n{name}",
            "Sincerely,\n{name}",
            "Thanks,\n{name}",
            "Regards,\n{name}",
            "Best,\n{name}",
            "Thank you,\n{name}",
            "Kind regards,\n{name}",
        ]

        self.body_templates = [
            """Dear Hiring Manager,

I am writing to express my strong interest in the pseudo internship position at your company. I believe this opportunity would be perfect for my career development.

I have relevant experience in software development and am eager to contribute to your team.

{ending}""",
            """Hello,

I came across your pseudo internship posting and I am very interested in applying. I think this role aligns perfectly with my career goals.

My background includes programming and problem-solving skills that would be valuable for this position.

{ending}""",
            """Hi there,

I would like to apply for the pseudo internship program. I am passionate about technology and excited about the opportunity to learn.

I have been developing my skills and would love to contribute to your organization.

{ending}""",
        ]

    def generate_valid_email(self) -> Email:
        name = random.choice(self.names)
        company = random.choice(self.companies)
        subject = random.choice(self.subject_templates)
        body_template = random.choice(self.body_templates)
        ending_template = random.choice(self.email_endings)

        ending = ending_template.format(name=name)
        body = body_template.format(ending=ending)

        email_address = f"{name.lower().replace(' ', '.')}@{company.lower()}.com"

        return Email(
            id=f"email_{random.randint(1000, 9999)}",
            subject=subject,
            body=body,
            sender=email_address,
            recipient="hiring@company.com",
        )

    def generate_invalid_email(self) -> Email:
        name = random.choice(self.names)
        company = random.choice(self.companies)
        subject = random.choice(self.invalid_subjects)
        body_template = random.choice(self.body_templates)
        ending_template = random.choice(self.email_endings)

        ending = ending_template.format(name=name)
        body = body_template.format(ending=ending)

        email_address = f"{name.lower().replace(' ', '.')}@{company.lower()}.com"

        return Email(
            id=f"email_{random.randint(1000, 9999)}",
            subject=subject,
            body=body,
            sender=email_address,
            recipient="hiring@company.com",
        )

    def generate_email_without_name(self) -> Email:
        company = random.choice(self.companies)
        subject = random.choice(self.subject_templates)

        body = """Dear Hiring Manager,

I am writing to express my strong interest in the pseudo internship position at your company.

I have relevant experience and am eager to contribute to your team.

Looking forward to hearing from you."""

        email_address = f"anonymous@{company.lower()}.com"

        return Email(
            id=f"email_{random.randint(1000, 9999)}",
            subject=subject,
            body=body,
            sender=email_address,
            recipient="hiring@company.com",
        )

    def generate_test_emails(self, count: int = 1000) -> list[Email]:
        emails = []

        valid_count = int(count * 0.6)  # 60% valid emails
        invalid_count = int(count * 0.3)  # 30% invalid emails
        no_name_count = count - valid_count - invalid_count  # remaining without names

        for _ in range(valid_count):
            emails.append(self.generate_valid_email())

        for _ in range(invalid_count):
            emails.append(self.generate_invalid_email())

        for _ in range(no_name_count):
            emails.append(self.generate_email_without_name())

        random.shuffle(emails)
        return emails
