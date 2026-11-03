# PYSNAKE-LOGICA:Proyecto de Videojuego en Python con Pygame

## Descripción del Proyecto y Autora
* *Nombre de la estudiante:* Nimsi Jehieli Velazquez Flores
* *Descripción:* Este repositorio contiene el desarrollo de un proyecto centrado en la creación de un juego clásico tipo Snake programado en Python utilizando la librería Pygame. La idea principal es estructurar el código de manera limpia, ordenada y modular, integrando elementos visuales atractivos, menús de inicio, paletas de colores personalizadas y un sistema de puntajes eficiente.

## Objetivo General del Juego
Desarrollar un videojuego interactivo de tipo Snake en 2D que resulte más estructurado, llamativo y funcional, aplicando los fundamentos de programación lógica y diseño modular. El juego busca ofrecer una experiencia fluida mediante el uso de menús de bienvenida, controles responsivos de teclado, colores modernos y un sistema de control de colisiones y puntuaciones integrado con alertas de sonido en Windows.

---

## Investigación autónoma sobre Pygame

### ¿Qué es Pygame y para qué se utiliza?
Pygame es un conjunto de módulos de código abierto en Python creados para escribir videojuegos y aplicaciones multimedia. Se utiliza principalmente para manejar de manera sencilla los gráficos en dos dimensiones, la reproducción de efectos de sonido y música, la gestión de la ventana de visualización y la captura de eventos de entrada por parte del usuario (como el teclado o el ratón) sin tener que programar todo desde cero.

### ¿Cómo se relaciona Pygame con los temas vistos en clase?
* *Ciclos:* Se usan en el bucle principal del juego (game loop) para mantener la aplicación ejecutándose constantemente, actualizando la pantalla y escuchando lo que hace el usuario fotograma a fotograma.
* *Eventos:* Permiten detectar cuando la persona presiona una tecla (por ejemplo, las flechas direccionales para mover la serpiente) o decide cerrar la ventana de juego.
* *Estructuras de datos:* Se emplean listas y tuplas para almacenar las coordenadas exactas del cuerpo de la serpiente, manejar la posición aleatoria de la comida y configurar la paleta de colores RGB.
* *Funciones:* Sirven para dividir el código en bloques reutilizables, separando la lógica del menú principal, la función para generar la comida, el movimiento y la ejecución general del juego.

### ¿Qué significa que Pygame permita "tomar mucho o poco" de la librería?
Significa que la librería no te ata a un motor de juego pesado ni te obliga a seguir una estructura estricta u obligatoria. Te da la libertad de usar únicamente los módulos que necesites para tu proyecto (por ejemplo, puedes usar solo la gestión de superficies gráficas ignorando otras herramientas), lo que te permite diseñar la arquitectura del programa a tu propia medida.

---

## Documentación del flujo de trabajo en las ramas
Para mantener ordenado el desarrollo del proyecto a lo largo del curso, el repositorio se encuentra estructurado bajo las siguientes ramas de trabajo:

* *main:* Es la rama principal y oficial del proyecto. Aquí se almacena únicamente la versión estable, limpia y funcional del juego que ya ha sido probada.
* *v01:* Es la rama intermedia de integración. Funciona como un espacio de respaldo y validación general desde donde se une el código hacia main mediante fusiones (merges).
* *actividad_uno:* Rama designada específicamente para alojar los avances, pruebas y modificaciones individuales correspondientes a la primera sesión o actividad previa sobre la estructura inicial de Pygame.
* *actividad_dos:* Rama destinada a guardar los nuevos avances, mejoras visuales, lógica de control o complementos desarrollados en las sesiones posteriores del curso.
