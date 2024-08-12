# DeltoBot. Creado por Lázaro Borghi

DeltoBot es un bot de Telegram diseñado para ofrecer una variedad de funcionalidades útiles y entretenidas.

### Funcionalidades

¡Quiero saber el clima!:

Consulta el clima actual en cualquier ciudad del mundo. Utilizando la API de OpenWeatherMap, el bot proporciona la temperatura actual, las condiciones meteorológicas y una recomendación basada en el clima.

![saber el clima](https://github.com/lazaroborghi/telegrambot_delto_lb/tree/main/images/quierosaberelclima.png)

¡Quiero contar!: 

Cada vez que el usuario selecciona esta opción, el bot incrementa un contador específico para ese usuario. Este contador es persistente, manteniéndose incluso si el bot se reinicia.

![contar](https://github.com/lazaroborghi/telegrambot_delto_lb/blob/main/quierocontar.png?raw=true)

Charlar con Delto: 

Esta funcionalidad permite al usuario charlar interactivamente con Delto y luego enviar la conversación OpenAI para un análisis de sentimientos. 
El bot clasifica el sentimiento como positivo, negativo o neutral, y proporciona una breve explicación.

Traducción de voz (funcionalidad libre):

Esta funcionalidad permite al usuario elegir un idioma al cual traducir un mensaje. Luego, el usuario envía un audio al bot, que traduce el contenido al idioma seleccionado y responde con una nota de voz generada automáticamente por inteligencia artificial. Esta funcionalidad mejora la accesibilidad y ofrece una experiencia interactiva e innovadora.
Esta funcionalidad es muy útil porque genera una nota de voz traducida al instante de lo que le envías. Un caso de uso interesante podría ser si necesitas comunicarte rápidamente con una persona que hable otro idioma, tan solo sería enviar una nota de voz y reproducir la traducción. Especialmente útil si estás como turista en otro país.

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
  Crear archivo .env con las variables de entorno necesarias. Como ejemplo utiliza el archivo ".env.example".

4. Ejecutar el bot:
  python main.py
