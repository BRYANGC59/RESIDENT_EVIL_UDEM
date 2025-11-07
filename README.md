Simulación de propagación de infección en una matriz con árbol de contagio

(Proyecto para la práctica de árboles – UDEM 2025-2)

Este proyecto implementa una simulación gráfica de contagio dentro de una matriz NxN, donde varias personas se mueven aleatoriamente y pueden infectarse según compartan celda con personas infectadas.
Incluye la visualización dinámica del árbol de infección, curación, adición de personas, modo furia, y una bomba de sanación.

Este desarrollo cumple los requisitos de la práctica práctica_árboles_20252.pdf: propagación, defensa, árbol de contagio, curación con eliminación y reparenting, visualización y movimiento aleatorio.

📌 1. Descripción general

La simulación opera en rondas. En cada ronda:

Todas las personas se mueven a una celda adyacente aleatoria.

Se procesan los contagios en las celdas donde coinciden sanos e infectados.

Se actualiza el árbol de infección.

Se muestran los estados de las personas y la matriz.

La interfaz está desarrollada en Tkinter, permitiendo:

✅ Siguiente ronda
✅ Curar personas
✅ Agregar nuevas personas
✅ Lanzar bomba de sanación
✅ Activar modo furia
✅ Visualizar el árbol de propagación
✅ Finalizar la simulación

📌 2. Supuestos asumidos

✔ Movimiento tipo toroide:
Si una persona sale del límite, reaparece por el borde opuesto.

✔ Cada persona comienza con defensa = 3, excepto si ya está infectada.

✔ Un infectado furioso solo infecta automáticamente a una persona, luego se desactiva.

✔ La bomba de sanación cura completamente al único infectado del tablero, lo elimina del árbol y reinicia la raíz.

✔ El árbol de infección:

Siempre tiene al paciente cero como raíz.

Si el único infectado está solo, igual se dibuja.

Es una lista de adyacencia.

✔ La interfaz gráfica muestra:

Sano = verde

Infectado = rojo

Furioso = morado

✔ La infección reduce defensa según cantidad de infectados en la misma celda.
