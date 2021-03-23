#include<bits/stdc++.h>
using namespace std;

int main(){
	unsigned char encrypted_flag[20];
	encrypted_flag[0] = 'A';
	encrypted_flag[1] = ']';
	encrypted_flag[2] = 'K';
	encrypted_flag[3] = 'r';
	encrypted_flag[4] = '=';
	encrypted_flag[5] = '9';
	encrypted_flag[6] = 'k';
	encrypted_flag[7] = '0';
	encrypted_flag[8] = '=';
	encrypted_flag[9] = '0';
	encrypted_flag[10] = 'o';
	encrypted_flag[11] = '0';
	encrypted_flag[12] = ';';
	encrypted_flag[13] = 'k';
	encrypted_flag[14] = '1';
	encrypted_flag[15] = '?';
	encrypted_flag[16] = 'k';
	encrypted_flag[17] = '8';
	encrypted_flag[18] = '1';
	encrypted_flag[19] = 't';

	for(int i=0; i< 20; i++){
		int index = int(encrypted_flag[i]);
		printf("%c", index^9);
	}
	cout << endl;
}