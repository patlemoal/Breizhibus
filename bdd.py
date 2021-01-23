import mysql.connector

class BDD:
    # Connexion a la base sql
    def __init__(self):
        self.mydb=mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="root",
            database="lignesbus")
        self.cursor = self.mydb.cursor()

    # Fermeture de connexion 
    def dbCloseConnexion(self):
        self.cursor.close()


    # Ajouter bus
    def dbAddBus (self,numero, immatriculation, nombre_place, id_ligne):
        request = "INSERT INTO bus (numero, immatriculation, nombre_place, id_ligne) values (%s, %s, %s, %s)"
        parametre = (numero, immatriculation, nombre_place, id_ligne)
        self.cursor.execute(request, parametre)
        self.mydb.commit()
    
    # Supprimer bus
    def dbDeleteBus (self, id):
        self.cursor.execute("DELETE FROM bus WHERE id_bus = {}".format(id))
        self.mydb.commit()

    # Afficher bus
    def dbDisplayBus(self):
        self.cursor.execute("SELECT * FROM bus")
        bus = self.cursor.fetchall()
        return bus

    # Modifier les champs des lignes de bus en fonction de la necessité de la requête dans tkinter
    def dbModifyBus(self, id_bus, numero, immatriculation, nombre_place, id_ligne):
        request = "UPDATE bus SET numero = %s, immatriculation = %s, nombre_place = %s, id_ligne = %s WHERE id_bus = %s"
        parametre = (numero, immatriculation, nombre_place, id_ligne, id_bus, )
        self.cursor.execute(request, parametre)
        self.mydb.commit()

    def dbSelectBus(self):
        self.cursor.execute("SELECT id_ligne FROM lignes")
        ligne = self.cursor.fetchall()
        return ligne

    # Renvoie les lignes en saisisant un numéro de ligne
    def dbrequete_recuperation_ligne(self, ligne):
        sql = "SELECT * FROM bus WHERE id_ligne = %s "
        param = (ligne, )
        self.cursor.execute(sql, param)
        query = self.cursor.fetchall()
        return query 

    def dbafficher_arret(self, ligne):
        sql = "SELECT arrets.id_arret, noms, adresse FROM arrets JOIN arrets_lignes ON arrets.id_arret = arrets_lignes.id_arret JOIN lignes ON arrets_lignes.id_ligne = lignes.id_ligne WHERE lignes.id_ligne = %s"
        #sql = "SELECT * FROM arrets WHERE id_ligne = %s"

        param = (ligne, )
        self.cursor.execute(sql, param)
        query = self.cursor.fetchall()
        return query
                
  
    
    




 
 





               
    # # Renvoie les lignes de bus
    # def requete_recuperation_lignes(self):
    #     sql = "SELECT * FROM lignes"
    #     self.cursor.execute(sql)
    #     query = self.cursor.fetchall()
    #     return query 

    # # Renvoie les lignes en saisisant un numéro de ligne
    # def requete_recuperation_ligne(self, ligne):
    #     sql = "SELECT * FROM bus WHERE id_ligne = %s "
    #     param = (ligne, )
    #     self.cursor.execute(sql, param)
    #     query = self.cursor.fetchall()
    #     return query 

    # def afficher_arret(self, arret):
    #     sql = "SELECT noms, adresse FROM arrets JOIN arrets_lignes ON arrets.id_arret = arrets_lignes.id_arret JOIN lignes ON arrets_lignes.id_ligne = lignes.id_ligne WHERE nom = %s"
    #     #sql = "SELECT * FROM arrets WHERE id_ligne = %s"

    #     param = (arret, )
    #     self.cursor.execute(sql, param)
    #     query = self.cursor.fetchall()
    #     return query
    


    # def ajouter_bus(self, reference):
    #     sql = "SELECT * FROM bus where numero = %s LIMIT 1"
    #     adr = (reference[0], )
    #     self.cursor.execute(sql, adr)
    #     query = self.cursor.fetchall()
    #     print(query)
    #     if not query :
    #         self.cursor.execute("INSERT INTO bus (numero, immatriculation, nombre_place, id_ligne) VALUES (%s, %s, %s, %s)", reference) 
    #         self.mydb.commit()
    #         print("Enregistrement mis à jour avec succès")
    #     else : 
    #         print("l'enregistrement existe déjà")




    # def modifier_bus(self, nombre_place,id_bus):
    #     sql = "UPDATE bus SET nombre_place = %s WHERE id_bus = %s"
    #     param = (nombre_place, id_bus, )
    #     self.cursor.execute(sql, param)
    #     self.mydb.commit()
    #     print("Enregistrement mis à jour avec succès")



    # def supprimer_bus(self, nombre_place,id_bus):  
    #     sql = "DELETE FROM bus WHERE nombre_place = %s  AND id_bus = %s"
    #     param = (nombre_place, id_bus, )
    #     self.cursor.execute(sql,param)
    #     self.bdd.commit()
    #     print("Enregistrement mis à jour avec succès")



    # #saisir  la couleur du bus et cela nous ramène le nom des arrêts et les références des bus
    # def afficher_arret2(self,ligne):
    #     self.cursor.execute(f"""SELECT arrets.noms FROM arrets
    #                 JOIN arrets_lignes ON arrets.id_arret = arrets_lignes.id_arret 
    #                 JOIN lignes ON arrets_lignes.id_ligne = lignes.id_ligne 
    #                 WHERE lignes.nom = '{ligne}' ;""")
    #     arret = self.cursor.fetchall()

    #     self.cursor.execute(f"""SELECT bus.numero, bus.immatriculation FROM bus
    #                 JOIN lignes ON bus.id_ligne = lignes.id_ligne
    #                 WHERE lignes.nom = '{ligne}' ;""")    
    #     bus = self.cursor.fetchall()
    #     return(arret, bus)




# import tkinter as tk
# from bdd import BDD

# class AffichageGraphique(tk.Tk):

#     def __init__(self):
#         # Fenêtre 
#         self.root = tk.Tk()
#         self.root.title(" Breizibus ")

#         # Connexion avec la base de données
#         self.bdd = BDD()
        
#         # Boutton qui ferme l'application
#         self.closeButton = tk.Button(self.root, text = "Exit", command = self.closeApp)
#         self.closeButton.pack()

#         self.root.mainloop()
    
#     def closeApp(self):
#         self.bdd.dbCloseConnection()
#         self.root.destroy()
    