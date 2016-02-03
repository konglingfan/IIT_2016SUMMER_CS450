#include "types.h"
#include "user.h"
#include "syscall.h"

unsigned short lfsr = 0xACE1u;
unsigned bit;

unsigned rand() {
	bit  = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) ) & 1;
	return lfsr =  (lfsr >> 1) | (bit << 15);
}

int main(int argc, char *argv[])
{
	int process_count;
	int pid = -1;
	
	for (process_count = 0; process_count <= 2; process_count++) {
		pid = fork();
	}
	
	if (pid == 0) { // Children execute the test
		int i, j, garbage;
		
		for (i = 0; i < 10; i++) {
			int rand_num = rand() * (100 * getpid());
			garbage = 0;
			
			for (j = 0; j < rand_num; j++) {
				garbage += 1;
			}
			
			sleep(0);
		}
		
		printf(1, "Process %d bursts: ", getpid());
		print_bursts();
	}
	else {
		while (wait() != -1);
	}
	
  exit();
}
