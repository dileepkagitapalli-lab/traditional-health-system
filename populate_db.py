import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traditional_health_cms.settings")
django.setup()

from django.contrib.auth.models import User
from main.models import Profile, Post

def create_sample_data():
    print("Creating admin...")
    admin, created = User.objects.get_or_create(username='admin', email='admin@admin.com')
    if created:
        admin.set_password('admin123')
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        Profile.objects.get_or_create(user=admin, role='admin')

    print("Creating user...")
    user1, created = User.objects.get_or_create(username='janedoe', email='jane@test.com')
    if created:
        user1.set_password('test1234')
        user1.save()
        Profile.objects.get_or_create(user=user1, role='user')

    print("Creating creator...")
    creator1, created = User.objects.get_or_create(username='ayurveda_expert', email='expert@test.com')
    if created:
        creator1.set_password('creator1234')
        creator1.save()
        Profile.objects.get_or_create(user=creator1, role='creator')

    print("Creating posts...")
    if Post.objects.count() == 0:
        Post.objects.create(
            title="Benefits of Ashwagandha",
            content="Ashwagandha is an ancient medicinal herb. It's classified as an adaptogen, meaning that it can help your body manage stress.",
            category="ayurveda",
            creator=creator1,
            status="approved"
        )
        Post.objects.create(
            title="Ginger Tea for Colds",
            content="Boil ginger in water for 10 minutes. Add honey and lemon. This is an excellent natural remedy for sore throats and colds.",
            category="remedies",
            creator=creator1,
            status="pending"
        )
        Post.objects.create(
            title="Sun Salutation (Surya Namaskar)",
            content="A sequence of 12 powerful yoga poses. Besides being a great cardiovascular workout, Surya Namaskar is also known to have an immensely positive impact on the body and mind.",
            category="yoga",
            creator=creator1,
            status="approved"
        )
        print("Posts created successfully.")
    else:
        print("Posts already exist.")

if __name__ == '__main__':
    create_sample_data()
