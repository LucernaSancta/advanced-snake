# 🍓Custom Food Textures

## ⚙️How It Works
Food textures are loaded dynamically from:
```
📂textures/food/
```
When an 🍎`Apple` is created, it:

- 🖼️Loads the image by filename
- 📏Automatically scales it to the right size
- 🎯Draws it directly at its in-game position

👉There’s no tile grid, no layout rules, just one image per food.

## 🧑‍🎨Image Guidelines
- ✅Any shape or size works — it's scaled for you
- 🧼Transparent PNGs are supported
- 🟰Keep the aspect ratio `1:1` (e.g. 64×64)
- 🎯Center your design — it’s placed as-is on the game grid

## 🎨Example Custom Textures
- ✏️Create a new PNG (suggested: 64×64)
- 🍍Draw your food item
- 💾Save to `textures/food/` with whatever name you like

## 📥Load a Custom Texture
To load a custom food texture you can just change the `FOOD_DEFAULT_TEXTURES` variable in the `config.toml` file to the name of the texture's file.
(e.g.📌FOOD_DEFAULT_TEXTURES = "custom.png")