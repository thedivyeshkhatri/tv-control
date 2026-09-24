import pychromecast
import time

# --- Discover and connect ---
chromecasts, browser = pychromecast.get_chromecasts()
cast = chromecasts[0]          # your TV was the first (and only) one found
cast.wait()

# --- Show current status ---
print("Name:  ", cast.cast_info.friendly_name)
print("Volume:", cast.status.volume_level)
print("App:   ", cast.status.display_name)

# --- Volume actions (these always work) ---
# cast.set_volume(0.3)          # set volume to 30%
# cast.volume_up()
# cast.volume_down()
# cast.set_volume_muted(True)

# --- Cast your OWN media, then control it ---
# This is the reliable way to use pause/play/stop, because YOU own the session.
# cast.quit_app()
# mc = cast.media_controller
# mc.play_media(
#    "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
#    "video/mp4"
#)

# mc.play_media(
#    "http://LAPTOP_IP:8000/images.jpeg",   # <-- your laptop IP + filename
#    "image/jpeg"
#)

mc.block_until_active()        # wait until the TV is actually playing it

time.sleep(5)                  # let it play for 5 seconds
# mc.pause()                     # now pause works — this is your session
print("Media state:", mc.status.player_state)

# time.sleep(3)
# mc.play()                    # resume
# mc.stop()                    # stop

# --- Stop discovery cleanly ---
pychromecast.discovery.stop_discovery(browser)
