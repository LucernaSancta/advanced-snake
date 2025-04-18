# 🎑 Background Textures Documentation

## ⚙️ How It Works
Background textures are used to create the ground or sky in-game environments. Each texture is a grid of tiles that can be repeated to cover large areas seamlessly or stretched to the whole screen.

## 🖼️ Image Rules
- Must be a PNG file.

## 📁 Where to Put Them
All background textures are stored in:
```bash
textures/background/
```

## 🎨 Tips for Custom Textures
1. Start with a template texture (e.g., `default.png`).
2. Design your desired pattern or style.
3. Ensure that the edges of the tiles align perfectly to create seamless transitions.

## 🧩 Example Workflow
1. Open an image editor and create a **32x32** PNG file. (32x32 is a suggestion, you can create whatever size you want)
2. Design the texture.
3. Save the file to `textures/background/` with your desired filename ('example.png').
4. Configure your game engine or application to use the new background texture via its configuration settings.

## 🎨 Loading Custom Textures
To use a custom background texture, modify the `config.toml` file by modifying the `[background]` section:
```toml
[background]
textures = "custom_background.png"
```

This will apply your custom background texture to the game environment.

## 🏁 Tiling
Tiling cna be applied to background textures to repeat them in a grid-like patters, to activate tiling simpli set the `background.tiling.active` flag to `true` and set a zixe relative to the game grid size, for example:
```toml
[background]
textures = "grass.png"
    [background.tiling]
    active = true
    size = [1, 1]
```
In this example the grass texture is tiled across the screen with the same size of the game grid tiles.