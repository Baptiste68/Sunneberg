# SUNNEBERG Project

Ce rep contient les éléments nécessaires au déploiement du projet "Sunneberg"

## Petit scope du projet

Répondre au besoin d’un couple d’agriculteur. 
Nous proposons un site internet afin que ce dernier puisse être visible sur le web 
et avoir une communication active avec ses clients.

## Point technique

Le projet est développé principalement en Python avec le framework Django.
Les modifications au code sont faites dans un environnement de développement et sont « push » sur la branche « origin ». Sur cette branche, le service de « Travis » a été mis en place.
Une fois validé les branches « origin » et « master » peuvent être « merged ».
Le code est ensuite directement « pull » du Github depuis le site.

Le site web est hébergé sur Digital Ocean. La connexion se fait en ssh.
Certaines commandes sont utiles lors de changement du code :
sudo supervisorctl stop all
python manage.py collectstatic
python manage.py makemigrations --settings=sunneberg_project.settings.production 
sudo service nginx reload
sudo supervisorctl start all

L’architecture de déploiement est représenté par le diagramme suivant


![Screenshot](https://github.com/Baptiste68/Sunneberg/blob/master/DeploymentDiag.PNG)


