from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt

c0 = 16.35


def transform(signal: list, octaves: int, factors: list, fs: float, ):  # order?
    assert (len(factors) == octaves)
    filtered_signal = []
    result = np.zeros(len(signal))
    borders = [c0 * 2 ** i for i in range(octaves + 1)]
    for i in range(octaves):
        filtered_signal.append(butter_bandpass_filter(signal, borders[i], borders[i + 1], fs))
    for i in range(octaves):
        result += filtered_signal[i] * factors[i]
    return result


def butter_bandpass(lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 5000.0
    lowcut = 500.0
    highcut = 1250.0

    # # Filter a noisy signal.
    T = 0.1
    nsamples = T * fs
    t = np.linspace(0, T, nsamples, endpoint=False)
    a = 0.01
    f0 = 600.0
    f1 = 700.0
    x = np.sin(200 * np.pi * t)
    x += np.cos(400 * np.pi * t)

    x += np.cos(800 * np.pi * t)
    plt.figure(2)
    plt.clf()
    plt.plot(t, x, label='Noisy signal')

    y = transform(x, 7, [0, 0, 0, 0, 0.5, 0, 0], fs)

    plt.plot(t, y, label='Filtered signal ({} Hz), ({} Hz)'.format(f0, f1))
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()