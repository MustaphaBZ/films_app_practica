# PREGUNTAS
## 1. Què fan els mètodes get_configuracio i get_persistencies?
- El mètode ‘get_configuració’ el que fa és llegir el fitxer .yml que conté la configuració a la base de dades, i utilitza la llibreria ‘yaml’ per interpretar el contingut que es la configuració de la base de dades que té el motor de la base de dades, el host, l’usuari, la contrasenya i el nom de la base de dades. I que posteriorment s'utilitzarà en el mètode de ‘get_persistencies’.

- El mètode ‘get_persistencies’ crea persistències de dades en funció de la configuració rebuda. Si la configuració especifica el motor de la base de dades com a MySQL, crea una instància de ‘Persistencia_pelicula_mysql’ amb les credencials proporcionades. I fa el mateix amb el PostgreSQL.


## 2. A procesa_opcio veureu instruccions com aquestes: Què fa lambda? Com es podria reescriure el codi sense utilitzar lambda? Quina utilitat hi trobeu a utilitzar lambda?
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis'])
    }
- El que fa ‘lambda’ per crear funcions anònimes que es passen com a valors a un diccionari.
Jo ho escriuria com està en el menú amb condicions on relacion-ho cada funció amb una opció. Exemple:

    if ctx['opcio'] == '0':
        options["0"] = lambda: mostra_lent("Fins la propera")
  
- La utilitat que li trobo es que es pot treballar amb funcions, que poden ser arguments.
## 3. Penseu que s’ha desacoblat suficientment la lògica de negoci de la lògica d’aplicació? Raoneu la resposta i digueu si hi ha cap millora que es pugui fer. 

- Si està ben desacoblat la lògica de negoci de la lògica d’aplicació i s'utilitza la interfície per gestionar las persistèncias de les pel·lícules, aleshores per una aplicació així de petita està bé, ja que si fos una gran s’hauria d’utilitzar una altre arquitectura, com per exemple la arquitectura hexagonal on pots només cambiar la base de dades i no afecta res a la resta de projecte, com es el cas d’aquesta app.
