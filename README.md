# Projet_info Chat
Le projet consiste a réaliser un chat contenant une partie client server qui permet de connaitre les gens disponible pour chatter et une partie peer to peer pour communiquer en direct avec la paersonne

# Lancement du code
## lancement du server 
 Dans un fenetre de commande, tapper:
 ```
 python cs.py server 
```
## lancement du chat 
utiliser la commande:
```
python cs.py 
```
Le chat écoutera sur le port 5000 part défault.
il est possible de le spécifier en rajoutant l'addresse ip ansi que le port a la suite de la dernière commande 

```
python cs.py IP PORT
```

# Commande disponible 
voila une liste de toute les commande disponnible dans le chat

| Commande      | Utilité                          | 
| ------------- | -------------------------------- | 
| /connect      | conenct you to the chat          | 
| /disconnect   | disconnect you from the chat     | 
| /editPseudo   | edit your pseudo                 | 
| /connected    |show a list of connected people   |
| /quit         | disconnect your from a person    |
| /exit         | leave the chat ad disconnect you |

En utilisant la commande ```/connected``` la liste des personnes disponnible s'affiche. Vous pouvez choisir un quelqu'un dans cette liste et vous serrez connect a cette personne. Vous pouvez commencer a lui envoyer des messages sans utiliser de commande.
