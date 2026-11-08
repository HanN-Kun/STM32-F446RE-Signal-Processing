import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window

# Deney 1: FFT ile spektrum
fs, N = 1000, 1000
n = np.arange(N); t = n/fs
x = 1.0*np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*120*t) + 0.25*np.sin(2*np.pi*300*t)

X = np.fft.rfft(x)/N
P = np.abs(X); P[1:-1] *= 2          # tek taraflı genlik
f = np.fft.rfftfreq(N, 1/fs)

plt.figure(); plt.stem(f, P); plt.xlim(0, 500); plt.grid(True)
plt.xlabel('Frekans (Hz)'); plt.ylabel('Genlik'); plt.title('Deney 1: Genlik spektrumu')

# Deney 2: Aliasing
f0, fs_s = 900, 1000
f_alias = abs(f0 - round(f0/fs_s)*fs_s)
print('Beklenen alias frekansı:', f_alias)

t_c = np.arange(0, 0.02, 1/50000)
t_s = np.arange(0, 0.02, 1/fs_s)

plt.figure()
plt.plot(t_c, np.sin(2*np.pi*f0*t_c), 'b', label='900 Hz sinyal')
plt.stem(t_s, np.sin(2*np.pi*f0*t_s), linefmt='r-', markerfmt='ro', basefmt=' ', label='Örnekler (fs=1000)')
plt.plot(t_c, -np.sin(2*np.pi*f_alias*t_c), 'k--', label='100 Hz alias')
plt.legend(); plt.grid(True); plt.xlabel('Zaman (s)'); plt.title('Deney 2: Aliasing')

xs = np.sin(2*np.pi*f0*n/fs_s)
Xs = np.abs(np.fft.rfft(xs))/N; Xs[1:-1] *= 2
plt.figure(); plt.stem(f, Xs); plt.xlim(0, 500); plt.grid(True)
plt.xlabel('Frekans (Hz)'); plt.title('900 Hz sinyalin fs=1000 ile örneklenmiş spektrumu')

# Deney 3: Pencere fonksiyonları ve spektral sızıntı
x3 = np.sin(2*np.pi*50.5*t)
plt.figure()
for name in ['boxcar', 'hann', 'hamming', 'blackman']:
    w = get_window(name, N)          # periyodik pencere (spektral analiz için doğru form)
    Xw = np.abs(np.fft.rfft(x3*w))/np.sum(w)*2
    plt.plot(f, 20*np.log10(Xw + 1e-12), label=name)
plt.xlim(0, 200); plt.ylim(-120, 5); plt.grid(True); plt.legend()
plt.xlabel('Frekans (Hz)'); plt.ylabel('Genlik (dB)'); plt.title('Deney 3: Pencere karşılaştırması')

plt.show()