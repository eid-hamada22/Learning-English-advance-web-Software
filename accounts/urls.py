
from django.urls import include, path

from . import views

app_name='accounts'

urlpatterns = [
    path('signup/choose_plan',views.signup_choose_plan , name='signup_choose_plan'),
    path('signup/choose_plan/<str:plan>',views.signup , name='signup'),
    path('signup/code_activation',views.signup_code_activation , name='signup_code_activation'),
    path('login/',views.login , name='login'),
    # path('profile',views.profile , name='profile'),
    # path('profile/edit',views.profile_edit , name='profile_edit'),

]