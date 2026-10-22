Algoritmo CalcularElIgvDeUnProducto
    Definir precio, IGV, precioFinal Como Real
    
    Escribir "Ingrese el precio del producto:"
    Leer  precio
	
	IGV <- precio * (18 / 100)
	precioFinal <- precio + IGV
    
    Escribir "El precio del producto es:", precio
    Escribir "El IGV del producto es: ", IGV
	Escribir "El precio final del producto es: ", precioFinal
FinAlgoritmo
