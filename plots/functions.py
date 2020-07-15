import random as rand
import numpy as np
import scipy.special as sp
import scipy.linalg as linalg

def binom(a,b):
    out = 1
    for i in range(0,b):
        out *= (a - i)
        out /= (b-i)
    return out

def lengthNoregen(a, h, m):
    if h > 7*m: return lengthNoregenAppr(a,h,m)
    r = (1+1/m)
    p = -1/(1+m)
    imax = (h-1)//(m+1)
    out = 0
    for i in range(0,imax+1):
        out += r**(h-m*i) * p**(i) * binom(h-m*i-1, i)
    return out/a

def lengthNoregenAppr(a, h, m):
    return 2/(m*a)*(h + (m - 1)/3)

# regenerationless transition probabilities
def pi(i, j, a, m, h):
    if j > 0:
        return dmgRollProb(i-j,a,m)
    summa = 0
    for k in range(i-j, h+1):
        summa += dmgRollProb(k,a,m)
    return summa

# transition probabilities
def p(i, j, a, h, m, r):
    if i == 0 or i == h:
        return pi(i,j,a,m,h)
    return r * pi(i+1,j,a,m,h) + (1-r) * pi(i,j,a,m,h)

# probability distribution of accuracy corrected damage roll
def dmgRollProb(x, a, m):
    if x == 0:
        return 1 - a*m/(m+1)
    if 1 <= x and x <= m:
        return a/(m+1)
    return 0

def transitionMatrix(a, h, m, r):
    T = np.empty([h+1,h+1])
    for i in range(h+1):
        for j in range(h+1):
            T[i,j] = p(i, j, a, h, m, r)
    M = -T[1:,1:] # the transient part
    for i in range(h):
        M[i,i] += 1
    return M

def length(a, h, m, r):
    M = transitionMatrix(a,h,m,r)
    rhs = np.ones(h)
    L = linalg.solve(M, rhs)
    return L[h-1]

def regen(a, h, m, r):
    M = transitionMatrix(a,h,m,r)
    rhs = np.ones(h)
    rhs[h-1]=0
    R = linalg.solve(M, r*rhs)
    return R[h-1]

def lengthEffhp(a, h, m, r):
    Lappr = lengthNoregenAppr(a,h,m)
    if h < 7*m:
        Lappr = lengthNoregen(a,h,m)
    return 1/(1-(2*r)/(a*m)) * (Lappr - 2*r*(m+1)/(a*m)**2)

def regenEffhp(a, h, m, r):
    L = lengthEffhp(a,h,m,r)
    return r*(L - (m+1)/(a*m))

def lengthTriAppr(a, h, m, r):
    coeff = (1+1/(m-r))
    return (m+1)/(a*m) * coeff**(h-1)

def killRate(ta, L):
    return 1/(ta*L)

def damageRate(ta, L, h, R):
    return (h+R)/(ta*L)

def damageRateMax(a, h, m):
    return 0.5*a*m
