#include<stdio.h>
#include<iostream>

using namespace std;

int main(){
	cout << "[";
	for(int i=33 ; i<=126; i++){
		printf(" '%c',", i);
	}
	cout << "]";
}