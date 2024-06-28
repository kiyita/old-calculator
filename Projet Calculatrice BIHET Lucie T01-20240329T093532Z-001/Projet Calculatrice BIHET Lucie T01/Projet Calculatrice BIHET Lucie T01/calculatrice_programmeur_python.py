from tkinter import *
from math import *

#####
"""Variables globales"""

NOMBRES = [i for i in range(1, 10)] + [0]
SIGNES = ['+', '-', '*']
ERREUR = ['valeur trop élevée', 'division par 0']
ERREUR += ['calcul impossible', "mauvaise syntaxe"]
LETTRES = ['a', 'b', 'c', 'd', 'e', 'f']

#####


class Calculatrice:
    def __init__(self, window):
        """Construit et lance la calculatrice"""
        self.operation = Operation(window)

        """boutons des modes"""
        self.bouton_dec = Button(window, width=5, height=2, text='dec', command=lambda: self.selection_mode_dec(window), bg='yellow')
        self.bouton_dec.grid(row=0, column=0, padx=5, pady=5)

        self.bouton_bin = Button(window, width=5, height=2, text='bin', command=lambda: self.selection_mode_bin(window), bg='#fbcfff')
        self.bouton_bin.grid(row=0, column=1, padx=5, pady=5)

        self.bouton_hex = Button(window, width=5, height=2, text='hex', command=lambda: self.selection_mode_hex(window), bg='#cfecff')
        self.bouton_hex.grid(row=0, column=2, padx=5, pady=5)

        """boutons des lettres"""
        indice = 0
        for i in range(4, 7):
            for j in range(2):
                self.bouton = Button(window, width=10, height=3, text=str(LETTRES[indice]), command=lambda nombre=LETTRES[indice]: self.operation.affiche(nombre), bg="lightgreen")
                self.bouton.grid(row=i, column=5+j, padx=5, pady=2)
                indice += 1

        """touches numériques"""
        indice = 0
        for i in range(4, 7):
            for j in range(3):
                self.bouton = Button(window, width=10, height=3, text=str(NOMBRES[indice]), command=lambda nombre=indice+1: self.operation.affiche(nombre), bg="lightgreen")
                self.bouton.grid(row=i, column=j, padx=5, pady=2)
                indice += 1

        """boutons pour supprimer un ou des elements"""
        self.bouton_suppr = Button(window, width=10, height=3, text='suppr', bg="lightgreen", command=lambda: self.operation.efface_tout())
        self.bouton_suppr.grid(row=4, column=3, padx=5, pady=2, rowspan=2, sticky="NSEW")

        self.bouton_supp_un = Button(window, width=10, height=3, text='<--', bg="lightgreen", command=lambda: self.operation.efface_un_caractere())
        self.bouton_supp_un.grid(row=6, column=3, padx=5, pady=2)

        """boutons de calcul"""
        for j in range(4, 7):
            self.bouton = Button(window, width=10, height=3, text=str(SIGNES[j-4]), command=lambda nombre=SIGNES[j-4]: self.operation.affiche(nombre), bg="lightgreen")
            self.bouton.grid(row=j, column=4, padx=5, pady=2)

        self.bouton_zero = Button(window, width=10, height=3, text=str(0), command=lambda: self.operation.affiche(0), bg="lightgreen")
        self.bouton_zero.grid(row=7, column=1, padx=5, pady=2, columnspan=2, sticky="NSEW")

    def selection_mode_dec(self, window):
        """fait passer au mode decimal"""
        self.operation.passage_mode_dec(window)
        self.bouton_dec['bg'] = 'yellow'
        self.bouton_bin['bg'] = '#fbcfff'
        self.bouton_hex['bg'] = '#cfecff'

    def selection_mode_bin(self, window):
        """fait passer au mode binaire"""
        self.operation.passage_mode_bin(window)
        self.bouton_bin['bg'] = 'yellow'
        self.bouton_dec['bg'] = '#ffcfd9'
        self.bouton_hex['bg'] = '#cfecff'

    def selection_mode_hex(self, window):
        """fait passer au mode hexadecimal"""
        self.operation.passage_mode_hex(window)
        self.bouton_hex['bg'] = 'yellow'
        self.bouton_dec['bg'] = '#ffcfd9'
        self.bouton_bin['bg'] = '#fbcfff'


#####


class Operation:
    def __init__(self, window):
        """Construit et lance les fonctions des opérations effectuées par la calculatrice"""
        self.barre_decimal = Label(window, font=("Courier", 15), bg="#ffcfd9")
        self.barre_decimal.grid(row=1, column=0, columnspan=7, padx=5, pady=5, sticky="NSEW")

        self.barre_binaire = Label(window, font=("Courier", 15), bg="#fbcfff")
        self.barre_binaire.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky="NSEW")

        self.barre_hexa = Label(window, font=("Courier", 15), bg="#cfecff")
        self.barre_hexa.grid(row=3, column=0, columnspan=7, padx=5, pady=5, sticky="NSEW")

        self.bouton_egal = Button(window, width=10, height=3, text='=', bg="lightgreen", command=self.calcul_decimal)
        self.bouton_egal.grid(row=7, column=3, padx=5, pady=2)

        self.mode = 0

    def passage_mode_dec(self, window):
        """Fait passer la calculatrice en mode décimal"""
        self.efface_tout()
        self.bouton_egal = Button(window, width=10, height=3, text='=', bg="lightgreen", command=self.calcul_decimal)
        self.bouton_egal.grid(row=7, column=3, padx=5, pady=2)
        self.mode = 0

    def passage_mode_bin(self, window):
        """Fait passer la calculatrice en mode binaire"""
        self.efface_tout()
        self.mode = 2
        self.bouton_egal = Button(window, width=10, height=3, text='=', bg="lightgreen", command=self.calcul_binaire)
        self.bouton_egal.grid(row=7, column=3, padx=5, pady=2)

    def passage_mode_hex(self, window):
        """Fait passer la calculatrice en mode hexadécimal"""
        self.efface_tout()
        self.mode = 16
        self.bouton_egal = Button(window, width=10, height=3, text='=', bg="lightgreen", command=self.calcul_hexa)
        self.bouton_egal.grid(row=7, column=3, padx=5, pady=2)

    def affiche(self, nombre):
        """Affiche en direct le chiffre ou le signe saisi"""
        if self.mode == 0:
            self.mode_decimal(nombre)
        elif self.mode == 2:
            self.mode_binaire(nombre)
        else:
            self.mode_hexa(nombre)

    def mode_decimal(self, nombre):
        """Affiches les valeurs dans le label decimal"""
        texte = self.barre_decimal['text']
        if len(texte) < 31:
            if nombre in NOMBRES or nombre in SIGNES:
                if texte in ERREUR:
                    texte = ''
                if texte == '':
                    self.barre_decimal['text'] = texte + str(nombre)
                elif texte[-1] in SIGNES and nombre == SIGNES[-1]:
                    self.barre_decimal['text'] = texte + ''
                else:
                    self.barre_decimal['text'] = texte + str(nombre)

    def mode_binaire(self, nombre):
        """Affiches les valeurs dans le label binaire"""
        texte = self.barre_binaire['text']
        if len(texte) < 51:
            if nombre in (1, 0, '*', '-', '+'):
                if texte in ERREUR:
                    texte = ''
                if texte == '':
                    self.barre_binaire['text'] = texte + str(nombre)
                elif texte[-1] in SIGNES and nombre == SIGNES[-1]:
                    self.barre_binaire['text'] = texte + ''
                else:
                    self.barre_binaire['text'] = texte + str(nombre)

    def mode_hexa(self, nombre):
        """Affiches les valeurs dans le label hexadecimale"""
        texte = self.barre_hexa['text']
        if len(texte) < 26:
            if texte in ERREUR:
                texte = ''
            if texte == '':
                self.barre_hexa['text'] = texte + str(nombre)
            elif texte[-1] in SIGNES and nombre == SIGNES[-1]:
                self.barre_hexa['text'] = texte + ''
            else:
                self.barre_hexa['text'] = texte + str(nombre)

    def calcul_mode(self):
        """Appelle la fonction nécessaire selon le type de calcul"""
        if self.mode == 0:
            self.calcul_decimal()
        elif self.mode == 2:
            self.calcul_binaire()
        else:
            self.calcul_hexa()

    def calcul_decimal(self):
        """Calcule les valeurs decimales"""
        valeurs = self.barre_decimal['text']
        try:
            resultat = eval(valeurs)
            #if len(str(resultat)) > 20:
            #resultat = format(resultat, '.5E')
            self.barre_decimal['text'] = str(resultat)
            self.calcul_decimal_exception(resultat)
        except OverflowError:
            self.barre_decimal['text'] = ERREUR[0]
        except ValueError:
            self.barre_decimal['text'] = ERREUR[2]
        except:
            self.barre_decimal['text'] = ERREUR[3]

    def calcul_decimal_exception(self, resultat):
        """Gère les execption de calcul decimal (quand c'est des valeurs négatives)"""
        if int(resultat) > 0:
            result = bin(resultat)[2:]
            self.barre_binaire['text'] = result
            result = hex(resultat)[2:]
            self.barre_hexa['text'] = result
        else:
            result = bin(resultat)[3:]
            self.barre_binaire['text'] = '-' + result
            result = hex(resultat)[3:]
            self.barre_hexa['text'] = '-' + result

    def calcul_binaire(self):
        """Calcule les valeurs binaires"""
        try:
            valeurs = self.barre_binaire['text']
            liste_binaire = []
            nombre_binaire = ''
            for i in range(len(valeurs)):
                if valeurs[i] in SIGNES:
                    if nombre_binaire != '':
                        liste_binaire.append(str(int(nombre_binaire, 2)))
                    nombre_binaire = ''
                    liste_binaire.append(str(valeurs[i]))
                else:
                    nombre_binaire += str(valeurs[i])
            liste_binaire.append(str(int(nombre_binaire, 2)))
            result = "".join(liste_binaire)
            self.calcul_binaire_exception(result)
        except:
            self.barre_binaire['text'] = ERREUR[3]

    def calcul_binaire_exception(self, result):
        """Gère les execption de calcul bianire (quand c'est des valeurs négatives)"""
        if eval(result) > 0:
            self.barre_binaire['text'] = str(bin(eval(result))[2:])
            resultat = hex(eval(result))[2:]
            self.barre_hexa['text'] = resultat
        else:
            self.barre_binaire['text'] = '-' + str(bin(eval(result))[3:])
            resultat = hex(eval(result))[3:]
            self.barre_hexa['text'] = '-' + str(resultat)
        resultat = int(eval(result))
        self.barre_decimal['text'] = resultat

    def calcul_hexa(self):
        """Calcule les valeurs hexadecimales"""
        valeurs = self.barre_hexa['text']
        try:
            liste_hexa = []
            nombre_hexa = ''
            for i in range(len(valeurs)):
                if valeurs[i] in SIGNES:
                    if nombre_hexa != '':
                        liste_hexa.append(str(int(nombre_hexa, 16)))
                    nombre_hexa = ''
                    liste_hexa.append(str(valeurs[i]))
                else:
                    nombre_hexa += str(valeurs[i])
            liste_hexa.append(str(int(nombre_hexa, 16)))
            result = "".join(liste_hexa)
            self.calcul_hexa_exception(result)
        except:
            self.barre_hexa['text'] = ERREUR[3]

    def calcul_hexa_exception(self, result):
        """gère les execption de calcul hexadecimal (quand c'est des valeurs négatives)"""
        if eval(result) > 0:
            self.barre_hexa['text'] = str(hex(eval(result))[2:])
            resultat = bin(eval(result))[2:]
            self.barre_binaire['text'] = resultat
        else:
            self.barre_hexa['text'] = '-' + str(hex(eval(result))[3:])
            resultat = bin(eval(result))[3:]
            self.barre_binaire['text'] = '-' + str(resultat)
        resultat = int(eval(result))
        self.barre_decimal['text'] = resultat

    def efface_un_caractere(self):
        """Supprime le dernier caractere du label de calcul"""
        if self.mode == 0:
            texte = self.barre_decimal['text']
            if texte in ERREUR:
                texte = ''
            self.barre_decimal['text'] = texte[:-1]
        elif self.mode == 2:
            texte = self.barre_binaire['text']
            if texte in ERREUR:
                texte = ''
            self.barre_binaire['text'] = texte[:-1]
        else:
            texte = self.barre_hexa['text']
            if texte in ERREUR:
                texte = ''
            self.barre_hexa['text'] = texte[:-1]

    def efface_tout(self):
        """Supprime tout ce qu'il y avait dans les labels de calcul"""
        self.barre_decimal['text'] = ''
        self.barre_binaire['text'] = ''
        self.barre_hexa['text'] = ''


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
    window.bind("a", lambda event: calculatrice.operation.affiche('a'))
    window.bind("b", lambda event: calculatrice.operation.affiche('b'))
    window.bind("c", lambda event: calculatrice.operation.affiche('c'))
    window.bind("d", lambda event: calculatrice.operation.affiche('d'))
    window.bind("e", lambda event: calculatrice.operation.affiche('e'))
    window.bind("f", lambda event: calculatrice.operation.affiche('f'))


def creation_touches2(window, calculatrice):
    """Relie les touches du clavier aux opérations qu'elles peuvent effectuer
    Remarque : Cela aurait pu probablement être crée dans une boucle pour éviter les répétitions
    mais je n'ai pas réussi à le rendre fonctionnel dans un boucle"""
    window.bind("*", lambda event: calculatrice.operation.affiche('*'))
    window.bind("-", lambda event: calculatrice.operation.affiche('-'))
    window.bind("+", lambda event: calculatrice.operation.affiche('+'))
    window.bind("<BackSpace>", lambda event: calculatrice.operation.efface_un_caractere())
    window.bind("<Delete>", lambda event: calculatrice.operation.efface_tout())
    window.bind("<Escape>", lambda event: calculatrice.operation.efface_tout())
    window.bind("<Return>", lambda event: calculatrice.operation.calcul_mode())


#####


def main():
    """fonction permettant de lancer la fenêtre"""
    window = Tk()
    calculatrice = Calculatrice(window)
    window.configure(bg='grey')
    window.resizable(0, 0)
    creation_touches(window, calculatrice)
    creation_touches2(window, calculatrice)
    window.title('Calculatrice Programmeur')
    window.mainloop()

main()
