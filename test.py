list = ["16170275"]

code = int("16170275")

print("dsaddsa" + str(123))


from unicodedata import name
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
    forbidden_words = models.ManyToManyField('words')
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
    words = models.ManyToManyField('words')
    basic = models.BooleanField(default=0)
    made_by = models.ForeignKey(users,on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.made_by)


class words(models.Model):
    en_word = models.CharField(max_length=255)
    ar_word = models.CharField(max_length=255)
    sentences = models.ManyToManyField('sentence')
    entry_date = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return str(self.en_word)


class sentence(models.Model):
    en_word_id = models.IntegerField()
    sentence = models.CharField(max_length=1000)
    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name)


from django.urls import path
from . import views

app_name='pages'

urlpatterns = [
    path('', views.index, name="index"),
    path('learning', views.learning, name="learning"),
    path('learning/<str:word_group>', views.word_group, name="word_group"),
]


from tokenize import group
from django.shortcuts import render
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import Http404

# Create your views here.
# ..\Scripts\activate
# python manage.py startapp
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

def index(request):
    return render(request ,'pages/index.html')


@login_required(login_url='/accounts/login/')
def learning(request):
    return render(request ,'pages/learning.html')

@login_required(login_url='/accounts/login/')
def word_group(request,word_group):
    word_group_model = apps.get_model('pages', 'word_groups')
    try:
        group = word_group_model.objects.get(en_name = word_group)
    except word_group_model.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    group = word_group_model.objects.get_or
    return render(request ,'pages/word_group.html')