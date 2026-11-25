#include <iostream>
#include <vector>
using namespace std;

// ---------- Utilidades ----------
void mostrar(const vector<int> &v) {
    cout << "[";
    for (size_t k = 0; k < v.size(); k++) {
        cout << v[k];
        if (k + 1 < v.size()) cout << ", ";
    }
    cout << "]";
}

void intercambiar(int &a, int &b) {
    int aux = a;
    a = b;
    b = aux;
}

vector<int> ingresarDatos() {
    int n;
    do {
        cout << "Cantidad de valores (minimo 2): ";
        cin >> n;
    } while (n < 2);
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cout << "  Valor [" << i << "]: ";
        cin >> v[i];
    }
    return v;
}

// ---------- 1. Seleccion ----------
void seleccion(vector<int> d) {
    int n = d.size();
    cout << "\n=== ORDENAMIENTO POR SELECCION ===\n";
    cout << "Arreglo inicial: "; mostrar(d); cout << endl;
    for (int i = 0; i < n - 1; i++) {
        int menor = i;
        cout << "\nPasada " << i + 1 << ": posicion i = " << i
             << ", menor = datos[" << menor << "] = " << d[menor] << endl;
        for (int j = i + 1; j < n; j++) {
            cout << "   j = " << j << " : " << d[j] << " < " << d[menor] << "? ";
            if (d[j] < d[menor]) {
                menor = j;
                cout << "Si -> nuevo menor en posicion " << menor << endl;
            } else {
                cout << "No" << endl;
            }
        }
        if (menor != i) {
            cout << "   Intercambio datos[" << i << "] <-> datos[" << menor << "]: "
                 << d[i] << " <-> " << d[menor] << endl;
            intercambiar(d[i], d[menor]);
        } else {
            cout << "   El menor ya esta en su posicion, sin intercambio" << endl;
        }
        cout << "   Resultado: "; mostrar(d); cout << endl;
    }
    cout << "\nArreglo ordenado: "; mostrar(d); cout << endl;
}

// ---------- 2. Burbuja ----------
void burbuja(vector<int> d) {
    int n = d.size();
    cout << "\n=== ORDENAMIENTO BURBUJA ===\n";
    cout << "Arreglo inicial: "; mostrar(d); cout << endl;
    for (int pasada = 1; pasada < n; pasada++) {
        cout << "\nPasada " << pasada << ":" << endl;
        bool huboCambio = false;
        for (int j = 0; j < n - pasada; j++) {
            cout << "   j = " << j << " : " << d[j] << " > " << d[j + 1] << "? ";
            if (d[j] > d[j + 1]) {
                cout << "Si -> intercambio datos[" << j << "] <-> datos[" << j + 1 << "]" << endl;
                intercambiar(d[j], d[j + 1]);
                huboCambio = true;
            } else {
                cout << "No" << endl;
            }
        }
        cout << "   Resultado: "; mostrar(d); cout << endl;
        if (!huboCambio) {
            cout << "   No hubo intercambios, el arreglo ya esta ordenado." << endl;
            break;
        }
    }
    cout << "\nArreglo ordenado: "; mostrar(d); cout << endl;
}

// ---------- 3. Insercion ----------
void insercion(vector<int> d) {
    int n = d.size();
    cout << "\n=== ORDENAMIENTO POR INSERCION ===\n";
    cout << "Arreglo inicial: "; mostrar(d); cout << endl;
    for (int i = 1; i < n; i++) {
        int clave = d[i];
        int j = i - 1;
        cout << "\nPasada " << i << ": clave = datos[" << i << "] = " << clave << endl;
        while (j >= 0) {
            cout << "   j = " << j << " : " << d[j] << " > " << clave << "? ";
            if (d[j] > clave) {
                cout << "Si -> desplazo " << d[j] << " a la posicion " << j + 1 << endl;
                d[j + 1] = d[j];
                j--;
            } else {
                cout << "No" << endl;
                break;
            }
        }
        d[j + 1] = clave;
        cout << "   Inserto " << clave << " en la posicion " << j + 1 << endl;
        cout << "   Resultado: "; mostrar(d); cout << endl;
    }
    cout << "\nArreglo ordenado: "; mostrar(d); cout << endl;
}

// ---------- 4. Insercion con incremento (Shell) ----------
void insercionIncremento(vector<int> d) {
    int n = d.size();
    cout << "\n=== ORDENAMIENTO POR INSERCION CON INCREMENTO (SHELL) ===\n";
    cout << "Arreglo inicial: "; mostrar(d); cout << endl;
    int ronda = 0;
    for (int inc = n / 2; inc > 0; inc /= 2) {
        ronda++;
        cout << "\n--- Ronda " << ronda << ": incremento = " << inc << " ---" << endl;
        for (int i = inc; i < n; i++) {
            int clave = d[i];
            int j = i;
            cout << "  i = " << i << ": clave = " << clave << endl;
            while (j >= inc) {
                cout << "     comparo datos[" << j - inc << "] = " << d[j - inc]
                     << " > " << clave << "? ";
                if (d[j - inc] > clave) {
                    cout << "Si -> desplazo " << d[j - inc] << " a la posicion " << j << endl;
                    d[j] = d[j - inc];
                    j -= inc;
                } else {
                    cout << "No" << endl;
                    break;
                }
            }
            d[j] = clave;
            cout << "     Inserto " << clave << " en la posicion " << j << " -> ";
            mostrar(d); cout << endl;
        }
        cout << "  Resultado de la ronda: "; mostrar(d); cout << endl;
    }
    cout << "\nArreglo ordenado: "; mostrar(d); cout << endl;
}

// ---------- 5. Quick sort ----------
int contadorParticion = 0;

int particion(vector<int> &d, int inicio, int fin) {
    contadorParticion++;
    int pivote = d[fin];
    int i = inicio - 1;
    cout << "\nParticion " << contadorParticion << ": tramo [" << inicio << ".." << fin
         << "], pivote = " << pivote << ", i = " << i << endl;
    for (int j = inicio; j < fin; j++) {
        cout << "   j = " << j << " : " << d[j] << " <= " << pivote << "? ";
        if (d[j] <= pivote) {
            i++;
            intercambiar(d[i], d[j]);
            cout << "Si -> i = " << i << ", intercambio datos[" << i << "] <-> datos[" << j << "]" << endl;
        } else {
            cout << "No" << endl;
        }
    }
    int p = i + 1;
    cout << "\n   P = i + 1 => P = " << i << "+1 = " << p
         << ", intercambio datos[" << p << "] <-> datos[" << fin << "]" << endl;
    cout << "   " << d[p] << " <-> " << d[fin] << endl;
    intercambiar(d[p], d[fin]);
    cout << "   Resultado: "; mostrar(d); cout << endl;
    return p;
}

void quickSort(vector<int> &d, int inicio, int fin) {
    if (inicio < fin) {
        int p = particion(d, inicio, fin);
        quickSort(d, inicio, p - 1);
        quickSort(d, p + 1, fin);
    }
}

void quick(vector<int> d) {
    cout << "\n=== ORDENAMIENTO RAPIDO (QUICK SORT) ===\n";
    cout << "Arreglo inicial: "; mostrar(d); cout << endl;
    contadorParticion = 0;
    quickSort(d, 0, d.size() - 1);
    cout << "\nArreglo ordenado: "; mostrar(d); cout << endl;
}

// ---------- Menu ----------
int main() {
    vector<int> datos = ingresarDatos();
    int op;
    do {
        cout << "\n========== MENU DE ORDENAMIENTO ==========\n";
        cout << "Datos actuales: "; mostrar(datos); cout << endl;
        cout << "1. Ordenamiento por seleccion\n";
        cout << "2. Ordenamiento burbuja\n";
        cout << "3. Ordenamiento por insercion\n";
        cout << "4. Ordenamiento por insercion con incremento\n";
        cout << "5. Ordenamiento rapido (Quick Sort)\n";
        cout << "6. Ingresar nuevos valores\n";
        cout << "0. Salir\n";
        cout << "Elija una opcion: ";
        cin >> op;
        switch (op) {
            case 1: seleccion(datos); break;
            case 2: burbuja(datos); break;
            case 3: insercion(datos); break;
            case 4: insercionIncremento(datos); break;
            case 5: quick(datos); break;
            case 6: datos = ingresarDatos(); break;
            case 0: cout << "Fin del programa." << endl; break;
            default: cout << "Opcion no valida." << endl;
        }
    } while (op != 0);
    return 0;
}