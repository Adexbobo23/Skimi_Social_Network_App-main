from django.db import models
from django.contrib.auth.models import User

""" Model for User Profile """

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name='my_friends', blank=True)
    bio = models.TextField(blank=True, null=True, max_length=350)
    date_of_birth = models.DateField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    about = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    RELATIONSHIP_CHOICES = [
        ('Single', 'Single'),
        ('In a relationship', 'In a relationship'),
        ('Engaged', 'Engaged'),
        ('Married', 'Married'),
        ('Complicated', 'Complicated'),
    ]
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, blank=True)
    location = models.CharField(max_length=255, blank=True)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    email_address = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Additional Fields
    hobbies = models.TextField(blank=True)
    favourite_movies = models.TextField(blank=True)
    favourite_books = models.TextField(blank=True)
    favourite_games = models.TextField(blank=True)
    favourite_bands_artists = models.TextField(blank=True)
    favourite_series = models.TextField(blank=True)
    other_interest = models.TextField(blank=True)
    education = models.TextField(blank=True)
    work = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'



STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted')
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

