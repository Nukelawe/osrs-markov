import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from functions import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)

def plotMhValues():
    a = 0.5
    ta = 4
    tr = 100
    r = ta/tr
    hmax = 100
    mmax = 100
    hrange = np.arange(2, hmax)
    mrange = np.arange(1, mmax)
    L = np.zeros([mmax, hmax])
    R = np.zeros(L.shape)
    vk = np.zeros(L.shape)
    vd = np.zeros(L.shape)
    # populate the data arrays
    for hi,h in enumerate(hrange):
        for mi,m in enumerate(mrange):
            L[m,h] = lengthEffhp(a,h,m,r)
            R[m,h] = np.maximum(regenEffhp(a,h,m,r),0)
            vk[m,h] = killRate(ta,L[m,h])
            vd[m,h] = damageRate(ta,L[m,h],h,R[m,h])
    # fix outliers for better coloring
    R[1:,0] = np.amin(R[1:,2])
    L[1:,0] = np.amin(L[1:,2])
    vk[1:,1] = np.amax(vk[1:,2])

    (fig, axes) = plt.subplots(2,2)
    plt.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=0,hspace=None)
    im = np.empty(axes.shape, dtype=axes.dtype)
    im[0,0] = axes[0,0].imshow(L, origin="lower", cmap="jet", norm=mpl.colors.LogNorm())
    im[0,1] = axes[0,1].imshow(R, origin="lower", cmap="jet", norm=mpl.colors.LogNorm())
    im[1,0] = axes[1,0].imshow(vk, origin="lower", cmap="jet", norm=mpl.colors.LogNorm())
    im[1,1] = axes[1,1].imshow(vd, origin="lower", cmap="jet", norm=mpl.colors.Normalize())
    for i in range(2):
        for j in range(2):
            ax = axes[i,j]
            ax.set_xlim([0.5,hmax-0.5])
            ax.set_ylim([0.5,mmax-0.5])
            ax.set_xticks(np.arange(20,hmax,20))
            ax.set_yticks(np.arange(20,mmax,20))
            fig.colorbar(im[i,j], ax=ax)
    axes[0,0].set_title("$\\langle L\\rangle$")
    axes[0,1].set_title("$\\langle R\\rangle$")
    axes[1,0].set_title("$v_k$")
    axes[1,1].set_title("$v_d$")
    axes[0,0].set_xticklabels([])
    axes[0,1].set_xticklabels([])
    axes[0,1].set_yticklabels([])
    axes[1,1].set_yticklabels([])
    axes[1,0].set_xlabel("hitpoints")
    axes[1,1].set_xlabel("hitpoints")
    axes[0,0].set_ylabel("maximum hit")
    axes[1,0].set_ylabel("maximum hit")
    fig.savefig('mhValues.pdf', bbox_inches='tight', pad_inches=0.1)

plotMhValues()
