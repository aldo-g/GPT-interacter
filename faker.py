from faker import Faker

fake = Faker()

def generate_fake_cv():
    return {
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'job_title': fake.job(),
        'skills': [fake.word() for _ in range(5)],
        'education': {
            'university': fake.university(),
            'degree': fake.job(),
            'graduation_year': fake.year()
        },
        'experience': [{
            'company': fake.company(),
            'position': fake.job(),
            'duration': f"{fake.month_name()} {fake.year()} - {fake.month_name()} {fake.year()}",
            'description': fake.sentence()
        } for _ in range(3)]
    }

def generate_fake_job_listing():
    return {
        'job_title': fake.job(),
        'company': fake.company(),
        'location': fake.city(),
        'description': fake.text(),
        'requirements': [fake.sentence() for _ in range(5)],
        'responsibilities': [fake.sentence() for _ in range(5)],
        'benefits': [fake.sentence() for _ in range(3)]
    }

# Generate a fake CV
cv = generate_fake_cv()
print("Fake CV:", cv)

# Generate a fake job listing
job_listing = generate_fake_job_listing()
print("Fake Job Listing:", job_listing)