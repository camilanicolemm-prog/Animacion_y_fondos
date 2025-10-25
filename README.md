# Animacion_y_fondos

Practica 4 – Fondos y Animaciones

Alumno: Camila Nicole Mejía Macías
Grupo: 6010

Descripción
Esta práctica implementa un fondo con efecto parallax, un ciclo día/noche y un sprite animado con estados idle y run. Se aplican diferentes capas para simular profundidad y movimiento.

Velocidades por capa y justificación

Capa            	Velocidad	      Justificación
StarsLayer	        0.25	        Movimiento muy lento para simular que las estrellas están lejos.
CloudsLayer       	1.2	          Velocidad media para dar sensación de altura intermedia y movimiento natural de nubes.
HillsLayer        	2.0	          Más rápido para simular cercanía y profundidad.


Duración de frames por estado
Estado	        frame_duration	     Justificación
Idle            	0.10 s          	Animación tranquila, sin movimiento rápido.
Run             	0.06 s	          Animación más rápida y dinámica para reflejar movimiento.


Extensiones implementadas
Ciclo día/noche:
Un fondo que se difumina gradualmente entre los colores del día y la noche usando una interpolación que simula una onda sinusoidal.
 seno.
Evidencia: el cielo y horizonte cambian continuamente, creando un efecto de transición realista.


HUD informativo:
Muestra FPS, animación actual y controles activos en pantalla.
Evidencia: texto visible en la esquina superior izquierda que indica FPS, frame y anim: idle/run.


<img width="962" height="572" alt="idle png" src="https://github.com/user-attachments/assets/a2913cad-659a-4345-92c7-9f42d7a26ede" />


Controles
Izquierda: tecla A
Derecha: tecla D
Salir: Esc
