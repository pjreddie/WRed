

#define DEBUG
#ifdef DEBUG
#  define debug(a,b,c,d) printf(a,b,c,d)
#  define assert(x) if(!(x)) printf("\n Assert failed in line %d \n", __LINE__)
#else
#  define debug(a,b,c,d)
#  define assert(x) 
#endif

#define TRUE 1
#define FALSE 0
#define LINELEN 88

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

#ifdef __TURBOC__
#  define STDOUT "CON"
#  include "c:\numrec\nr.h"
#  include "c:\numrec\nrutil.h"
#  include <alloc.h>
#  define STD_LIB_PROT 1
   void dummy() {float t; sscanf("1.234","%f",&t);} /* to get float libs in */
#  define COMMENT_CHAR '#'
#  define TOP_TITLE_STR "title"
#  define strcasecmp stricmp
void add_history(char * s) {}
char * readline(char * prompt){
        char * p;
        if ((p = malloc(40)) == NULL) 
                nrerror ("Internal malloc error in readline");
        else{
                printf(prompt);
                gets(p);
        }
}
#elif defined(vax)
#  define STDOUT "SYS$OUTPUT"
#  include "sys$dlog:[numrec]nrutil.h"
#  include "sys$dlog:[numrec]nr.h"
#  define COMMENT_CHAR '('
#  define TOP_TITLE_STR "title"
#else  /* Unix?? */
#  define STDOUT "/dev/tty"
#  include <nrutil.h>
#  include <nr.h>
#  define COMMENT_CHAR '#'
#  define TOP_TITLE_STR "title"
#endif
#ifdef __STDC__
# define STD_LIB_PROT 1
# define VOID void
#else
# if !(defined(__TURBOC__) || defined(MIPSEL))
#  define void
#  define VOID int
# else
#  define VOID void
# endif
#endif

#ifdef STD_LIB_PROT
#   include <stdlib.h>
#endif
#include <alloca.h>

static float **covar, **alpha, chisq, alamda = -1;
#include <setjmp.h>
jmp_buf jmpbuf;

#define NRICH 10
float **d;

char datafilename[80]="No file defined initially";
float xmin=1e30, xmax=-1e30, xspan=0;

char * readline(char * prompt);
VOID add_history(char * line);
VOID booboo(char *f, char *s);
VOID report_memory_error_and_abort (void); 
VOID usage(void);
VOID botched_line(char * line);
float bsol(float temp, float * p);
float brill(float j, float x);
float fnc(float temp, float * p);
float chito2(float * p);
float bfun(float x, float t, float * p);
float deriv(float x, float p[], int n);
float pklzbrent(float (*func)(float, float, float *),
                float x1, float x2, float tol, float t, float *p);
VOID dump(void);
VOID fitit(void);
VOID data(void);
VOID parm(void);
VOID myfix(void);
VOID help(void);
VOID fileit(void);
VOID plotit(void);
VOID stop(void);


struct comm {   
        char cmdn[5]; 
        VOID (*cmdf)(void); 
} comm[] = { 
  {"fit",  fitit},
  {"data", data},
  {"parm", parm},
  {"fix",  myfix},
  {"help", help},
  {"file", fileit},
  {"plot", plotit},
  {"quit", stop},
  {"stop", stop}};
#define NCMD (sizeof (comm)/sizeof (struct comm))

#define DUMMY_zero 0.0
#define TnNum 1
#define JtNum 2
#define NfNum 3
#define BkNum 4
#define Tn (p[TnNum])
#define Jt (p[JtNum])
#define Nf (p[NfNum])
#define Bk (p[BkNum])
#define TnErr (sqrt(covar[TnNum][TnNum]))
#define JtErr (sqrt(covar[JtNum][JtNum]))
#define NfErr (sqrt(covar[NfNum][NfNum]))
#define BkErr (sqrt(covar[BkNum][BkNum]))
char * ParStr[]={"DUMMY", "Tn", "Jt", "Nf", "Bk"};
float pars[]={ DUMMY_zero,              /* parameters */
   60.,                         /* Tn */
   2.5,                         /* j  */
  8.25,                         /* Norm */
  .32};                         /* background */
#define NPAR ((sizeof(pars))/(sizeof(float)) - 1)
static int lista[NPAR+1], nparfit=NPAR;
char * Stars="*******************************************************************";

#define NPTS npoints
#define DATASIZE 200
float pointt[DATASIZE],pointy[DATASIZE],pointdy[DATASIZE];
int npoints=0;

#define NITER 100

static float sqrarg;
#define SQR(a) (sqrarg=(a),sqrarg*sqrarg)
#define max(a,b) (a>b?a:b)
#define min(a,b) (a<b?a:b)
char * xmalloc (int bytes){
  char *temp = (char *)malloc (bytes);

  if (!temp)
    report_memory_error_and_abort ();
  return (temp);
}

char * xrealloc (char *pointer, int bytes){
  char *temp;

  if (!pointer)
    temp = (char *)malloc (bytes);
  else
    temp = (char *)realloc (pointer, bytes);

  if (!temp)
    report_memory_error_and_abort ();
  return (temp);
}
void report_memory_error_and_abort ()
{
  fprintf (stderr, "history: Out of virtual memory!\n");
  abort ();
}


int Intensity = TRUE;
VOID main(argc, argv){
  char * resp, *p;
  int i,j;

  printf("Brilsolve, $Revision: 1.13 $\n\n");
  if (argc > 1) {
    Intensity = FALSE;
    printf("This program fits the mean field magnetization (square root of\n");
    printf("the neutron peak intensity) as a function of the temperature: \n");
    printf("M(Tn,J)*Nf+Bk. Type \"help\" for short writeup\n");
  } else {
    printf("This program fits the magnetic neutron diffraction peak intensity\n");
    printf("(squared mean field magnetization) as a function of the temperature:\n");
    printf("(M(Tn,J)^2)*Nf+Bk. Type \"help\" for short writeup\n");
  }
  
  for (i=1; i<=NPAR; i++){
          lista[i] = i;
  };
  covar = matrix(1,NPAR,1,NPAR); /* freed at program exit */
  setjmp(jmpbuf);
  while(1){
         p = readline("? ");
         if((resp = strtok(p," \t")) != NULL){
           /* \verb.resp. = first non-whitespace char; NUL put after string */
           for (i=0; i<NCMD; i++){
             if(!strcasecmp(comm[i].cmdn,resp)) {
               comm[i].cmdf();
               break;
             }
           }
           printf("\n");
           if (i==NCMD) printf("Beg pardon?\n");
         }
         free(p);
     ;
  }
}void nrerror(char * error_text){
        fprintf(stderr,"Numerical Recipes run-time error...\n");
        fprintf(stderr,"%s\n",error_text);
        fprintf(stderr,"...returning (without deallocation)...\n");
        longjmp(jmpbuf,1);
}float bsol(float temp, float * p){
  float t=4.0*(Jt/(Jt+1))*Tn/temp; 
  return (((Tn<=0) || (Jt<=0) || (temp >= Tn)) ? 
              0.0 :
              pklzbrent(bfun,0,t,1e-6,temp,p));
}float bfun(float x, float t, float * p){
        if(x==0) return -1.0;   /* so that it wont find solution at zero */
        /* let's do it for a change the straight way */
        return (x-3*brill(Jt,x)*(Jt/(Jt+1))*(Tn/t));
}float brill(float j, float x)
{
        float temp;
        temp=(2*j+1)/2/j;
        return (x==0? 0 :temp/tanh((double)temp*x)-1/tanh((double)x/2/j)/2/j);
}
void 
fitit(void)
{
  float fret, chisqold=0, * p=pars; 
  int iter=0,i,j;
  float funcs(float x, float a[], float * y, float dyda[], int na);
  int icurfmax; 
  float curfmax = -1, delta;    /* \verb.curfmax. set to guard value */

  alpha = matrix(1,NPAR,1,NPAR);
  d = matrix(0,NRICH,0,NRICH);;
  alamda = -1;                  /* for the initial call to \verb.mrqmin. */
  
    do{
      mrqmin(pointt, pointy, pointdy, NPTS, pars, NPAR, lista, nparfit, covar, 
             alpha, &chisq, funcs, (float *)&alamda);
      
        if((curfmax < 0) || ((icurfmax=(60.0 * chisq/curfmax)) <= 4)){
          curfmax  = chisq;
          icurfmax = 60.0;
        }
        if (! (icurfmax <= 60)) icurfmax=0;
        fprintf(stderr, "\r%.*s %4.4f%*.c\r", 
                          icurfmax, Stars, chisq, 70-icurfmax,' ');
      ;
      if (iter++ > NITER){
        printf("More than %d iterations; giving up.\n", NITER);
        break;
      }
      delta = chisqold-chisq;
      chisqold = chisq;           /* store it for comparison */
      
          if (   ( (delta > 0) && (delta < max (0.1, 0.001 * chisq)) ) 
              || (alamda > 1e5))
            break;
      ;
    } while (1);
  ;
  alamda = 0;                   /* for the final covariance calculation */
  mrqmin(pointt, pointy, pointdy, NPTS, pars, NPAR, lista, nparfit, covar, 
            alpha, &chisq, funcs, (float *)&alamda);
  printf("\nAfter %d iterations got to chisq=%f\n",
         iter, chisq);
  printf("Tn=%g+-%.2g Jt=%g+-%.2g Nf=%g+-%.2g Bk=%g+-%.2g\n",
         Tn,TnErr, Jt,JtErr, Nf,NfErr, Bk,BkErr);
  free_matrix(alpha,1,NPAR,1,NPAR);
  free_matrix(d,0,NRICH,0,NRICH);;
}float funcs(float x, float p[], float * y, float dyda[], int na){
  int i; 

  assert(na==4);   /* na is always 4 */
/*   brute force approach is to
 *   for (i=1; i<=2; i++){
 *     dyda[i] = deriv(x,p,i);
 *       }
 *   *y = fnc(x,p);
 */
   dyda[TnNum] = deriv(x,p,TnNum);  dyda[JtNum] = deriv(x,p,JtNum);
   *y = fnc(x,p);
   dyda[NfNum] = (*y - Bk)/Nf;
   dyda[BkNum] = 1;
}
float fnc(float t, float * p){
  if (Intensity)
     return Bk+Nf*SQR(brill(Jt,bsol(t,p)));
  else
     return Bk+Nf*brill(Jt,bsol(t,p));
}
float deriv(float x, float p[], int n){
    int i, j;
    float q,deriv_val,deriv_old;
    float h=max(p[n],1)/100;
    float pp[5];

    for (i = 1; i <= NRICH; ++i) {
        for(j=1; j<=4; j++){ /* prepare 'perturbed' parameter vector */
            pp[j] = p[j] + ((j==n) ? h : 0);
        }       
        d[i][1] = (fnc(x,pp) - fnc(x,p)) / (2.0*h);
        q = 4.0;
        for (j = 1; j <= i-1 ; ++j) {
            d[i][j + 1] = d[i][j] + (d[i][j] - d[i-1][j]) / (q - 1.0);
            q *= 4.0;
        }
        h /= 2.0;
    }
    deriv_val=d[NRICH][NRICH];
    
    if (fabs(deriv_val-d[NRICH-1][NRICH-1]) > max(1,deriv_val)/1000){
        Stars[n] = '-'; /* problem parameter displayed */
/*      printf("Poor convergence of param. %d's derivative; h/(2^%d)=%f\n",
                n,NRICH,h);
 */
        /* calculate derivative by up to 10 iterations of a naive 
           single-sided difference with decreasing step */
        h=max(p[n],1)/100;
        deriv_old=0;
        for(i=1; i<=10; h /= 5, deriv_old = deriv_val, i++){
          for(j=1; j<=4; j++){ /* prepare 'perturbed' parameter vector */
            pp[j] = p[j] + ((j==n) ? h : 0);
          }
          deriv_val = (fnc(x,pp) - fnc(x,p))/h;
          if (fabs(deriv_val-deriv_old) > max(1,deriv_val)/1000) 
                return deriv_val;
        }
    } else {
        Stars[n] = '*'; /* problem parameter display cancelled */
/*      printf("Good convergence of param. %d's derivative; h/(2^%d)=%f\n",
                n,NRICH,h);         
 */
    }
    return deriv_val;
}
void data(void){
#define BL 80
  char buf[BL], * p;
  FILE * fp;
  float x,y,dy;
  int n;
  add_history(p = readline("filename: "));
  if((fp=fopen(p,"r"))==NULL){ 
    printf("cannot open %s",p);
  }else{
    strcpy(datafilename, p);
    npoints=0;
    while (NULL != fgets(buf,BL,fp)){
      n=sscanf(buf," %f %f %f ",&x,&y,&dy);
      if((n==3) || (n==2)){
        /* perhaps printf(..., x,y,dy);  here */
        pointt[++npoints]=x;
        xmin = min(xmin, pointt[npoints]);
        xmax = max(xmax, pointt[npoints]);
        pointy[npoints]=y;
        pointdy[npoints] = (n==3)? dy : sqrt(y);
        if (pointdy[npoints] == 0) {
          pointdy[npoints] = 1;
          printf("zero error on point %d (x=%f, y=%f); changed to +-1\n", npoints, x, y);
        }
        if (npoints>=(DATASIZE-1)) {
          printf("no more room (only %d points allowed)\n",DATASIZE);break;
        }
      } else {  printf ( "botched line\n");
      }
    }
  }
  xspan = xmax-xmin; xmin -= 0.1*xspan; xmax += 0.1*xspan;
  xmin = max(0,xmin);
  xspan = xmax-xmin;    
  if (npoints == 0) printf (" Didn't find any points in this file\n");
  free(p);
}
void parm(void){ 
  float *p=pars;
  char * buf;
  char name[10];
  int param;
  float value;
  while(1){
    printf("Tn=%g  Jt=%g  Nf=%g  Bk=%g'\n",Tn,Jt,Nf,Bk);
    buf = readline("Input name and value:  ");
    if (strlen(buf) == 0) return;
    if (2 != sscanf(buf," %s %f",name,&value)){
        printf("\nBeg Pardon?\n");
    }else{
        add_history(buf);
        free(buf);
        if (param=param_no(name)){
                p[param]=value;
        }else{
                printf("\nBeg Pardon?\n");
        }
    }
  }
}
int param_no(char * name){
            if(isupper(*name)) *name = tolower(*name);
            switch (*name){
            case 't': return TnNum;
            case 'j': return JtNum;
            case 'n': return NfNum;
            case 'b': return BkNum;
            default : printf("\nNo such parameter: %s",name);
                      return 0;
            }
}
void stop(void){  exit(1); }
void help(void){ 
  printf("Commands are DATA, PARM, FIX, FIT, FILE, PLOT, HELP and STOP/QUIT.\n");
  printf("On UNIX systems, you can use Emacs-style commands to correct errors in\n");
  printf("the input; moreover Ctrl-N/Ctrl-P bring back previous input lines.\n");
  printf("Use DATA to input measurement data file (3 values per line:\n");
  printf("temperature, intensity and its error; or 2 values, the error is\n");
  printf("calculated as a square root of intensity), PARM sets parameters;\n");
  printf("FIX parameters to their initial values during the fit. When ready, you\n");
  printf("FIT, put results in disk FILE, PLOT, reFIT and STOP/QUIT when done\n");
  printf("Other combinations might give interesting results:\n");
  printf("e.g. FILE w/o fit outputs data for chosen parameter values.\n\n");
  printf("This program will normally fit the square of magnetization\n");
  printf("use the option `-m' to fit the magnetization\n");
}
char plotfnbuf[85];
void fileit(void){ 
  FILE * fp;
  int j;
  float tt, *p = pars;
  char buf[80];

  printf("filename: ");
  gets(buf);
  if (strlen(buf) == 0) {
        strcpy(buf, datafilename);
        strcat(buf, ".fit");
  }
  if((fp=fopen(buf,"w")) == NULL) booboo("cannot open %s\n",buf);
  
    fprintf(fp,"%c Tn=%g+-%.2g Jt=%g+-%.2g Nf=%g+-%.2g Bk=%g+-%.2g\n",
          COMMENT_CHAR, Tn,TnErr, Jt,JtErr, Nf,NfErr, Bk,BkErr);
    fprintf(fp,"%c Fit to data from file %s\n", COMMENT_CHAR, datafilename);
    for(j=1; j<100; j++){
      tt=xmin+(float)j/100.0*xspan;
      fprintf(fp,"%f  %f\n",tt,fnc(tt,p));
    }
  ;
  fclose (fp);
  strcpy(plotfnbuf, buf);
  strcat(plotfnbuf, ".plot");
  if((fp=fopen(plotfnbuf,"w")) == NULL) booboo("cannot open %s\n",plotfnbuf);
  
  fprintf(fp,
   "set title \"File %s: Tn=%g+-%.2g Jt=%g+-%.2g Nf=%g+-%.2g Bk=%g+-%.2g\"\n",
    datafilename, Tn,TnErr, Jt,JtErr, Nf,NfErr, Bk,BkErr);
  fprintf(fp,"plot \"%s\" with errorbars, \"%s\" with lines\n",datafilename,buf);
  ;
  fclose (fp);
}

FILE * gnuplot = NULL;
void plotit(void){ 
  fileit();
  if (gnuplot == NULL) {
    gnuplot = popen("gnuplot","w");
  }
  fprintf(gnuplot,"load '%s'\n",plotfnbuf);
  fflush(gnuplot);
}    
void myfix(void){
  char buf[80];
  float value;
  int i,j, mfit;
  static char fixedp[NPAR+1];
  while (1){
    printf("\nFixed? ");
    for (i=1;i<=NPAR;i++){
      printf("%s: %s  ", ParStr[i], (fixedp[i]==1) ? "Yes" : "No ");
    }
    printf("\nFix/release parameter: ");
    gets(buf);
    if (strlen(buf) == 0) break;
    i = param_no(buf);
    if (i>0){
      fixedp[i] ^= 1;           /* flip it */
    }
  }
  mfit=NPAR;
  for (i=1;i<=NPAR;i++){
    if (fixedp[i] == 1){        /* if this par is fixed */
      lista[mfit] = i;  /* put the param number at the end of \verb.lista.*/
      mfit--;                   /* decrease no of free params */
    }else{
      lista[mfit - NPAR + i]=i; /* put param \verb.i. at the left */
    }
  }
  nparfit=mfit;
}

#define ITMAX 100
#define EPS 3.0e-8
float pklzbrent(float (*func)(float, float, float *),
                float x1,float x2,float tol,float t,float * pars)
{
        int iter;
        float a=x1,b=x2,c,d,e,min1,min2;
        float fa=(*func)(a,t,pars),fb=(*func)(b,t,pars),fc,p,q,r,s,tol1,xm;
        if (fb*fa > 0.0) {
                printf("ZBRENT -- (f(%g)=%g * f(%g)=%g) = %g\n",
                                      a,fa,b,fb,fb*fa);
                nrerror("Root must be bracketed in ZBRENT");
        }
        fc=fb;
        for (iter=1;iter<=ITMAX;iter++) {
                if (fb*fc > 0.0) {
                        c=a;
                        fc=fa;
                        e=d=b-a;
                }
                if (fabs(fc) < fabs(fb)) {
                        a=b;
                        b=c;
                        c=a;
                        fa=fb;
                        fb=fc;
                        fc=fa;
                }
                tol1=2.0*EPS*fabs(b)+0.5*tol;
                xm=0.5*(c-b);
                if (fabs(xm) <= tol1 || fb == 0.0) return b;
                if (fabs(e) >= tol1 && fabs(fa) > fabs(fb)) {
                        s=fb/fa;
                        if (a == c) {
                                p=2.0*xm*s;
                                q=1.0-s;
                        } else {
                                q=fa/fc;
                                r=fb/fc;
                                p=s*(2.0*xm*q*(q-r)-(b-a)*(r-1.0));
                                q=(q-1.0)*(r-1.0)*(s-1.0);
                        }
                        if (p > 0.0)  q = -q;
                        p=fabs(p);
                        min1=3.0*xm*q-fabs(tol1*q);
                        min2=fabs(e*q);
                        if (2.0*p < (min1 < min2 ? min1 : min2)) {
                                e=d;
                                d=p/q;
                        } else {
                                d=xm;
                                e=d;
                        }
                } else {
                        d=xm;
                        e=d;
                }
                a=b;
                fa=fb;
                if (fabs(d) > tol1)
                        b += d;
                else
                        b += (xm > 0.0 ? fabs(tol1) : -fabs(tol1));
                fb=(*func)(b,t,pars);
        }
        nrerror("Maximum number of iterations exceeded in ZBRENT");
}
#undef ITMAX
#undef EPS
void booboo(char *f, char *s){
  fprintf(stderr,f,s);
  fprintf(stderr,"\nReturning to the main loop\n");
  longjmp(jmpbuf,1);
}

void
usage(void){
  fprintf(stderr,"Usage: BrilSolv [-h] filename\n");
}
