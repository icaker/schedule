// RandGenerator.cpp: implementation of the RandGenerator class.
//
//////////////////////////////////////////////////////////////////////

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sstream>
#include <math.h>
#include "RandomGenerator.h"

using namespace std;

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

const gsl_rng_type * 
RandomGenerator::T;

gsl_rng * 
RandomGenerator::r;

void
RandomGenerator::init(int seed)
{
	stringstream ssseed;
	//ssseed << time(NULL);
	ssseed << seed;

	//this setenv() does not work on sand.cise.ufl.edu, but works under linux	
	//you might remove the comment on your machine
	setenv("GSL_RNG_SEED", (ssseed.str()).data(), 1);
	
	gsl_rng_env_setup();

	T = gsl_rng_default;
	r = gsl_rng_alloc (T);
}

void
RandomGenerator::destroy()
{
	gsl_rng_free (r);

	//this unsetenv() does not work on sand.cise.ufl.edu, but works under linux	
	//you might remove the comment on your machine
	unsetenv("GSL_RNG_SEED");
}

int
RandomGenerator::genUniformInt(int lower, int upper)
{
	if(lower > upper)
	{
		cerr << "lowr needs to be less than or equal to upper." << endl;
		return lower;
	}

	if(lower == upper)
		return lower;

	// u is a uniform random number in the range [0.0, 1.0), 
	double u = gsl_rng_uniform (r);

	return lower + (int) ((upper - lower) * u);
}

double
RandomGenerator::genUniformDouble(double lower, double upper)
{
	if(lower > upper)
	{
		cerr << "lowr needs to be less than or equal to upper." << endl;
		return lower;
	}

	if(lower == upper)
		return lower;

	// u is a uniform random double value in the range [0.0, 1.0), 
	double u = gsl_rng_uniform (r);

	return lower + (upper - lower) * u;
}

double
RandomGenerator::genUniform()
{
	//a uniform random numbers in the range [0.0, 1.0), 
	return gsl_rng_uniform (r);
}

int
RandomGenerator::genBernoulliInt(double p)
{
	unsigned int k = gsl_ran_bernoulli(r, p);
	return (int)k;
}

int
RandomGenerator::genPoissonInt(double mu)
{
	unsigned int k = gsl_ran_poisson(r, mu);
	return (int)k;	
}


double
RandomGenerator::genParetoDouble(double a, double b)
{
/* This function returns a random variate from the Pareto distribution of order a. The distribution function is,

              p(x) dx = (a/b) / (x/b)^{a+1} dx

    for x >= b. 
*/
	return gsl_ran_pareto(r, a, b);
}

double
RandomGenerator::genTruncatedParetoDouble(double a, double b)
{
/* This function returns a random variate from the Pareto distribution of order a. The distribution function is,

              p(x) dx = (a/b) / (x/b)^{a+1} dx

    for x >= b. 

	mean(x) = ab / a - 1

	if random_value > Truncated_Factor * mean(x), we return a large number max; else we return random_value;
*/
	if(a < 1)
	{
		cerr << "Error: a > 1" << endl;
		exit(1);
	}

	double value = gsl_ran_pareto(r, a, b);

	double mean = a * b / (a - 1);

	double c = Truncated_Factor * mean;

	if(value <= c)
		return value;

	return a * c / (a - 1);
}

