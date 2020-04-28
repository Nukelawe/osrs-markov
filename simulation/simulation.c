#include "simulation.h"

void simulate(SimulationResult* r, FightParameters* p, long time) {
	r->ticks = 0;
	r->heals = 0;
	r->damage = 0;
	r->fights = 0;
	// keep simulating fights until time limit is reached
	clock_t begin = clock();
    while (double(clock() - begin) / CLOCKS_PER_SEC * 1000 < time) {
		r->fights++;
        int regenCooldown  = GetRand(1, p->regenInterval);
        int attackCooldown = p->attackInterval;
        int hitpoints = p->maxHp;
		int ticks  = 0;
		int heals  = 0;
		int damage = 0;

        while (hitpoints > 0) {
			// next heal will occur before next hit
            if (regenCooldown < attackCooldown) {
				ticks += regenCooldown;
				attackCooldown -= regenCooldown;
                regenCooldown = p->regenInterval;
                hitpoints = min(hitpoints + 1, p->maxHp);
            }

			// hit the enemy once
            if (GetRandProbability() < p->accuracy) {
                int hit = min(hitpoints, GetRand(0, p->maxHit));
                hitpoints -= hit;
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


double GetRandProbability() {
    return (double)rand()/(RAND_MAX);
}

int GetRand(int minimum, int maximum) {
    static int Init = 0;
    if (Init == 0) {
        /*
         *  As Init is static, it will remember it's value between
         *  function calls.  We only want srand() run once, so this
         *  is a simple way to ensure that happens.
         */
        srand(time(NULL));
        Init = 1;
    }
    /*
    * Formula:
    *    rand() % N   <- To get a number between 0 - N-1
    *    Then add the result to min, giving you
    *    a random number between min - max.
    */
    return rand()%(maximum-minimum+1) + minimum;
}
