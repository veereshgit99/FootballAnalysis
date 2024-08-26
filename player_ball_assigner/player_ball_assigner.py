import sys
sys.path.append('../')
from utils import get_center_of_bbox, measure_distance_between_points

class PlayerBallAssigner:
    def __init__(self):
        self.max_player_ball_distance = 70
        
    def assign_ball_to_players(self, players, ball_bbox):
        ball_position = get_center_of_bbox(ball_bbox)
        
        minimum_distance = 999999
        player_with_ball = None
        
        for player_id, player in players.items():
            player_bbox = player['bbox']
            
            distance_left = measure_distance_between_points((player_bbox[0], player_bbox[-1]), ball_position)
            distance_right = measure_distance_between_points((player_bbox[2], player_bbox[-1]), ball_position)
            distance = min(distance_left, distance_right)
            
            if distance < self.max_player_ball_distance:
                if distance < minimum_distance:
                    minimum_distance = distance
                    player_with_ball = player_id
                    
        return player_with_ball
                