#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector
import logging


class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
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
    
    #def totes_pag(self, id=None) -> List[Pelicula]:
        #pass
        #falta codi
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        if id is None:
            query = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA ORDER BY id LIMIT 10;"
            cursor.execute(query)
        else:
            query = f"SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE id > {id} ORDER BY id LIMIT 10;"
            cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
            resultat.append(pelicula)
        return resultat




    def desa(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = "INSERT INTO PELICULA (ID, TITULO, ANYO, PUNTUACION, VOTOS) VALUES (%s, %s, %s, %s, %s)"
        val = (pelicula.id, pelicula.titol,pelicula.any,pelicula.puntuacio,pelicula.vots)
        cursor.execute(query,val)
        self._conn.commit()
        
        #pass
        #falta codi
    
    def llegeix(self, any: int) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = f"SELECT * FROM PELICULA WHERE ANYO = {any}"
        cursor.execute(query)
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
        #pass
        #falta codi
    
    def canvia(self,pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor(buffered=True)
        query = f"UPDATE PELICULA SET ID = {pelicula.id}, TITULO = {pelicula.titol}, ANYO = {pelicula.any}, PUNTUACION = {pelicula.puntuacio}, VOTOS = {pelicula.vots}"
        cursor.execute(query)
        self._conn.commit()
        #pass
        #falta codi
