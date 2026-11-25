#include<iostream>
using namespace std;

int suma(int n){
	if (n == 0)                
		return 0;
	else
		return suma(n-1) + n;  
}

int main ()
{
	int n;
	
	cout << "Ingrese un numero n: " << endl;
	cin >> n;
	
	cout << "La suma de 1 a " << n << " es : " << suma(n) << endl;
	return 0;