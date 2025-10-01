# Mall Path Optimizer

This project generates a virtual mall with multiple floors and shops, then visualizes it in 3D using [Plotly](https://plotly.com/python/).  

It also calculates an **efficient walking path** to visit all shops, based on a Traveling Salesman Problem (TSP) heuristic.

**You are most welcome to use this code in your commercial projects, all that I ask in return is that you credit my work by providing a link back to this repository. Thank you & Enjoy!**

Note: Wait a few seconds for the demo GIF below to load...  
![Demo](mall_demo.gif)

# Features

- **Mall generation**:
  - Randomly places shops on multiple floors.
  - Stores mall layout in JSON (`mall_coordinates.json`).

- **Visualization**:
  - 3D scatter plot of shops (with floor as the z-axis).
  - Interactive Plotly figure with shop labels.
  - Option to highlight an efficient walking path.

- **Path optimization**:
  - Uses a **Nearest-Neighbor + 2-opt heuristic** to approximate the optimal tour through all shops.
  - Includes a **floor-change penalty** to reduce unnecessary trips between floors.

# File Overview

- **`generate_mall.py`**
  - Generates a random mall with a specified number of floors and shops per floor.
  - Saves the mall layout as `mall_coordinates.json`.

- **`view_mall_optimized.py`**
  - Loads mall coordinates (or generates them if missing).
  - Computes a near-optimal path to visit all shops using a TSP heuristic.
  - Visualizes both the shops and the computed walking path.
  - Displays the total path distance, including floor penalties.

# Setup

Install dependencies in a virtual environment:

```sh
pip install -r requirements.txt
```

# Run

## 1. Generate a mall:

```sh
python generate_mall.py
```

This creates `mall_coordinates.json` with random shop coordinates.


## 2. Visualize an efficient walking path:

```sh
python view_mall.py
```

Opens an interactive 3D scatter plot of the Mall with:

- All shops (blue dots)
- An optimized walking path (blue line)
- Start (Diamond) and end point (X) marked
- Path length displayed in the title
- Click and drag to rotate mall
- Middle scroll to zoom in and out

# Configuration

- Number of floors/shops per floor: Edit `generate_mall.py` or pass custom logic to `Mall`.
- Floor-change penalty: Adjust `FLOOR_CHANGE_PENALTY` in `view_mall_optimized.py`:

```
FLOOR_CHANGE_PENALTY = 50.0  # higher = fewer floor changes
```