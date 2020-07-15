import random as rand
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)

resolution = 500
contours = 40
m = 7

def D(z, m):
    return m - (m+1)*z + z**(m+1)

def Q(z, m):
    out = 0
    for i in range(0,m):
        out += (m-i) * z**i
    return out

def Dr(z, m, r):
    return (m-r) - (m-r+1)*z + (1-r)*z**(m+1) + r*z**(m+2)

def rootPlot():
    rhos = np.arange(0,1,0.01)
    rs = np.zeros(rhos.shape)
    plt.clf()
    for m in range(1,20):
        d = np.zeros(m+3)
        for irho,rho in enumerate(rhos):
            d[m+2] = m-rho
            d[m+1] = -(m+rho+1)
            d[1] = 1-rho
            d[0] = rho
            roots = np.roots(d)
            for root in roots:
                if np.abs(root) < 1: rs[irho] = np.real(root)
        plt.plot(rhos, rs)
    plt.savefig('regenDominantRoot.pdf', bbox_inches='tight', pad_inches=0)

plt.clf()
plt.axvline(x=0,lw=0.1,color="k")
plt.axhline(y=0,lw=0.1,color="k")
theta = np.arange(0, resolution+1)*2*np.pi/resolution
r1 = m/(m-1)
r2 = 2
gamma1 = r1*np.exp(theta * 1j)
gamma2 = r2*np.exp(theta * 1j)
plt.plot(np.real(Q(gamma1, m)), np.imag(Q(gamma1, m)))
plt.axis("equal")
plt.savefig('winds.pdf', bbox_inches='tight', pad_inches=0)


plt.clf()
plt.plot(theta, np.abs(Q(gamma1, m)))
plt.savefig('circle.pdf', bbox_inches='tight', pad_inches=0)

plt.clf()
d = np.zeros(m+3)
r = 0.7
d[m+2] = m-r
d[m+1] = -(m-r+1)
d[1] = 1-r
d[0] = r
q = np.zeros(m+2)
for i in range(0, m): q[i] = i+1
roots = np.roots(d)
arg = np.arctan2(np.imag(roots), np.real(roots))
for i,a in enumerate(arg):
    if a < 0: arg[i] = a + 2 * np.pi
ind = np.argsort(arg, axis=0)
N = len(roots)
mid = np.sum(roots)/N
#plt.plot(np.real(mid), np.imag(mid), ls="none", marker="o")
for j,i in enumerate(ind):
    line = [roots[i], roots[ind[(j+1+N)%N]]]
    #print(np.abs(line[0] - line[1]))
    #plt.plot(np.real(line), np.imag(line), lw="0.5", color="b")
plt.plot(np.real(roots), np.imag(roots), ls="none", marker="x")
plt.plot(np.real(gamma1), np.imag(gamma1), lw=1.0, color="r")
plt.plot(np.real(gamma2), np.imag(gamma2), lw=1.0, color="r")
plt.axvline(x=0,lw=0.1,color="#020202",ls="dotted")
plt.axhline(y=0,lw=0.1,color="#020202",ls="dotted")
c = 1.15
plt.xlim((-r2, r2))
plt.ylim((-r2, r2))
plt.gca().set_aspect('equal', adjustable='box')
x = y = np.arange(-r2, r2, 0.01)
X, Y = np.meshgrid(x, y)
Z = np.abs(Dr(X + Y*1j, m, r))
levels = np.arange(0,1,1/contours)*100
plt.contour(X, Y, Z, levels, linewidths=0.2, colors="k")
plt.savefig('roots.pdf', bbox_inches='tight', pad_inches=0)
plt.savefig('roots.png', bbox_inches='tight', pad_inches=0)

rootPlot()
