// Programa: Compatibilidad Sanguinea (version con bandera bool y string)
// Funcion : Solicita el tipo de sangre del donante y receptor (8 tipos), determina si la donacion es compatible con switch anidados y una bandera bool, y muestra el resultado unificado al final usando string.
#include <iostream>
#include <string>
using namespace std;

int main() {
    int opcionDonante, opcionReceptor;
    string donante, receptor;
    bool compatible = false;

    cout << "=== Consulta de Compatibilidad Sanguinea ===\n\n";
    cout << "Tipos de sangre disponibles:\n";
    cout << "1. O-\n2. O+\n3. A-\n4. A+\n5. B-\n6. B+\n7. AB-\n8. AB+\n\n";

    cout << "Seleccione el tipo de sangre del DONANTE: ";
    cin >> opcionDonante;
    cout << "Seleccione el tipo de sangre del RECEPTOR: ";
    cin >> opcionReceptor;

    switch (opcionDonante) {
        case 1: donante = "O-"; compatible = true; break;
        case 2:
            donante = "O+";
            switch (opcionReceptor) {
                case 2: case 4: case 6: case 8: compatible = true; break;
                default: compatible = false;
            }
            break;
        case 3:
            donante = "A-";
            switch (opcionReceptor) {
                case 3: case 4: case 7: case 8: compatible = true; break;
                default: compatible = false;
            }
            break;
        case 4:
            donante = "A+";
            switch (opcionReceptor) {
                case 4: case 8: compatible = true; break;
                default: compatible = false;
            }
            break;
        case 5:
            donante = "B-";
            switch (opcionReceptor) {
                case 5: case 6: case 7: case 8: compatible = true; break;
                default: compatible = false;
            }
            break;
        case 6:
            donante = "B+";
            switch (opcionReceptor) {
                case 6: case 8: compatible = true; break;
                default: compatible = false;
            }
            break;
        case 7:
            donante = "AB-";
            switch (opcionReceptor) {
                case 7: case 8: compatible = true; break;
                default: compatible = false;
            }
            break;
        case 8:
            donante = "AB+";
            switch (opcionReceptor) {
                case 8: compatible = true; break;
                default: compatible = false;
            }
            break;
        default: cout << "\nOpcion de donante invalida.\n"; return 1;
    }

    switch (opcionReceptor) {
        case 1: receptor = "O-"; break;
        case 2: receptor = "O+"; break;
        case 3: receptor = "A-"; break;
        case 4: receptor = "A+"; break;
        case 5: receptor = "B-"; break;
        case 6: receptor = "B+"; break;
        case 7: receptor = "AB-"; break;
        case 8: receptor = "AB+"; break;
        default: cout << "\nOpcion de receptor invalida.\n"; return 1;
    }

    cout << "\n--- Resultado ---\n";
    cout << "Donante: " << donante << "\n";
    cout << "Receptor: " << receptor << "\n";

    if (compatible)
        cout << "Compatibilidad: SI, la donacion es compatible.\n";
    else
        cout << "Compatibilidad: NO, la donacion NO es compatible.\n";

    return 0;
}
