#include <iostream>
using namespace std;

int tabla(int n);

int main() {
    int n;
    cout << "Ingrese el numero del cual desea ver la tabla: " << endl;
    cin >> n;

    int total = tabla(n);

    return 0;
}

int tabla(int n) {
    int i;
    for (int i = 1; i <= ; i++) { 
        cout << n << " * " << i << " = " << n * i << endl;
    }
    return 1;
}