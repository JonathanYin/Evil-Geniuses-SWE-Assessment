from matplotlib.path import Path
import json
import pandas as pd


class ProcessGameState:
    def __init__(self, file_path):
        self.data = pd.read_parquet(file_path)

    def is_in_boundary(self, boundary):
        # Construct a polygon from boundary points
        polygon = Path([(boundary['13']), (boundary['15']),
                        (boundary['16']), (boundary['17'])])

        # Get x, y coordinates
        x = self.data['x']
        y = self.data['y']

        # Check if each pair of x, y coordinates is within the boundary
        self.data['in_boundary'] = polygon.contains_points(list(zip(x, y)))
        return self.data

    def extract_weapon_classes(self):
        self.data['inventory'] = self.data['inventory'].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x)
        return self.data


def boundary_analysis(game_state, tick_rate):
    # Filter out the actions of Team2 when they are playing T-side.
    team2_actions = game_state.data.loc[(game_state.data['team'] == 'Team2') &
                                        (game_state.data['side'] == 'T')]

    # Filter out actions within the boundary
    team2_in_boundary = team2_actions.loc[team2_actions['in_boundary'] == True]

    # Calculate the total ticks and total time spent in the boundary
    total_ticks_in_boundary = len(team2_in_boundary)
    total_time_in_boundary = total_ticks_in_boundary / \
        tick_rate  # Convert ticks to seconds

    # Calculate the number of unique boundary entry instances
    # By checking when 'in_boundary' changes from False to True
    team2_actions['entry_instance'] = (
        team2_actions['in_boundary'].shift() != team2_actions['in_boundary'])
    unique_entries = len(team2_actions.loc[(team2_actions['in_boundary'] == True) &
                                           (team2_actions['entry_instance'] == True)])

    print(f"Team2 entered the boundary {total_ticks_in_boundary} times.")
    print(
        f"Team2 spent a total of {total_time_in_boundary} seconds within the boundary.")
    print(
        f"Team2 had {unique_entries} unique instances of entering the boundary.")
