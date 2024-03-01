#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from persistencia_postgres import Persistencia_postgres
from llistapelis import Llistapelis
from pelicula import Pelicula
import logging

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
print(RUTA_FITXER_CONFIGURACIO)

def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    try:
        with open(ruta_fitxer_configuracio, 'r') as conf:
            config = yaml.safe_load(conf)
    except(FileNotFoundError):
        print(f"No existeix la següent ruta: {ruta_fitxer_configuracio}")
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
    elif conf["base de dades"]["motor"].lower().strip() == "postgresql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'pelicula': Persistencia_postgres(credencials)
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
    print("1.- Mostra les següents 10 pel·lícules")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis']),
        "2": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_read(id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)["pelicula"]
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    films.llegeix_de_disc(id) 
    return films 


def database_add( id:int):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencies = get_persistencies(la_meva_configuracio)["pelicula"]
    films = Llistapelis(
        persistencia_pelicula=persistencies
    )
    return films

def bucle_principal(context):
    opcio = None
    try:
        fitxer = input("Escriu '1' per a configuració de MySQL o '2' per a la configuaració PostgreSQL: ")
        global RUTA_FITXER_CONFIGURACIO
        if fitxer == '1':
            RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml')
        elif fitxer == '2':
            RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuraciopgsql.yml')
        else:
            print("Opció incorrecta. Utilitzant configuració per defecte de MySQL.")
            RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml')
        
        open(RUTA_FITXER_CONFIGURACIO, "rt")
    except FileNotFoundError:
        print(f"No existeix el fitxer de configuració: {fitxer}")
        sys.exit(1)
    
    print(f"Fitxer de configuració seleccionat: {fitxer}")

    while opcio != '0':
        print("-----------------------------------------------------------")
        mostra_menu()
        opcio = input("-SELECCIONA UNA OPCIÓ: ")
        context["opcio"] = opcio

        if context["opcio"] == '1':
            id = input("Escriu la id per on vols començar: ")
            films = database_read(id)
            
            context["llistapelis"] = films
            procesa_opcio(context)
            
            mostra_menu_next10()
            opcio=input("-SELECCIONA UNA OPCIÓ: ")
            context["opcio"] = opcio
            while context["opcio"] != '0':
                id = films.ult_id

                films = database_read(id)
                context["llistapelis"] = films
                procesa_opcio(context)
                
                mostra_menu_next10()
                opcio=input("-SELECCIONA UNA OPCIÓ:")
                context["opcio"] = opcio

        elif context["opcio"] == '2':
            id = input("Introdueix l'id del registre que vols afegir: ")
            titol = input("Introdueix el titol: ")
            any = input("Introdueix l'any: ")
            puntuacio = input("Puntuació: ")
            vots = input("Numero de vots: ")
            
            films = database_add(id)
            films.afegir(id, titol, any, puntuacio, vots)
            context["opcio"] = opcio          
            continue

        elif context["opcio"] == '3':
            id = input("Introdueix l'id del registre que vols modificar: ")
            titol = input("Introdueix el titol: ")
            any = input("Introdueix l'any: ")
            puntuacio = input("Puntuació: ")
            vots = input("Numero de vots: ")
            
            films = database_add(id)
            films.canvia(id, titol, any, puntuacio, vots)
            context["opcio"] = opcio
            continue

        elif context["opcio"] == '4':
            any = int(input("Introdueix l'any: "))
            id = None
            films = database_add(id)
            films.lany(any)
            
            context["llistapelis"] = films
            continue
            
        procesa_opcio(context)

        #falta codi


def main():
    context = {
        "llistapelis": None
    }
    landing_text()
    bucle_principal(context)
    (get_configuracio(RUTA_FITXER_CONFIGURACIO))


if __name__ == "__main__":
    main()
