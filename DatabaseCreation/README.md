# Base de donnée en local

## Prérequis
* python installé
* une base de données en local pour contenir les données (postgresql)
* les modules python 
  * pandas (pour la lecture des .csv)
  * psycopg2 (pour la connexion à la base de données postgresql)
  * pickle (pour la lecture des .pkl)
  * tqdm (pour la barre de progres)
  * ast (pour convertir une chaîne de caractère en liste python)
  * python-dotenv

## Utilisation
* Créer un fichier **.env** dans le répertoire **LocalDatabaseVersion** avec les valeurs de connexion à la base de données
  * DB_HOST=nom_server
  * DB_PORT=num_port_ouvert
  * DB_NAME=nom_base_de_données
  * DB_USER=nom_utilisateur_avec_accès
  * DB_PASSWORD=mot_de_passe_utilisateur
* Exécuter le fichier **ResetDB&LoadData.py** à la racine du répertoire **LocalDatabaseVersion**

## Tests locals
Si souhaitez tester des fonctions séparemment, vous pouvez créer un fichier **local_test.py** qui sera ignoré par git.  