// Simulator.cpp: implementation of the Simulator class.
//
//////////////////////////////////////////////////////////////////////

#include <iostream>
#include <fstream>
#include <time.h>
#include "RandomGenerator.h"

using namespace std;

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

int main(int argc, char **argv)
{
        int seed = 78368;
        //double seed = time(NULL);

	RandomGenerator::init(seed);

        ofstream outfile("simu",ofstream::out|ofstream::app);
        int value_poisson=0;
        float value_pareto=0;
        float k=10.0/3.0;

        for(int i=1;i<3601;i++){
          //mean:10Mbits
          value_poisson = RandomGenerator::genPoissonInt(5);
          for (int j=0;j<value_poisson;j++){
            value_pareto = RandomGenerator::genTruncatedParetoDouble(1.5,k);
            outfile<<i<<'\t'<<value_pareto<<'\t'<<"0"<<endl;
          }
          //mean:1Mbits
          value_poisson = RandomGenerator::genPoissonInt(50);
          for (int j=0;j<value_poisson;j++){
            value_pareto = RandomGenerator::genTruncatedParetoDouble(1.5,k/10);
            outfile<<i<<'\t'<<value_pareto<<'\t'<<"1"<<endl;
          }
          //mean:0.1Mbits
          value_poisson = RandomGenerator::genPoissonInt(50);
          for (int j=0;j<value_poisson;j++){
            value_pareto = RandomGenerator::genTruncatedParetoDouble(1.5,k/100);
            outfile<<i<<'\t'<<value_pareto<<'\t'<<"2"<<endl;
          }
        }
        outfile.close();
	RandomGenerator::destroy();

	return 0;
}
