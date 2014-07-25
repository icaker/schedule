// RandGenerator.h: interface for the RandGenerator class.
//
//////////////////////////////////////////////////////////////////////
#define Truncated_Factor 20

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>

class RandomGenerator  
{
private:
	static const gsl_rng_type * T;
	static gsl_rng * r;

public:
	//initialize the environment, set the seed
	static void init(int seed);
	//restore the environment
	static void destroy();

	//Generate a uniform distributed integer between lower and upper
	//lower included, upper excluded
	static int genUniformInt(int lower, int upper);

	//Generate a uniform distributed double value between lower and upper
	//lower included, upper excluded
	static double genUniformDouble(double lower, double upper);

	//Generate a uniform random numbers in the range [0.0, 1.0)
	static double genUniform();

	//This function returns either 0 or 1, the result of a Bernoulli trial with probability p.
	//The probability distribution for a Bernoulli trial is, 
	static int genBernoulliInt(double p);

	//This function returns a random integer from the Poisson distribution with mean mu.
	static int genPoissonInt(double mu);

	//This function returns a random variate from the Pareto distribution of order a.
	static double genParetoDouble(double a, double b);

	//This function returns a random variate from the truncated Pareto distribution of order a.
	static double genTruncatedParetoDouble(double a, double b);
};
