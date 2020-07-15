import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import osrsmath.combat.monsters as monsters
import osrsmath.combat.player as player
from functions import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)
np.set_printoptions(precision=3)

def hmplot(hrange, mrange, data, filename, norm=None, title=""):
    fig, ax = plt.subplots()
    hmin = hrange[0]
    mmin = mrange[0]
    hmax = hrange[len(hrange)-1]
    mmax = mrange[len(mrange)-1]
    datafull = np.zeros([mmax+1,hmax+1])
    datafull[mmin:,hmin:] = data
    ax.set_title(title)
    ax.set_ylabel('maximum hit')
    ax.set_xlabel('hitpoints')
    ax.set_xlim(hrange[0]-0.5, hmax-0.5)
    ax.set_ylim(mrange[0]-0.5, mmax-0.5)
    ax.set_aspect('equal', adjustable='box')
    divider = make_axes_locatable(ax)
    cax = divider.new_horizontal(size=0.15, pad=0.1, pack_start=False)
    fig.add_axes(cax)
    im = ax.imshow(datafull,origin="lower", cmap="jet", norm=norm)
    cbar = fig.colorbar(im, ax=ax, cax=cax, orientation="vertical")
    #cbar.ax.xaxis.set_label_position("top")
    #cbar.ax.xaxis.tick_top()
    print("Saving "+filename)
    fig.savefig(filename, bbox_inches='tight', pad_inches=0.1)

def plotNoregenAsymptoticErr():
    a = 1
    hrange = np.arange(1, 300)
    mrange = np.arange(2, 110)
    vmin = 1e-8
    data = np.zeros([mrange.shape[0], hrange.shape[0]])
    for hi,h in enumerate(hrange):
        for mi,m in enumerate(mrange):
            Lappr = lengthNoregenAppr(a,h,m)
            L = lengthNoregen(a,h,m)
            data[mi,hi] = np.maximum(vmin,np.abs(Lappr-L)/L)
    norm=mpl.colors.LogNorm(vmin=vmin)
    hmplot(hrange,mrange,data,"asymptoticApprComparison.pdf",norm=norm)

plotNoregenAsymptoticErr()
