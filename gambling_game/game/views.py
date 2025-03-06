from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from .models import PlayerProfile, GameSession, GameStage
from .game_logic import GameEngine
from .forms import BetForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup(request):
    """Sign up a new user"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful signup
        else:
            messages.error(request, 'There was an error with your signup.')
    else:
        form = UserCreationForm()

    return render(request, 'game/signup.html', {'form': form})


def index(request):
    """Home page view"""
    return render(request, 'game/index.html')



@login_required
def profile(request):
    """Player profile view"""
    # Get or create player profile
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)
    
    # Get active game sessions
    active_sessions = GameSession.objects.filter(player=profile, is_active=True)
    
    # Get game history (completed sessions)
    completed_sessions = GameSession.objects.filter(player=profile, is_active=False)[:10]
    
    context = {
        'profile': profile,
        'active_sessions': active_sessions,
        'completed_sessions': completed_sessions,
    }
    
    return render(request, 'game/profile.html', context)

@login_required
def start_game(request):
    """Start a new game"""
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet_amount = form.cleaned_data['bet_amount']
            session, message = GameEngine.initialize_game(profile, Decimal(bet_amount))
            
            if session:
                messages.success(request, message)
                return redirect('play_game', session_id=session.id)
            else:
                messages.error(request, message)
                return redirect('start_game')
    else:
        form = BetForm()
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'game/start_game.html', context)

@login_required
def play_game(request, session_id):
    """Main gameplay view"""
    # Get the game session
    session = get_object_or_404(GameSession, id=session_id, player__user=request.user)
    
    if not session.is_active:
        messages.warning(request, "This game session has ended.")
        return redirect('profile')
    
    # Get door options for the current stage
    doors, stage_config = GameEngine.get_door_options(session)
    
    context = {
        'session': session,
        'doors': doors,
        'door_count': len(doors),
        'stage_config': stage_config,
    }
    
    return render(request, 'game/play_game.html', context)

@login_required
def make_move(request, session_id):
    """Process a player's move"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    # Get the game session
    session = get_object_or_404(GameSession, id=session_id, player__user=request.user)
    
    if not session.is_active:
        return JsonResponse({'success': False, 'message': 'This game session has ended'})
    
    # Get the selected door
    door_index = int(request.POST.get('door_index', -1))
    
    # Process the move
    success, message = GameEngine.make_move(session, door_index)
    
    # Refresh the session data
    session.refresh_from_db()
    
    return JsonResponse({
        'success': success,
        'message': message,
        'current_bet': float(session.current_bet),
        'current_stage': session.current_stage,
        'current_label': session.current_label,
        'is_active': session.is_active,
    })

@login_required
def cash_out(request, session_id):
    """Cash out from a game"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    # Get the game session
    session = get_object_or_404(GameSession, id=session_id, player__user=request.user)
    
    if not session.is_active:
        return JsonResponse({'success': False, 'message': 'This game session has ended'})
    
    # Process the cash out
    success, message = GameEngine.cash_out(session)
    
    # Refresh the session data
    session.refresh_from_db()
    
    return JsonResponse({
        'success': success,
        'message': message,
        'current_bet': float(session.current_bet),
        'is_active': session.is_active,
    })

@login_required
def game_history(request):
    """View game history"""
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)
    
    # Get completed game sessions
    completed_sessions = GameSession.objects.filter(player=profile, is_active=False).prefetch_related('moves')
    
    context = {
        'profile': profile,
        'completed_sessions': completed_sessions,
    }
    
    return render(request, 'game/game_history.html', context)

@login_required
def leaderboard(request):
    """View leaderboard"""
    # Get top players by balance
    top_by_balance = PlayerProfile.objects.order_by('-balance')[:10]
    
    # Get top players by win rate
    top_by_win_rate = PlayerProfile.objects.filter(games_played__gt=0).order_by('-games_won', '-games_played')[:10]
    
    # Get top players by highest label
    label_order = {'King': 1, 'Ultra Rich': 2, 'Middle Class': 3, 'Poor': 4}
    top_by_label = sorted(
        PlayerProfile.objects.all(),
        key=lambda x: label_order.get(x.highest_label, 5)
    )[:10]
    
    context = {
        'top_by_balance': top_by_balance,
        'top_by_win_rate': top_by_win_rate,
        'top_by_label': top_by_label,
    }
    
    return render(request, 'game/leaderboard.html', context)

def about(request):
    """About page view"""
    return render(request, 'game/about.html')