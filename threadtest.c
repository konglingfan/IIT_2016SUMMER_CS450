#include "types.h"
#include "user.h"
#include "syscall.h"


int test=0;
int mtxid;


//Test file
//4 threads to counts
void mythread(void* argv);

int main(int argc, char *argv[])
{
  void *stack1,*stack2,*stack3,*stack4;
  void *stack;
  int result;

  mtxid=mtx_create(0);
  
  stack1=malloc(4096);
  stack2=malloc(4096);
  stack3=malloc(4096);
  stack4=malloc(4096);
  
  memset(stack1,0,4096);
  memset(stack2,0,4096);
  memset(stack3,0,4096);
  memset(stack4,0,4096);
  
  result=thread_create(mythread,stack1,(void*)1);
  printf(1,"thread %d created\n",result);
  result=thread_create(mythread,stack2,(void*)2);
  printf(1,"thread %d created\n",result);
  result=thread_create(mythread,stack3,(void*)3);
  printf(1,"thread %d created\n",result);
  result=thread_create(mythread,stack4,(void*)4);
  printf(1,"thread %d created\n",result);
  

  
  result=thread_join(&stack);
  free(stack);
  printf(1,"thread %d exited\n",result);
  result=thread_join(&stack);
  free(stack);
  printf(1,"thread %d exited\n",result);
  result=thread_join(&stack);
  free(stack);
  printf(1,"thread %d exited\n",result);
  result=thread_join(&stack);
  free(stack);
  printf(1,"thread %d exited\n",result);

  printf(1,"Final result : Test = %d\n",test);
  exit();
  return 0;
}

void mythread(void* argv)
{
  int i;
  printf(1,"Thread %d start",(int)argv);
  for(i=0;i<1000;i++){
    mtx_lock(mtxid);
    test+=1;
    mtx_unlock(mtxid);
  }
  printf(1,"Thread %d count: %d\n",(int)argv,test);
  exit();
  return;
}
