from django.contrib.auth.models import User
from django.db import models

# models.py

class Box(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    price_per_month = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    open_gym = models.BooleanField(default=False)

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 2)
        return None

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    home_box = models.ForeignKey('Box', null=True, blank=True, on_delete=models.SET_NULL)
    favorite_workout = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)


# class Coach(models.Model):
#     box = models.ForeignKey(Box, related_name='coaches', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     certifications = models.TextField(blank=True)
#     bio = models.TextField(blank=True)

class Review(models.Model):
    box = models.ForeignKey(Box, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ClassSchedule(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)  # e.g. 'Monday'
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_type = models.CharField(max_length=100)

