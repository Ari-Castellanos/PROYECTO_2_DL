# INSTRUCCIONES DE EJECUCION
1. En el archivo ´Descarga_Kaggle.ipynb´ se ha escrito el código para descargar la base de datos que se ha usado desde HuggingFace.
2. Se ejecuta después el archivo ´Limpiado_personajes.ipynb´, que hace uso del archivo ´limpiar_personajes.py´, con 
3. Se corre después el archivo ´DCGAN_base_arknights_azurlane.ipynb´, el cuál corre una red neuronal DCGAN sobre una muestra de imágenes de personajes. Al final devuelve las imágenes generadas por la red.
4. Después se ha de correr el archivo ´Experimentos_GAN.ipynb´ para realizar los experimentos de pérdida y estabilización.
5. Se corre el archivo ´Galeria_vecinos_regeneracion.ipynb´ para comparar las imágenes generadas con sus vecinos más cercanos en la base de datos.


# Base de datos
La base de datos se ha extraído desde HuggingFace, y tiene el nombre de ´JosephPaul2244/game_character_skins´. Este conjunto tiene la siguiente estructura:


game_character_skins/

├── arknights/          # 377 characters with multiple skins

├── azurlane/           # 737 characters with multiple skins  

├── bluearchive/        # 113 characters with multiple skins

├── fgo/               # 406 characters with multiple skins

├── genshin/           # 79 characters with multiple skins

├── girlsfrontline/    # 439 characters with multiple skins

├── neuralcloud/       # 81 characters with multiple skins

├── nikke/             # 113 characters with multiple skins

├── pathtonowhere/     # 88 characters with multiple skins

└── starrail/          # 44 characters with multiple skins


En el presente repositorio se ha hecho uso solamente del conjunto arknights/ y azurlane/

## Licencia de uso de datos
title: Creative Commons Attribution 4.0 International
spdx-id: CC-BY-4.0
description: >-
  Permits almost any use subject to providing credit and license notice.
  Frequently used for media assets and educational materials. The most common
  license for Open Access scientific publications. Not recommended for software.
how: >-
  Create a text file (typically named LICENSE or LICENSE.txt) in the root of
  your source code and copy the text of the license into the file. It is also
  acceptable to solely supply a link to a copy of the license, usually to the <a
  href='https://creativecommons.org/licenses/by/4.0/'>canonical URL for the
  license</a>.
using:
  caniuse: https://github.com/Fyrd/caniuse/blob/master/LICENSE
  FiveThirtyEight data: https://github.com/fivethirtyeight/data/blob/master/LICENSE
  Kubernetes documentation: https://github.com/kubernetes/website/blob/master/LICENSE
permissions:
  - commercial-use
  - modifications
  - distribution
  - private-use
conditions:
  - include-copyright
  - document-changes
limitations:
  - liability
  - trademark-use
  - patent-use
  - warranty
# Semilla
Se ha usado SEED=2026

# DECLARACIÓN DEL USO DE ASISTENTES DE IA

Se declara por este medio que se ha hecho uso de IA en el presente trabajo. Su uso se limitó al mejoramiento del código preexistente, ya sea para hacerlo más eficiente en el proceso de cómputo, ya para el mejoramiento de la estructura o la solución de errores cuya solución no era trivial.
