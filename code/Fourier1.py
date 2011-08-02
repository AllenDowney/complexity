# importing cmath makes exp and other math functions handle
# complex numbers
from cmath import *


def fft(h):
    """compute the discrete Fourier transform of the sequence h.
    Assumes that len(h) is a power of two.
    """
    return h

if __name__ == '__main__':

    # make a signal with two sine components, f=6 and f=12
    N = 128
    t = [1.0*n/N for n in range(N)]
    h = [sin(2*pi*6*tn) + sin(2*pi*12*tn) for tn in t]

    # compute the Fourier transform
    H = fft(h)

    # print the spectral density function
    sdf = [Hn * Hn.conjugate() for Hn in H]
    for n in range(N/2 + 1):
        print '%d  %.3f' % (n, sdf[n].real)
