Projet Calculatrice Python
BIHET Lucie Term1

calculatrice_python.py:
- C'est la calculatrice de base avec un certain nombre d'opération possible
- Elle peut être utilisée au clavier ou avec les boutons
- Pour les plus grandes valeurs, elle convertit le nombre en écriture scientifique
- Il y a au démarage une fenêtre d'information
- Le calcul et résultat précédent sont affichés sur la barre du haut
- Si le calcul du haut est trop long, il affichera seulement le résultat
- Problèmes rencontrés #la calculatrice crash lorsque l'exposant d'une puissance est au dessus de 1 000 000 généralement
# Cette erreur apparaît sur certains calculs (apparemment lorsqu'il y a des problèmes de syntaxe comprenant des parenthèses, par ex : 45(2+7)) mais la calculatrice continue de fonctionner même après: 
	<string>:1: SyntaxWarning: 'int' object is not callable; perhaps you missed a comma?

calculatrice_programmeur_python.py:
- C'est une calculatrice avec trois barres d'affichage : une pour décimal, une pour binaire et une pour héxadecimal
- Elle peut être utilisée au clavier ou avec les boutons
- Selon les modes, les certains boutons sont bloqués mais pas grisés
- La calculatrice sert aussi de convertisseur entre les différents systèmes de numération
- Problèmes, manque de temps ou pas su faire sans trop alourdir le programme :
# pas de codage en complément à 2, seleument un signe '-' devant un nombre négatif
# pas de conversion en même temps que les valeurs sont écrites entre les systèmes de numération
# pas de grisement des touches non utilisables
# pas de bouton qui donne la taille maximale de codage des entiers manipulés
