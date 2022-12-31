from random import choices
from time import timezone



from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f'{self.username} '



class Category(models.Model):
    NAME_CHOICES = [ 
        ('Fashion', 'Fashion'),
        ('Toys','Toys'),
        ('Electronics','Electronics'),
        ('Home', 'Home'),
        ('Other', 'Other')
    ]

    name = models.CharField(max_length=12, choices= NAME_CHOICES, unique=True)
    def __str__(self):
        return self.name

class Bid(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', null=True)
    value = models.DecimalField(decimal_places=2, max_digits=256)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bids', default=20.00)
    date = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return f'{self.value}'



class Listing(models.Model):
    NAME_CHOICES = [ 
        ('Fashion', 'Fashion'),
        ('Toys','Toys'),
        ('Electronics','Electronics'),
        ('Home', 'Home'),
        ('Other', 'Other')
    ]
    
    title = models.CharField(max_length= 64)
    date_made = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, related_name='user_listings', null=True)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=264, default=10.00)
    upload_image = models.ImageField(blank=True, upload_to='media/media')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='name', related_name='category_listings', default=NAME_CHOICES[4][0], db_constraint=False)
    listing_category = models.CharField(max_length=12, choices=NAME_CHOICES, null=True, default=NAME_CHOICES[4][0])
    is_active = models.BooleanField(default=True)
    watchlist = models.ForeignKey('Watchlist', on_delete=models.DO_NOTHING, related_name='listings', null=True)
    class Meta:
        ordering = ['-date_made']
    def __str__(self):
        return f'{self.title}'
    


class Comment(models.Model):
    user = models.ForeignKey(User,to_field='username', on_delete=models.CASCADE, related_name='user_comments')
    comment_text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_comments')
    def __str__(self):
        return f'comment by {self.user}'

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    




    




