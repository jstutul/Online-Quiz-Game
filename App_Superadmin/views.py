from django.contrib import messages
from django.core.mail import message
from django.shortcuts import render,HttpResponse,redirect
from App_Account.models import *
from App_Quiz.models import *
# Create your views here.
from django.contrib.sessions.models import Session
from django.utils import timezone
def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)

def Dashboard(request):
    if request.user.is_superuser:
        alluser=User.objects.all().count()
        allcat=Categoty.objects.all().count()
        allquestion=Question.objects.all().count()
        alltournament=Tournament.objects.all().count()
        users=User.objects.all().exclude(is_superuser=True)
        attem=QuizAtemp.objects.all()
        queryset = get_current_users()
        print(queryset)
        context={
            'totaluser':alluser,
            'totalcat':allcat,
            'allrournament':alltournament,
            'allquestion':allquestion,
            'users':users,
            'attemp':attem,
        }
        return render(request,'App_Superadmin/index.html',context)
    else:
        return HttpResponse("<h1>You are not superuser </h1>")

def Removeuser(request,id):
    if User.objects.filter(id=id).exists():
        user=User.objects.get(id=id)
        user.delete()
        return redirect('App_Superadmin:dashboard')
    else:
        return HttpResponse("<h1>User not found with this ID</h1>")
def AddCategory(request):
    if request.method=="POST":
        category_name=request.POST.get('cat_name')
        category_time=request.POST.get('cat_time')
        category_details=request.POST.get('cat_description')
        if len(request.FILES) !=0:
            category_photo = request.FILES['cat_photo']
            cat=Categoty.objects.create(
                name=category_name,total_time=category_time,description=category_details,photo=category_photo
            )
            cat.save()
            messages.error(request, "Category added succesfully", extra_tags="cat_add")
            return redirect(request.POST['next'])
        else:
            cat = Categoty.objects.create(
                name=category_name, total_time=category_time, description=category_details
            )
            cat.save()
            messages.error(request, "Category added succesfully", extra_tags="cat_add")
            return redirect(request.POST['next'])
    return render(request,'App_Superadmin/addcategory.html')

def ManageCategory(request):
    allcat=Categoty.objects.all().order_by("-id")
    context={
        'allcat':allcat,
    }
    return render(request,'App_Superadmin/managecategory.html',context)

def DeleteCategory(request,id):
    if request.user.is_authenticated:
        cat=Categoty.objects.get(id=id)
        cat.delete()
        return redirect('App_Superadmin:manage-category')

def UpdateCategory(request,id):
    cat=Categoty.objects.get(id=id)
    if request.method == "POST":
        category_name = request.POST.get('cat_name')
        category_time = request.POST.get('cat_time')
        category_details = request.POST.get('cat_description')
        category_photo=cat.photo
        if len(request.FILES) != 0:
            category_photo = request.FILES['cat_photo']

        cat.name=category_name
        cat.total_time=category_time
        cat.description=category_details
        cat.photo=category_photo
        cat.save()
        messages.success(request, "Category updated successfully",extra_tags="cat_update")
        return redirect(request.POST['next'])

    context={
        'cat':cat,
    }
    return render(request,'App_Superadmin/updatecategory.html',context)


def AddTournament(request):
    if request.method == "POST":
        tournament_name = request.POST.get('tournament_name')
        tournament_entrypoint = request.POST.get('tournament_entry_point')
        tournament_details = request.POST.get('tournament_description')
        tournament_winningpoint = request.POST.get('winning_point')
        tournament_time = request.POST.get('tournament_time')
        tournament_enddate = request.POST.get('tournament_date')

        if len(request.FILES) != 0:
            category_photo = request.FILES['tournament_photo']
            tour = Tournament.objects.create(
                name=tournament_name,entry_point=tournament_entrypoint,description=tournament_details,winning_points=tournament_winningpoint,
                end_date=tournament_enddate,time=tournament_time,photo=category_photo
            )
            tour.save()
            messages.error(request, "Tournament added succesfully", extra_tags="tournament")
            return redirect(request.POST['next'])
        else:
            tour = Tournament.objects.create(
                name=tournament_name, entry_point=tournament_entrypoint, description=tournament_details,
                winning_points=tournament_winningpoint,
                end_date=tournament_enddate, time=tournament_time
            )
            tour.save()
            messages.error(request, "Tournament added succesfully", extra_tags="tournament")
            return redirect(request.POST['next'])
    return render(request, 'App_Superadmin/addtournament.html')

def ManageTournament(request):
    allcat = Tournament.objects.all().order_by("-id")
    context = {
        'allcat': allcat,
    }
    return render(request, 'App_Superadmin/managetournament.html', context)

def DeleteTournament(request,id):
    if request.user.is_superuser:
        cat=Tournament.objects.get(id=id)
        cat.delete()
        return redirect('App_Superadmin:manage-tournament')
def UpdateTournament(request,id):
    cat = Tournament.objects.get(id=id)
    if request.method == "POST":
        tournament_name = request.POST.get('tournament_name')
        tournament_entrypoint = request.POST.get('tournament_entry_point')
        tournament_details = request.POST.get('tournament_description')
        tournament_winningpoint = request.POST.get('winning_point')
        tournament_time = request.POST.get('tournament_time')
        tournament_enddate = request.POST.get('tournament_date')
        category_photo=cat.photo
        if len(request.FILES) != 0:
            category_photo = request.FILES['tournament_photo']
        cat.name=tournament_name
        cat.time=tournament_time
        cat.description=tournament_details
        cat.entry_point=tournament_entrypoint
        cat.winning_points=tournament_winningpoint
        cat.end_date=tournament_enddate
        cat.photo = category_photo
        cat.save()
        messages.success(request, "Tournament updated successfully", extra_tags="tournament")
        return redirect(request.POST['next'])

    context = {
        'cat': cat,
    }
    return render(request, 'App_Superadmin/updatetournamanet.html', context)


def AddCategoryQuestion(request):
    allcat=Categoty.objects.all()
    if request.method=="POST":
        title=request.POST.get('cat_question_title')
        level=request.POST.get('level')
        category=request.POST.get('category')
        a=request.POST.get('optiona')
        b=request.POST.get('optionb')
        c=request.POST.get('optionc')
        d=request.POST.get('optiond')
        answer=request.POST.get('answer')
        hints=request.POST.get('hints')

        quet=Question.objects.create(
            title=title,level=level,category=Categoty.objects.get(id=category),option1=a,
            option2=b,option3=c,option4=d,answer=answer,hints=hints
        )
        messages.success(request,"Question Saved Successfully",extra_tags="question")
        quet.save()
    context={
        'attcat':allcat,
    }
    return render(request,'App_Superadmin/addcategoryquestion.html',context)

def ManageCategoryQuestion(request):
    allquestion = Question.objects.all().order_by("-id")
    context = {
        'question': allquestion,
    }
    return render(request, 'App_Superadmin/managequestion.html', context)

def UpdateCategoryQuestion(request,id):
    ques = Question.objects.get(id=id)
    allcat = Categoty.objects.all()
    if request.method == "POST":
        title = request.POST.get('cat_question_title')
        level = request.POST.get('level')
        category = request.POST.get('category')
        a = request.POST.get('optiona')
        b = request.POST.get('optionb')
        c = request.POST.get('optionc')
        d = request.POST.get('optiond')
        answer = request.POST.get('answer')
        hints = request.POST.get('hints')
        ques.title=title
        ques.category=Categoty.objects.get(id=category)
        ques.level=level
        ques.option1=a
        ques.option2=b
        ques.option3=c
        ques.option4=d
        ques.answer=answer
        ques.hints=hints
        ques.save()
        messages.success(request, "Question updated successfully", extra_tags="question")
        return redirect(request.POST['next'])

    context = {
        'question': ques,
        'attcat': allcat,
    }
    return render(request, 'App_Superadmin/updatecategoryquestion.html', context)

def DeleteCategoryQuestion(request,id):
    if request.user.is_superuser:
        cat=Question.objects.get(id=id)
        cat.delete()
        return redirect('App_Superadmin:manage-category-question')

def AddTournamentQuestion(request):
    alltour = Tournament.objects.all()
    if request.method == "POST":
        title = request.POST.get('cat_question_title')
        tournament = request.POST.get('tournament')
        a = request.POST.get('optiona')
        b = request.POST.get('optionb')
        c = request.POST.get('optionc')
        d = request.POST.get('optiond')
        answer = request.POST.get('answer')

        quet = TournamentQuestion.objects.create(
            title=title, tournament=Tournament.objects.get(id=tournament), option1=a,
            option2=b, option3=c, option4=d, answer=answer
        )
        quet.save()
        messages.success(request, "Question Added successfully", extra_tags="tournament")
        return redirect(request.POST['next'])
    context = {
        'alltour': alltour,
    }
    return render(request,'App_Superadmin/addtournamentquestion.html',context)
def ManageTournamentQuestion(request):
    allquestion = TournamentQuestion.objects.all().order_by("-id")
    context = {
        'question': allquestion,
    }
    return render(request, 'App_Superadmin/managetournamentquestion.html', context)

def UpdateTournamentQuestion(request,id):
    ques = TournamentQuestion.objects.get(id=id)
    alltour = Tournament.objects.all()
    if request.method == "POST":
        title = request.POST.get('cat_question_title')
        tournament = request.POST.get('tournament')
        a = request.POST.get('optiona')
        b = request.POST.get('optionb')
        c = request.POST.get('optionc')
        d = request.POST.get('optiond')
        answer = request.POST.get('answer')
        print( Tournament.objects.get(id=tournament))
        ques.title = title
        ques.tournament= Tournament.objects.get(id=tournament)
        ques.option1 = a
        ques.option2 = b
        ques.option3 = c
        ques.option4 = d
        ques.answer = answer
        ques.save()
        messages.success(request, "Question updated successfully", extra_tags="tournament")
        return redirect(request.POST['next'])

    context = {
        'question': ques,
        'attcat': alltour,
    }
    return render(request, 'App_Superadmin/updatetournamentquestion.html', context)

def DeleteTournamentQuestion(request,id):
    if request.user.is_superuser:
        cat=TournamentQuestion.objects.get(id=id)
        cat.delete()
        return redirect('App_Superadmin:manage-tournament-question')

def UpdateAttempResult(request,id):
    quiz=QuizAtemp.objects.get(id=id)
    if request.method=="POST":
        correct=request.POST['correct']
        wrong=request.POST['wrong']
        score=request.POST['score']

        quiz.correct=correct
        quiz.wrong=wrong
        quiz.score=score
        quiz.save()
        messages.success(request,'Result updated succesfully',extra_tags="attempresult")
        return redirect(request.POST['next'])
    context={
        'quiz':quiz,
    }
    return render(request,'App_Superadmin/updateattemp.html',context)
def DeleteAttempResult(request,id):
    atmp=QuizAtemp.objects.get(id=id)
    atmp.delete()
    return redirect('App_Superadmin:dashboard')
