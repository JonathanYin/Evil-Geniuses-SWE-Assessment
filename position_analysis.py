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

        # Identify high frequency points (those with frequencies greater than 80% of the maximum)
        high_freq_threshold = 0.8 * hist_data.max()
        high_freq_points_indices = np.where(hist_data >= high_freq_threshold)
        for x_index, y_index in zip(*high_freq_points_indices):
            x_range = (x_edges[x_index], x_edges[x_index + 1])
            y_range = (y_edges[y_index], y_edges[y_index + 1])
            print(
                f"High frequency points at X range: {x_range}, Y range: {y_range}")

        # Create the heatmap using seaborn
        fig, ax = plt.subplots(figsize=(9, 9))  # adjust size
        sns.heatmap(hist_data.T, cmap='hot', square=True,
                    cbar_kws={'label': 'Frequency'}, ax=ax)
        ax.invert_yaxis()

        # Adjusting ticks on the axes
        ax.set_xticks([0, hist_data.shape[0]//3, 2 *
                      hist_data.shape[0]//3, hist_data.shape[0]-1])
        ax.set_yticks([0, hist_data.shape[1]//3, 2 *
                      hist_data.shape[1]//3, hist_data.shape[1]-1])
        ax.set_xticklabels(
            [x_edges[0], x_edges[hist_data.shape[0]//3],
                x_edges[2*hist_data.shape[0]//3], x_edges[-1]],
            rotation=45)  # rotate x-axis labels to avoid overlap
        ax.set_yticklabels(
            [y_edges[0], y_edges[hist_data.shape[1]//3], y_edges[2*hist_data.shape[1]//3], y_edges[-1]])

        # Add labeling
        plt.title("Heatmap of Team2 Positions in BombsiteB (CT Side)", fontsize=15)
        plt.xlabel("X Coordinate", fontsize=13)
        plt.ylabel("Y Coordinate", fontsize=13)

        # Show the plot
        plt.show()
