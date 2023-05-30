# Evil Geniuses SWE Intern 2023 Assessment

## Files

**process_game_state.py**: This file processes the game data from the game_state_frame_data.parquet file.

**position_analysis.py**: This file creates a heatmap plot for the highest frequency positions that Team2 players utilize on BombsiteB during CT-side.

**main.py**: This file runs the boundary_analysis from process_game_state.py in order to determine the instances where Team2 enters the light blue boundary area on T-side, as well as the position_analysis from position_analysis.py to plot high frequency positions for Team2 on CT-side. It also outputs Bombsite B analysis that determines the average timer that Team2 on T side enters the B site with at least 2 rifles or SMGs.

Running the command

```bash
python main.py
```

generates the following output:

== BombsiteB Analysis ==

== Round 21 ==

=> Player5 entered BombsiteB at 21 seconds with weapon(s): AK-47

=> Player8 entered BombsiteB at 19 seconds with weapon(s): AK-47

== Round 28 ==

=> Player5 entered BombsiteB at 32 seconds with weapon(s): AK-47

=> Player6 entered BombsiteB at 28 seconds with weapon(s): AK-47

=> Player7 entered BombsiteB at 0 seconds with weapon(s): Galil AR

=> Player8 entered BombsiteB at 29 seconds with weapon(s): AK-47

=> Player9 entered BombsiteB at 0 seconds with weapon(s): AK-47

== Round 30 ==

=> Player5 entered BombsiteB at 39 seconds with weapon(s): Galil AR

=> Player7 entered BombsiteB at 41 seconds with weapon(s): Galil AR

=> Player8 entered BombsiteB at 36 seconds with weapon(s): AK-47

== Boundary Analysis ==

=> In round 16, Player Player5, instance 1, spent 2 seconds within the boundary.

=> In round 16, Player Player9, instance 1, spent 2 seconds within the boundary.

=> Number of rounds where at least one player from Team2 enters the boundary: 1

=> Total number of Team2 players that enter the boundary: 2

== Position Analysis ==

High frequency points at X range: (-1142.08, -1128.46), Y range: (256.0, 272.0)

High frequency points at X range: (-1019.5, -1005.88), Y range: (160.0, 176.0)

High frequency points at X range: (-801.58, -787.96), Y range: (368.0, 384.0)

## Libraries

Pandas, Shapely, Matplotlib, Json, Numpy, Seaborn

### Is entering via the light blue boundary a common strategy used by Team2 on T (terrorist) side?

Entering the light blue boundary is not a common strategy used by Team2 on T side. Based off of the boundary analysis, there was only one round in which Team2 players entered the boundary area (round 16), which was only for a brief moment.

### What is the average timer that Team2 on T (terrorist) side enters “BombsiteB” with at least 2 rifles or SMGs?

The average timer that Team2 on T side enters Bombsite B with at least 2 rifles or SMGs is approximately 35 seconds into the round. This is based on the BombsiteB analysis, which shows three instances where Team2 players entered the bombsite with at least 2 players having a rifle or an SMG (round 21, 28, 30).

### BombsiteB CT (counter-terrorist) side

Based on the data gathered regarding Team2's CT side, their players tend to play around three areas of BombsiteB in more frequency:
X: (-1142.08, -1128.46), Y: (256.0, 272.0)
X: (-1019.5, -1005.88), Y: (160.0, 176.0)
X: (-801.58, -787.96), Y: (368.0, 384.0)

## Future Development

In the future, it may be useful to implement a GUI or dashboard system for coaching staff to run these programs and analyze data for themselves, without as much hassle. Some ideas could include utilizing frameworks such as Dash and Plotly, Flask, or Django to create a web application to provide data analytics, and host it on a site for easy access and data acquisition. It would also be relatively straightforward to set up, given the code for these programs is written in Python.
