#include <iostream>
#include <iomanip>
using namespace std;

// ORDENAMIENTO BURBUJA CON BANDERA
void burbuja(string p[], int precio[], int u[],
             int ing[], int n, int &comp,
             int &inter, int &pasadas) {

    comp=0;
    inter=0;
    pasadas=0;
    bool bandera=true;

    while(bandera && pasadas<n-1) {
        bandera=false;
        pasadas++;

        for(int j=0; j<n-pasadas; j++) {
            comp++;

            if(ing[j]<ing[j+1] ||
              (ing[j]==ing[j+1] && u[j]<u[j+1])) {

                int aux=ing[j];
                ing[j]=ing[j+1];
                ing[j+1]=aux;

                aux=precio[j];
                precio[j]=precio[j+1];
                precio[j+1]=aux;

                aux=u[j];
                u[j]=u[j+1];
                u[j+1]=aux;

                string temp=p[j];
                p[j]=p[j+1];
                p[j+1]=temp;

                inter++;
                bandera=true;
            }
        }
    }
}

// MOSTRAR TABLA
void mostrar(string p[], int precio[], int u[],
             int ing[], int n) {

    cout << "\n";
    cout << left << setw(22) << "PLATO"
         << setw(12) << "PRECIO"
         << setw(12) << "UNIDADES"
         << "INGRESO\n";

    cout << "--------------------------------------------------\n";

    for(int i=0; i<n; i++) {
        cout << left << setw(22) << p[i]
             << setw(12) << precio[i]
             << setw(12) << u[i]
             << ing[i] << endl;
    }
}

// PROCESAR ESCENARIOS
void escenario(string nombre, string p[],
               int precio[], int u[], int ing[], int n) {

    int c, in, pa;

    cout << "\n========================================";
    cout << "\n" << nombre;
    cout << "\n========================================";

    burbuja(p,precio,u,ing,n,c,in,pa);

    mostrar(p,precio,u,ing,n);

    cout << "\nComparaciones: " << c;
    cout << "\nIntercambios: " << in;
    cout << "\nPasadas: " << pa << endl;
}

int main() {
    const int n=8;

    string platos[8]={
        "Aji de gallina","Chairo","Trucha frita",
        "Lomo saltado","Sopa de quinua",
        "Pollo broaster","Cuy chactado",
        "Tallarin saltado"
    };

    int precio[8]={8,5,12,10,4,9,25,7};
    int unidades[8]={45,60,25,50,70,40,8,30};
    int ingreso[8];

    int total=0, totalU=0, mayores=0;
    int mayor=0, pos=0;

    cout << "\n========================================";
    cout << "\n       MENU DEL COMEDOR UNIVERSITARIO";
    cout << "\n========================================";

    // CALCULAR INGRESOS
    for(int i=0; i<n; i++) {
        ingreso[i]=precio[i]*unidades[i];
        total+=ingreso[i];
        totalU+=unidades[i];

        if(unidades[i]>unidades[mayor])
            mayor=i;
    }

    cout << "\n\nVENTAS DE LA SEMANA";
    mostrar(platos,precio,unidades,ingreso,n);

    // ESTADISTICAS
    float promedio=(float)total/n;

    for(int i=0; i<n; i++)
        if(ingreso[i]>promedio)
            mayores++;

    cout << "\n========================================";
    cout << "\n             ESTADISTICAS";
    cout << "\n========================================";

    cout << "\nIngreso total: S/ " << total;
    cout << "\nPromedio: S/ " << fixed << setprecision(2) << promedio;
    cout << "\nPlatos sobre el promedio: " << mayores;
    cout << "\nUnidades totales: " << totalU;
    cout << "\nPlato mas vendido: " << platos[mayor];
    cout << "\nUnidades vendidas: " << unidades[mayor];

    // BUSQUEDA SECUENCIAL
    cout << "\n\n========================================";
    cout << "\n          BUSQUEDA SECUENCIAL";
    cout << "\n========================================";

    string buscar="Trucha frita";
    int encontrado=-1;

    for(int i=0; i<n; i++) {
        if(platos[i]==buscar) {
            encontrado=i;
            break;
        }
    }

    cout << "\nBuscar: " << buscar;

    if(encontrado!=-1)
        cout << "\nEncontrado en orden original: " << encontrado+1;
    else
        cout << "\nNo encontrado";

    buscar="Arroz chaufa";
    encontrado=-1;

    for(int i=0; i<n; i++)
        if(platos[i]==buscar) {
            encontrado=i;
            break;
        }

    cout << "\nBuscar: " << buscar;

    if(encontrado==-1)
        cout << "\nNo encontrado";

    // COPIAS PARA ORDENAR
    string p[8];
    int pr[8], u[8], ing[8];

    for(int i=0; i<n; i++) {
        p[i]=platos[i];
        pr[i]=precio[i];
        u[i]=unidades[i];
        ing[i]=precio[i]*unidades[i];
    }

    int c,in,pa;

    burbuja(p,pr,u,ing,n,c,in,pa);

    cout << "\n\n========================================";
    cout << "\n          RANKING DE INGRESOS";
    cout << "\n========================================";

    mostrar(p,pr,u,ing,n);

    cout << "\nComparaciones: " << c;
    cout << "\nIntercambios: " << in;
    cout << "\nPasadas: " << pa;

    // PRIMER INGRESO MENOR A 250
    cout << "\n\nPRIMER PLATO CON INGRESO MENOR A S/ 250";

    for(int i=0; i<n; i++) {
        if(ing[i]<250) {
            cout << "\nPlato: " << p[i];
            cout << "\nPuesto: " << i+1;
            cout << "\nIngreso: S/ " << ing[i];
            break;
        }
    }

    // MEJOR CASO
    string pm[8];
    int prm[8], um[8], im[8];

    for(int i=0; i<n; i++) {
        pm[i]=p[i];
        prm[i]=pr[i];
        um[i]=u[i];
        im[i]=ing[i];
    }

    escenario("MEJOR CASO: YA ORDENADO",
              pm,prm,um,im,n);

    // PEOR CASO: INVERTIDO
    string pi[8];
    int pri[8], ui[8], ii[8];

    for(int i=0; i<n; i++) {
        int j=n-1-i;
        pi[i]=p[j];
        pri[i]=pr[j];
        ui[i]=u[j];
        ii[i]=ing[j];
    }

    escenario("PEOR CASO: INVERTIDO",
              pi,pri,ui,ii,n);

    cout << "\n========================================";
    cout << "\n             FIN DEL PROGRAMA";
    cout << "\n========================================\n";

    return 0;
}