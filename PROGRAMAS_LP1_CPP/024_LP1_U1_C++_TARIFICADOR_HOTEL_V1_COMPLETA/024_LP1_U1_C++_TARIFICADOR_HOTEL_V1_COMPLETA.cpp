// Programa: Tarificador de Reservas de Hotel
// Funcion : Calcula el costo total de una reserva segun noches de estadia, numero de huespedes, plan de alimentacion y tipo de habitacion, aplicando recargo por huespedes adicionales y 12% de descuento por estadias mayores a 5 noches, mostrando un desglose detallado.
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int noches = 0, hues = 0, tipohabitacion = 0, plan = 0;
    double costoCategoria = 0.0, descuento = 0.0, Multahues = 0.0, plancom = 0.0;
    double totalPagar = 0.0, totalfinal = 0.0;

    cout << "TARIFICADOR DE RESERVAS DE HOTEL" << endl;
    cout << "Ingrese el numero de noches de estadia: ";
    cin >> noches;

    if (noches <= 0) {
        cout << "ERROR, el numero de noches debe ser un valor positivo" << endl;
        return 1;
    }

    cout << "Ingrese el numero de huespedes: ";
    cin >> hues;

    if (hues < 1) {
        cout << "ERROR, el numero de huespedes debe ser al menos 1" << endl;
        return 1;
    }

    cout << "Plan de alimentacion (1 = Solo desayuno, 2 = Pension Completa): " << endl;
    cin >> plan;

    if (plan != 1 && plan != 2) {
        cout << "ERROR: plan de alimentacion no valido" << endl;
        return 1;
    }

    cout << "Seleccione el tipo de habitacion" << endl;
    cout << "1: Habitacion Estandar (S/.50.00 por noche)" << endl;
    cout << "2: Habitacion Doble (S/.80.00 por noche)" << endl;
    cout << "3: Suite Ejecutiva (S/.140.00 por noche)" << endl;
    cout << "OPCION: ";
    cin >> tipohabitacion;

    switch (tipohabitacion) {
        case 1: costoCategoria = 50.00; break;
        case 2: costoCategoria = 80.00; break;
        case 3: costoCategoria = 140.00; break;
        default: cout << "ERROR: tipo de habitacion no valida" << endl; return 1;
    }

    if (tipohabitacion == 1 && hues > 1) Multahues = (hues - 1) * 15;
    if (tipohabitacion == 2 && hues > 2) Multahues = (hues - 2) * 15;
    if (tipohabitacion == 3 && hues > 3) Multahues = (hues - 3) * 15;

    if (plan == 2) plancom = 25 * hues;

    totalPagar = ((costoCategoria + plancom) + Multahues) * noches;

    if (noches > 5) descuento = totalPagar * 0.12;

    totalfinal = totalPagar - descuento;

    cout << fixed << setprecision(2);
    cout << "--------------- Desglose ---------------" << endl;

    if (tipohabitacion == 1) cout << "Tipo de habitacion : Habitacion Estandar " << endl;
    if (tipohabitacion == 2) cout << "Tipo de habitacion : Habitacion Doble " << endl;
    if (tipohabitacion == 3) cout << "Tipo de habitacion : Suite Ejecutiva " << endl;

    cout << "Subtotal de alojamiento: S/." << costoCategoria * noches << endl;

    if (tipohabitacion == 1 && hues > 1) cout << "Recargo por huespedes adicionales: S/." << Multahues * noches << endl;
    if (tipohabitacion == 2 && hues > 2) cout << "Recargo por huespedes adicionales: S/." << Multahues * noches << endl;
    if (tipohabitacion == 3 && hues > 3) cout << "Recargo por huespedes adicionales: S/." << Multahues * noches << endl;

    cout << "Costo de alimentacion: S/." << plancom * noches << endl;

    if (noches > 5) {
        cout << "Descuento por estadia larga: S/." << descuento << endl;
        cout << "Monto total a pagar: S/." << totalfinal << endl;
    } else {
        cout << "Monto total a pagar: S/." << totalPagar << endl;
    }

    return 0;
}
