# Minecraft Fishing Bot

Automatically detects the fishing bite sound and reels in/recasts for you, so you can AFK fish in Minecraft.

> **Windows only** — relies on WASAPI loopback audio capture.

## Requirements

- Minecraft Java Edition
- Python 3.x

Press **X** to stop the bot.

## Finding your threshold

Everyone's audio setup is different, so the default `volume_threshold` in `main.py` may not work for you. Run the debug script while fishing manually to find your optimal value:

```bash
python debug.py
```

Watch the printed peak values when a bite happens, then set `volume_threshold` in `main.py` to just below that number.

## Minecraft setup

Since 1.16, the fishing mechanic requires the bobber to be surrounded by water **5 blocks in every direction** for the optimal loot table and faster bite times. Make sure your fishing spot is set up correctly or you won't get treasures..

## How it works

1. Captures your default audio output via a WASAPI loopback device
2. Continuously monitors the last 200ms of audio for a volume peak above the threshold
3. When a bite is detected, double right-clicks to reel in and recast

## Notes

- The `keyboard` library may require running as administrator on some systems
- Make sure Minecraft is the focused window when running the bot
- For best results, turn every volume bar to 0% except for 'friendly mobs', so only the bobber splash is audible.
