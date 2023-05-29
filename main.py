# main.py
from process_game_state import ProcessGameState

# Initialize the class with your parquet file
game_state = ProcessGameState("./data/game_state_frame_data.parquet")

# Check if each row falls within the boundary
boundary_coordinates = {'x': [-2806, -1565], 'y': [250, 1233], 'z': [285, 421]}
boundary_data = game_state.in_boundary(boundary_coordinates)

# Extract weapon classes from inventory
weapon_data = game_state.extract_weapon_classes()

# Print to check
print(boundary_data.head())
print(weapon_data.head())
