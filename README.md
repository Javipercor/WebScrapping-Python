Demo de webscrapping realizada con beautifulsoup sobre la página https://www.worldometers.info/coronavirus/

En la carpeta src se encuentran todo el código empleado
En la carpeta dataset se encuentran los datasets generados
En la carpeta pdf se encuentra un pdf con las respuestas a las 11 preguntas planteandas en la guía de la PRA1, que también sirve como guía de datasets y motivación

Atendiendo al código, el scrapper se podría dividir en dos partes:
En la primera parte se extrae información de la tabla con información de coronacirus para todos los países y para los continentes
En la segunda parte se ha recuperado la información referente a los casos que se han producido cada día. 
En este caso ha hecho falta utilizar expresiones regulares para recuprar la información del script (dentro del tag) que la servía, ya que beautiful soup no es capaz de hacerlo



La intención es seguir trabajando en este scraper para obtener más información y cruzarlo con datos de Api´s públicas
