import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from bdd import BDD


class AffichageGraphique(tk.Tk):

    def __init__(self):
        # Création du la fenêtre
        self.root = tk.Tk()
        self.root.title("BREIZHIBUS")
        self.root.geometry("720x480")
        self.root.minsize(480, 360)
        self.root.iconbitmap("gwen-ha-du.ico")
        self.root.config(background='#41B77F')

        # Connexion avec la base de données
        self.bdd = BDD()
        
        # Création du label bus
        self.lbLignebus = tk.Label(self.root, text ="FLOTTE BUS :", font=("Comic Sans MS", 10), bg="darkblue", fg="white")
        self.lbLignebus.place(x=180, y=0, width = 440)

        # Création des 4 champs et de leurs entrées (saisie utilisateurs)
        self.tabEntry = []

        self.lblNumero = tk.Label(self.root, text = "Numero de bus :", bg="black", fg="yellow")
        self.lblNumero.place(x=5, y=50, width = 125)
        self.entryNumero = tk.Entry(self.root)
        self.entryNumero.place(x=140, y=50, width = 400)
        self.tabEntry.append(self.entryNumero)

        self.lblImmat = tk.Label(self.root, text = "Immatriculation:", bg="black", fg="yellow")
        self.lblImmat.place(x=5, y=80, width = 125)
        self.entryImmat = tk.Entry(self.root)
        self.entryImmat.place(x=140, y=80, width = 400)
        self.tabEntry.append(self.entryImmat)

        self.lblNbeplaces = tk.Label(self.root, text = "Nombre de places:", bg="black", fg="yellow")
        self.lblNbeplaces.place(x=5, y=110, width = 125)
        self.entryNbeplaces = tk.Entry(self.root)
        self.entryNbeplaces.place(x=140, y=110, width = 400)
        self.tabEntry.append(self.entryNbeplaces)

        self.lblligne = tk.Label(self.root, text = "N° de ligne:", bg="black", fg="yellow")
        self.lblligne.place(x=5, y=140, width = 125)
        self.entryIdligne = tk.Entry(self.root)
        self.entryIdligne.place(x=140, y=140, width = 320)
        self.tabEntry.append(self.entryIdligne)
        
        # Création du tableau
        self.insertTableau()

        # Bouton interface d'actions utilisateurs
        self.bAdd = tk.Button(self.root, text = "Ajouter bus:", bg="darkblue", fg="yellow", command=self.add_bus) # Lambda permet de passer un paramètre à la fonction  
        self.bAdd.place(x=5, y=170, width = 255)

        self.bDelete = tk.Button(self.root, text = "Supprimer bus:", bg="darkblue", fg="yellow", command = self.delete_bus)
        self.bDelete.place(x=5, y=205, width = 255)

        self.bMaj = tk.Button(self.root, text = "MAJ bus*:", bg="darkblue", fg="yellow", command = self.generationUpdate)
        self.bMaj.place(x=5, y=240, width = 255)

        self.bExit = tk.Button(self.root, text = "Exit App:", bg="darkblue", fg="yellow", command = quit)
        self.bExit.place(x=5, y=310, width = 255)

        self.bligne = tk.Button(self.root, text = "Aff lignes*:", bg="darkblue", fg="red", command = self.generationUpdate2)
        self.bligne.place(x=265, y=400, width = 255)


        # Insertion image dans l'appli
        load = Image.open("C:/Users/utilisateur/Google Drive/microsoft_ia/Google Drive/projets/breizhibus/bus.jpg")
        load.thumbnail((130,130))
        photo = ImageTk.PhotoImage(load)
        self.label_image = tk.Label(self.root, image = photo)
        self.label_image.place(x=10, y=350)

        self.root.mainloop()




    def add_bus(self):
        Numero = self.entryNumero.get()
        Immat = self.entryImmat.get()
        Nbeplaces = self.entryNbeplaces.get()
        Idligne = self.entryIdligne.get()
        # Transfère les données dans la BBD
        self.bdd.dbAddBus(Numero, Immat, Nbeplaces, Idligne)
        # Insère les informations dans le tableau affiché dans l'appli
        self.insertTableau()
        # Nettoie les infos saisie
        self.refreshChamps()

   

    def delete_bus(self):
        # On récupère les valeurs et on les supprime côté appli
        print(self.tree.item(self.tree.focus()))
        tags = self.tree.item(self.tree.focus())['tags']
        self.tree.delete(self.tree.focus())
        # Supprime dans la bdd le bus avec l'id= tags[0]
        self.bdd.dbDeleteBus(tags[0])
        
    def insertTableau(self):
        # Colonnes en bas à droite tableau pour afficher les données d une table sql
        self.tree = ttk.Treeview(self.root, columns = (1, 2, 3, 4), height = 5 , show = "headings")
        self.tree.place(x=265, y=170, width = 300, height=175)

        self.tree.heading(1, text = "Numero")
        self.tree.heading(2, text = "Immat")
        self.tree.heading(3, text = "Nbeplaces")
        self.tree.heading(4, text = "Idligne")

        self.tree.column(1, width = 75)
        self.tree.column(2, width = 75)
        self.tree.column(3, width = 75)
        self.tree.column(4, width = 75)

        # Affichage des bus
        bus = self.bdd.dbDisplayBus()
        for row in bus:
            #print(row)
            # Insertion des informations relatives au bus dans le tableau (les id ne sont pas affichés par nous avons indiqué tags =0)
            self.tree.insert('', 'end', values = (row[1],row[2], row[3],row[4]), tags= row[0])

    # Vide les champs saisis (exemple pour l'ajout de bus)
    def refreshChamps(self):
        for entre in self.tabEntry:
            entre.delete(0,'end')

    # Mettre à jour les champs affichés dans le tableau et dans la bdd, pour cela on crée une zone de sasie dans une fenetre popup
    def generationUpdate(self):
        #REVENIR SUR CE CHAMPS
        datas = self.tree.item(self.tree.focus())
        #print(datas)
        # Ouverture d'une fenêtre secondaire
        self.popup = tk.Toplevel(self.root)
        self.popup.minsize(480, 360)
        self.popup.iconbitmap("gwen-ha-du.ico")

        # Création du label bus
        self.lbLignebus2 = tk.Label(self.popup, text ="MAJ BUS : (modifier le champs)", font=("Comic Sans MS", 10), bg="darkblue", fg="white")
        self.lbLignebus2.place(x=20, y=0, width = 440)
       
        # On recrée un tableau, mêmes informations que dans la fenêtre principale
        self.lblNumero2 = tk.Label(self.popup, text = "Numero de bus :", bg="black", fg="yellow")
        self.lblNumero2.place(x=5, y=50, width = 125)
        self.entryNumero2 = tk.Entry(self.popup)
        #?
        self.entryNumero2.insert(0, datas['values'][0])
        self.entryNumero2.place(x=140, y=50, width = 400)

        self.lblImmat2 = tk.Label(self.popup, text = "Immatriculation:", bg="black", fg="yellow")
        self.lblImmat2.place(x=5, y=80, width = 125)
        self.entryImmat2 = tk.Entry(self.popup)
        self.entryImmat2.insert(0, datas['values'][1])
        self.entryImmat2.place(x=140, y=80, width = 400)

        self.lblNbeplaces2 = tk.Label(self.popup, text = "Nombre de places:", bg="black", fg="yellow")
        self.lblNbeplaces2.place(x=5, y=110, width = 125)
        self.entryNbeplaces2 = tk.Entry(self.popup)
        self.entryNbeplaces2.insert(0, datas['values'][2])
        self.entryNbeplaces2.place(x=140, y=110, width = 400)

        self.lblligne2 = tk.Label(self.popup, text = "N° de ligne:", bg="black", fg="yellow")
        self.lblligne2.place(x=5, y=140, width = 125)
        self.entryIdligne2 = tk.Entry(self.popup)
        self.entryIdligne2.insert(0, datas['values'][3])
        self.entryIdligne2.place(x=140, y=140, width = 320)

        self.bMaj2 = tk.Button(self.popup, text = "Validation MAJ bus:", bg="darkblue", fg="yellow", command = lambda: self.majUpdate(datas['tags'][0]))#lamda pour permettre de mettre plusieurs paramètre à la fonction, tag permet de ne pas afficher la valeur
        self.bMaj2.place(x=105, y=240, width = 255)

    def majUpdate(self, id):
        Numero = self.entryNumero2.get()
        Immat = self.entryImmat2.get()
        Nbeplaces = self.entryNbeplaces2.get()
        Idligne = self.entryIdligne2.get()

        self.popup.destroy()
        self.bdd.dbModifyBus(id, Numero, Immat, Nbeplaces, Idligne)
        self.insertTableau()
    
    def generationUpdate2(self):
        #REVENIR SUR CE CHAMPS
        # datas = self.tree.item(self.tree.focus())
        #print(datas)
        # Ouverture d'une fenêtre secondaire
        self.popup = tk.Toplevel(self.root)
        self.popup.minsize(480, 360)
        self.popup.iconbitmap("gwen-ha-du.ico")

        
        list_lignes = self.bdd.dbSelectBus()
        self.combolistlignes = ttk.Combobox(self.popup, values = list_lignes)
        self.combolistlignes.place(x=0, y=0, width = 125)
        #bouton pour afficher arrets
        self.bligne = tk.Button(self.popup, text = "Affichage bus & arrêts", bg="darkblue", fg="yellow", command = self.lienlignearret)
        self.bligne.place(x=265, y=0, width = 255)
        
        
    def lienlignearret(self):
        #récupère la valeur de notre combolist
        ligneselectionnee=self.combolistlignes.get()
        #on appelle la requete avec notre ligne selectionnée
        x = self.bdd.dbafficher_arret(ligneselectionnee)
        y= self.bdd.dbrequete_recuperation_ligne(ligneselectionnee)

        # Colonnes en bas à droite tableau pour afficher les données d une table sql
        self.btitre = tk.Button(self.popup, text = "Arrêts", bg="darkblue", fg="yellow")
        self.btitre.place(x=240, y=50, width = 215)

        self.tree2 = ttk.Treeview(self.popup, columns = (1, 2), height = 5 , show = "headings")
        self.tree2.place(x=240, y=80, width = 215, height=175)

        self.tree2.heading(1, text = "Nom")
        self.tree2.heading(2, text = "Adresse")


        self.tree2.column(1, width = 75)
        self.tree2.column(2, width = 130)

        self.btitre3 = tk.Button(self.popup, text = "Bus", bg="darkblue", fg="yellow")
        self.btitre3.place(x=50, y=50, width = 160)

        self.tree3 = ttk.Treeview(self.popup, columns = (1, 2), height = 5 , show = "headings")
        self.tree3.place(x=50, y=80, width = 160, height=175)

        self.tree3.heading(1, text = "Numero")
        self.tree3.heading(2, text = "Immat")


        self.tree3.column(1, width = 75)
        self.tree3.column(2, width = 75)
    
        
        self.bExit = tk.Button(self.popup, text = "Exit", bg="darkblue", fg="yellow", command = quit)
        self.bExit.place(x=5, y=310, width = 255)


        # Affichage des bus
       
        for row in x:
            #print(row)
            # Insertion des informations relatives au bus dans le tableau (les id ne sont pas affichés par nous avons indiqué tags =0)
            self.tree2.insert('', 'end', values = (row[1],row[2]), tags= row[0])
        
        for row in y:
            #print(row)
            # Insertion des informations relatives au bus dans le tableau (les id ne sont pas affichés par nous avons indiqué tags =0)
            self.tree3.insert('', 'end', values = (row[1],row[2]), tags= row[0])




                

        








