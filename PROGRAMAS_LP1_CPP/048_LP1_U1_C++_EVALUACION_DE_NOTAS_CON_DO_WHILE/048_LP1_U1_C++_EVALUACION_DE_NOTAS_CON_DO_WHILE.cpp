#include <iostream>
using namespace std;

int main()
{
    double nota,n,i=0;
    
    cout<<"Ingrese la cantidad de notas"<<endl;
    cin >> n;
    
    do {
        cout << "Ingrese la nota del Examen Parcial (0 a 20) "<<i<<" : "<<endl;
        cin >> nota;

        if (nota < 0 || nota > 20) {
            cout <<endl<< "La nota ingresada no es correcta " << endl;
        }
        if (nota >= 10.5 && nota <= 20) {
        cout << "Estado: Aprobado" << endl;
    	} 
    	if (nota >= 0 && nota <=5 10.4) {
        cout << "Estado: Desprobado" << endl;
    	}
		else {
        cout << "nota no valida" << endl;
   		}
   		 i = i + 1;
    } while (i<=n);


    return 0;
}
