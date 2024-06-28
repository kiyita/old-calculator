from tkinter import *
from math import *

#####
"""Variables globales"""

NOMBRES = [i for i in range(1, 10)] + [0]
SIGNES = ['+', '-', '*', '/', '//', '%']
SIGNES += ['sqrt(', '**', '.']
SIGNES2 = ['(', ')']
ERREUR = ['valeur trop élevée', 'division par 0']
ERREUR += ['calcul impossible', "mauvaise syntaxe"]
ERREUR += ['problème de parenthèse']

#####
class Pile:
    ''' classe Pile
    création d'une instance Pile avec une liste
    '''
    def __init__(self):
        "Initialisation d'une pile vide"
        self.liste=[]

    def vide(self):
        "teste si la pile est vide"
        return self.liste==[]

    def depiler(self):
        "dépile"
        assert not self.vide(),"Pile vide"
        return self.liste.pop()

    def empiler(self,elt):
        "empile"
        self.liste.append(elt)

#####

class Calculatrice:
    def __init__(self, window):
        """Construit et lance la calculatrice"""
        self.operation = Operation(window)

        """touches numériques"""
        indice = 0
        for i in range(2, 5):
            for j in range(3):
                self.bouton = Button(window, width=10, height=3, text=str(NOMBRES[indice]), command=lambda nombre=indice+1: self.operation.affiche(nombre), bg="lightgreen")
                self.bouton.grid(row=i, column=j, padx=5, pady=2)
                indice += 1

        """boutons pour supprimer un ou des elements et le bouton '='"""
        self.bouton_suppr = Button(window, width=10, height=3, text='suppr', bg="lightgreen", command=lambda: self.operation.efface_tout())
        self.bouton_suppr.grid(row=2, column=3, padx=5, pady=2, rowspan=2, sticky="NSEW")

        self.bouton_supp_un = Button(window, width=10, height=3, text='<--', bg="lightgreen", command=lambda: self.operation.efface_un_caractere())
        self.bouton_supp_un.grid(row=4, column=3, padx=5, pady=2)

        self.bouton_egal = Button(window, width=10, height=3, text='=', bg="lightgreen", command=self.operation.calcul)
        self.bouton_egal.grid(row=5, column=3, padx=5, pady=2)

        """boutons de calcul"""
        indice = 0
        for i in range(2, 6):
            for j in range(4, 6):
                self.bouton = Button(window, width=10, height=3, text=str(SIGNES[indice]), command=lambda nombre=SIGNES[indice]: self.operation.affiche(nombre), bg="lightgreen")
                self.bouton.grid(row=i, column=j, padx=5, pady=2)
                indice += 1

        """boutons 0 et virgule"""
        self.bouton_virgule = Button(window, width=10, height=3, text='.', bg="lightgreen", command=lambda: self.operation.affiche('.'))
        self.bouton_virgule.grid(row=5, column=0, padx=5, pady=2)

        self.bouton_zero = Button(window, width=10, height=3, text=str(0), command=lambda: self.operation.affiche(0), bg="lightgreen")
        self.bouton_zero.grid(row=5, column=1, padx=5, pady=2, columnspan=2, sticky="NSEW")

        """bouton de paranthèses"""
        self.bouton = Button(window, width=10, height=3, text=SIGNES2[0], command=lambda: self.operation.affiche(SIGNES2[0]), bg="lightgreen")
        self.bouton.grid(row=2, column=6, padx=5, pady=2, rowspan=2, sticky="NSEW")

        self.bouton = Button(window, width=10, height=3, text=SIGNES2[1], command=lambda: self.operation.affiche(SIGNES2[1]), bg="lightgreen")
        self.bouton.grid(row=4, column=6, padx=5, pady=2, rowspan=2, sticky="NSEW")

#####


class Operation:
    def __init__(self, window):
        """Construit et lance les fonctions des opérations effectuées par la calculatrice"""
        self.barre_affichage = Label(window, font=("Courier", 20), bg="white")
        self.barre_affichage.grid(row=0, column=0, columnspan=7, padx=5, pady=5, sticky="NSEW")

        self.barre_calcul = Label(window, font=("Courier", 20), bg="white")
        self.barre_calcul.grid(row=1, column=0, columnspan=7, padx=5, pady=5, sticky="NSEW")

    def affiche(self, nombre):
        """Affiche en direct le chiffre ou le signe saisi"""
        texte = self.barre_calcul['text']
        if len(texte) < 38:
            if texte in ERREUR:
                texte = ''
            self.barre_calcul['text'] = texte + str(nombre)

    def calcul(self):
        """Effectue le calcul du label calcul
        Elle est appelée par la touche 'entrée' du clavier ou le '=' de la calculatrice"""
        self.valeurs = self.barre_calcul['text']
        try:
            if self.verification_parenthese(self.valeurs):
                resultat = eval(str(self.valeurs))
                if len(str(resultat)) > 15:
                    resultat = format(resultat, '.5E')
                self.barre_calcul['text'] = str(resultat)
                self.affiche_calcul(resultat)
            else:
                self.barre_calcul['text'] = ERREUR[4]
        except OverflowError:
            self.barre_calcul['text'] = ERREUR[0]
        except ZeroDivisionError:
            self.barre_calcul['text'] = ERREUR[1]
        except ValueError:
            self.barre_calcul['text'] = ERREUR[2]
        except:
            self.barre_calcul['text'] = ERREUR[3]

    def verification_parenthese(self, valeurs):
        """Vérifie si le nombre de parenthèse est juste"""
        pile = Pile()
        for elt in valeurs:
            if elt == "(":
                pile.empiler(elt)
            elif elt == ")":
                if not pile.vide():
                    pile.depiler()
                else:
                    return False
        if not pile.vide():
            return False
        return True

    def affiche_calcul(self, resultat):
        """Affiche sur le label affichage le dernier calcul effectué"""
        result = self.valeurs + ' = ' + str(resultat)
        if len(result) > 38:
            self.barre_affichage['text'] = str(resultat)
        else:
            self.barre_affichage['text'] = result

    def efface_un_caractere(self):
        """Supprime le dernier caractere du label de calcul"""
        texte = self.barre_calcul['text']
        if texte in ERREUR:
            texte = ''
        self.barre_calcul['text'] = texte[:-1]

    def efface_tout(self):
        """Supprime tout ce qu'il y avait dans le label de calcul"""
        self.barre_calcul['text'] = ''

#####


class Explication:
    def __init__(self, window2):
        """Construit et lance la fenêtre d'explication"""
        self.titre = Label(window2, font=("Comic Sans MS", 14, 'bold'), padx=10, pady=5, bg='#c4e5ff')
        self.titre.grid()

        self.label = Label(window2, font=("Comic Sans MS", 12), padx=10, pady=10, borderwidth=7, relief="groove", bg='#c4e5ff')
        self.label.grid()

        self.vide = Label(window2, bg='#c4e5ff')
        self.vide.grid()

        self.bouton = Button(window2, text='Cliquer ici pour lancer la calculatrice', command=window2.destroy, bg="lightblue")
        self.bouton.grid()

        self.vide = Label(window2, bg='#c4e5ff')
        self.vide.grid()

        self.texte_label()

    def texte_label(self):
        """Affiche le texte de la fenêtre de présentation"""
        self.titre['text'] = "Fonctionnement de la calculatrice\n"

        self.label['text'] += "- Vous pouvez appuyer sur les boutons ou les touches correspondantes pour écrire un calcul\n"
        self.label['text'] += "- La racine carré est représentée par sqrt( ou en appuyant sur la touche 'v' du clavier\n"
        self.label['text'] += "- // correspond à la division euclidienne et % au reste de la division euclidienne\n"
        self.label['text'] += "- ** correspond à l'exposant pour une puissance\n"
        self.label['text'] += "- suppr supprime tous les caractères et <-- supprime le dernier\n"
        self.label['text'] += "- Au clavier, 'entrée' pour afficher le résultat, 'suppr' ou 'echap' pour tout effacer et 'delete' pour effacer le dernier caractère"

#####


def creation_touches(window, calculatrice):
    """Relie les touches du clavier aux opérations qu'elles peuvent effectuer
    Remarque : Cela aurait pu probablement être crée dans une boucle pour éviter les répétitions
    mais je n'ai pas réussi à le rendre fonctionnel dans un boucle"""
    window.bind("1", lambda event: calculatrice.operation.affiche(1))
    window.bind("2", lambda event: calculatrice.operation.affiche(2))
    window.bind("3", lambda event: calculatrice.operation.affiche(3))
    window.bind("4", lambda event: calculatrice.operation.affiche(4))
    window.bind("5", lambda event: calculatrice.operation.affiche(5))
    window.bind("6", lambda event: calculatrice.operation.affiche(6))
    window.bind("7", lambda event: calculatrice.operation.affiche(7))
    window.bind("8", lambda event: calculatrice.operation.affiche(8))
    window.bind("9", lambda event: calculatrice.operation.affiche(9))
    window.bind("0", lambda event: calculatrice.operation.affiche(0))
    window.bind(".", lambda event: calculatrice.operation.affiche('.'))
    window.bind("*", lambda event: calculatrice.operation.affiche('*'))
    window.bind("/", lambda event: calculatrice.operation.affiche('/'))
    window.bind("-", lambda event: calculatrice.operation.affiche('-'))
    window.bind("+", lambda event: calculatrice.operation.affiche('+'))
    window.bind(")", lambda event: calculatrice.operation.affiche(')'))
    window.bind("(", lambda event: calculatrice.operation.affiche('('))
    window.bind("%", lambda event: calculatrice.operation.affiche('%'))


def creation_touches2(window, calculatrice):
    """Relie les touches du clavier aux opérations qu'elles peuvent effectuer
    Remarque : Cela aurait pu probablement être crée dans une boucle pour éviter les répétitions
    mais je n'ai pas réussi à le rendre fonctionnel dans un boucle"""
    window.bind("<BackSpace>", lambda event: calculatrice.operation.efface_un_caractere())
    window.bind("<Delete>", lambda event: calculatrice.operation.efface_tout())
    window.bind("<Escape>", lambda event: calculatrice.operation.efface_tout())
    window.bind("<Return>", lambda event: calculatrice.operation.calcul())
    window.bind("v", lambda event: calculatrice.operation.affiche('sqrt('))

#####


def main():
    """fonction permettant de lancer les fenêtres"""
    window2 = Tk()
    window2.configure(bg='#c4e5ff')
    explication = Explication(window2)
    window2.title('Explications')
    window2.mainloop()
    window = Tk()
    calculatrice = Calculatrice(window)
    window.configure(bg='grey')
    window.resizable(0, 0)
    creation_touches(window, calculatrice)
    creation_touches2(window, calculatrice)
    window.title('Calculatrice')
    window.mainloop()

main()