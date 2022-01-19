import datetime
import json
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,F
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App_Quiz.models import *
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from App_Account.models import *

def Home(request):
    rankuser=Profile.objects.all().order_by('-points')[:3]
    category=Categoty.objects.all().order_by("-id")[:4]
    tournament=Tournament.objects.filter(end_date__gte=datetime.date.today()).order_by("-id")[:4]

    context={
        'category':category,
        'rankuser':rankuser,
        'tournament':tournament,
    }
    return render(request,'OnlineQuiz/index.html',context)

def CategoryView(request):
    categories=Categoty.objects.all().order_by("-id")
    categories = Paginator(categories, 8)
    page = request.GET.get('page')
    try:
        posts = categories.page(page)
    except PageNotAnInteger:
        posts = categories.page(1)
    except EmptyPage:
        posts = categories.page(categories.num_pages)
    context={
        'categories':posts,
    }
    return render(request,'App_Quiz/category.html',context)


def TournamentView(request):
    all_tournaments=Tournament.objects.filter(end_date__gte=datetime.date.today()).order_by("-id")
    all_tournaments = Paginator(all_tournaments, 8)
    page = request.GET.get('page')
    try:
        posts = all_tournaments.page(page)
    except PageNotAnInteger:
        posts = all_tournaments.page(1)
    except EmptyPage:
        posts = all_tournaments.page(all_tournaments.num_pages)
    context={
        'all_tournaments':posts,
    }
    return render(request,'App_Quiz/tournaments.html',context)


@login_required(login_url='App_Account:login')
def Tournamentstart(request,id):
    is_complete=False
    is_first=False
    tournament=Tournament.objects.get(id=id)
    if tournament.attemp.filter(id=request.user.id).exists():
        is_complete=True
    if tournament.fisrt_attemp.filter(id=request.user.id).exists():
        is_first=True
    questions=[]
    all_question=TournamentQuestion.objects.filter(tournament=tournament)
    for q in all_question:
        if q.attemp.filter(id=request.user.id).exists():
            pass
        else:
            questions.append(q)
    qunique_question_id=[]
    for i in all_question:
        qunique_question_id.append(i.id)
    context={
        'all_question':questions,
        'remain_question':len(questions),
        'tournament':tournament,
        'is_complete':is_complete,
        'qunique_question_id':qunique_question_id,
        'is_first':is_first,
    }
    return render(request,'App_Quiz/starttournament.html',context)

def Completed(request):
    body = json.loads(request.body)
    q_id=body['journalId']
    question=TournamentQuestion.objects.get(id=q_id)
    if question.attemp.filter(id=request.user.id).exists():
        pass
    else:
        question.attemp.add(request.user)
        question.save()
    return HttpResponse("Done")
def GetPoints(request,id):
    tournament = Tournament.objects.get(id=id)
    if tournament.attemp.filter(id=request.user.id).exists():
        pass
    else:
        tournament.attemp.add(request.user)
        tournament.save()
    prof = Profile.objects.get(user=request.user)
    prof.points = prof.points + tournament.winning_points
    prof.save()
    return redirect(tournament.get_absolute_url())
def TournamentResult(request,id):
    tournament = Tournament.objects.get(id=id)
    if tournament.fisrt_attemp.filter(id=request.user.id).exists():
        pass
    else:
        tournament.fisrt_attemp.add(request.user)
        tournament.save()

    all_question = TournamentQuestion.objects.filter(tournament=tournament)
    count=0
    for i in all_question:
        if i.attemp.filter(id=request.user.id).exists():
            count=count+1
    context={
        'corrent':count,
        'tournament':tournament,
        'total_question':len(all_question),
    }
    return render(request,'App_Quiz/tournamentresult.html',context)
def Wronganswer(request):
    body = json.loads(request.body)
    tournament = Tournament.objects.get(id=body['tournament_id'])
    prof = Profile.objects.get(user=request.user)
    if prof.points>=tournament.entry_point:
        prof.points = F('points') - tournament.entry_point
        prof.save()
        return redirect('App_Quiz:home')


def ViewCategory(request,id):
    if Categoty.objects.filter(id=id).exists():
        cate=Categoty.objects.get(id=id)
        question=Question.objects.filter(category=cate).order_by("-id")[:10]
        is_attemp=False
        if request.user.is_authenticated:
            print("login")
            if cate.attemp.filter(id=request.user.id).exists():
                is_attemp=True
        context={
            'category':cate,
            'question':question,
            'is_attemp':is_attemp,
        }
        return render(request,'App_Quiz/quizdetails.html',context)
    else:
        context = {
            'category': None,
            'question': None,
        }
        return render(request,'App_Quiz/quizdetails.html',context)

def StartQuiz(request,id):
    from requests import get
    ip = get('https://api.ipify.org').text
    print(ip)
    if Categoty.objects.filter(id=id).exists():
        cat=Categoty.objects.get(id=id)
        qunique_question=[]
        qunique_question_id=[]
        attend_question=[]
        questtion = Question.objects.filter(category_id=cat)
        if len(questtion)==0:
            context={
                'msg':"There is no question is these category"
            }
            return render(request, 'App_Quiz/startquiz.html', context)
        else:
            if request.user.is_authenticated:
                level=""
                if UserLevel.objects.filter(user=request.user, categry=cat).exists():
                    user = UserLevel.objects.get(user=request.user, categry=cat)
                    if user.points <=20:
                        level="Novice learner"
                        questtion=Question.objects.filter(category=cat,level="easy")
                    elif request.user.profile.level >20 and request.user.profile.level <=40:
                        level = "Advanced learner"
                        questtion=Question.objects.filter(category=cat,level="medium")
                        for i in questtion:
                            print(i.level)
                    elif request.user.profile.level > 40:
                        level = "Expert learner"
                        questtion=Question.objects.filter(category=cat,level="hard")

                for i in questtion:
                    if i.read_at.filter(id=request.user.id):
                        attend_question.append(i.id)
                    else:
                        qunique_question.append(i.id)
                print("unique=",qunique_question)
                n = 5
                if len(qunique_question)>=5:
                    qunique_question_id=random.sample(qunique_question,n)
                    questtion_=Question.objects.filter(id__in=qunique_question_id)
                    attend_question=len(attend_question)
                else:
                    questtion_ = []
                    attend_question = len(attend_question)
                attemps = QuizAtemp.objects.filter(user=request.user, category_id=cat)

                context = {
                    'question': questtion_,
                    'all_question': questtion,
                    'qunique_question_id':qunique_question_id,
                    'attend_question':questtion.count()-attend_question,
                    'category':cat,
                    'attemps':attemps,
                    'user':level,
                }
                return render(request, 'App_Quiz/startquiz.html', context)
            else:
                questtion = Question.objects.filter(category=cat)
                for i in questtion:
                    if i.read_at.filter(id=request.user.id):
                        attend_question.append(i.id)
                    else:
                        qunique_question.append(i.id)
                print("unique=", qunique_question)
                n = 5
                if len(qunique_question) >= 5:
                    qunique_question_id = random.sample(qunique_question, n)
                    questtion_ = Question.objects.filter(id__in=qunique_question_id)
                    attend_question = len(attend_question)
                else:
                    questtion_ = []
                    attend_question = len(attend_question)
                context = {
                    'question': questtion_,
                    'all_question': questtion,
                    'qunique_question_id': qunique_question_id,
                    'attend_question': questtion.count() - attend_question,
                    'category': cat,
                }
                return render(request, 'App_Quiz/startquiz.html', context)

    else:
        return HttpResponse("<h1>Category is not valid</h1>")

def CheckResult(request,id):
    cat=Categoty.objects.get(id=id)
    if request.method == "POST":
        try:
            time_Toke = request.POST['time']
            ftr = [60, 1]
            res = sum([a * b for a, b in zip(ftr, map(int, time_Toke.split(':')))])
        except:
            return render(request, 'App_Quiz/404page.html')
        correct_answer=int(request.POST['correct'])
        wrong_answer=int(request.POST['wrong'])
        select_question=request.POST['question_no']
        total_poin=0
        if correct_answer<=0:
            total_poin=0
        else:
            total_poin=correct_answer * 100 + res
        if request.user.is_authenticated:
            if UserLevel.objects.filter(user=request.user,categry=cat).exists():
                user=UserLevel.objects.get(user=request.user,categry=cat)
                user.points=user.points+correct_answer
                user.save()
            else:
                user=UserLevel.objects.create(
                    user=request.user,points=correct_answer,categry=cat
                )
                user.save()
            pro=Profile.objects.get(user=request.user)
            pro.points=pro.points+total_poin
            pro.save()
            for i in select_question.split(','):
                Question.objects.get(id=i).read_at.add(request.user)
            atm = QuizAtemp.objects.create(
                user=request.user, category_id=cat.id, score=correct_answer * 100 + res,correct=correct_answer,wrong=wrong_answer
            )
            atm.save()
        context = {
            'score': correct_answer,
            'total_question':request.POST['total_question'],
            'point': total_poin,
            'category': cat,
            'time': cat.total_time-res/60,
            'total_time': cat.total_time,
        }
        return render(request, 'App_Quiz/unauthresult.html', context)
    return HttpResponse("hi")

def Result(request,id):
    res=TempResult.objects.get(id=id)
    return render(request,'App_Quiz/result.html',context={'result':res})

def ViewAnswer(request,id):
    all_q=Question.objects.filter(category_id=id)
    context={
        'questions':all_q,
    }
    return render(request,'App_Quiz/showanswe.html',context)

def AttemView(request,id):
    if Categoty.objects.filter(id=id).exists():
        cat=Categoty.objects.get(id=id)
        userattemp=QuizAtemp.objects.filter(user=request.user,category_id=cat.id)
        context={
            'userattemp':userattemp,
            'cat':cat
        }
        return render(request,'App_Quiz/showattemp.html',context)
    else:
        return HttpResponse("<h1>Category not Fount/h1>")
