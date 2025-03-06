from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('start-game/', views.start_game, name='start_game'),
    path('play-game/<int:session_id>/', views.play_game, name='play_game'),
    path('make-move/<int:session_id>/', views.make_move, name='make_move'),
    path('cash-out/<int:session_id>/', views.cash_out, name='cash_out'),
    path('history/', views.game_history, name='game_history'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    
    # Add this line to handle accounts/profile/
    path('accounts/profile/', views.profile, name='accounts_profile'),  # Redirect to 'profile'
]
