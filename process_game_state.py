# process_game_state.py
import pandas as pd
import json


class ProcessGameState:
    def __init__(self, data_path):
        self.data = pd.read_parquet(data_path)

    def in_boundary(self, coordinates):
        x_min, x_max = coordinates['x']
        y_min, y_max = coordinates['y']
        z_min, z_max = coordinates['z']

        self.data['in_boundary'] = (self.data['x'].between(x_min, x_max) &
                                    self.data['y'].between(y_min, y_max) &
                                    self.data['z'].between(z_min, z_max))
        return self.data

    def extract_weapon_classes(self):
        self.data['inventory'] = self.data['inventory'].apply(json.loads)
        self.data['weapon_classes'] = self.data['inventory'].apply(
            lambda x: x.get('weapon', None))
        return self.data
