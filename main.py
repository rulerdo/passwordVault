from pymongo import MongoClient,errors
from getpass import getpass
import pyperclip


def connect_mongo(user,pwd):

    host = "mongodb+srv://{}:{}@cluster0.pk2u7.mongodb.net/"
    arguments = "?tls=true&tlsAllowInvalidCertificates=true"
    uri_string = host + arguments
    mongodb_uri = uri_string.format(user, pwd)

    try:
        client = MongoClient(mongodb_uri)
        db = client["MyVault"]
        col = db["connection_test"]
        test = col.find_one({"name": "test"})["value"]
        
        if test:
            print('Connected to MongoDB!')
            return client

    except errors.OperationFailure as e:

        if e.code == 8000:
            print(e.details['errmsg'])
        
        exit(1)

    except:
        print('Connection error! Try again later')
        exit(1)
        

def name_exists(client,name):

    try:
        db = client["MyVault"]
        col = db["MyPass"]
        col.find_one({"name": name})["secret"]
        result = True

    except TypeError:
        print(f'Record {name}: not found')
        result = False
        
    return result


def get_secret(client):
    
    name = input('name: ')
    db = client["MyVault"]
    col = db["MyPass"]
    
    if name_exists(client,name):

        secret = col.find_one({"name": name})["secret"]
        pyperclip.copy(secret)
        print(f'{name} secret saved on clipboard!')


def insert_record(client):

    data = dict()

    data['name'] = input('name: ')
    
    if name_exists(client,data['name']):
    
        print(f'Record {name} already exists, choose a different name')
        
    else:
        print('Proceeding...')
        data['url'] = input('url: ')
        data['secret'] = getpass('secret: ')

        db = client["MyVault"]
        col = db["MyPass"]
        response = col.insert_one(data)

        print('Document saved with id:',response.inserted_id)


def list_records(client):

    db = client["MyVault"]
    col = db["MyPass"]
    # dir = col.find()
    dir = col.find({},{ "_id": 0, "secret": 0 })

    for doc in dir:
        print(doc) 


def edit_record(client):

    name = input('name: ')
    db = client["MyVault"]
    col = db["MyPass"]
    
    if name_exists(client,name):
    
        url = input('NEW url: ')
        secret = getpass('NEW secret: ')
        filter = { "name": name}
        newvalues = { "$set": { "secret": secret , "url": url} }
        col.update_one(filter, newvalues)
        print(f'{name} updated!')

  
def delete_record(client):

    name = input('name: ')
    db = client["MyVault"]
    col = db["MyPass"]
    
    if name_exists(client,name):

        filter = { "name": name}
        col.delete_one(filter)
        print(f'{name} deleted!')
    

if __name__ == '__main__':

    user = input('username: ')
    pwd = getpass('password: ')
    client = connect_mongo(user,pwd)
    finish = False
    menu = '''
Choose from the following options:
1. List all records
2. Retrieve secret
3. Add new record
4. Edit existing record
5. Delete record
6. Exit

selection : '''

    while not finish:

        option = input(menu)

        if option not in ['1','2','3','4','5','6']:

            print('INVALID OPTION! Please try again')

        else:

            if option == '1':
                list_records(client)

            elif option == '2':
                get_secret(client)

            elif option == '3':
                insert_record(client)
                
            elif option == '4':
                edit_record(client)

            elif option == '5':
                delete_record(client)

            elif option == '6':
                finish = True
