# INSTRUCCIONES DE EJECUCION
1. En el archivo Descarga_Kaggle.ipynb se ha escrito el código para descargar la base de datos que se ha usado desde HuggingFace.
2. Se ejecuta después el archivo Limpiado_personajes.ipynb, que hace uso del archivo limpiar_personajes.py, con 
3. Se corre después el archivo DCGAN_base_arknights_azurlane.ipynb, el cuál corre una red neuronal DCGAN sobre una muestra de imágenes de personajes. Al final devuelve las imágenes generadas por la red.
4. Después se ha de correr el archivo Experimentos_GAN.ipynb para realizar los experimentos de pérdida y estabilización.


# Base de datos
La base de datos se ha extraído desde HuggingFace, y tiene el nombre de JosephPaul2244/game_character_skins. Este conjunto tiene la siguiente estructura:


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
