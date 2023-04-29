
from django.urls import path
from . import views

app_name='pages'

urlpatterns = [
    path('', views.index, name="index"),
    path('eid_hamada/password/222007/@eid_hamada22', views.word_admin_panel),
    path('learning', views.learning, name="learning"),
    path('learning/passed_words', views.passed_words, name="passed_words"),
    path('learning/<str:word_group>', views.word_group, name="word_group"),
    path('learning/<str:word_group>/<str:word>', views.word, name="word"),
]
