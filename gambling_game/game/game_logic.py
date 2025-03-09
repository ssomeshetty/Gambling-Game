import random
from decimal import Decimal
from .models import GameStage, GameSession, GameMove, PlayerProfile

class GameEngine:
    """Core game logic engine"""
    
    @staticmethod
    def initialize_game(player_profile, bet_amount):
        """Start a new game session"""
        if bet_amount <= Decimal('0'):
            return None, "Bet amount must be greater than 0"
        
        if bet_amount > player_profile.balance:
            return None, "Insufficient balance"
        
        # Deduct the bet amount from player's balance
        player_profile.balance -= bet_amount
        player_profile.total_bet += bet_amount
        player_profile.games_played += 1
        player_profile.save()
        
        # Create a new game session
        session = GameSession.objects.create(
            player=player_profile,
            current_bet=bet_amount,
            original_bet=bet_amount,
            current_stage=1,
            current_label="Poor"
        )
        
        return session, "Game started successfully"
    
    @staticmethod
    def get_door_options(session):
        """Get the door options for the current stage"""
        try:
            stage_config = GameStage.objects.get(stage_number=session.current_stage)
        except GameStage.DoesNotExist:
            # Use default configuration if not found
            stage_config = GameStage(
                stage_number=session.current_stage,
                safe_doors=2,
                mid_safe_doors=1,
                not_safe_doors=1,
                label_on_complete="Poor"
            )
            if session.current_stage >= 3:
                stage_config.label_on_complete = "Middle Class"
            if session.current_stage >= 5:
                stage_config.label_on_complete = "Ultra Rich"
            if session.current_stage >= 7:
                stage_config.label_on_complete = "King"
        
        # Create a list of door types based on the configuration
        doors = (
            ['SAFE'] * stage_config.safe_doors + 
            ['MID_SAFE'] * stage_config.mid_safe_doors + 
            ['NOT_SAFE'] * stage_config.not_safe_doors
        )
        
        # Adjust difficulty based on player's profile and current bet
        GameEngine._adjust_difficulty(session, doors)
        
        # Shuffle the doors
        random.shuffle(doors)
        
        return doors, stage_config
    
    @staticmethod
    def _adjust_difficulty(session, doors):
        """Adjust game difficulty based on player behavior and current stage"""
        player = session.player
        
        # Check if player is on a winning streak (winning more than losing)
        winning_streak = player.games_won > (player.games_played / 2)
        
        # Check if player has a high bet relative to their usual bets
        high_bet = session.original_bet > (player.total_bet / max(player.games_played, 1)) * Decimal('1.5')
        
        # Check if player is close to the end (potentially big win)
        close_to_end = session.current_stage >= 5
        
        # Get player's moves in this session
        moves = GameMove.objects.filter(session=session)
        safe_moves_count = moves.filter(move_type='SAFE').count()
        
        # Adjust difficulty based on factors
        if winning_streak or high_bet or close_to_end:
            # Make the game harder
            for i in range(len(doors)):
                if doors[i] == 'SAFE' and random.random() < 0.3:
                    doors[i] = 'MID_SAFE'
                elif doors[i] == 'MID_SAFE' and random.random() < 0.3:
                    doors[i] = 'NOT_SAFE'
        
        # If player consistently chooses SAFE, reduce SAFE options
        if safe_moves_count >= 2 and len(moves) >= 2:
            for i in range(len(doors)):
                if doors[i] == 'SAFE' and random.random() < 0.4:
                    doors[i] = 'MID_SAFE'
    
    @staticmethod
    def make_move(session, door_index):
        """Process a player's move"""
        doors, stage_config = GameEngine.get_door_options(session)
        
        if door_index < 0 or door_index >= len(doors):
            return False, "Invalid door selection"
        
        door_type = doors[door_index]
        bet_before = session.current_bet
        
        # Process the outcome based on door type
        if door_type == 'SAFE':
            # Double the bet
            session.current_bet *= 2
            outcome = 'WIN'
        elif door_type == 'MID_SAFE':
            # Halve the bet
            session.current_bet /= 2
            outcome = 'PARTIAL'
        else:  # NOT_SAFE
            # Nullify the bet
            session.current_bet = Decimal('0')
            outcome = 'LOSS'
        
        # Create a record of this move
        GameMove.objects.create(
            session=session,
            stage=session.current_stage,
            move_type=door_type,
            outcome=outcome,
            bet_before=bet_before,
            bet_after=session.current_bet
        )
        
        # Check if game should end
        if door_type == 'NOT_SAFE':
            GameEngine._end_game(session, False)
            return True, "Game over! You lost your bet."
        
        # Advance to the next stage
        session.current_stage += 1
        
        # Update the player's label if they completed the stage
        session.current_label = stage_config.label_on_complete
        
        # Save the session
        session.save()
        
        # Check if the player has completed all stages
        if session.current_stage > 7:
            GameEngine._end_game(session, True)
            return True, "Congratulations! You've completed all stages and reached the King status!"
        
        return True, f"Move successful! You're now at Stage {session.current_stage} with {session.current_label} status."
    
    @staticmethod
    def cash_out(session):
        """Player cashes out their current winnings"""
        if not session.is_active:
            return False, "This game session has already ended."
        
        if session.current_bet <= 0:
            GameEngine._end_game(session, False)
            return True, "Game over! You have no winnings to cash out."
        
        # Add the current bet amount to the player's balance
        player = session.player
        player.balance += session.current_bet
        player.total_winnings += session.current_bet
        
        # If player reached a high stage, update their highest label
        label_rank = {'Poor': 1, 'Middle Class': 2, 'Ultra Rich': 3, 'King': 4}
        current_rank = label_rank.get(session.current_label, 0)
        highest_rank = label_rank.get(player.highest_label, 0)
        
        if current_rank > highest_rank:
            player.highest_label = session.current_label
        
        # If they cashed out with a win, count as a game won
        if session.current_bet > session.original_bet:
            player.games_won += 1
        
        player.save()
        
        # End the game
        GameEngine._end_game(session, True)
        
        return True, f"Cashed out successfully! You've added {session.current_bet} to your balance."
    
    @staticmethod
    def _end_game(session, success):
        """End the game session"""
        session.is_active = False
        session.save()