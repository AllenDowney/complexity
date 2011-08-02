# importing cmath makes exp and other math functions handle
# complex numbers
from cmath import *


def fft(h):
    """compute the discrete Fourier transform of the sequence h.
    Assumes that len(h) is a power of two.
    """
    N = len(h)
 
    # the Fourier transform of a single value is itself
    if N == 1: return h
 
    # recursively compute the FFT of the even and odd values
    He = fft(h[0:N:2])
    Ho = fft(h[1:N:2])
 
    # merge the half-FFTs
    i = complex(0,1)
    W = exp(2*pi*i/N)
    ws = [pow(W,k) for k in range(N)]
    H = [e + w*o for w, e, o in zip(ws, He+He, Ho+Ho)]
    return H

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
