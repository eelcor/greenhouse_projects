#include <stdio.h>
#include <iostream>
using namespace std;

const int buflen = 6;

void send_string(char* str, int len)
{
	char buffer[buflen]={0};
	cout << str << "\n\r";
/*	printf("Size of argument string: %i \n\r", sizeof(str));
	printf("Size of argument passed %i \n\r", len);
	printf("Size of buffer is %i \n\r", buflen);
	printf("Amount of whole packets %i \n\r", len/buflen);
	printf("Remainder %i \n\r", len%buflen); */
	int rem = len%buflen;
	int pkt = len/buflen;
	for (int j=0; j<pkt; j++)
	{
		for (int i=0; i<buflen; i++)
		{
			buffer[i]=str[i+j*buflen];
			//cout << i << "\n\r";
		}
		cout << buffer << "\n\r";
	}
	for (int i=0; i<buflen; i++)
	{
		if(i<rem)
		{
			buffer[i]=str[i+pkt*buflen];
		} else
		{
			buffer[i]=0;
		}
	}
	cout << buffer << "\n\r";
}

int main()
{
	char a[] = {'D','i','t',' ','i','s',' ','e','e','n',' ','t','e','s','t','!'};
	cout << a << "\n\r";
	printf("Size of original string: %i \n\r",sizeof(a));
	send_string(a, sizeof(a));
	return 0;
}
