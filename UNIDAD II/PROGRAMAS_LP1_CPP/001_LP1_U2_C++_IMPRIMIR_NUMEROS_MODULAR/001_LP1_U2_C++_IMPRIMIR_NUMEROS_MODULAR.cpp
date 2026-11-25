#include <iostream>

void imprimirNumeros(int inicio, int fin); // Declaración de prototipo

int main() {
    imprimirNumeros(1, 10);
    return 0; //falta
}

// ImprimirNumeros (int inicio, int fin)
void imprimirNumeros(int inicio, int fin) { //funcion
    for (int i = inicio; i <= fin; ++i) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}