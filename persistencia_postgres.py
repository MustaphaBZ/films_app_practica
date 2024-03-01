#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector
import psycopg
import logging


class Persistencia_postgres(IPersistencia_pelicula):
    def __init__(self, credencials) -> None: 
        self._credencials = credencials
        host=credencials["host"]
        user=credencials["user"]
        password=credencials["password"]
        database=credencials["database"]
        logging.basicConfig(filename="pelicules.log", encoding='utf-8', level=logging.DEBUG)
        self._conn = psycopg.connect(f"host={host} dbname={database} user={user} password={password}")
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM PELICULA;")
        except(Exception, psycopg.Error):
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        cursor = self._conn.cursor()
        
        query = f"SELECT * FROM PELICULA WHERE ID >= {id} ORDER BY ID LIMIT 10"
        cursor.execute(query)
        
        registres = cursor.fetchall()
        
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
            resultat.append(pelicula)
        logging.info(f"S'ha rebut 10 pel·lícules a partir d'aquesta id: {pelicula.id}") 
        return resultat




    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        query = "INSERT INTO PELICULA (ID, TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s, %s)"
        val = (pelicula.id, pelicula.titol,pelicula.any,pelicula.puntuacio,pelicula.vots)
        cursor.execute(query,val)
        self._conn.commit()
        logging.info(f"S'ha afegit la pel·licula: {pelicula.id}") 
        
        
    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor()
        
        cursor.execute(f"SELECT * FROM PELICULA WHERE ANYO = {any}")
        registres = cursor.fetchall()
        
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
            print(pelicula)
        logging.info(f"Lectura de les pel·lícules d'aquest any: {any}")    
        return resultat
        
        
    
    def canvia(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        query = "UPDATE PELICULA SET TITULO = %s, ANYO = %s, PUNTUACION = %s, VOTOS = %s WHERE ID = %s"
        values = (pelicula.titol, pelicula.any, pelicula.puntuacio, pelicula.vots, pelicula.id)
        cursor.execute(query, values)
        self._conn.commit()
        logging.info(f"Modificació de la pel·lícula: {pelicula.id}") 

        
