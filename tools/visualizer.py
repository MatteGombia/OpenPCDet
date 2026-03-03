import pickle
import numpy as np
from visual_utils import open3d_vis_utils as V

# 1. Set your paths here
RESULT_PKL = "/media/franco/hdd/matteogombia/OpenPCDet/output/kitti_models/PP_radar/default/eval/epoch_80/val/default/result.pkl"  # <-- Change this to your result.pkl path
VOD_RADAR_DIR = "/media/franco/hdd/dataset/VoD/view_of_delft_PUBLIC/radar_5frames/training/velodyne"

# 2. Load the predictions
with open(RESULT_PKL, 'rb') as f:
    results = pickle.load(f)

# 3. Pick a frame to visualize (0 is the first frame in the pkl)
frame_index = 1
frame_data = results[frame_index]

frame_id = frame_data['frame_id']
pred_boxes = frame_data['boxes_lidar']
pred_scores = frame_data['score']

# 4. Filter out low-confidence predictions (e.g., keep only > 50% confidence)
score_threshold = 0.5
mask = pred_scores > score_threshold
confident_boxes = pred_boxes[mask]

# 5. Load the raw radar point cloud for this exact frame
# Note: VoD radar has 7 features, so we reshape(-1, 7)
pc_path = f"{VOD_RADAR_DIR}/{frame_id}.bin"
points = np.fromfile(pc_path, dtype=np.float32).reshape(-1, 7)

print(f"Visualizing Frame ID: {frame_id}")
print(f"Total points: {points.shape[0]}")
print(f"Showing {len(confident_boxes)} confident bounding boxes.")

# 6. Launch the Open3D Visualizer!
# We only pass points[:, :3] because Open3D only uses X, Y, Z for drawing
V.draw_scenes(
    points=points[:, :3], 
    ref_boxes=confident_boxes,
    ref_scores=pred_scores[mask]
)