#include <stdlib.h>
#include <stdio.h>
#include <glpk.h>

int main(int argc,char *argv[]){
  int q[] = {atoi(argv[1]),atoi(argv[2]),atoi(argv[3])};    //queue length
  int n[] = {atoi(argv[4]),atoi(argv[5]),atoi(argv[6])};    //different request number
  int ra[] ={atoi(argv[7]),atoi(argv[8]),atoi(argv[9]),atoi(argv[10]),atoi(argv[11])};  //bandwidth availiable
  glp_prob *mip = glp_create_prob();
  glp_set_prob_name(mip, "sample");
  glp_set_obj_dir(mip, GLP_MAX);

  glp_add_rows(mip, 8);
  glp_set_row_name(mip, 1, "n1");
  if (n[0]==0)
    glp_set_row_bnds(mip, 1, GLP_FX, 0.0, n[0]);
  else
    glp_set_row_bnds(mip, 1, GLP_DB, 0.0, n[0]);
  glp_set_row_name(mip, 2, "n2");
  if (n[1]==0)
    glp_set_row_bnds(mip, 2, GLP_FX, 0.0, n[1]);
  else
    glp_set_row_bnds(mip, 2, GLP_DB, 0.0, n[1]);
  glp_set_row_name(mip, 3, "n3");
  if (n[2]==0)
    glp_set_row_bnds(mip, 3, GLP_FX, 0.0, n[2]);
  else
    glp_set_row_bnds(mip, 3, GLP_DB, 0.0, n[2]);
  glp_set_row_name(mip, 4, "c1");
  glp_set_row_bnds(mip, 4, GLP_DB, 0.0, ra[0]);
  glp_set_row_name(mip, 5, "c2");
  glp_set_row_bnds(mip, 5, GLP_DB, 0.0, ra[1]);
  glp_set_row_name(mip, 6, "c3");
  glp_set_row_bnds(mip, 6, GLP_DB, 0.0, ra[2]);
  glp_set_row_name(mip, 7, "c4");
  glp_set_row_bnds(mip, 7, GLP_DB, 0.0, ra[3]);
  glp_set_row_name(mip, 8, "c5");
  glp_set_row_bnds(mip, 8, GLP_DB, 0.0, ra[4]);

  glp_add_cols(mip, 15);
  glp_set_col_name(mip, 1, "x11");
  glp_set_col_bnds(mip, 1, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 1, q[0]);                           //queue length
  glp_set_col_kind(mip, 1, GLP_IV);

  glp_set_col_name(mip, 2, "x12");
  glp_set_col_bnds(mip, 2, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 2, q[1]);
  glp_set_col_kind(mip, 2, GLP_IV);

  glp_set_col_name(mip, 3, "x13");
  glp_set_col_bnds(mip, 3, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 3, q[2]);
  glp_set_col_kind(mip, 3, GLP_IV);

  glp_set_col_name(mip, 4, "x21");
  glp_set_col_bnds(mip, 4, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 4, q[0]);
  glp_set_col_kind(mip, 4, GLP_IV);

  glp_set_col_name(mip, 5, "x22");
  glp_set_col_bnds(mip, 5, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 5, q[1]);
  glp_set_col_kind(mip, 5, GLP_IV);

  glp_set_col_name(mip, 6, "x23");
  glp_set_col_bnds(mip, 6, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 6, q[2]);
  glp_set_col_kind(mip, 6, GLP_IV);

  glp_set_col_name(mip, 7, "x31");
  glp_set_col_bnds(mip, 7, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 7, q[0]);
  glp_set_col_kind(mip, 7, GLP_IV);

  glp_set_col_name(mip, 8, "x32");
  glp_set_col_bnds(mip, 8, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 8, q[1]);
  glp_set_col_kind(mip, 8, GLP_IV);

  glp_set_col_name(mip, 9, "x33");
  glp_set_col_bnds(mip, 9, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 9, q[2]);
  glp_set_col_kind(mip, 9, GLP_IV);

  glp_set_col_name(mip, 10, "x41");
  glp_set_col_bnds(mip, 10, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 10, q[0]);
  glp_set_col_kind(mip, 10, GLP_IV);

  glp_set_col_name(mip, 11, "x42");
  glp_set_col_bnds(mip, 11, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 11, q[1]);
  glp_set_col_kind(mip, 11, GLP_IV);

  glp_set_col_name(mip, 12, "x43");
  glp_set_col_bnds(mip, 12, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 12, q[2]);
  glp_set_col_kind(mip, 12, GLP_IV);

  glp_set_col_name(mip, 13, "x51");
  glp_set_col_bnds(mip, 13, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 13, q[0]);
  glp_set_col_kind(mip, 13, GLP_IV);

  glp_set_col_name(mip, 14, "x52");
  glp_set_col_bnds(mip, 14, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 14, q[1]);
  glp_set_col_kind(mip, 14, GLP_IV);

  glp_set_col_name(mip, 15, "x53");
  glp_set_col_bnds(mip, 15, GLP_LO, 0, 0);
  glp_set_obj_coef(mip, 15, q[2]);
  glp_set_col_kind(mip, 15, GLP_IV);

  int ia[1+30], ja[1+30];
  double ar[1+30];
  int i=1,j=1,k=1;
  for (i=1;i<4;i++)
    for (j=1;j<6;j++){
      ia[k]=i,ja[k]=(j-1)*3+i,ar[k]=1;
      k++;
    }
  ia[16]=4,ja[16]=1,ar[16]=10;
  ia[17]=4,ja[17]=2,ar[17]=1;
  ia[18]=4,ja[18]=3,ar[18]=0.1;
  ia[19]=5,ja[19]=4,ar[19]=10;
  ia[20]=5,ja[20]=5,ar[20]=1;
  ia[21]=5,ja[21]=6,ar[21]=0.1;
  ia[22]=6,ja[22]=7,ar[22]=10;
  ia[23]=6,ja[23]=8,ar[23]=1;
  ia[24]=6,ja[24]=9,ar[24]=0.1;
  ia[25]=7,ja[25]=10,ar[25]=10;
  ia[26]=7,ja[26]=11,ar[26]=1;
  ia[27]=7,ja[27]=12,ar[27]=0.1;
  ia[28]=8,ja[28]=13,ar[28]=10;
  ia[29]=8,ja[29]=14,ar[29]=1;
  ia[30]=8,ja[30]=15,ar[30]=0.1;
  /*
  for (i=1;i<31;i++){
    printf("%d,%d,%f\n",ia[i],ja[i],ar[i]);
  }
  */

  glp_load_matrix(mip, 30, ia, ja, ar);

  glp_iocp parm;
  glp_init_iocp(&parm);
  parm.presolve = GLP_ON;
  int err = glp_intopt(mip, &parm);


  //glp_simplex(mip, NULL);
  // double t = glp_mip_obj_val(mip);
  int result[15]={0};
  for (i=0;i<15;i++){
    result[i] = glp_mip_col_val(mip, i+1);
  }


  printf("\n");
  //display the result
  for (i=0;i<14;i++){
    printf("%d,",result[i]);
  }
  printf("%d\n",result[14]);

  glp_delete_prob(mip);
  return 0;
}
