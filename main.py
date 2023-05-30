from process_game_state import ProcessGameState
from shapely.geometry import Point, Polygon

file_path = './data/game_state_frame_data.parquet'
game_state = ProcessGameState(file_path)

# Define boundary
boundary_vertices = [
    [-1735, 250],  # 13
    [-2024, 398],  # 14
    [-2806, 742],  # 15
    [-2472, 1233],  # 16
    [-1565, 580]  # 17
]

boundary_polygon = Polygon(boundary_vertices)
z_boundary = [285, 421]

# Check if each row is within boundary
game_state.data['in_boundary'] = game_state.data.apply(
    lambda row: boundary_polygon.contains(Point(row['x'], row['y'])) and z_boundary[0] <= row['z'] <= z_boundary[1], axis=1)


def boundary_fraction(game_state):
    # Filter out the actions of Team2 when they are playing T-side.
    team2_actions = game_state.data.loc[(
        game_state.data['team'] == 'Team2') & (game_state.data['side'] == 'T')].copy()

    # Calculate the fraction of Team2's T-side actions within the boundary.
    fraction_in_boundary = team2_actions['in_boundary'].sum(
    ) / len(team2_actions)

    print("Fraction of Team2's T-side actions within the boundary:",
          fraction_in_boundary)

    # Unique entry instances
    team2_actions.loc[:, 'entry_instance'] = (
        team2_actions['in_boundary'].shift() != team2_actions['in_boundary'])
    unique_entry_instances = team2_actions['entry_instance'].sum()

    # Number of entries in the boundary
    entries_in_boundary = team2_actions['in_boundary'].sum()

    # Time spent in boundary
    time_in_boundary = entries_in_boundary * (1 / 128)

    print(f"Team2 entered the boundary {entries_in_boundary} times.")
    print(
        f"Team2 spent a total of {time_in_boundary} seconds within the boundary.")
    print(
        f"Team2 had {unique_entry_instances} unique instances of entering the boundary.")


boundary_fraction(game_state)

# Extract weapon classes
weapon_classes_data = game_state.extract_weapon_classes()
print(weapon_classes_data)
