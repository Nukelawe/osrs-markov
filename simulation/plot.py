import random as rand
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)

def dph(a, m, h):
    y = min(m,h)
    return a*y*(y+1)/(h*(m+1))*((1/2)*(m+h+1) - (1/3)*(2*y+1))
    return a*h/hpk(m, h)

def binom(a,b):
    out = 1
    for i in range(0,b):
        out *= (a - i)
        out /= (b-i)
    return out

#def hpk(a, m, h):
#    r = (1+1/m)
#    p = -1/(1+m)
#    imax = (h-1)//(m+1)
#    out = 0
#    for i in range(0,imax+1):
#        out += r**(h-m*i) * p**(i) * binom(h-m*i-1, i)
#    return out/a

def hpkAppr(a, m, h):
    return 2*h/(m*a) + (2*m - 2)/(3*m*a)

def hpk(a, m, h, tr, ta):
    if h==0: return 0
    rho = ta/tr
    r = (m-rho+1)/(m-rho)
    if h <= m+1: return (m+1)/(a*m) * r**(h-1)
    return (m-rho+1)/(m-rho)*hpk(a,m,h-1,tr,ta) -rho/(m-rho)*hpk(a,m,h-m,tr,ta) -(1-rho)/(m-rho)*hpk(a,m,h-m-1,tr,ta)

def heals(a, m, h, tr, ta):
    return hpkSim(a, m, h, tr, ta)[2]

def hpkSim(a, m, hpmax, tr, ta):
    if tr < ta: raise ValueError("Regeneration period must not be shorter than attack period")
    if a <= 0 or m <= 0: return np.inf
    if hpmax == 0: return [0,0,0]
    fightCount = 10000
    rho = ta/tr
    dphNet = 0
    hpkNet = 0
    hlkNet = 0
    for i in range(fightCount):
        regencooldown = rand.randint(1,tr)
        attackcooldown = ta
        h = hpmax
        dmg = 0
        hits = 0
        while h > 0:
            regencooldown = ta+1 #skips the periodic regen method
            if regencooldown < attackcooldown:
                h = min(h+1, hpmax)
                attackcooldown -= regencooldown
                regencooldown = tr
            else:
                regencooldown -= attackcooldown
                attackcooldown = ta
                hits += 1
                if rand.random() < a:
                    d = min(h,rand.randint(0, m))
                    dmg += d
                    h -= d
            if rand.random() < rho and h > 0 and h < hpmax: h += 1
        dphNet += dmg/hits
        hpkNet += hits
        hlkNet += dmg-hpmax
    return [hpkNet/fightCount, dphNet/fightCount, hlkNet/fightCount]

def plothpk(a,m,hpmax,periods):
    hrange = np.arange(0, hpmax*m + 1 + 1)
    ysim = np.zeros((periods.shape[0], len(hrange)))
    ymod = np.zeros(ysim.shape)
    cols = ['r','g','b','k']
    plt.clf()
    for p in range(periods.shape[0]):
        tr = periods[p,0]
        ta = periods[p,1]
        for i in range(len(hrange)):
            h = hrange[i]
            ysim[p,i] = hpkSim(a, m, h, tr, ta)[0]
            ymod[p,i] = hpk(a, m, h, tr, ta)
        plt.plot(hrange, ysim[p,:], '+'+cols[p], markersize=5)
        plt.plot(hrange, ymod[p,:], cols[p], linewidth=0.5, label='$\\rho='+str(ta/tr)+'$')
    #plt.tight_layout()
    ax = plt.gca()
    ax.yaxis.set_label_coords(-0.05, 0.5)
    plt.xlim([0,hpmax*m+1])
    xticks = [i*m for i in range(0,hpmax+1)]
    xticklabels = ["$"+str(i)+"m$" for i in range(0,hpmax+1)]
    xticklabels[0] = "$0$"
    xticklabels[1] = "$m$"
    plt.xticks(xticks, xticklabels)
    plt.xlabel('hitpoints ($h$)')
    plt.ylabel('expected fight length $\\left(\\overline{L}_h\\right)$')
    plt.title("$m="+str(m)+"\qquad a="+str(a)+"$")
    plt.legend(loc='lower right')
    plt.margins(0,0)
    plt.savefig('test.pdf', bbox_inches='tight', pad_inches=0)

def plotdps(a,m,hpmax):
    dpsmax = m*a/2
    rCrit = (1+1/m)**m
    hsim = np.arange(1, hpmax*m + 1)
    ysim = np.zeros(hsim.shape)
    hmod = np.arange(0, hpmax*m + 1 + 1)
    ymod = np.zeros(hmod.shape)
    ymodtest1 = np.zeros(hmod.shape)
    yterm = np.zeros([hpmax, hmod.shape[0]])
    for i in range(len(ysim)):
        ysim[i] = hpkSim(a, m, h, tr, ta)[1]
    for i in range(len(ymod)):
        h = hmod[i]
        if h == 0:
            ymod[i] = 0
            continue
        heff = h + (ta/tr)*(hits-1-heals(a,m,h,tr,ta))
        ymod[i] = heff/hpk(a, m, h, tr, ta)
    plt.clf()
    plt.tight_layout()
    ax = plt.gca()
    ax.yaxis.set_label_coords(-0.05, 0.5)
    plt.xlim([0,hpmax*m+1])
    xticks = [i*m for i in range(0,hpmax+1)]
    xticklabels = ["$"+str(i)+"m$" for i in range(0,hpmax+1)]
    xticklabels[0] = "$0$"
    xticklabels[1] = "$m$"
    plt.xticks(xticks, xticklabels)
    plt.xlabel('hitpoints')
    plt.ylim([0,1.05*dpsmax])
    plt.yticks([0,m*a/rCrit,dpsmax], ['0', '$\\frac{ma}{\\left(1 + \\frac{1}{m}\\right)^m}$', '$\\frac{ma}{2}$'])
    plt.ylabel('damage per hit')
    plt.axhline(dpsmax, dashes=[1,1], linewidth=1.0)
    plt.axhline(m*a/rCrit, dashes=[1,1], linewidth=1.0)
    plt.title("$m="+str(m)+"\qquad a="+str(a)+"\qquad \\rho="+str(ta/tr)+"$")
    plt.ylim([0,1.05*dpsmax])
    plt.plot(hsim, ysim, '+r', label='simulation', markersize=5)
    plt.plot(hmod, ymod, 'k', linewidth=0.5, label='$h/\overline{L}_h$')
    plt.plot(hmod, ymodtest1, 'b', linewidth=0.5, label='approximation')
    plt.legend(loc='lower right')
    plt.margins(0,0)
    plt.savefig('test.pdf', bbox_inches='tight', pad_inches=0)

m = 5
a = 0.99
tr = 30
ta = 10
hpmax = 1
#plotdps(a,m,hpmax,tr,ta)
periods = np.array([[100,0],[100,50],[100,100]])
plothpk(a,m,hpmax,periods)

#plt.clf()
#plt.plot(hsim, ysim, '.b', label='approximation 1')
#plt.savefig('test.pdf')
