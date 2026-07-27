#include <stdio.h>
#include <time.h>

void delay(int number_of_seconds)
{
	// Converting time into milli_seconds
	int milli_seconds = 1000 * number_of_seconds;

	// Storing start time
	clock_t start_time = clock();

	// looping till required time is not achieved
	while (clock() < start_time + milli_seconds)
		;
}

void program1(){
    printf("program1");
}

void program2(){
    printf("program2");
    program1();
}



int main(){
    program1();   
    program2();  
    return 1;
}