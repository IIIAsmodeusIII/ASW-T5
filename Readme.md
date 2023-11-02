### Tarea 5 - Arquitectura de Software

## Integrantes
1. Constanza Alvarado Valenzuela | 201975521-7
2. Bruno Vega Pizarro | 201854051-k

## API REST
1. https://domainName/farms/id - Devuelve un arreglo de bytes en forma de imagen png correspondiente a la granja del usuario

## Instrucciones de ejecución:
1. Ejecutar docker compose up en carpeta /logs para activar registros de AMQP
2. Ejecutar docker compose up en /apigategay para activar graphql en el microservicio render y los microservicios de prueba
3. Ejecutar docker compose up en /constructTestService y en /usersTestService para activar los microservicios de prueba
4. Ejecutar docker compose up en /render para activar el microservicio de render. Puede ser probado manualmente en 127.0.0.1:5001
5. Ejecutar docker compose up en /chat para activar el chatbot en el puerto 127.0.0.1:3000

## Detalles del render 
1. Separa la tierra construida de la posible a construir con pasto y tierra respectivamente.
2. La tierra lista para sembrar posee un color de tierra distintivo
3. La tierra regada es oscurecida
4. Existen 3 estados para cada plantación: Semilla (1 o 2 días), en crecimiento (Más de 2 días) y lista para cosechar. Este último estado posee un ícono de instrumento de cosecha sobre el cultivo listo.
