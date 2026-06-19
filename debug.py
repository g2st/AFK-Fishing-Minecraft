import main
import time
import numpy as np
import pyaudiowpatch


stream = main.p.open(
    format=pyaudiowpatch.paInt16,
    channels=main.channels,
    rate=main.sample_rate,
    input=True,
    frames_per_buffer=1024,
    input_device_index=main.loopback_device["index"],
    stream_callback=main.callback,
)

def get_peak():
    while True:
        window=main.buffer[-int(main.sample_rate * 0.2):]
        peak=np.max(np.abs(window))
        print(f"Volume Peaks at:{peak:.4f}", end="\r")
        time.sleep(0.1)

stream.start_stream()
get_peak()