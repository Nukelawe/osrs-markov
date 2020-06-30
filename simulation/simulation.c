#include "simulation.h"
#include "mt_rand.h"
#include <time.h>
#include <stdio.h>

int min(int a, int b) {
	if (a > b) return b;
	else return a;
}

/* generate a random integer in the interval [a, b] */
long long rand(long long a, long long b) {
	return a + genrand64_int63() % (b - a + 1);
}

void simulate(struct SimulationResult *r, struct FightParameters *p, long time) {
	r->ticks = 0;
	r->heals = 0;
	r->damage = 0;
	r->fights = 0;
	// keep simulating fights until time limit is reached
	clock_t begin = clock();
	int regenCooldown, attackCooldown, hp, ticks, heals, damage, hit;
	double t;
    while ((t = (double)(clock() - begin) / CLOCKS_PER_SEC * 1000) < time) {
		r->fights++;
        regenCooldown  = rand(1, p->regenInterval);
        attackCooldown = p->attackInterval;
        hp = p->maxHp;
		ticks  = 0;
		heals  = 0;
		damage = 0;

        while (hp > 0) {
			// next heal will occur before next hit
            if (regenCooldown < attackCooldown) {
				ticks += regenCooldown;
				attackCooldown -= regenCooldown;
                regenCooldown = p->regenInterval;
				hp = min(hp + 1, p->maxHp);
				++heals;
            }

			// hit the enemy once
            if (genrand64_real2() < p->accuracy) {
                hit = min(hp, rand(0, p->maxHit));
                hp -= hit;
                damage += hit;
            }

			ticks += attackCooldown;
            regenCooldown -= attackCooldown;
			attackCooldown = p->attackInterval;
        }

		r->ticks += ticks;
		r->heals += heals;
		r->damage += damage;
    }
}
