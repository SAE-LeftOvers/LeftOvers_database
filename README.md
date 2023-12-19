# LeftOvers_database

Base de données des Recettes utilisé pour développer l'application LeftOvers, son IA et son API.

## Prérequis
* python
* librairies python :
  * pickle
  * os
  * dotenv
  * tqdm
  * pandas
  * psycopg2
  * ast
* une base de donnée postgresql vide

## Utilisation
* Télécharger les fichiers cités ci-après, disponible à l'adresse *https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions*, et positionner-ler dans un dossier **LeftOvers_database/input** :
  * **ingr_map.pkl**
  * **RAW_recipes.csv**
  * **RAW_interactions.csv**
  * **PP_recipes.csv**
* Créer un fichier **LeftOvers_database/DatabaseCreation/.env** qui contiendra les variables d'environnement suivantes :
  * **DB_HOST**
  * **DB_NAME**
  * **DB_PORT**
  * **DB_USER**
  * **DB_PASSWORD**
* Placer vous dans le répertoire **LeftOvers_database/DatabaseCreation** et executer la commande : ```python3 'ResetDB&LoadData.py'```
