struct SimulationResult {
	long ticks;
	long heals;
	long damage;
	int fights;
};

struct FightParameters {
	double accuracy;
	int maxHit;
	int maxHp;
	int attackInterval;
	int regenInterval;
};

/** Returns a random double between 0 and 1 */
double GetRandProbability();

/** Returns a random integer between the arguments */
int GetRand(int minimum, int maximum);

/**
	Run multiple simulations of an osrs fight against a single enemy type

	@param r pointer to a SimulationResults struct to store the results
	@param p pointer to a FightParams struct that stores all fight parameters
	@param time The number of milliseconds to simulate for
*/
void simulate(SimulationResult* r, FightParameters* p, long time);
