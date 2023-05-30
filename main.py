from process_game_state import ProcessGameState
from shapely.geometry import Point, Polygon
from position_analysis import PositionAnalysis

file_path = './data/game_state_frame_data.parquet'
game_state = ProcessGameState(file_path)

# Define boundary box
boundary_vertices = [
    [-1735, 250],
    [-2024, 398],
    [-2806, 742],
    [-2472, 1233],
    [-1565, 580]
]
boundary_polygon = Polygon(boundary_vertices)
z_boundary = [285, 421]

# Check if each row is within boundary
game_state.data['in_boundary'] = game_state.data.apply(
    lambda row: boundary_polygon.contains(Point(row['x'], row['y'])) and z_boundary[0] <= row['z'] <= z_boundary[1], axis=1)

# Filter for Rifle/SMG in player inventory


def get_rifles_smgs(inventory):
    weapons = []
    if inventory is not None:
        for item in inventory:
            if item['weapon_class'] in ['Rifle', 'SMG']:
                weapons.append(item['weapon_name'])
    return weapons


# Filter out the actions of Team2 when they are playing T-side.
team2_actions = game_state.data.loc[(game_state.data['team'] == 'Team2') & (
    game_state.data['side'] == 'T')].copy()

# Create a new column indicating the rifles/SMGs each player has at each tick.
team2_actions.loc[:, 'rifles_smgs'] = team2_actions['inventory'].apply(
    get_rifles_smgs)

# Filter for rows where players are alive, in BombsiteB, and have a Rifle or SMG
team2_actions_alive_bombsiteB_rifleSMG = team2_actions[(team2_actions['is_alive']) & (
    team2_actions['area_name'] == 'BombsiteB') & (team2_actions['rifles_smgs'].str.len() > 0)]

entry_times = {}

print("\n== BombsiteB Analysis ==")
# For each round, get the entry time into BombsiteB for players with rifles/SMGs who are alive.
for (round_num, player), group in team2_actions_alive_bombsiteB_rifleSMG.groupby(['round_num', 'player']):
    if round_num not in entry_times:
        entry_times[round_num] = []
    entry_time = group['seconds'].min()
    # Get weapon(s) at entry time
    weapons = ", ".join(group['rifles_smgs'].iloc[0])
    entry_times[round_num].append((player, entry_time, weapons))

# Print out the players, their entry times, and their weapons per round where at least 2 players with rifles/SMGs enter BombsiteB
for round_num, times in entry_times.items():
    if len(times) > 1:
        print(f"\n== Round {round_num} ==")
        for player, time, weapons in times:
            print(
                f"=> {player} entered BombsiteB at {time} seconds with weapon(s): {weapons}")

# Boundary analysis
print("\n== Boundary Analysis ==")


def boundary_fraction(game_state):
    # Identify entry instances
    team2_actions_in_boundary = team2_actions.loc[team2_actions['in_boundary']].copy(
    )
    team2_actions_in_boundary.loc[:, 'entry_instance'] = (
        team2_actions_in_boundary['in_boundary'].shift() != team2_actions_in_boundary['in_boundary']).cumsum()

    # Group by round, player, and entry instance
    entries_grouped = team2_actions_in_boundary.groupby(
        ['round_num', 'player', 'entry_instance'])
    for (round_num, player, instance), group in entries_grouped:
        entry_time = group['seconds'].min()
        exit_time = group['seconds'].max()
        time_in_boundary = exit_time - entry_time
        print(
            f"=> In round {round_num}, {player}, instance {instance}, spent {time_in_boundary} seconds within the boundary.")

    # Count the number of rounds in which at least one player from Team2 enters the boundary
    rounds_with_boundary_entry = team2_actions_in_boundary['round_num'].nunique(
    )
    print(
        f"=> Number of rounds where at least one player from Team2 enters the boundary: {rounds_with_boundary_entry}")

    # Count the total number of players from Team2 that enter the boundary
    players_entering_boundary = team2_actions_in_boundary['player'].nunique()
    print(
        f"=> Total number of Team2 players that enter the boundary: {players_entering_boundary}")


boundary_fraction(game_state)

print("\n== Position Analysis ==")
position_analysis = PositionAnalysis(game_state)
position_analysis.generate_heatmap()
