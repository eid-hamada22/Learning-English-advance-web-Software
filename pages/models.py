from django.db import models
from django.contrib.auth.models import User
import random
User._meta.get_field('email')._unique = True

# Create your models here.
stage_choices = [
    ('graduate', 'graduate'),
    ('College', 'College'),
    ('High_school', 'High_school'),
    ('middle_School', 'middle_School'),   
    ('primary_school', 'primary_school'),
]

class users(models.Model):
    user_au = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    age = models.IntegerField()
    gender = models.CharField(choices=[('male', 'male'),('female', 'female'),],max_length=50)
    stage = models.CharField(choices=stage_choices, max_length=50)
    phone = models.IntegerField()
    word_groups = models.ManyToManyField('groups')
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class subscriptions(models.Model):
    user = models.OneToOneField("users",on_delete=models.CASCADE)
    card = models.OneToOneField("cards",on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.user)

class cards(models.Model):
    num = models.IntegerField(blank=True,null=True,unique=True)
    active = models.BooleanField(default=False)
    entry_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.num = random.randrange(10000000, 100000000)
        super(cards, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.num)

class groups(models.Model):
    en_name = models.CharField(max_length=255)
    ar_name = models.CharField(max_length=255)
    words = models.ManyToManyField('words',blank=True)
    made_by = models.ForeignKey(users,on_delete=models.CASCADE)
    basic = models.BooleanField(default=False)
    professional = models.BooleanField(default=False)
    book = models.BooleanField(default=False)
    img = models.ImageField()
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.en_name)


class words(models.Model):
    en_word = models.CharField(max_length=255)
    ar_word = models.CharField(max_length=255)
    sentences = models.ManyToManyField('sentence')
    entry_date = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return str(self.en_word)

    class Meta:
        ordering = ("en_word",)


class sentence(models.Model):
    en_word_id = models.IntegerField()
    en_sentence = models.CharField(max_length=1000)
    ar_sentence = models.CharField(max_length=1000)
    entry_date = models.DateTimeField(auto_now_add=True)
    audio_dir = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.en_sentence)


class answer(models.Model):
    word = models.ForeignKey('words',on_delete=models.CASCADE)
    group = models.ForeignKey('groups',on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey('users',on_delete=models.CASCADE)
    right = models.BooleanField()
    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.word)


class pass_word(models.Model):
    word = models.ForeignKey('words',on_delete=models.CASCADE)
    group = models.ForeignKey('groups',on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey('users',on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.word)
