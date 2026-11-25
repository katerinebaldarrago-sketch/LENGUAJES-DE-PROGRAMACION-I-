#include <iostream>
#include <vector>

using namespace std;

int main (){
	int n, i, valor, indice = -1, iteracion = 0;
	int arreglo[100];
	
	cout << "Ingrese la cantidad de elementos del arreglo: ";
	cin >> n; 
	
	cout << "Ingreso de valores: " << endl; 
	
    for (i = 0; i < n; i++) {
        cout << "Elemento [" << i << "]: ";
        cin >> arreglo[i];
        }
	
	cout << "Arreglo : " << endl;
	cout <<  "[ "; 
	
    for (i = 0; i < n; i++) {
        cout << arreglo[i] << " ";
    }
    
	cout << "]" << endl;
	
	cout << "Que valor desea buscar? ";
    cin >> valor;
    

    for (i = 0; i < n; i++) {
        iteracion++;                
        if (arreglo[i] == valor) {
            indice = i;
            break;              
        }
    }
	
    if (indice != -1) {
        cout << "Valor buscado: " << valor << endl;
        cout << "Indice: " << indice << endl;
        cout << "Iteracion: " << iteracion << endl;
        cout << "Contenido:  arreglo[" << indice << "] = " << arreglo[indice] << endl;
    } else {
        cout << "El valor " << valor << " NO se encontro en el arreglo"<<endl;
    }

    return 0;
	
}