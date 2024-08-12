# DeltoBot. Creado por Lázaro Borghi

DeltoBot es un bot de Telegram diseñado para ofrecer una variedad de funcionalidades útiles y entretenidas.

### Enlace para probarlo: [Probar DeltoBot](https://t.me/delto_lb_bot)

### Funcionalidades

¡Quiero saber el clima!:

Consulta el clima actual en cualquier ciudad del mundo. Utilizando la API de OpenWeatherMap, el bot proporciona la temperatura actual, las condiciones meteorológicas y una recomendación basada en el clima.
También genera una imagen del lugar con OpenAI (configurable para que no genere).

![quiero saber el clima](https://github.com/user-attachments/assets/1f3f6203-bcc4-446f-bc0c-d0d47630d872)

¡Quiero contar!: 

Cada vez que el usuario selecciona esta opción, el bot incrementa un contador específico para ese usuario. Este contador es persistente, manteniéndose incluso si el bot se reinicia.

![quiero contar](https://github.com/user-attachments/assets/3e7b29bf-484e-4f48-bba0-70e6f412835d)

Charlar con Delto: 

Esta funcionalidad permite al usuario charlar interactivamente con Delto y luego enviar la conversación OpenAI para un análisis de sentimientos. 
El bot clasifica el sentimiento como positivo, negativo o neutral, y proporciona una breve explicación.

![hablar con delto](https://github.com/user-attachments/assets/13fc0bd0-900f-460e-bb97-14ecf24e4a71)

Delto entiende los audios que le envías:

![hablar con delto 2](https://github.com/user-attachments/assets/2b634f5d-9aba-4166-a651-d801d7295f64)

Traducción de voz (funcionalidad libre):

Esta funcionalidad permite al usuario elegir un idioma al cual traducir un mensaje. Luego, el usuario envía un audio al bot, que traduce el contenido al idioma seleccionado y responde con una nota de voz generada automáticamente por inteligencia artificial. Mejora la accesibilidad y ofrece una experiencia interactiva e innovadora.
Es muy útil porque genera una nota de voz traducida al instante de lo que le envías. Un caso de uso interesante podría ser si necesitas comunicarte rápidamente con una persona que hable otro idioma, tan solo sería enviar una nota de voz y reproducir la traducción. Especialmente útil si estás como turista en otro país.

![traductor 1](https://github.com/user-attachments/assets/f3827fe2-77c7-4c2f-b169-5165b1d3ad19)
![traductor2](https://github.com/user-attachments/assets/b2b80203-f5b1-4e84-9729-5fd9969026d1)

### Probar DeltoBot

Puedes probar a Delto haciendo click en el siguiente enlace: [Probar DeltoBot](https://t.me/delto_lb_bot)

### Instalación de ambiente de desarrollo

Para generar un ambiente de desarrollo en necesario:
- Python (última versión estable).
- Instalación de librerías (listadas en el archivo requirements.txt).
- Credenciales de API (API de Telegram, OpenWeatherMap, OpenAI).

### Configuración

1. Clonar repositorio:
  git init
  git clone https://github.com/lazaroborghi/telegrambot_delto_lb.git

2. Instalar dependencias:
  pip install -r requirements.txt

3. Configurar variables de entorno:
  Crear archivo .env con las variables de entorno necesarias. Como ejemplo utiliza el archivo ".env.example". El archivo tiene que llamarse ".env" y el contenido tienen que ser las variables de entorno como claves de APIs y demás.

4. Ejecutar el bot:
  python main.py
