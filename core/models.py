from django.db import models
from django.contrib.auth.models import User

ROOM_TYPE_CHOICES = [
    ('Single Room', 'Single Room'),
    ('Double Room', 'Double Room'),
    ('Flat 2BHK', 'Flat 2BHK'),
    ('Flat 3BHK', 'Flat 3BHK'),
    ('PG', 'PG'),
]

class Room(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    location = models.CharField(max_length=200)
    full_address = models.TextField()
    description = models.TextField()
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # ✅ CONTACT DETAILS
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Images
    image1 = models.ImageField(upload_to='rooms/')
    image2 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image3 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image4 = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return self.title