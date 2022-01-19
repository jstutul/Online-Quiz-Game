from django.urls import path
from App_Superadmin import views
app_name = 'App_Superadmin'
urlpatterns = [
    path('',views.Dashboard,name='dashboard'),
    path('delete-user-data/<int:id>',views.Removeuser,name="deleuserdata"),
    path('update-user-attemp/<int:id>',views.UpdateAttempResult,name="updateattempdata"),
    path('delete-user-attemp/<int:id>',views.DeleteAttempResult,name="deleteattempdata"),

    path('add-category',views.AddCategory,name='add-category'),
    path('manage-category',views.ManageCategory,name='manage-category'),
    path('delete-category/<int:id>',views.DeleteCategory,name='delete-category'),
    path('update-category/<int:id>',views.UpdateCategory,name='update-category'),

    path('add-tournaments', views.AddTournament, name='add-tournament'),
    path('manage-tournaments', views.ManageTournament, name='manage-tournament'),
    path('delete-tournaments/<int:id>', views.DeleteTournament, name='delete-tournament'),
    path('update-tournaments/<int:id>', views.UpdateTournament, name='update-tournament'),


    path('add-category-question/',views.AddCategoryQuestion,name='add-cat-question'),
    path('manage-category-question/', views.ManageCategoryQuestion, name='manage-category-question'),
    path('update-category-question/<int:id>', views.UpdateCategoryQuestion, name='update-category-question'),
    path('delete-category-question/<int:id>', views.DeleteCategoryQuestion, name='delete-category-question'),



    path('add-tournament-question/',views.AddTournamentQuestion,name='add-tournament-question'),
    path('manage-tournament-question/', views.ManageTournamentQuestion, name='manage-tournament-question'),
    path('update-tournament-question/<int:id>', views.UpdateTournamentQuestion, name='update-tournament-question'),
    path('delete-tournament-question/<int:id>', views.DeleteTournamentQuestion, name='delete-tournament-question'),


]

