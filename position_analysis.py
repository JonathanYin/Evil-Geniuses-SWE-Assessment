import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from process_game_state import ProcessGameState


class PositionAnalysis:
    def __init__(self, game_state: ProcessGameState):
        self.data = game_state.data

    def generate_heatmap(self):
        # Filter out the actions of Team2 when they are playing CT-side and are in BombsiteB.
        team2_actions_CT_BombsiteB = self.data.loc[(self.data['team'] == 'Team2') &
                                                   (self.data['side'] == 'CT') &
                                                   (self.data['area_name'] == 'BombsiteB')].copy()

        # Create a heatmap based on the player positions in BombsiteB
        heatmap_data = team2_actions_CT_BombsiteB[['x', 'y']].values

        # Calculate histogram2d for x and y coordinates
        hist_data, x_edges, y_edges = np.histogram2d(
            *heatmap_data.T, bins=[50, 50])

        # Create the heatmap using seaborn
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(hist_data.T, cmap='hot', square=True,
                    cbar_kws={'label': 'Frequency'}, ax=ax)
        ax.invert_yaxis()

        # Customize plot
        plt.title("Heatmap of Team2 Positions in BombsiteB (CT Side)", fontsize=15)
        plt.xlabel("X Coordinate", fontsize=13)
        plt.ylabel("Y Coordinate", fontsize=13)

        # Show the plot
        plt.show()
