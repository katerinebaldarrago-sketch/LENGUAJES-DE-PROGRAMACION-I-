#include <iostream>
using namespace std;

int main()
{
    int suma = 0,n= 0;
    
    do{
        cout<<"Numero :"<<n<<endl;
        cin >> n;
        suma = suma + n;
        n = n + 1;
    } while(n <= 10);

    return 0;
}

//suma parcial