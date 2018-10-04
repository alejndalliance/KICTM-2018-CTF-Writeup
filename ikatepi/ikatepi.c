//
// We managed to hack the server and retrieve partial source code for the service
// running at port 11111. Use this to your advantage ;)
//


#include <stdio.h>
#include <unistd.h>
#include <string.h>

char* password = "xxxxx[data_lost]xxxxx";
char input[100] = {0};

int main()
{
	int i, len, flag=1;
	printf("KICTM2018\nPassword: ");
	scanf("%s", input);

	len = strlen(input);

	for(i = 0;i < len;i++)
	{
		if (password[i] != input[i])
		{
			//added delay to prevent brute force attack. I am smart ok !!!
			sleep(3);
			flag=0;
		}
	}

	if(flag && len==strlen(password))
	{
		printf("The flag is xxxxx[data_lost]xxxxx :) \n");
	}
	else
	{
		printf("xxxxx[data_lost]xxxxx \n");
	}

	return 0;
}

