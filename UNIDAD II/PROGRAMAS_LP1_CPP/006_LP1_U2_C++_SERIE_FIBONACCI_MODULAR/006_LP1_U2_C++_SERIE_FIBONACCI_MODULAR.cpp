#include <iostream>
using namespace std;
void Fibonacci(int n);

int main() {
    int n;

    cout << "Ingrese la cantidad de terminos: ";
    cin >> n;

    if (n > 0) {
        Fibonacci(n);
    } else {
        cout << "Por favor, ingrese un numero mayor a 0." << endl;
    }

    return 0;
}

void Fibonacci(int n) {
    int a = 0, b = 1, c;
    int i = 1;

    do {
        if (i == 1) {
            cout << a << " ";
        } else if (i == 2) {
            cout << b << " ";
        } else {
            c = a + b;
            a = b;
            b = c;
            cout << c << " ";
        }
        i++;
    } while (i <= n);

    cout << endl;
}