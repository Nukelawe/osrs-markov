import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from functions import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)

hs = np.array([3,50])
ms = np.array([3,50])
ta = 4
r = 4/100
xs = np.power(10,np.arange(-3.5, 0.5, 0.01))
L = np.ones([len(xs),len(ms),len(hs)])*float("nan")
R = np.ones(L.shape)*float("nan")
vk = np.ones(L.shape)*float("nan")
vd = np.ones(L.shape)*float("nan")
Lerr = np.ones(L.shape)*float("nan")
Rerr = np.ones(L.shape)*float("nan")
vkerr = np.ones(L.shape)*float("nan")
vderr = np.ones(L.shape)*float("nan")
# populate the data arrays
(fig1, axes1) = plt.subplots(2,2)
(fig2, axes2) = plt.subplots(2,2)
fig1.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=0.4,hspace=0.1)
fig2.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=0.4,hspace=0.1)
cmap = np.empty([2,2,4])
for mi,m in enumerate(ms):
    for hi,h in enumerate(hs):
        for xi,x in enumerate(xs):
            a = 2*r/(x*m)
            if a > 1: continue
            L[xi,mi,hi] = length(a,h,m,r)
            R[xi,mi,hi] = regen(a,h,m,r)
            vk[xi,mi,hi] = killRate(ta,L[xi,mi,hi])
            vd[xi,mi,hi] = damageRate(ta,L[xi,mi,hi],h,R[xi,mi,hi])
            Lappr = lengthEffhp(a,h,m,r)
            Rappr = regenEffhp(a,h,m,r)
            vkappr = killRate(ta,Lappr)
            vdappr = damageRate(ta,Lappr,h,Rappr)
            Lerr[xi,mi,hi] = np.abs(L[xi,mi,hi]-Lappr)/L[xi,mi,hi]
            Rerr[xi,mi,hi] = np.abs(R[xi,mi,hi]-Rappr)/R[xi,mi,hi]
            vkerr[xi,mi,hi] = np.abs(vk[xi,mi,hi]-vkappr)/vk[xi,mi,hi]
            vderr[xi,mi,hi] = np.abs(vd[xi,mi,hi]-vdappr)/vd[xi,mi,hi]
        axes1[0,0].plot(xs, xs, color="k")
        axes1[0,0].plot(xs, L[:,mi,hi])
        axes1[0,1].plot(xs, R[:,mi,hi])
        axes1[1,0].plot(xs, vk[:,mi,hi])
        axes1[1,1].plot(xs, vd[:,mi,hi])
        axes2[0,0].plot(xs, Lerr[:,mi,hi])
        axes2[0,1].plot(xs, Rerr[:,mi,hi])
        axes2[1,0].plot(xs, vkerr[:,mi,hi])
        plot = axes2[1,1].plot(xs, vderr[:,mi,hi])
        cmap[mi,hi,:] = mpl.colors.to_rgba(plot[0].get_color())
for ax in axes1.flatten():
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_xlim([1e-3,3])
for ax in axes2.flatten():
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_xlim([3e-3,1])
for ax in axes2.flatten():
    ax.set_ylim([axes2[1,1].get_ylim()[0],2])
for ax in axes1[1,:]: ax.set_xlabel("$\\frac{2\\rho}{am}$")
for ax in axes2[1,:].flatten(): ax.set_xlabel("$\\frac{2\\rho}{am}$")

# inset colormap legend
for ax in [axes1[0,0],axes2[0,0]]:
    inset = inset_axes(ax,width=.3,height=.3,loc=2)
    inset.imshow(cmap,origin="lower")
    inset.set_xticks([0,1])
    inset.set_yticks([0,1])
    hlabels = ["$h\\!=\\!"+str(h)+"$" for h in hs]
    mlabels = ["$m\\!=\\!"+str(m)+"$" for m in ms]
    inset.set_xticklabels(hlabels,rotation=90)
    inset.set_yticklabels(mlabels)
    inset.yaxis.tick_right()

axes1[0,0].set_xticklabels([])
axes2[0,0].set_xticklabels([])
axes1[0,1].set_xticklabels([])
axes2[0,1].set_xticklabels([])
axes1[0,0].set_ylabel("$\\langle L\\rangle$")
axes2[0,0].set_ylabel("$\\delta\\langle L\\rangle$")
axes1[0,1].set_ylabel("$\\langle R\\rangle$")
axes2[0,1].set_ylabel("$\\delta\\langle R\\rangle$")
axes1[1,0].set_ylabel("$v_k$")
axes2[1,0].set_ylabel("$\\delta v_k$")
axes1[1,1].set_ylabel("$v_d$")
axes2[1,1].set_ylabel("$\\delta v_d$")
fig1.savefig('arValues.pdf', bbox_inches='tight', pad_inches=0.1)
#fig2.savefig('arErrors.pdf', bbox_inches='tight', pad_inches=0.1)
