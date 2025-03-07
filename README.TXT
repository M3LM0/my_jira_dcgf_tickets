===================================================================
                   My_JIRA_DCGF_Tickets
===================================================================

Description :
-------------
Ce projet est une application de gestion et de traitement des tickets
de problèmes utilisateurs. L'application utilise PyQt5 pour l'interface
graphique et pandas (avec openpyxl) pour la gestion d'un fichier Excel
(.xlsx) servant de base de données.

L'application permet de :
- Charger et afficher la liste des tickets existants.
- Filtrer les tickets par divers critères (N°, Nom, Programme,
  Description, Statut, Priorité).
- Créer un nouveau ticket via une interface dédiée.
- Modifier ou supprimer un ticket existant.
- Appliquer un code couleur aux colonnes Statut et Priorité.

L'interface intègre également des fonctionnalités modernes, telles que
l'utilisation du style "Fusion", une palette personnalisée et des
composants graphiques adaptés (QComboBox pour certains filtres).

Architecture du projet :
-------------------------
Le projet est structuré de la manière suivante :

My_JIRA_DCGF_Tickets/
│
├── config.json
│   --> Fichier de configuration contenant le chemin vers le fichier
│       Excel et les listes de valeurs pour les menus déroulants.
│
├── main.py
│   --> Point d'entrée de l'application. Initialise le style, la
│       palette et la fenêtre principale.
│
├── ticket_service.py
│   --> Module responsable du chargement, de la sauvegarde, de l'ajout,
│       de la suppression et de la modification des tickets dans le
│       fichier Excel.
│
├── main_window.py
│   --> Fenêtre principale affichant la liste des tickets, les filtres,
│       et les boutons d'action (Nouveau, Modifier, Supprimer).
│
├── new_ticket_window.py
│   --> Fenêtre d'interface pour la création d'un nouveau ticket.
│
└── edit_ticket_window.py
    --> Fenêtre d'interface pour la modification d'un ticket existant.

Installation :
---------------
1. Assurez-vous d'avoir Python 3.9 (ou une version compatible) installé.
2. Créez un environnement virtuel (recommandé) et activez-le.
3. Installez les dépendances nécessaires avec pip :
      pip install pyqt5 pandas openpyxl

Configuration Git :
-------------------
Pour éviter que le fichier Excel de suivi (suivi_jira_dcgf.xlsx) soit
committé, vérifiez que votre fichier .gitignore contient une ligne telle que :
      *.xlsx
Si le fichier a déjà été ajouté, retirez-le du suivi avec :
      git rm --cached suivi_jira_dcgf.xlsx

Utilisation :
-------------
Lancez l'application en exécutant le fichier main.py :
      python main.py

Lors du démarrage, l'application charge le fichier Excel spécifié dans
config.json. Si le fichier n'existe pas, il sera créé automatiquement.
Vous pouvez alors consulter, filtrer, ajouter, modifier ou supprimer des
tickets via l'interface graphique.

Code Couleur :
---------------
- Statut :
    - "Ouvert"  : fond vert (HEX #82E0AA)
    - "Fermé"   : fond rouge (HEX #F1948A)
- Priorité :
    - "P1"      : fond bleu (HEX #85C1E9)
    - "P2"      : fond orange (HEX #F8C471)
    - "P3"      : fond rouge (HEX #E74C3C)

Notes :
-------
- L'interface a été conçue pour être moderne et responsive. Les champs
  de recherche ont des largeurs adaptées et certaines valeurs se sélectionnent
  via des menus déroulants pour faciliter l'utilisation.
- Si vous rencontrez des problèmes d'affichage (notamment au premier lancement),
  assurez-vous que la fenêtre a bien été redimensionnée et que le recalcul des
  lignes s'effectue correctement.

Contact :
---------
Pour toute question ou suggestion d'amélioration, n'hésitez pas à contacter
le responsable du projet.

===================================================================