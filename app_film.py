#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from llistapelis import Llistapelis
#from app_film import desa
from pelicula import Pelicula
import logging

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
print(RUTA_FITXER_CONFIGURACIO)

def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    with open(ruta_fitxer_configuracio, 'r') as conf:
        config = yaml.safe_load(conf)
    return config

def get_persistencies(conf: dict) -> dict:
    credencials = {}
    if conf["base de dades"]["motor"].lower().strip() == "mysql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'pelicula': Persistencia_pelicula_mysql(credencials)
        }
    else:
        return {
            'pelicula': None
        }
    
def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()


def landing_text():
    os.system('clear')
    print("Benvingut a la app de pel·lícules")
    time.sleep(1)
    msg = "Desitjo que et sigui d'utilitat!"
    mostra_lent(msg)
    input("Prem la tecla 'Enter' per a continuar")
    os.system('clear')

def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()

def mostra_llista(llistapelicula):
    os.system('clear')
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.01)

def mostra_seguents(llistapelicula):
    os.system('clear')


def mostra_menu():
    print("0.- Surt de l'aplicació.")
    print("1.- Mostra les primeres 10 pel·lícules")
    print("2.- Afegir una nova pel·lícula")
    print("3.- Modificar una pel·lícula")
    print("4.- Llegir les pel·lícules d'un any específic")



def mostra_menu_next10():
    print("0.- Surt de l'aplicació.")
    print("2.- Mostra les següents 10 pel·lícules")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis'])
        #"2": lambda ctx : mostra_llista(ctx['llistapelisany'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_read(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)#falta codi
    persistencies = get_persistencies(la_meva_configuracio)#falta codi
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    films.llegeix_de_disc #falta codi
    return films
def database_add( id:int, titol: str, any:int, puntuacio:float, vots:any):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)#falta codi
    persistencies = get_persistencies(la_meva_configuracio)#falta codi
    
    #peli = Pelicula(titol, any, puntuacio, vots,persistencies['pelicula'], None)
     #falta codi
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    films.afegir(id, titol, any, puntuacio, vots)
    return films

def bucle_principal(context):
    opcio = None
    
    mostra_menu()

    while opcio != '0':
        opcio = input("Selecciona una opció: ")
        context["opcio"] = opcio
        #la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
        #persistencies = get_persistencies(la_meva_configuracio)
        
        if context["opcio"] == '1':
            id = input("Introdueix id: ")
            #id = None
            films = database_read(id)
            films.llegeix_de_disc(id)
            context["llistapelis"] = films


        elif context["opcio"] == '2':
            id = input("Introdueix l'id: ")
            titol = input("Introdueix el titol: ")
            any = input("Introdueix l'any: ")
            puntuacio = input("Puntuació: ")
            vots = input("Numero de vots: ")
            #pelicula = Pelicula(titol, any, puntuacio, vots, None, None)
            films = database_add(id, titol, any, puntuacio, vots)
            films.afegir(id, titol, any, puntuacio, vots)
            context["llistapelisdesa"] = films
            #nueva_peli = Pelicula(titol, any, puntuacio, vots, Persistencia_pelicula_mysql)
            
            #Persistencia_pelicula_mysql.desa(nueva_peli)
            
        elif context["opcio"] == '3':
            pass
            

        elif context["opcio"] == '4':
            any = input("Introdueix l'any: ")
            id = None
            films = database_read(id)
            films.lany(any)
            context["llistapelisany"] = films
            #falta codi
        procesa_opcio(context)

        #falta codi


def main():
    context = {
        "llistapelis": None,
        "llistapelisany": None,
        "llistapelisdesa": None
    }
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
