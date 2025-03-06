from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    """Player profile containing balance and stats"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=100.00)
    highest_label = models.CharField(max_length=20, default="Poor")
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    total_bet = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_winnings = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class GameSession(models.Model):
    """Active game session data"""
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    current_bet = models.DecimalField(max_digits=15, decimal_places=2)
    original_bet = models.DecimalField(max_digits=15, decimal_places=2)
    current_stage = models.IntegerField(default=1)
    current_label = models.CharField(max_length=20, default="Poor")
    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Game Session {self.id} - {self.player.user.username}"
    
    class Meta:
        ordering = ['-started_at']

class GameMove(models.Model):
    """Individual move history in a game session"""
    MOVE_CHOICES = [
        ('SAFE', 'Safe'),
        ('MID_SAFE', 'Mid-Safe'),
        ('NOT_SAFE', 'Not Safe'),
    ]
    
    OUTCOME_CHOICES = [
        ('WIN', 'Win'),
        ('LOSS', 'Loss'),
        ('PARTIAL', 'Partial'),
    ]
    
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='moves')
    stage = models.IntegerField()
    move_type = models.CharField(max_length=10, choices=MOVE_CHOICES)
    outcome = models.CharField(max_length=10, choices=OUTCOME_CHOICES)
    bet_before = models.DecimalField(max_digits=15, decimal_places=2)
    bet_after = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Move at Stage {self.stage} - {self.move_type}"
    
    class Meta:
        ordering = ['timestamp']

class GameStage(models.Model):
    """Configuration for each game stage"""
    stage_number = models.IntegerField(unique=True)
    safe_doors = models.IntegerField(default=1)  # Number of safe doors
    mid_safe_doors = models.IntegerField(default=2)  # Number of mid-safe doors
    not_safe_doors = models.IntegerField(default=1)  # Number of not-safe doors
    label_on_complete = models.CharField(max_length=20, default="Poor")
    
    def __str__(self):
        return f"Stage {self.stage_number}"
    
    class Meta:
        ordering = ['stage_number']