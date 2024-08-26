from utils import read_video, save_video
from trackers import Tracker
import cv2
import numpy as np
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedandDistanceEstimator


def main():
    print("Hello World!")
    
    # Read Video
    video_frames = read_video('input_videos/test_video.mp4')
    
    # Initialize Tracker
    tracker = Tracker('models/best.pt')
    
    tracks = tracker.get_object_tracks(
                                       video_frames, 
                                       read_from_stub=True, 
                                       stub_path='stubs/track_stubs.pkl'
                                       )
    
    # Get Object positions
    tracker.add_position_to_track(tracks)
    # Camera Movement Estimation
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                              read_from_stub=True,
                                                                              stub_path='stubs/camera_movement_stubs.pkl'
                                                                              ) 
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)
    
    # View Transformer
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)
    
    # Interpolate ball positions
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    
    # Speed and Distance Estimator
    speed_and_distance_estimator = SpeedandDistanceEstimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)
    
    # Assign Teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0],
                                    tracks["players"][0])
    
    for frame_num, player_tracks in enumerate(tracks["players"]):
        for player_id, track in player_tracks.items():
            team = team_assigner.get_player_team(video_frames[frame_num], 
                                                 track["bbox"], 
                                                 player_id
                                                 )
            tracks["players"][frame_num][player_id]["team"] = team
            tracks["players"][frame_num][player_id]["team_color"] = team_assigner.team_colors[team]
            
    
    # Assign Ball to Players
    ball_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks["players"]):
        ball_bbox = tracks["ball"][frame_num][1]["bbox"]
        player_with_ball = ball_assigner.assign_ball_to_players(player_track, ball_bbox)
        
        if player_with_ball is not None:
            tracks["players"][frame_num][player_with_ball]["has ball"] = True
            team_ball_control.append(tracks["players"][frame_num][player_with_ball]["team"])
        else:
            team_ball_control.append(team_ball_control[-1])
            
    team_ball_control = np.array(team_ball_control)
            
    
    
    # Draw Output
    # Draw object tracks on video frames
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
    
    # Draw camera movement
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
    
    # Draw speed and distance
    speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)
    
    
    # Save Video
    save_video(output_video_frames, 'output_videos/test_video.avi')
    
if __name__ == "__main__":
    main()