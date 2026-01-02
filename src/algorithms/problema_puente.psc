Algoritmo problema_puente
	
	//  Definimos la variable tiempo en 0
	time = 0
	
	A = 1 // 1 Min
	B = 2 // 2 Min
	C = 5 // 5 Min
	D = 8 // 8 Min
	
	// 	Cruzan 1min y 2 min
	time = time + B
	// Regresa 1 min
	time = time + A
	
	// Cruzan 5 y 8 mins
	time = time + D 
	// Regresa 2 mins
	time = time + B
	
	// Cruzan 1 min y 2 mins	
	time = time + B
	
	Escribir "El tiempo total fue: ' time
	
	Si time <= 15 Entonces
		Escribir "Estrategia Funcionó"
	SiNo
		Escribir "Estrategia No Funcionó"
	Fin Si
	
FinAlgoritmo