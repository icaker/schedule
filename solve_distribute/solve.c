#include <stdlib.h>
#include <stdio.h>
#include <glpk.h>

int main(int argc,char *argv[]){
  int q[] = {atof(argv[1]),atof(argv[2]),atof(argv[3])};    //queue length
  int n[] = {atoi(argv[4]),atoi(argv[5]),atoi(argv[6])};
  int cmax = atof(argv[7]);    //amount
  glp_prob *mip = glp_create_prob();
  glp_set_prob_name(mip, "sample");
  glp_set_obj_dir(mip, GLP_MAX);

  glp_add_rows(mip, 1);
  glp_set_row_name(mip, 1, "p");
  glp_set_row_bnds(mip, 1, GLP_DB, 0.0, cmax);

  glp_add_cols(mip, 3);
  glp_set_col_name(mip, 1, "x1");
  if (n[0]==0)
    glp_set_col_bnds(mip, 1, GLP_FX, 0, 0);
  else
    glp_set_col_bnds(mip, 1, GLP_DB, 0, n[0]);
  glp_set_obj_coef(mip, 1, q[0]);
  glp_set_col_kind(mip, 1, GLP_IV);

  glp_set_col_name(mip, 2, "x2");
  if (n[1]==0)
    glp_set_col_bnds(mip, 2, GLP_FX, 0, 0);
  else
    glp_set_col_bnds(mip, 2, GLP_DB, 0, n[1]);
  glp_set_obj_coef(mip, 2, q[1]);
  glp_set_col_kind(mip, 2, GLP_IV);

  glp_set_col_name(mip, 3, "x3");
  if (n[2]==0)
    glp_set_col_bnds(mip, 3, GLP_FX, 0, 0);
  else
    glp_set_col_bnds(mip, 3, GLP_DB, 0, n[2]);
  glp_set_obj_coef(mip, 3, q[2]);
  glp_set_col_kind(mip, 3, GLP_IV);


  int ia[1+3], ja[1+3];
  double ar[1+3];
  ia[1]=1,ja[1]=1,ar[1]=10;   // a[1,1] = 10
  ia[2]=1,ja[2]=2,ar[2]=1;    // a[1,2] = 1
  ia[3]=1,ja[3]=3,ar[3]=0.1;    // a[1,3] = 0.1

  glp_load_matrix(mip, 3, ia, ja, ar);

  glp_iocp parm;
  glp_init_iocp(&parm);
  parm.presolve = GLP_ON;
  int err = glp_intopt(mip, &parm);


  //glp_simplex(mip, NULL);
  //double t = glp_mip_obj_val(mip);
  int x = glp_mip_col_val(mip, 1);
  int y = glp_mip_col_val(mip, 2);
  int z = glp_mip_col_val(mip, 3);

  printf("%d,%d,%d\n", x, y, z);

  glp_delete_prob(mip);
  return 0;
}
