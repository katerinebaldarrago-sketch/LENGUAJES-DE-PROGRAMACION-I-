#include <iostream>
#include <vector>
#include <iomanip>
#include <string>

using namespace std;

// Función auxiliar para imprimir el arreglo de forma bonita
string vectorToString(const vector<int>& v) {
    string s = "[ ";
    for (size_t i = 0; i < v.size(); ++i) {
        s += to_string(v[i]);
        if (i < v.size() - 1) s += ", ";
    }
    s += " ]";
    return s;
}

// Función que ejecuta el método de la burbuja con bandera y muestra la tabla
void ejecutarBurbuja(vector<int> notas, string nombreEscenario) {
    int n = notas.size();
    bool huboCambio;
    int comparacionesTotales = 0;
    int intercambiosTotales = 0;
    int pasadas = 0;

    cout << "\n================================================================" << endl;
    cout << "  ESCENARIO: " << nombreEscenario << endl;
    cout << "  Arreglo Inicial: " << vectorToString(notas) << endl;
    cout << "================================================================" << endl;

    for (int i = 0; i < n - 1; i++) {
        huboCambio = false;
        pasadas++;
        
        // Imprimir cabecera de la pasada
        cout << "\n--- PASADA " << pasadas << " (i = " << i << ") ---" << endl;
        cout << "| J | Comparacion | ¿Cambio? | Arreglo Resultante                 | Interc. Acum. |" << endl;
        cout << "|---|-------------|----------|------------------------------------|---------------|" << endl;

        for (int j = 0; j < n - 1 - i; j++) {
            comparacionesTotales++;
            bool cambioEnEstaComparacion = false;
            string textoComparacion = to_string(notas[j]) + " vs " + to_string(notas[j+1]);
            
            // Condición: Ordenar de MAYOR a MENOR
            if (notas[j] < notas[j + 1]) {
                // Intercambio
                int temp = notas[j];
                notas[j] = notas[j + 1];
                notas[j + 1] = temp;
                huboCambio = true;
                cambioEnEstaComparacion = true;
                intercambiosTotales++;
            }

            // Imprimir fila de la tabla
            cout << "| " << j << " | " << setw(11) << left << textoComparacion 
                 << " | " << (cambioEnEstaComparacion ? "   SI   " : "   NO   ") 
                 << " | " << setw(34) << left << vectorToString(notas) 
                 << " | " << setw(13) << left << intercambiosTotales << " |" << endl;
        }

        cout << "-------------------------------------------------------------------------------------------------" << endl;
        cout << "  Fin de Pasada " << pasadas << ". Arreglo: " << vectorToString(notas) << endl;

        // Verificación de la bandera
        if (!huboCambio) {
            cout << "  [!] BANDERA: No hubo cambios en esta pasada. El arreglo ya esta ordenado." << endl;
            cout << "  [!] El algoritmo se DETIENE aqui para ahorrar trabajo." << endl;
            break;
        } else {
            cout << "  [>] BANDERA: Hubo cambios. Continuamos a la siguiente pasada." << endl;
        }
    }

    // --- CÁLCULOS FINALES ---
    double suma = 0;
    int aprobados = 0;
    for (int nota : notas) {
        suma += nota;
        if (nota >= 11) aprobados++;
    }
    double promedio = suma / n;

    // --- MOSTRAR RESULTADOS ---
    cout << "\n================= RESULTADOS DEL RANKING =================" << endl;
    cout << " Ranking Final (Mayor a Menor): " << vectorToString(notas) << endl;
    cout << " Promedio del salon: " << fixed << setprecision(2) << promedio << endl;
    cout << " Cantidad de aprobados (>= 11): " << aprobados << endl;
    cout << "\n================= METRICAS DE TRABAJO ====================" << endl;
    cout << " Comparaciones totales: " << comparacionesTotales << endl;
    cout << " Intercambios totales : " << intercambiosTotales << endl;
    cout << " Pasadas realizadas   : " << pasadas << endl;
    cout << "==========================================================\n" << endl;
}

int main() {
    // ESCENARIO 1: Caso Base (Desordenado)
    vector<int> notasBase = {12, 17, 9, 15, 20, 11, 14, 8};
    ejecutarBurbuja(notasBase, "CASO BASE (Desordenado)");

    // ESCENARIO 2: Mejor Caso (Ya ordenado de mayor a menor)
    vector<int> notasMejorCaso = {20, 17, 15, 14, 12, 11, 9, 8};
    ejecutarBurbuja(notasMejorCaso, "MEJOR CASO (Ya ordenado)");

    // ESCENARIO 3: Peor Caso (Ordenado al revés: de menor a mayor)
    vector<int> notasPeorCaso = {8, 9, 11, 12, 14, 15, 17, 20};
    ejecutarBurbuja(notasPeorCaso, "PEOR CASO (Al revés)");

    return 0;
}