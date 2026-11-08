import struct
import numpy as np
import serial
import matplotlib.pyplot as plt

PORT = 'COM3'          # kendi COM portunu yaz (Aygıt Yöneticisi'nde ST-Link Virtual COM Port)
BAUD = 115200
BLOCK = 512
FS = 1000

ser = serial.Serial(PORT, BAUD, timeout=2)

def read_exact(n):
    buf = b''
    while len(buf) < n:
        chunk = ser.read(n - len(buf))
        if not chunk:
            raise TimeoutError('Karttan veri gelmiyor')
        buf += chunk
    return buf

def sync():
    """Başlığı (0xAA 0x55) bulana kadar bayt oku."""
    prev = b''
    while True:
        b = read_exact(1)
        if prev == b'\xaa' and b == b'\x55':
            return
        prev = b

def read_frame():
    if read_exact(2) != b'\xaa\x55':
        sync()
    cnt = struct.unpack('<H', read_exact(2))[0]
    data = np.frombuffer(read_exact(BLOCK * 2), dtype='<u2')
    return cnt, data

plt.ion()
fig, ax = plt.subplots(figsize=(9, 4))
t = np.arange(BLOCK) / FS
line, = ax.plot(t, np.zeros(BLOCK))
ax.set_ylim(-3, 3)
ax.set_xlabel('Zaman (s)')
ax.set_ylabel('Genlik (birim)')
ax.grid(True)

while plt.fignum_exists(fig.number):
    cnt, data = read_frame()
    x = (data.astype(float) - 2048) / 600     # DAC sayılarını Seviye 2'deki birime çevir
    line.set_ydata(x)
    ax.set_title(f'Ham ADC verisi, blok {cnt}')
    plt.pause(0.001)

ser.close()