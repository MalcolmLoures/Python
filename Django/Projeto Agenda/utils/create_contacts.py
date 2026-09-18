import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice
import django # type: ignore
from django.conf import settings # type: ignore

DJANGO_BASE_DIR = Path(__file__).parent.parent

NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    
    import faker # type: ignore
    from contact.models import Category, Contact

    Contact.objects.all().delete()    
    Category.objects.all().delete()
    
    fake = faker.Faker('pt_BR')
    categories = ['Amigos', 'Família', 'Conhecidos', 'Trabalho']
    django_categories = [Category(name = namecateg) for namecateg in categories]
    
    for category in django_categories:
        category.save()
        
    django_contacts = []
    
    for _ in range(NUMBER_OF_OBJECTS):
        
        profile = fake.profile()
        email = profile['mail']
        fist_name , last_name = profile['name'].split(' ', 1)
        phone = fake.phone_number()
        create_date: datetime = fake.date_this_year()
        
        description = fake.text(max_nb_chars = 100)
        category = choice(django_categories)
        
        django_contacts.append (
            Contact (
                first_name = fist_name,
                last_name = last_name,
                phone = phone,
                email = email,
                created_date = create_date,
                description = description,
                category = category
            )
        )
    
    if len(django_contacts) > 0:
        Contact.objects.bulk_create(django_contacts)