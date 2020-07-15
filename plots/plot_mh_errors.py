import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from functions import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import ImageGrid
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)

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
for hi,h in enumerate(hrange):
    for mi,m in enumerate(mrange):
        Lval = length(a,h,m,r)
        Rval = regen(a,h,m,r)
        vkval = killRate(ta,Lval)
        vdval = damageRate(ta,Lval,h,Rval)
        Lappr = lengthEffhp(a,h,m,r)
        Rappr = regenEffhp(a,h,m,r)
        vkappr = killRate(ta,Lappr)
        vdappr = damageRate(ta,Lappr,h,Rappr)
        L[m,h] = np.abs(Lval-Lappr)/Lval
        R[m,h] = np.abs(Rval-Rappr)/Rval
        vk[m,h] = np.abs(vkval-vkappr)/vkval
        vd[m,h] = np.abs(vdval-vdappr)/vdval
print(np.mean(vd[2:,2:]))
L[1:,1] = np.amin(L[1:,2:])
R[1:,1] = np.amin(R[1:,2:])
vk[1:,1] = np.amin(vk[1:,2:])
vd[1:,1] = np.amin(vd[2:,2:])
vd[1,0:] = np.amin(vd[2:,2:])
#(fig, axes) = plt.subplots(1,2)
fig, (ax0, ax1, cax) = plt.subplots(ncols=3, gridspec_kw={"width_ratios":[1,1, 0.05]})
plt.subplots_adjust(wspace=0.1)
#im = np.empty(axes.shape, dtype=axes.dtype)
#im[0,0] = axes[0,0].imshow(L, origin="lower", cmap="jet", norm=mpl.colors.LogNorm())
#im[0,1] = axes[0,1].imshow(R, origin="lower", cmap="jet", norm=mpl.colors.LogNorm())
im0 = ax0.imshow(vk, origin="lower", cmap="jet", norm=mpl.colors.LogNorm())
vmin = im0.norm.vmin
vmax = im0.norm.vmax
im1 = ax1.imshow(vd, origin="lower", cmap="jet", norm=mpl.colors.LogNorm(vmin=vmin, vmax=vmax))
ims = [im0,im1]
for i,ax in enumerate([ax0,ax1]):
    im = ims[i]
    ax.set_xlim([0.5,hmax-0.5])
    ax.set_ylim([0.5,mmax-0.5])
    ax.set_xticks(np.arange(20,hmax,20))
    ax.set_xlabel("hitpoints")
    ax.set_yticks(np.arange(20,mmax,20))
ax1.set_yticklabels([])
ax0.set_ylabel("maximum hit")

ip = InsetPosition(ax1, [1.05,0,0.05,1])
cax.set_axes_locator(ip)
fig.colorbar(im, cax=cax, ax=[ax0,ax1])
#axes[0,0].set_title("$\\delta\\langle L\\rangle$")
#axes[0,1].set_title("$\\delta\\langle R\\rangle$")
ax0.set_title("$\\delta v_k$")
ax1.set_title("$\\delta v_d$")
#axes[0,0].set_xticklabels([])
#axes[0,1].set_xticklabels([])
#axes[0,1].set_yticklabels([])
#axes[1,1].set_yticklabels([])
#axes[1,0].set_xlabel("hitpoints")
#axes[0,0].set_ylabel("maximum hit")
#fig.savefig('test.pdf', bbox_inches='tight', pad_inches=0.1)
fig.savefig('mhErrors.pdf', bbox_inches='tight', pad_inches=0.1)
