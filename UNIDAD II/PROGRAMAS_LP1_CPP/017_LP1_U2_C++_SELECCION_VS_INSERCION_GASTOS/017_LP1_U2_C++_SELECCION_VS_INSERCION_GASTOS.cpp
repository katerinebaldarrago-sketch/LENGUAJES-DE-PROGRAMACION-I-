#include <iostream>
#include <vector>
#include <iomanip>
#include <string>

using namespace std;

// Variables globales para contar el trabajo de cada algoritmo
int compSeleccion = 0, intcSeleccion = 0;
int compInsercion = 0, intcInsercion = 0;

// Función auxiliar para imprimir vectores
void imprimirVector(const vector<int>& v) {
    cout << "[ ";
    for (int x : v) cout << x << " ";
    cout << "]";
}

// 1 y 4. ORDENAMIENTO POR SELECCIÓN (Mayor a Menor) + Métricas
vector<int> ordenamientoSeleccion(vector<int> gastos) {
    int n = gastos.size();
    compSeleccion = 0; 
    intcSeleccion = 0;

    cout << "\n--- ORDENAMIENTO POR SELECCION ---" << endl;
    for (int i = 0; i < n - 1; i++) {
        int max_idx = i; // Suponemos que el actual es el máximo
        for (int j = i + 1; j < n; j++) {
            compSeleccion++;
            if (gastos[j] > gastos[max_idx]) { // Buscamos el mayor
                max_idx = j;
            }
        }
        if (max_idx != i) {
            swap(gastos[i], gastos[max_idx]);
            intcSeleccion++;
            cout << "  Pasada " << i+1 << ": Intercambio -> ";
            imprimirVector(gastos);
            cout << endl;
        } else {
            cout << "  Pasada " << i+1 << ": Sin intercambio -> ";
            imprimirVector(gastos);
            cout << endl;
        }
    }
    return gastos;
}

// 4. ORDENAMIENTO POR INSERCIÓN (Mayor a Menor) + Métricas (Para comparar)
void ordenamientoInsercion(vector<int> gastos) {
    int n = gastos.size();
    compInsercion = 0; 
    intcInsercion = 0;
    
    for (int i = 1; i < n; i++) {
        int key = gastos[i];
        int j = i - 1;
        compInsercion++; // Comparación inicial del while
        while (j >= 0 && gastos[j] < key) {
            gastos[j + 1] = gastos[j];
            j--;
            intcInsercion++;
            if (j >= 0) compInsercion++; // Siguiente comparación
        }
        gastos[j + 1] = key;
    }
}

// Función principal para procesar un escenario
void procesarEscenario(vector<int> gastosOriginales, string nombreEscenario) {
    cout << "\n=======================================================" << endl;
    cout << "  ESCENARIO: " << nombreEscenario << endl;
    cout << "  Gastos Originales: "; imprimirVector(gastosOriginales); cout << endl;
    cout << "=======================================================" << endl;

    vector<string> dias = {"Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"};
    
    // 3. Búsqueda Secuencial del gasto más alto en la lista ORIGINAL
    int maxGasto = gastosOriginales[0];
    int posMax = 0;
    for (int i = 1; i < gastosOriginales.size(); i++) {
        if (gastosOriginales[i] > maxGasto) {
            maxGasto = gastosOriginales[i];
            posMax = i;
        }
    }
    cout << "-> Busqueda Secuencial: El gasto mas alto fue " << maxGasto << " el dia " << dias[posMax] << endl;

    // 1. Ordenamiento por Selección
    vector<int> gastosOrdenados = ordenamientoSeleccion(gastosOriginales);
    
    cout << "\nRanking de Gastos (Mayor a Menor): "; imprimirVector(gastosOrdenados); cout << endl;

    // 2. Total, Promedio y días por encima del promedio
    double total = 0;
    for (int g : gastosOriginales) total += g;
    double promedio = total / gastosOriginales.size();
    
    int diasPorEncima = 0;
    for (int g : gastosOriginales) {
        if (g > promedio) diasPorEncima++;
    }

    cout << "\n--- CALCULOS ---" << endl;
    cout << "  Total gastado: S/ " << total << endl;
    cout << "  Promedio diario: S/ " << fixed << setprecision(2) << promedio << endl;
    cout << "  Dias por encima del promedio: " << diasPorEncima << endl;

    // 4. Comparación de métricas
    ordenamientoInsercion(gastosOriginales); // Solo ejecutamos para obtener sus contadores

    cout << "\n--- COMPARACION DE METRICAS ---" << endl;
    cout << "  SELECCION -> Comparaciones: " << compSeleccion << " | Intercambios: " << intcSeleccion << endl;
    cout << "  INSERCION -> Comparaciones: " << compInsercion << " | Intercambios: " << intcInsercion << endl;
    if (compSeleccion < compInsercion) cout << "  * Seleccion hizo menos comparaciones en este escenario." << endl;
    else cout << "  * Insercion hizo menos comparaciones en este escenario." << endl;
}

int main() {
    // Escenario Original
    vector<int> gastos = {12, 5, 20, 8, 15, 3, 10};
    procesarEscenario(gastos, "CASO BASE (Desordenado)");

    // Escenario Extra 1: Ya ordenado (Mayor a menor)
    vector<int> gastosOrdenados = {20, 15, 12, 10, 8, 5, 3};
    procesarEscenario(gastosOrdenados, "ESCENARIO EXTRA 1 (Ya ordenado)");

    // Escenario Extra 2: Invertido (Menor a mayor)
    vector<int> gastosInvertidos = {3, 5, 8, 10, 12, 15, 20};
    procesarEscenario(gastosInvertidos, "ESCENARIO EXTRA 2 (Invertido)");

    return 0;
}