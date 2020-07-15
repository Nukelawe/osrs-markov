import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import osrsmath.combat.monsters as monsters
import osrsmath.combat.player as player
from functions import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import ImageGrid
mpl.rc('font', family='serif')
mpl.rc('mathtext',fontset='cm')
mpl.rc('text', usetex=True)

# setuplist
# fresh account, no gear
player1 = player.Player({'attack': 10, 'strength': 10, 'defence': 1, 'prayer': 1, 'hitpoints': 10, 'magic': 1, 'ranged': 1})
player1.equip_by_name("Iron Scimitar")
player1.combat_style = 'slash'
# f2p max melee gear minimal requirements
player3 = player.Player({'attack': 40, 'strength': 40, 'defence': 1, 'prayer': 1, 'hitpoints': 10, 'magic': 1, 'ranged': 1})
player3.equip_by_name("Rune Scimitar")
player3.combat_style = 'slash'
# lvl 70 melee stats, d scimmy
player4 = player.Player({'attack': 70, 'strength': 70, 'defence': 1, 'prayer': 1, 'hitpoints': 10, 'magic': 1, 'ranged': 1})
player4.equip_by_name("Dragon Scimitar")
player4.combat_style = 'slash'
# maxed account, abyssal whip
player5 = player.Player({'attack': 99, 'strength': 99, 'defence': 99, 'prayer': 99, 'hitpoints': 99, 'magic': 99, 'ranged': 99})
player5.equip_by_name("Abyssal whip")
player5.combat_style = 'flick'
setups = [player1,player3, player4, player5]

# list of enemies
monsterdata = monsters.get_monster_data()
enemyIds = [
    "3028", # goblin lvl 2
    "2098", # hill giant lvl 28
    "2005", # lesser demon lvl 82
    "104", # hellhound lvl 122
    "240" # black demon lvl 172
]
enemies = [monsters.Monster.from_id(e) for e in enemyIds]
enemynames = [monsterdata[e]["name"] for e in enemyIds]
hitpoints = [monsterdata[e]["hitpoints"] for e in enemyIds]

setupnames = [
    s.gear["weapon"]["name"]+", "
    +str(s.levels["attack"])+" attack, "+str(s.levels["strength"])+" strength"
    for s in setups
]

tr = 100
fig, axes = plt.subplots(ncols=2)
fig.subplots_adjust(wspace=0.1)
fig2 = plt.figure(None, (1,1))
ax2 = fig2.add_axes([0,0,1,1])
colors = ["tab:gray", "tab:blue", "tab:red", "tab:brown"]
markers = ["s", "^", "P", "*", "."]
for si,setup in enumerate(setups):
    color = mpl.colors.to_rgba(colors[si])
    for ei,enemy in enumerate(enemies):

        # calculate fight parameters
        m = setup.get_max_hit(lambda x: 0, lambda x: 1)
        A = setup.get_attack_roll(lambda x: 0, lambda x: 1)
        attack_type = setup.get_stances()[setup.combat_style]['attack_type']
        D = enemy.get_defence_roll(attack_type)
        a = enemy.get_accuracy(A, D)
        ta = setup.get_stats()["attack_speed"]/0.6
        r = ta/tr
        h = hitpoints[ei]
        if a < 0.01: continue

        # calculate errors
        L = length(a,h,m,ta/tr)
        R = regen(a,h,m,ta/tr)
        vk = killRate(ta,L)
        vd = damageRate(ta,L,h,R)
        Lappr = lengthEffhp(a,h,m,r)
        Rappr = regenEffhp(a,h,m,r)
        #Lappr = lengthNoregen(a,h,m)
        #Rappr = 0
        vkappr = killRate(ta,Lappr)
        vdappr = damageRate(ta,Lappr,h,Rappr)
        Lerr = np.abs(L-Lappr)/L
        Rerr = np.abs(R-Rappr)/R
        vkerr = np.abs(vk-vkappr)/vk
        vderr = np.abs(vd-vdappr)/vd

        # plot
        x = 2*r/(a*m)
        marker = markers[ei]
        ms = 5
        #axes[0,0].plot(x, Lerr, ms=ms, color=color, marker=marker)
        #axes[0,1].plot(x, Rerr, ms=ms, color=color, marker=marker)
        axes[0].plot(x, vkerr, ms=ms, color=color, marker=marker)
        axes[1].plot(x, vderr, ms=ms, color=color, marker=marker)

        # label plot
        ax2.plot(ei,si, ms=5, color=color, marker=marker)

# label plot
ax2.set_xticks(np.arange(len(enemies))-0.3)
ax2.set_xticklabels(enemynames, rotation=-45, ha="left")
ax2.set_yticks(np.arange(len(setups)))
ax2.tick_params(axis='both', which='both',length=0)
ax2.set_yticklabels(setupnames)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
pad = 0.0
xlim = ax2.get_xlim()
ylim = ax2.get_xlim()
ax2.set_xlim([xlim[0]-pad,xlim[1]+pad])
ax2.set_ylim([ylim[0]-pad,ylim[1]+pad])
ax2.set_aspect('equal', adjustable='box')

for ax in axes.flatten():
    ax.set_aspect('equal', adjustable='box')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ylim = ax.get_ylim()
    xlim = ax.get_xlim()
    ax.set_ylim([1e-4, 1.5e-2])
    ax.set_xlim([2e-3, 1])
axes[1].set_yticklabels([])
#for ax in axes[0,:]: ax.set_xticklabels([])
for ax in axes[:]: ax.set_xlabel("$\\frac{2\\rho}{am}$")
#axes[0,0].set_ylabel("$\\delta\\langle L\\rangle$")
#axes[0,1].set_ylabel("$\\delta\\langle R\\rangle$")
axes[0].set_ylabel("relative error")
axes[0].set_title("$\\delta v_k$")
axes[1].set_title("$\\delta v_d$")
fig.savefig('arErrors.pdf', bbox_inches='tight', pad_inches=0.0)
fig2.savefig('arErrorLabels.pdf', bbox_inches='tight', pad_inches=0.0)
