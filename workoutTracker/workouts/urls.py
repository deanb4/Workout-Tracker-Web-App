from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', views.home, name='home-page'),
    path('accounts/profile/', views.profile, name='profile'),
    path('logout', auth_views.LogoutView.as_view(template_name='workouts/logout.html'), name ='logout'),
    path('login', auth_views.LoginView.as_view(template_name='workouts/login.html'), name ='login'),
    path('workout-detail<int:pk>/', views.detail, name='detailed-view'),
    path('workouts/<int:pk>/delete/', WorkoutDelete.as_view(), name='delete'),
    path('workouts/<int:pk>/delete-two/', WorkoutDeleteTwo.as_view(), name='delete-two'),
    path('workouts/<int:pk>/update/', UpdatedView.as_view(), name='update'),
    path('workouts/<int:pk>/update-two/', UpdatedViewTwo.as_view(), name='update-two'),
    path('workouts/new/', CreateWorkout.as_view(), name = 'create-workout'),
    path('workouts/logn/', views.workout_log, name='workout-log'),
    path('workouts/<int:pk>/exercise-new/', CreateExerciseList.as_view(), name='create-exercise'),
    path('register', views.register, name = 'register'),
    path('password-reset', auth_views.PasswordResetView.as_view(
        template_name = 'workouts/password_reset.html'), name='password-reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name = 'workouts/password_reset_done.html'),
        name = 'password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name = 'workouts/password_reset_confirm.html'),
        name = 'password_reset_confirm'),
    path('password_reset/confirm/',
        auth_views.PasswordResetCompleteView.as_view(template_name = 'workouts/password_reset_complete.html'),
        name = 'password_reset_complete'),
    path('workouts/new/base/<int:pk>/', CreateBaseExercise.as_view(), name='new-base'),
    path('accounts/update/user', views.updateUser, name='update-user'),
    path('workouts/exercises/listview/<int:pk>/', ExercisesListView.as_view(), name= 'exercises-listview'),
    path('workouts/<int:pk>/update-three/', UpdateExercises.as_view(), name='update-three'),
    path('workouts/<int:pk>/delete-three/', WorkoutDelThree.as_view(), name='delete-three'),
    # path(r'^auth/', include('django.contrib.auth.urls')),
    path('workouts/graph', EditorChartView.as_view(), name='workout-graph'),
]
    # path('workouts/redirect', views.redirect_to_previous, name='redirect-previous')

