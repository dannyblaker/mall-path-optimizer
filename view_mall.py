# view_mall_optimized.py
import json
import math
import os
import random
from dataclasses import dataclass
from typing import List, Tuple

import plotly.graph_objects as go


# ---------------------------
# Data structures & helpers
# ---------------------------
@dataclass
class Shop:
    name: str
    floor: int
    x: float
    y: float


def load_or_generate_mall(json_path: str = "mall_coordinates.json",
                          num_floors: int = 3,
                          num_shops_per_floor: int = 5,
                          seed: int = 42) -> List[Shop]:
    """
    Loads mall coordinates from JSON if present; otherwise generates and saves a new mall.
    """
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        return [Shop(d["name"], int(d["floor"]), float(d["x"]), float(d["y"])) for d in data]

    # Fallback: generate mall like your generator
    random.seed(seed)
    shops: List[Shop] = []
    for floor in range(1, num_floors + 1):
        for shop_id in range(1, num_shops_per_floor + 1):
            shop_name = f"Shop_{floor}_{shop_id}"
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            shops.append(Shop(shop_name, floor, x, y))
    # Save for consistency with your pipeline
    with open(json_path, "w") as f:
        json.dump([shop.__dict__ for shop in shops], f, indent=4)
    return shops


# ---------------------------
# Distance model & TSP tools
# ---------------------------
def step_cost(a: Shop, b: Shop, floor_penalty: float = 50.0) -> float:
    """
    Walking 'distance' between shops.
    - Horizontal movement uses Euclidean distance on (x, y).
    - Vertical movement adds a linear penalty per floor change to discourage ping-ponging between floors.
      Tune floor_penalty to match how annoying floor changes are (elevators/escalators distance/time).
    """
    dx = a.x - b.x
    dy = a.y - b.y
    horizontal = math.hypot(dx, dy)
    vertical_penalty = floor_penalty * abs(a.floor - b.floor)
    return horizontal + vertical_penalty


def path_length(order: List[int], shops: List[Shop], floor_penalty: float) -> float:
    return sum(step_cost(shops[order[i]], shops[order[i + 1]], floor_penalty)
               for i in range(len(order) - 1))


def nearest_neighbor(shops: List[Shop], floor_penalty: float) -> List[int]:
    """
    Build an initial tour using Nearest Neighbor from a decent start:
    the shop with the smallest (floor, x, y) lexicographic tuple.
    """
    n = len(shops)
    if n == 0:
        return []
    start = min(range(n), key=lambda i: (shops[i].floor, shops[i].x, shops[i].y))
    unvisited = set(range(n))
    unvisited.remove(start)
    order = [start]

    current = start
    while unvisited:
        next_idx = min(unvisited, key=lambda j: step_cost(shops[current], shops[j], floor_penalty))
        unvisited.remove(next_idx)
        order.append(next_idx)
        current = next_idx
    return order


def two_opt(order: List[int], shops: List[Shop], floor_penalty: float,
            max_passes: int = 20) -> List[int]:
    """
    Classic 2-opt local improvement. Tries to remove edge crossings and reduce length.
    """
    improved = True
    passes = 0
    n = len(order)
    if n < 4:
        return order

    def seg_cost(i1, i2, j1, j2):
        return (step_cost(shops[order[i1]], shops[order[i2]], floor_penalty) +
                step_cost(shops[order[j1]], shops[order[j2]], floor_penalty))

    while improved and passes < max_passes:
        improved = False
        passes += 1
        for i in range(n - 3):
            for j in range(i + 2, n - 1):
                # Current segments: (i,i+1) and (j,j+1). Try reversing order[i+1:j+1]
                before = seg_cost(i, i + 1, j, j + 1)
                after = seg_cost(i, j, i + 1, j + 1)
                if after + 1e-9 < before:
                    order[i + 1:j + 1] = reversed(order[i + 1:j + 1])
                    improved = True
        # If no improvement in this pass, exit
    return order


def compute_efficient_path(shops: List[Shop], floor_penalty: float = 50.0) -> Tuple[List[int], float]:
    """
    Returns an order (index list) to visit all shops and the total path length (with penalties).
    """
    init = nearest_neighbor(shops, floor_penalty)
    improved = two_opt(init, shops, floor_penalty)
    total = path_length(improved, shops, floor_penalty)
    return improved, total


# ---------------------------
# Plotly visualization
# ---------------------------
def view_mall_efficient(shops: List[Shop], floor_penalty: float = 50.0) -> None:
    """
    Plots the mall shops and an efficient walking path (TSP heuristic) in 3D.
    - Points: shops
    - Line: the computed visit order
    """
    order, total = compute_efficient_path(shops, floor_penalty)

    # Scatter of shops
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=[s.x for s in shops],
        y=[s.y for s in shops],
        z=[s.floor for s in shops],
        mode="markers+text",
        text=[s.name for s in shops],
        textposition="top center",
        marker=dict(size=6, opacity=0.8),
        name="Shops",
        hovertext=[f"{s.name}<br>Floor {s.floor}<br>({s.x:.1f}, {s.y:.1f})" for s in shops],
        hoverinfo="text",
    ))

    # Path line (follow order)
    path_x = [shops[i].x for i in order]
    path_y = [shops[i].y for i in order]
    path_z = [shops[i].floor for i in order]

    fig.add_trace(go.Scatter3d(
        x=path_x,
        y=path_y,
        z=path_z,
        mode="lines+markers",
        line=dict(width=6),  # default color (no specific color per guidelines)
        marker=dict(size=3),
        name="Walking path",
        hoverinfo="skip",
    ))

    # Start and end markers
    start, end = order[0], order[-1]
    fig.add_trace(go.Scatter3d(
        x=[shops[start].x], y=[shops[start].y], z=[shops[start].floor],
        mode="markers+text",
        text=["START"],
        textposition="bottom center",
        marker=dict(size=8, symbol="diamond"),
        name="Start",
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter3d(
        x=[shops[end].x], y=[shops[end].y], z=[shops[end].floor],
        mode="markers+text",
        text=["END"],
        textposition="bottom center",
        marker=dict(size=8, symbol="x"),
        name="End",
        hoverinfo="skip",
    ))

    fig.update_layout(
        title=f"Efficient Walking Path Through All Shops — Total 'Distance' (with floor penalty) = {total:.1f}",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Floor",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=60, b=0),
    )

    fig.show()


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    # Load existing JSON or generate a mall identical in spirit to generate_mall.py
    shops = load_or_generate_mall("mall_coordinates.json", num_floors=3, num_shops_per_floor=5)

    # Tune this to change how costly floor changes are relative to horizontal walking
    FLOOR_CHANGE_PENALTY = 50.0
    view_mall_efficient(shops, floor_penalty=FLOOR_CHANGE_PENALTY)
