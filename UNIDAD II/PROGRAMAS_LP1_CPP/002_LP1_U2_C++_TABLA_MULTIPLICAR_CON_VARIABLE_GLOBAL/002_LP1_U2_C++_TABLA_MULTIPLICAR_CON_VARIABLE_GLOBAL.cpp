#include <iostream>
using namespace std;

//variable global 
int n; 

//prototipo de la funcion 
void mostrarTabla(int);

int main(){
    cout << "Ingrese un numero (1 al 9) ";
    cin >> n; 
    cout << "\nTabla de multiplicar del : " << n << "\n";
    mostrarTabla(n);
    return 0;
}

//funcion que muestra la tabla de multiplicar 
void mostrarTabla(int n){
    int i; // Variable Local 
    for (i = 1; i <= 10; i++)   
    {
        cout << n << " * " << i << " = " << n*i << endl;
    }
}