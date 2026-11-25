#include <iostream>
#include <vector>
#include <algorithm> // Necesario para usar swap()

using namespace std;

// Función para ordenar un vector usando Selection Sort
void selectionSort(vector<int>& arr) {
    int n = arr.size();
    
    for (int i = 0; i < n - 1; i++) {
        // Encontrar el índice del elemento mínimo en la porción no ordenada
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        
        // Intercambiar el elemento mínimo encontrado con el primer elemento de la sección no ordenada
        if (minIndex != i) {
            swap(arr[i], arr[minIndex]);
        }
    }
}

// --- Código para probarlo ---
int main() {
    // Datos del ejemplo
    vector<int> numeros = {8, 3, 6, 2, 5};
    
    cout << "Vector original: ";
    for(int num : numeros) cout << num << " ";
    cout << endl;
    
    // Llamamos a la función
    selectionSort(numeros);
    
    cout << "Vector ordenado: ";
    for(int num : numeros) cout << num << " ";
    cout << endl;
    
    return 0;
}