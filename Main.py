import pyaudio
import time
import numpy as np
from butter_transform import butter_bandpass_filter, transform
from matplotlib import pyplot as plt
import scipy.signal as signal

CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
fulldata = np.array([])
dry_data = np.array([])
counter = 0
DROP_FIRST = 3
buffer = []


def main():
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(10)
        stream.stop_stream()
    stream.close()

    p.terminate()


def callback2(in_data, frame_count, time_info, flag):
    global b, a, fulldata  # global variables for filter coefficients and array
    audio_data = np.fromstring(in_data, dtype=np.float32)
    # do whatever with data, in my case I want to hear my data filtered in realtime
    # audio_data = signal.filtfilt(b, a, audio_data, padlen=200).astype(np.float32).tostring()
    fulldata = np.append(fulldata, audio_data)
    # saves filtered data in an array
    return audio_data, pyaudio.paContinue


def callback(in_data, frame_count, time_info, flag):
    global b, a, fulldata, dry_data, counter
    audio_data = np.fromstring(in_data, dtype=np.float32)

    if counter > 100:
        f, Pxx_spec = signal.welch(audio_data,RATE, 'flattop', 1024, scaling='spectrum')
        plt.figure()
        plt.semilogy(f, np.sqrt(Pxx_spec))
        plt.xlabel('frequency [Hz]')
        plt.ylabel('Linear spectrum [V RMS]')
        plt.show()

        plt.plot(np.linspace(0,1,1024),audio_data)
        plt.show()



    counter += 1

    return audio_data, pyaudio.paContinue


main()
