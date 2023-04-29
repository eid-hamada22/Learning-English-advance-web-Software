from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.apps import apps
import random
from django.contrib.auth.decorators import login_required
# Create your views here.


def signup_choose_plan(request):
    step = 1

    x = {
        'step':step,
    }
    return render(request,'registration/signup.html',x)

def signup(request , plan):
    username_token = 0
    name_field,age_field,gender_field,stage_field,email_field,password_field,phone_field = None,None,None,None,None,None,None
    if request.method=="POST":
        data = request.POST
        user_dt = apps.get_model('pages', 'users')

        if User.objects.filter(email = data['email']).first():
            username_token = 1
            name_field,age_field,gender_field,stage_field,email_field,password_field,phone_field = data['name'],data['age'],data['gender'],data['stage'],data['email'],data['password'],data['phone']
        else:
            if User.objects.filter(username = data['name']).first():
                new_user = User.objects.create_user(username=(data['name'] + str(random.randrange(1,100000000))).replace(' ', '_'),email=data['email'],password=data['password'])
            else:
                new_user = User.objects.create_user(username=data['name'],email=data['email'].replace(' ', '_'),password=data['password'])
            new_user.save()
            user_dt.objects.create(user_au=new_user,name=data['name'],age=data['age'],gender=data['gender'],stage=data['stage'],phone=data['phone'])
            username = data['name']
            password = data['password']
            user = authenticate(username=username,password=password)
            auth_login(request,user)
            if plan == "pro":
                return redirect('/accounts/signup/code_activation')
            if plan == "free":
                return redirect('/accounts/free')




    step =2
    
    x = {
        'step':step,
        'username_token':username_token,
        'name_field':name_field,'age_field':age_field,'gender_field':gender_field,'stage_field':stage_field,'email_field':email_field,'password_field':password_field,'phone_field':phone_field,
    }
    return render(request,'registration/signup.html',x)

@login_required(login_url='/accounts/login/')
def signup_code_activation(request):
    cards = apps.get_model('pages', 'cards').objects.filter(active = False)
    subscriptions = apps.get_model('pages', 'subscriptions')
    user_profile = apps.get_model('pages', 'users')
    logging_user = request.user
    user_profile_dt = user_profile.objects.get(user_au = logging_user)

    # Check if the user has a pre-activated code
    if subscriptions.objects.filter(user = user_profile_dt).first():
        return redirect('pages:learning')

    step = 3
    code_rigte = 0
    code_notrigte = 0


    cards = apps.get_model('pages', 'cards').objects.filter(active = False)
    codes = []
    for card in cards:
        codes.append(int(card.num))
        print(card)
    if request.method=="GET" and 'code' in request.GET:
        data = request.GET
        code = data['code']
        if int(code) in codes:
            code_rigte = 1
        else:  
            code_notrigte =  1

    if request.method=="POST":
        data = request.POST
        code = data['code']
        if int(code) in codes:
            print('code_rigte')
            w_card = cards.get(num = code)

            mack_subscrip = subscriptions.objects.create(user = user_profile_dt,card=w_card)
            if mack_subscrip:
                w_card.active = True
                w_card.save()
                return redirect('pages:learning')
        else:
            return redirect('/accounts/signup/code_activation')



    
    print("coderight = " + str(code_rigte))
    x = {
        'step':step,
        'user':logging_user,
        'code_rigte':code_rigte,
        'code_notrigte':code_notrigte,
    }
    return render(request,'registration/signup.html',x)


def login(request):


    worng_password = 0
    worng_email = 0
    email_value = None
    password_value = None

    if request.method=="POST":
        data = request.POST
        try:
            user = User.objects.get(email = data['email'])
            if user.check_password(data['password']):
                user_login = authenticate(username=user.username,password=data['password'])
                auth_login(request,user_login)
                if data['next']:
                    return redirect(data['next'])
                else:
                    return redirect('pages:learning')
                
            else:
                worng_password = 1
                email_value = data['email']
                password_value = data['password']
        except User.DoesNotExist:
            worng_email = 1
            email_value = data['email']
            password_value = data['password']
    print(email_value)
    x = {
        'worng_email':worng_email,
        'worng_password':worng_password,
        'email_value':email_value,
        'password_value':password_value,
    }
    return render(request,'registration/login_user.html',x)

