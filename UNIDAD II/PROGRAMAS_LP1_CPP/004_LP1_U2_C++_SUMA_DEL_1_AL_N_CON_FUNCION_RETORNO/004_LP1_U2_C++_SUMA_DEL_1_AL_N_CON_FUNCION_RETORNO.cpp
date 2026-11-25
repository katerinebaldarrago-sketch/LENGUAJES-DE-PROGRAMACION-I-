#include <iostream>
using namespace std;

int calcularSuma(int n);

int main() {
    int total = calcularSuma(10);
    cout << "La suma total del 1 al 10 es : " << total << endl;

    return 0;
}

int calcularSuma(int n) {
    int suma = 0, i;
    for (int i = 1; i <= n; i++){
    	cout << i <<endl;
        suma += i;
	}
    return suma;
}