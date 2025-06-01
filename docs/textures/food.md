# 🍓 Custom Food Textures

## ⚙️ How It Works

Food textures are loaded dynamically from:
```
textures/food/
```
When an apple is created, it:

- Loads the image by filename
- Automatically scales it to the right size
- Draws it directly at its in-game position

👉 There’s no tile grid, no layout rules, just one image per food.

## 🧑‍🎨 Image Guidelines

- Any shape or size works — it's scaled for you
- Transparent PNGs are supported
- Keep the aspect ratio `1:1` (e.g. 64×64)
- Center your design — it’s placed as-is on the game grid

## 🎨 Example Custom Textures

- Create a new PNG (suggested: 64×64)
- Draw your food item
- Save to `textures/food/` with whatever name you like

## 🎞️ Advanced - animations

An animated texture is just a combination of different textures all in a single file, the images must be placed one under the other with the first one beeing the one on the top, if you have ever done animations for Minecraft textures it's the same principle

## 📥 Load texture

To load a food texture plese see the [`foods docs`](../configs/foods.md)