# 🧩 Template System Docs

Templates let you quickly switch between different game setups or config states.

## 🧭 What Templates Are

- JSON files that define settings like game rules, UI preferences, or map configurations
- Easily loaded to override your main `config.json`
- Great for testing, customizing player experiences, or having multiple presets

## 🧠 How to Use a Template

You can load a template from the UI using the settings menu:

- Opens a file picker (thanks, EasyGUI!)
- Select any `.json` file from the `templates/` folder
- The chosen file will replace your active `config.json` in the project root

⚠️ It’s a full overwrite — make sure you back up important configs!

## 💾 Want to Save Your Current Config as a Template?

You can do that too!

- Choose "Save Template" in the settings menu
- You’ll be prompted to pick a name and location (default: inside `templates/`)
- A copy of your current `config.json` will be saved there

## 📁 Template File Format

Templates are plain JSON files. Just make sure they follow the structure used by the config.json
See [config.md](./config.md) for more

## 🔄 Switching Between Templates

You can change templates anytime, ust load a different one through the UI in the settings menu to instantly reconfigure the game.