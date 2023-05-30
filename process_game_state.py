from matplotlib.path import Path
import json
import pandas as pd


class ProcessGameState:
    def __init__(self, file_path):
        self.data = pd.read_parquet(file_path)

    def extract_weapon_classes(self):
        self.data['inventory'] = self.data['inventory'].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x)
        return self.data


def boundary_analysis(game_state, tick_rate):
    team2_actions = game_state.data.loc[(game_state.data['team'] == 'Team2') &
                                        (game_state.data['side'] == 'T')]
    team2_actions['entry_instance'] = (
        team2_actions['in_boundary'].shift() != team2_actions['in_boundary'])

    unique_entries = team2_actions.loc[(team2_actions['in_boundary'] == True) &
                                       (team2_actions['entry_instance'] == True)]

    for i, entry in enumerate(unique_entries.groupby(unique_entries['entry_instance'].cumsum())):
        print(
            f"Instance {i+1} - Team2 spent {len(entry[1])/tick_rate} seconds within the boundary.")
