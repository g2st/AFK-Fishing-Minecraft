import pyautogui
import numpy as np
import time
import pyaudiowpatch
import keyboard as kb
import sys
import threading

### Config ###
buffer_time=1
volume_threshold=0.0470

p=pyaudiowpatch.PyAudio()

stop_event=threading.Event()
buffer_lock=threading.Lock()

def find_loopback_device():
    wasapi_info=p.get_host_api_info_by_type(pyaudiowpatch.paWASAPI)
    device=p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
    if not device["isLoopbackDevice"]:
        for loopback in p.get_loopback_device_info_generator():
            if device["name"] in loopback["name"]:
                return loopback
    return device

loopback_device=find_loopback_device()
sample_rate=int(loopback_device["defaultSampleRate"])
channels=loopback_device["maxInputChannels"]
buffer=np.zeros(sample_rate*buffer_time, dtype=np.float32)

def callback(in_data, frame_count, time_info, status):
    global buffer
    data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
    mono = data.reshape(-1, channels)[:, 0]
    with buffer_lock:
        buffer = np.roll(buffer, -len(mono))
        buffer[-len(mono):] = mono
    return (in_data, pyaudiowpatch.paContinue)

def reel_cast():
    time.sleep(0.5)
    pyautogui.rightClick()
    time.sleep(0.4)
    pyautogui.rightClick()
    time.sleep(1)

def stop_monitoring():
    stop_event.set()

kb.add_hotkey('x', stop_monitoring)

def monitor_volume(stream):
    while not stop_event.is_set():
        with buffer_lock:
            window=buffer[-int(sample_rate*0.2):]
            peak=np.max(np.abs(window))
        if peak > volume_threshold:
            reel_cast()
            time.sleep(0.05)
    stream.stop_stream()
    stream.close()
    p.terminate()
    sys.exit()

if __name__== "__main__":
    stream = p.open(format=pyaudiowpatch.paInt16,
                 channels=loopback_device["maxInputChannels"],
                 rate=sample_rate,
                 input=True,
                 frames_per_buffer=1024,
                 input_device_index=loopback_device["index"],
                 stream_callback=callback)
    
    stream.start_stream()
    monitor_volume(stream)