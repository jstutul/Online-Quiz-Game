from django.urls import path
app_name = 'App_Quiz'
from App_Quiz import views
urlpatterns = [
    path('',views.Home,name="home"),
    path('category',views.CategoryView,name="category"),
    path('tournaments',views.TournamentView,name="tournaments"),
    path('tournaments/start-tournament/<int:id>',views.Tournamentstart,name='tournament_start'),
    path('tournaments/result/completed',views.Completed,name="completed"),
    path('tournaments/result/wrong',views.Wronganswer,name="incompleted"),
    path('tournaments/getpoints/<int:id>',views.GetPoints,name="winning_points"),
    path('tournament/result/<int:id>',views.TournamentResult,name="tournament_result"),
    path('category/view/start-quiz/<int:id>',views.StartQuiz,name="startquiz"),
    path('check-result/<int:id>',views.CheckResult,name="checkresult"),
    path('result-page/<int:id>',views.Result,name="result"),
    path('view-answer/<int:id>',views.ViewAnswer,name="view_answer"),
    path('view-attemp-list/<int:id>',views.AttemView,name="attemp_view"),
]
