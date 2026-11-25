#include<iostream>
using namespace std;

int factorial(int n){    
	if (n == 0)
		return 1;
	else
		return factorial(n-1)*n;
}

int main ()
{
	int n;
	
	cout << "Ingrese un numero entero y positivo n: " << endl;   
	cin >> n;
	
	cout << "El factorial de " << n << " es : " << factorial(n) << endl;  
	return 0;                  
}
