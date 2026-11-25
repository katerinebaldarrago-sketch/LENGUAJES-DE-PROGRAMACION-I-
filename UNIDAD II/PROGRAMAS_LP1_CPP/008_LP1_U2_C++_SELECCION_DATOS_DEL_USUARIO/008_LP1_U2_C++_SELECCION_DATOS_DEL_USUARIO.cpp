#include <iostream>
#include <vector>
#include <algorithm> 

using namespace std;

void selectionSort(vector<int>& arr) {
    int n = arr.size();
    
    for (int i = 0; i < n - 1; i++) {
        
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        
        
        if (minIndex != i) {
            swap(arr[i], arr[minIndex]);
        }
    }
}

int main() {
    int cantidad;
    
    cout << "Cuantos numeros deseas ingresar?: ";
    cin >> cantidad;
   
    vector<int> numeros(cantidad);
    
    cout << "Ingresa los " << cantidad << " numeros :" << endl;
    for (int i = 0; i < cantidad; i++) {
        cout << "Numero [" << i + 1 << "]: ";
        cin >> numeros[i];
    }
    
    cout << "\nVector original: [ ";
    for (int num : numeros) {
        cout << num << " ";
    }
    cout << "]" << endl;
    
    selectionSort(numeros);
    
    cout << "Vector ordenado: [ ";
    for (int num : numeros) {
        cout << num << " ";
    }
    cout << "]" << endl;
    
    return 0;
}