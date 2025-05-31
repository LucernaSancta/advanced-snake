# 🌐 Online Multiplayer

Play with friends on the same local network—no need to share a single screen!

## 🚨 Warnings

⚠️ **This multiplayer mode is highly insecure**.

The current implementation can be exploited to run **malicious code** on your machine. Only use it on **trusted local networks**.

❌ **Never use this on public or untrusted networks**.

There is **no encryption or authentication** in place. You’ve been warned.

## ⚙️ How It Works

The game uses a client-server architecture:

- 🧠 The **server** runs the main game logic.
- 🖥️ **Clients** connect to the server and receive real-time updates (like snake positions and food locations).
- 🎮 Each client sends **player input** (e.g., movement keys) to the server.
- 🐍 Any connected client can control **any snake**.

## 🧠 Creating a Server

To start a server:

1. Navigate to `Main Menu` > `ONLINE` > `START SERVER`.
2. This launches a server in background.
3. A game window will open—you're both hosting and playing at the same time.

## 🔗 Connecting as a Client

To join a server:

1. Go to `Main Menu` > `ONLINE` > `JOIN SERVER`.
2. Enter the server’s **local IP address**.
3. A new game window will open—start playing!

## 🧩 Comaptibility client - server

No need to manually match client and server settings - 🧠 the server automatically **shares its configuration** with all connecting clients at startup.

However, **clients must have all the required textures and food assets referenced by the server’s configuration**. Make sure your game data matches to avoid missing visuals during gameplay.