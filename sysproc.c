#include "types.h"
#include "x86.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "mmu.h"
#include "proc.h"

int
sys_fork(void)
{
  return fork();
}

int
sys_exit(void)
{
  exit();
  return 0;  // not reached
}

int
sys_wait(void)
{
  return wait();
}

int
sys_kill(void)
{
  int pid;

  if(argint(0, &pid) < 0)
    return -1;
  return kill(pid);
}

int
sys_getpid(void)
{
  return proc->pid;
}

int
sys_sbrk(void)
{
  int addr;
  int n;

  if(argint(0, &n) < 0)
    return -1;
  addr = proc->sz;
  if(growproc(n) < 0)
    return -1;
  return addr;
}

int
sys_sleep(void)
{
  int n;
  uint ticks0;
  
  if(argint(0, &n) < 0)
    return -1;
  acquire(&tickslock);
  ticks0 = ticks;
  while(ticks - ticks0 < n){
    if(proc->killed){
      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
  }
  release(&tickslock);
  return 0;
}

// return how many clock tick interrupts have occurred
// since start.
int
sys_uptime(void)
{
  uint xticks;
  
  acquire(&tickslock);
  xticks = ticks;
  release(&tickslock);
  return xticks;
}

//system call start_burst
int
sys_start_burst(void)
{
  
  
  acquire(&tickslock);
  //cprintf("start burst pid %d: %d\n",proc->pid,ticks);
  if(proc->burst>=BURSTS)
  {
    proc->burst=0;
  }
  proc->bursts[proc->burst]=ticks;
  release(&tickslock);
  return 0;
}

//system call end_burst
int
sys_end_burst(void)
{
  //cprintf("end burst\n");
  acquire(&tickslock);
  //printf("end burst pid %d: %d\n",proc->pid,ticks);
  proc->bursts[proc->burst]=ticks-
    proc->bursts[proc->burst];
  if(proc->bursts[proc->burst]==0)
  {
    proc->bursts[proc->burst]=-1;
  }
  else	proc->burst++;
  release(&tickslock);
  return 0;
}

//system call print_bursts
int
sys_print_bursts(void)
{
  int i=0;
  //cprintf("print bursts\n");
  for(i=0;i<100;i++)
  {
    if(proc->bursts[i]!=-1)
    {
      if(i!=0) cprintf(", ");
      cprintf("%d",proc->bursts[i]);
    }
    else
    {
      break;
    }     
  }
  cprintf(", turnaround time: %d \n",ticks-proc->start_ticks);
  return 0;
}

int
sys_thread_create(void)
{
  int tmain,stack,arg;	//use int to get address of args.
  argint(0,&tmain);
  argint(1,&stack);
  argint(2,&arg);

  //cast to void pointer
  return thread_create((void*)tmain,(void*)stack,(void*)arg);
}

int
sys_thread_exit(void)
{
  thread_exit();
  return 0;
}

int
sys_thread_join(void)
{
  int stack;
  argint(0,&stack);

  return thread_join((void**)stack);
}

int
sys_mtx_create(void)
{
  int state;
  argint(0,&state);

  return mtx_create(state);
}

int
sys_mtx_lock(void)
{
  int id;
  argint(0,&id);

  return mtx_lock(id);
}

int
sys_mtx_unlock(void)
{
  int id;
  argint(0,&id);

  return mtx_unlock(id);
}
