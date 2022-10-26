from pymongo import MongoClient
from getpass import getpass
from tabulate import tabulate
import pyperclip


def conectar_mongo(user,pwd):

    host = f'mongodb+srv://{user}:{pwd}@cluster0.hebsb.mongodb.net/'
    cliente = MongoClient(host)
    db = cliente['Boveda']
    coleccion = db['password']

    print('Conectado a MongoDB!')

    return coleccion

#AHHHHHHHHHHHHHHHHHHH
def agregar_documento(coleccion):

    doc = dict()

    doc['name'] = input('nombre: ')
    doc['url'] = input('url: ')
    doc['secret'] = getpass('password: ')

    respuesta = coleccion.insert_one(doc)
    print('ID: ',respuesta.inserted_id)


def mostrar_documentos(coleccion):

    documentos = coleccion.find(projection={'_id':False,'secret':False})
    print('Todos los documentos: ')
    print(tabulate(documentos))


def obtener_password(coleccion):

    nombre = input('nombre: ')
    filtro = {'name':nombre}
    password = coleccion.find_one(filtro)['secret']
    pyperclip.copy(password)
    print(f'Password de {nombre} guardado en el portapales!')

## Otra edición de git
def editar_documento(coleccion):

    nombre = input('nombre: ')
    liga = input('NUEVA url: ')
    password = getpass('NUEVO password: ')
    filtro = {'name':nombre}
    valores = {'$set':{'secret':password,'url':liga}}
    respuesta = coleccion.update_one(filtro,valores)

    if respuesta.acknowledged:
        print(f'Documento {nombre} modificado!')


def eliminar_documento(coleccion):

    nombre = input('nombre: ')
    filtro = {'name':nombre}

    if input(f'Seguro de eliminar el documento {nombre} Y/N: ') == 'Y':

        respuesta = coleccion.delete_one(filtro)

        if respuesta.acknowledged:
            print(f'Documento {nombre} eliminado!')

    else:
        print('Operacion cancelada!')


if __name__ == '__main__':

    user = input('user: ')
    pwd = getpass('password: ')
    coleccion = conectar_mongo(user,pwd)

    menu = '''
Selecciona una de las siguientes opciones:
1. Mostrar documentos
2. Obtener password
3. Agregar documento nuevo
4. Editar documento existe
5. Eliminar documento
6. Salir

Opcion: '''

    salir = False

    while not salir:

        opcion = input(menu)

        if opcion in ['1','2','3','4','5']:

            if opcion == '1':
                mostrar_documentos(coleccion)

            elif opcion == '2':
                obtener_password(coleccion)

            elif opcion == '3':
                agregar_documento(coleccion)

            elif opcion == '4':
                editar_documento(coleccion)

            elif opcion == '5':
                eliminar_documento(coleccion)

            input('Presiona enter para continuar...')

        elif opcion == '6':
            salir = True
            print('Adios!')

        else:
            print('OPCION INVALIDA! Intenta de nuevo')
