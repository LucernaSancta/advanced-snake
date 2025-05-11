# 🗺️ Map Creator Tool

### Overview

The Map Creator Tool is a standalone graphical utility designed for creating and editing wall maps. It allows you to interactively place and remove walls, view live updates, and export the layout as a CSV file that can be later loaded into the game.

## 🚀 Getting Started

The map creator tool runs with the same libraries used by the main game so if you have already installed them you don't have to do that again

Downaload the required libraries
```bash
pip install -r requirements.txt
```
Execute the 'map_creator' file
```bash
python map_creator.py
```

## 🎮 Controls
| Key/Button | Action |
| --- | --- |
| Left Click | Add a wall |
| Right Click | Remove a wall |


## 🛠️ Configuration
The configurations are extracted directly from the 📄`config.json`, you can check the [`global configs`](./config.md) for more.

## 🧠 Dev Notes
- Snakes are loaded for display but not interactive in the map creator.