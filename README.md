# TV Control (Chromecast)

A small Python tool for discovering and controlling Chromecast devices on
the local network using the [`pychromecast`](https://github.com/home-assistant-libs/pychromecast) library.

## What it does

- Discovers Chromecast devices on the local network via mDNS/zeroconf
- Connects to a target device and reports its status (name, volume, current app)
- Controls volume (set, up, down, mute)
- Casts media (video/image) from a URL and controls playback (play, pause, stop)

## How it works

1. **Discovery** — `pychromecast.get_chromecasts()` listens for Chromecast
   devices broadcasting themselves via mDNS/zeroconf on the local network
   and returns a list of the devices found.
2. **Connection** — The script connects to the first device found and calls
   `cast.wait()`, which blocks until the connection is fully established
   and status info (friendly name, volume, active app) is available.
3. **Volume control** — Actions like `set_volume()`, `volume_up()`,
   `volume_down()`, and `set_volume_muted()` work regardless of what's
   currently playing on the device.
4. **Media casting & control** — Pause/play/stop only work reliably on a
   session you own. The script quits whatever app is currently running on
   the Cast device, then casts its own media via
   `media_controller.play_media(url, content_type)`. Because this session
   was initiated by the script, it now has full control over it.
   `block_until_active()` blocks until playback has actually started
   before further commands are issued.
5. **Cleanup** — `pychromecast.discovery.stop_discovery()` properly closes
   the mDNS listener when the script is done.

## Requirements

```bash
pip install pychromecast
```

Your machine and the Chromecast/TV must be on the same local network.

## Usage

Edit `tv-control.py` to point at your own media (a file hosted on your
machine or any reachable URL), then run:

```bash
python tv-control.py
```

Example — hosting a local file to cast:

```bash
# In the folder with your media file:
python -m http.server 8000
```

Then reference it in the script as `http://<your-laptop-ip>:8000/<filename>`.

## Example: basic status check

```python
import pychromecast

chromecasts, browser = pychromecast.get_chromecasts()
cast = chromecasts[0]
cast.wait()

print("Name:  ", cast.cast_info.friendly_name)
print("Volume:", cast.status.volume_level)
print("App:   ", cast.status.display_name)

pychromecast.discovery.stop_discovery(browser)
```

## Relevance to security work

Chromecasts, smart TVs, and similar cast-enabled devices are common on
internal networks and are often overlooked during enumeration. This tool
is a starting point for discovering and interacting with such devices —
useful groundwork for internal network assessments where IoT/smart-home
devices are in scope.

## Notes

- Only tested against a single Chromecast on the local network; behavior
  with multiple devices found by `get_chromecasts()` isn't handled yet
  (the script always grabs `chromecasts[0]`).
- All testing was done on my own devices in my own lab/home network.
