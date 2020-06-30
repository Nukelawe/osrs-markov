import random as rand
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)

def binom(a,b):
    out = 1
    for i in range(0,b):
        out *= (a - i)
        out /= (b-i)
    return out

def hpk(a, h, m):
    r = (1+1/m)
    p = -1/(1+m)
    imax = (h-1)//(m+1)
    out = 0
    for i in range(0,imax+1):
        out += r**(h-m*i) * p**(i) * binom(h-m*i-1, i)
    return out/a

def hpkAppr(a, h, m):
    return 2/(m*a)*(h + (m - 1)/3)

def plotColorErr(a,hmax,mmax):
    hrange = range(1, hmax)
    mrange = range(1, mmax)
    vmin = -10**-0.5
    vmax = 10**-0.5
    linthresh = -6
    C = np.zeros([mmax, hmax])
    for h in hrange:
        for m in mrange:
            c = hpkAppr(a,h,m)-hpk(a,h,m)
            bound = np.power(1-1/m, h)
            if np.abs(c) > bound: c = c/np.abs(c)*bound
            C[m, h] = c
    fig, ax = plt.subplots()
    ax.set_xlim([0.5,hmax-0.5])
    ax.set_ylim([0.5,mmax-0.5])
    ax.set_aspect('equal', adjustable='box')
    divider = make_axes_locatable(ax)
    cax = divider.new_vertical(size="7%", pad=0.1, pack_start=False)
    im = ax.imshow(C, cmap="bwr", origin="lower", norm=mpl.colors.SymLogNorm(
        linthresh=10**linthresh, vmin=vmin, vmax=vmax, base=10, linscale=0.5))
    fig.add_axes(cax)
    cbarticks = [10**i for i in range(-1,linthresh-1,-1)] + [-10**i for i in range(-1,linthresh-1,-1)]
    cbar = plt.colorbar(im, ax=ax, cax=cax, orientation="horizontal",
            drawedges=False, spacing="uniform",
            ticks=cbarticks)
    cbar.ax.xaxis.set_label_position("top")
    cbar.ax.xaxis.tick_top()
    ax.set_xlabel('hitpoints')
    ax.set_ylabel('maximum hit')
    plt.savefig('apprComparison.pdf', bbox_inches='tight', pad_inches=0.1)

def plotContourErr(a,hmax,mmax):
    hrange = np.arange(1, hmax)
    mrange = np.arange(1, mmax)
    h, m = np.meshgrid(hrange, mrange)
    Z = np.power(1-1/m, h)
    contours = 150
    levels = np.power(0.5, np.arange(contours,0-1,-1))
    plt.contour(h, m, Z, levels, linewidths=0.2, colors="k")
    plt.contourf(h, m, Z, levels, cmap="plasma_r")
    plt.savefig('apprComparison.pdf', bbox_inches='tight', pad_inches=0)

#plotdps(a,m,hpmax,tr,ta)
plotColorErr(1,90,30)

#plt.clf()
#plt.plot(hsim, ysim, '.b', label='approximation 1')
#plt.savefig('test.pdf')
