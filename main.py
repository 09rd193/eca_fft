# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

rule = 90
n = 5
size = 2 ** n ## ECA only

def convertR10toR2(r10):
    return format(r10, '08b')[-8:]

def getbintoint(integer, size):
    binnum = format(integer, 'b')
    binnum = binnum.zfill(size)
    return binnum

def onestep(rule, line):
    newline = ''
    for i in range(len(line)):
        x, y, z = 0, 0, 0
        if i == 0:
            x, y, z = 0, line[i], line[i + 1]
        elif i == len(line) - 1:
            x, y, z = line[i - 1], line[i], 0
        else:
            x, y, z = line[i - 1], line[i], line[i + 1]
        r = int(x) * 4 + int(y) * 2 + int(z)
        newline += str(rule[r])
    return newline

def makeprogression():
    progression = []
    rule90 = rule
    rule2 = convertR10toR2(rule90)
    binnum = getbintoint(1, size)
    progression.append(int(binnum, 2))
    print((2 ** (n + 1)) - 2)
    for i in range((2 ** (n + 1)) - 2 - 1):
        binnum = onestep(rule2, binnum)
        progression.append(int(binnum, 2))
    return progression

def main():
    progression = makeprogression()
    ## ref :: http://www2.kaiyodai.ac.jp/~kentaro/materials/new_HP/python/16fft.html
    # ydata = progression * len(progression)
    ydata = progression * 5
    xdata = range(len(ydata))
    time_step = 1
    
    #FFT
    sample_freq = fftpack.fftfreq(len(ydata), d=time_step)
    y_fft = fftpack.fft(ydata)
    pidxs = np.where(sample_freq > 0)
    freqs, power = sample_freq[pidxs], np.abs(y_fft)[pidxs]
    freq = freqs[power.argmax()]

    #PLot
    plt.figure(figsize=(6,8))
    plt.subplot(211)
    plt.plot(xdata, ydata,'b-', linewidth=1)
    plt.xlabel('Time')
    plt.ylabel('Ydata')
    plt.grid(True)

    plt.subplot(212)
    # plt.semilogx(freqs, power,'b.-',lw=1)
    plt.loglog(freqs, power, 'b.-', lw=1)
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.grid(True)

    plt.show()

if __name__ == '__main__':
    main()