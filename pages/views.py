
from tokenize import group
from django.shortcuts import redirect,render
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import Http404
from django.utils.text import slugify
import random

# Create your views here.
# C:\Users\ss\Desktop\en\project\
# ..\Scripts\activate
# python manage.py startapp
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
# python manage.py createsuperuser

def index(request):


    return render(request ,'pages/index.html')

@login_required(login_url='/accounts/login/')
def word_admin_panel(request):
    if request.user.is_superuser: 
        pass
    else:
        # raise Http404("superuser only.")
        pass
    word_group_model = apps.get_model('pages', 'groups')

    sentencees = []
    ar_sentencees = []
    sentence = 0
    word_alradey_exist = False
    ar_word = ""
    character_group = False
    out = "الحالة : Post"
    if request.method=="GET":
        from bs4 import BeautifulSoup
        from requests import get as get_link
        from googletrans import Translator

        data = request.GET
        if data:
            word_model = apps.get_model('pages', 'words')
            en_word_get = data['en_word'].strip().lower()
            if  word_model.objects.filter(en_word = en_word_get).first():
                word_alradey_exist = True
                ar_word = word_model.objects.filter(en_word = en_word_get).first().ar_word
            else:
                print(en_word_get)
                character_group =  [x for x in word_group_model.objects.all() if x.en_name.startswith(en_word_get[0]) & x.en_name.endswith("words")][0]

                translator = Translator()
                out = translator.translate(en_word_get, dest='ar')
                print(out.text)
                result = get_link(f"https://sentence.yourdictionary.com/{en_word_get}")
                print(result)
                if(result != "<Response [404]>"):
                    src = result.content
                    print("get_src")
                    soup = BeautifulSoup(src , "lxml")
                    sentence = soup.find_all("p", {"class":"sentence-item__text"})

                    for sent in sentence:
                        if len(sentencees) == 4:
                            break
                        sentencees.append(sent.text)
                        ar_sentencees.append(translator.translate(sent.text, dest='ar').text)
                        
                        print(len(sentencees))
    if request.method=="POST":
        from gtts import gTTS
        data = request.POST
        word_group_model = apps.get_model('pages', 'groups')
        word_model = apps.get_model('pages', 'words')
        sentence_model = apps.get_model('pages', 'sentence')

        make_word = word_model.objects.create(en_word=data['en_word_get'],ar_word=data['ar_word'])
        
        make_en_s1 = sentence_model.objects.create(en_word_id=make_word.id,en_sentence=data['en_sent1'],ar_sentence=data['ar_sent1'],audio_dir=slugify(data['en_sent1']))
        make_en_s2 = sentence_model.objects.create(en_word_id=make_word.id,en_sentence=data['en_sent2'],ar_sentence=data['ar_sent2'],audio_dir=slugify(data['en_sent2']))
        make_en_s3 = sentence_model.objects.create(en_word_id=make_word.id,en_sentence=data['en_sent3'],ar_sentence=data['ar_sent3'],audio_dir=slugify(data['en_sent3']))
        make_en_s4 = sentence_model.objects.create(en_word_id=make_word.id,en_sentence=data['en_sent4'],ar_sentence=data['ar_sent4'],audio_dir=slugify(data['en_sent4']))
        make_word.sentences.add(make_en_s1,make_en_s2,make_en_s3,make_en_s4)
        if 'groub' in data:
            for i in data['groub']:
                word_group_model.objects.get(id=i).words.add(make_word)

        # make sound Slugify
        word_sound = data['en_word_get']
        sound = f'C:\\Users\\ss\\Desktop\\en\\project\\project\\static\\audio\\{word_sound}.mp3' 
        sound_sen1 = f'C:\\Users\\ss\\Desktop\\en\\project\\project\\static\\audio\\sentences\\{slugify(data["en_sent1"])}.mp3' 
        sound_sen2 = f'C:\\Users\\ss\\Desktop\\en\\project\\project\\static\\audio\\sentences\\{slugify(data["en_sent2"])}.mp3' 
        sound_sen3 = f'C:\\Users\\ss\\Desktop\\en\\project\\project\\static\\audio\\sentences\\{slugify(data["en_sent3"])}.mp3' 
        sound_sen4 = f'C:\\Users\\ss\\Desktop\\en\\project\\project\\static\\audio\\sentences\\{slugify(data["en_sent4"])}.mp3' 
        sp = gTTS(text=word_sound,lang="en",slow=False)
        sp.save(sound)
        
         
        try:
            sp_sen1 = gTTS(text=data["en_sent1"],lang="en",slow=False)
            sp_sen1.save(sound_sen1)
        except:
            pass
        try:
            sp_sen2 = gTTS(text=data["en_sent2"],lang="en",slow=False)
            sp_sen2.save(sound_sen2)
        except:
            pass
        try:
            sp_sen3 = gTTS(text=data["en_sent3"],lang="en",slow=False)
            sp_sen3.save(sound_sen3)
        except:
            pass
        try:
            sp_sen4 = gTTS(text=data["en_sent4"],lang="en",slow=False)
            sp_sen4.save(sound_sen4)
        except:
            pass


    print("character_group" + str(character_group))
    if character_group != False :
        groups = word_group_model.objects.all().exclude(id = character_group.id).exclude(id = 4)
    else :
        groups = word_group_model.objects.all().exclude(id = 4) # all group
    all_group = word_group_model.objects.get(id = 4) # all group
    print(sentencees)
    print(ar_sentencees)
    
    x = {
        'sentencees':sentencees,
        'ar_sentencees':ar_sentencees,
        'groups':groups,
        'out':out.text if hasattr(out, 'text') else "الحالة : Post" ,
        'word_alradey_exist':word_alradey_exist,
        'ar_word':ar_word,
        'character_group':character_group,
        'all_group':all_group,
    }
    return render(request ,'pages/super_user.html',x)


@login_required(login_url='/accounts/login/')
def learning(request):
    word_group_model = apps.get_model('pages', 'groups')
    answer_model = apps.get_model('pages', 'answer')
    users_model = apps.get_model('pages', 'users')
    pass_word_model = apps.get_model('pages', 'pass_word')
    user = users_model.objects.get(user_au= request.user)
    word_model = apps.get_model('pages', 'words')
    subscription_model = apps.get_model('pages', 'subscriptions')

    professional_user = 1 if subscription_model.objects.filter(user = user).first() else 0
    print(professional_user)
    all_groups = word_group_model.objects.all()
    groups_inf = []

    passed_words = [model.word.id for model in pass_word_model.objects.filter(user = user)]

    for group in all_groups:
        # (groub,group_all_words_len,group_passed_wrods_len,user_have_thes_groub)
        groups_inf.append((group,
                           group.words.all().count(),
                           group.words.all().count() -len(group.words.all().exclude(id__in = passed_words)),
                           1 if group.id in [g.id for g in user.word_groups.all()] else 0
                           ))
    print(groups_inf)

    def takeSecond(elem):
        return elem[0].professional
    groups_inf.sort(key=takeSecond)

    if request.method=="POST" and 'groub' in request.POST and 'dlt' in request.POST:
        data = request.POST
        dlt_groub_id = data['groub']
        user.word_groups.remove(word_group_model.objects.get(id=dlt_groub_id))
        return redirect('pages:learning')

    x = {
        'groups_inf':groups_inf,
        'professional_user':professional_user
    }
    return render(request ,'pages/learning.html',x)

@login_required(login_url='/accounts/login/')
def word_group(request,word_group):

    word_group_model = apps.get_model('pages', 'groups')
    answer_model = apps.get_model('pages', 'answer')
    users_model = apps.get_model('pages', 'users')
    pass_word_model = apps.get_model('pages', 'pass_word')
    user = users_model.objects.get(user_au= request.user)
    word_model = apps.get_model('pages', 'words')
    subscription_model = apps.get_model('pages', 'subscriptions')

    try:
        group_ = word_group_model.objects.filter(en_name = word_group).first()
    except word_group_model.DoesNotExist:
        raise Http404("No MyModel matches the given query.")

    professional_user = 1 if subscription_model.objects.filter(user = user).first() else 0

    if group_.professional and professional_user == 0:
        return redirect('pages:learning')
    
    user.word_groups.add(group_)
    user.save()

    all_group_words = group_.words.all()
    passed_words = [model.word.id for model in pass_word_model.objects.filter(user = user)]
    words_from_same_group_notpass = group_.words.all().exclude(id__in = passed_words)

    words_from_same_group_notpass_ids = [model.id for model in words_from_same_group_notpass]
    words_from_same_group_passed = group_.words.all().exclude(id__in = words_from_same_group_notpass_ids)


    if request.method=="GET":
        data = request.GET
        
        ids_from_get = [v for k,v in data.items() if k in [word.en_word for word in words_from_same_group_notpass] ]
        print(ids_from_get)

        for id_ in ids_from_get:
            word_from_get_id = word_model.objects.get(id = id_)
            # pass_word_model.objects.get(word = word_from_get_id)
            pass_word_model.objects.create(user=user,word=word_from_get_id,group=group_)
        if len(data) > 0:
            return redirect('pages:word_group',group_)

    if request.method=="POST":
        data = request.POST
        
        ids_from_get = [v for k,v in data.items() if k in [word.en_word for word in words_from_same_group_passed] ]
        print(ids_from_get)
        
        for id_ in ids_from_get:
            word_from_get_id = word_model.objects.get(id = id_)
            pass_word_model.objects.filter(word = word_from_get_id,group = group_).first().delete()
            # pass_word_model.objects.create(user=user,word=word_from_get_id,group=group_)
        if len(data) > 0:
            return redirect('pages:word_group',group_)
    
    all_group_answers = answer_model.objects.filter(group=group_,user=user)

    word_and_worng_answer = []
    for word in all_group_words : 
        word_and_worng_answer.append((f'{word.en_word}',answer_model.objects.filter(word=word,right=False,group=group_,user=user).count(),word.id))
    
    def takeSecond(elem):
        return elem[1]

    word_and_worng_answer.sort(key=takeSecond)

    word_answer_f = []
    for word in word_and_worng_answer : 
        if answer_model.objects.filter(word=word[2],right=True,group=group_,user=user).first() and answer_model.objects.filter(word=word[2],right=False,group=group_,user=user).first() != True  :
            word_answer_f.append(word[0])
    print(word_answer_f)
    x = {
        'group_words_len':group_.words.all().count(),
        'words_from_same_group_notpass_len':group_.words.all().count() -len(words_from_same_group_notpass),
        'all_group_words':all_group_words,
        'words_from_same_group_notpass':words_from_same_group_notpass,
        'words_from_same_group_passed':words_from_same_group_passed,
        'next_word':random.choice(words_from_same_group_notpass) if len(words_from_same_group_notpass) > 0 else '',
        'group':group_,
        'allpass': 1 if group_.words.all().count() == len(words_from_same_group_passed) else 0 ,
        'word_and_worng_answer':word_and_worng_answer,
        'word_answer_f':word_answer_f,
        
        'all_group_answers_len':all_group_answers.count(),
        'worng_group_answer_len':answer_model.objects.filter(right=False,group=group_,user=user).count(),
        'right_answer_rate': answer_model.objects.filter(right=False,group=group_,user=user).count() / all_group_answers.count() * 100 if all_group_answers.count() else 0,

        'professional_user':professional_user,
    }
    return render(request ,'pages/word_group.html',x)

@login_required(login_url='/accounts/login/')
def passed_words(request):
    word_group_model = apps.get_model('pages', 'groups')
    answer_model = apps.get_model('pages', 'answer')
    users_model = apps.get_model('pages', 'users')
    pass_word_model = apps.get_model('pages', 'pass_word')
    user = users_model.objects.get(user_au= request.user)
    word_model = apps.get_model('pages', 'words')
    
    passed_wordss = [model for model in pass_word_model.objects.filter(user = user)]

    all_groups = word_group_model.objects.all()
    all_groups_words = []

    for group in  all_groups:
        for word in group.words.all():
            all_groups_words.append(word)
    passed_words_ids = [model.word.id for model in pass_word_model.objects.filter(user = user)]
    passed_words = [model.word for model in pass_word_model.objects.filter(user = user)]
    words_notpass = [word for word in all_groups_words if word.id not in passed_words_ids]

    words_notpass_ids = [model.id for model in words_notpass]


    
    all_group_answers = answer_model.objects.filter(user=user)

    word_and_worng_answer = []
    for word in all_groups_words : 
        word_and_worng_answer.append((f'{word.en_word}',answer_model.objects.filter(word=word,right=False,user=user).count(),word.id))
    
    def takeSecond(elem):
        return elem[1]

    word_and_worng_answer.sort(key=takeSecond)

    word_answer_f = []
    for word in word_and_worng_answer : 
        if answer_model.objects.filter(word=word[2],right=True,user=user).first() and answer_model.objects.filter(word=word[2],right=False,user=user).first() != True  :
            word_answer_f.append(word[0])

    x = {
        'passed_words':passed_wordss,
    }
    return render(request ,'pages/passed_words.html',x)

@login_required(login_url='/accounts/login/')
def word(request,word_group ,word):
    word_group_model = apps.get_model('pages', 'groups')
    answer_model = apps.get_model('pages', 'answer')
    users_model = apps.get_model('pages', 'users')
    pass_word_model = apps.get_model('pages', 'pass_word')
    user = users_model.objects.get(user_au= request.user)
    word_model = apps.get_model('pages', 'words')
    subscription_model = apps.get_model('pages', 'subscriptions')
    subscription_model = apps.get_model('pages', 'subscriptions')


    try:
        group_ = word_group_model.objects.filter(en_name = word_group).first()
    except word_group_model.DoesNotExist:
        raise Http404("No MyModel matches the given query.")

    try:
        word_ = word_model.objects.filter(en_word = word).first()
    except word_model.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    try   :
        group_.words.get(id = word_.id)
    except word_model.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    # professional_user = 1 if subscription_model.objects.filter(user = user).first() else 0
    # print(professional_user)
    # if group_.professional and professional_user == 0:
    #     return redirect('pages:learning')

    professional_user = 1 if subscription_model.objects.filter(user = user).first() else 0

    answer = 0
    answer_right = 0
    answer_worng = 0
    choices = []

    passed_words = [model.word.id for model in pass_word_model.objects.all()]
    words_from_same_group_notpass = group_.words.all().exclude(id__in = passed_words).exclude(id = word_.id) 

    if request.method=="POST":
        data = request.POST
        ids_from_get = [v for k,v in data.items() if k in ['en_word1','en_word2','en_word3','en_word4'] ] # and v != data['org_en_word']
        print(ids_from_get)
        print('up')
        choices = []
        # choices.append(word_)

        for choice_id in ids_from_get:
            print(choice_id)
            choices.append(word_model.objects.get(id = choice_id))

        if data['answer'] == data['org_en_word']:
            print('right')
            answer_right = 1
            answer = data['answer']
            answer_model.objects.create(word=word_,group=group_,user=user,right=True)
        else:
            print('worng')
            answer_worng = 1
            answer = data['answer']
            answer_model.objects.create(word=word_,group=group_,user=user,right=False)

        print(answer)
    elif request.method=="GET" and 'checkbox_for_save_word' in request.GET :
        data = request.GET
        pass_word_model.objects.create(user=user,word=word_,group=group_)
        if words_from_same_group_notpass:
            return redirect('pages:word',group_,random.choice(words_from_same_group_notpass))
        else:
            return redirect('pages:word_group',group_)


    else:
        
        try:
            random_1_id = random.choice(words_from_same_group_notpass)
            random_2_id = random.choice(words_from_same_group_notpass)
            random_3_id = random.choice(words_from_same_group_notpass)
        except:
            random_1_id = random.choice(word_model.objects.all())
            random_2_id = random.choice(word_model.objects.all())
            random_3_id = random.choice(word_model.objects.all())

        random_3_id = [random_1_id,random_2_id,random_3_id]
        print(random_3_id)
        choices = []
        choices.append(word_)
        for choice_id in random_3_id:
            print(choice_id)
            choices.append(word_model.objects.get(id = choice_id.id))

        while len(set(choices)) != 4 :
            if len(words_from_same_group_notpass) > 3 :
                random_1_id = random.choice(words_from_same_group_notpass)
                random_2_id = random.choice(words_from_same_group_notpass)
                random_3_id = random.choice(words_from_same_group_notpass)
            else:
                random_1_id = random.choice(word_model.objects.all())
                random_2_id = random.choice(word_model.objects.all())
                random_3_id = random.choice(word_model.objects.all())

            random_3_id = [random_1_id,random_2_id,random_3_id]
            print(random_3_id)
            choices = []
            choices.append(word_)
            for choice_id in random_3_id:
                print(choice_id)
                choices.append(word_model.objects.get(id = choice_id.id))

        random.shuffle(choices)

    x = {
        'word':word_,
        'choices':choices,
        'answer_right':answer_right,
        'answer_worng':answer_worng,
        'answer':int(answer),

        'next_word':random.choice(words_from_same_group_notpass) if len(words_from_same_group_notpass) > 0 else '',
        'group_':group_.en_name,

        'professional_user':professional_user,
    }
    return render(request ,'pages/word.html',x)


# expression