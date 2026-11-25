#include<iostream>
using namespace std;

int factorial(int n){
	if (n == 0)
		return 1;
	else
		return factorial(n-1) * n;
}

int suma(int n){
	if (n == 0)                     
		return 0;
	else
		return factorial(n) + suma(n-1);   
}

int main ()
{
	int n;
	
	cout << "Ingrese un numero n: " << endl;
	cin >> n;
	
	cout << "La suma de 1! + ... + " << n << "! es : " << suma(n) << endl;
	
	return 0;
}