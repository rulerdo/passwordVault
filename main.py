from pymongo import MongoClient,errors
from getpass import getpass
import pyperclip


def connect_mongo(user,pwd):

    try:
        host = "mongodb+srv://{}:{}@cluster0.pk2u7.mongodb.net/"
        client = MongoClient(host.format(user, pwd))
        db = client["Boveda"]
        collection = db["test_conexion"]
        test = collection.find_one({"name": "test"})["value"]
        
        if test:
            collection = db["passwords"]
            print('Connected to MongoDB!')
            return collection

    except errors.OperationFailure as e:

        if e.code == 8000:
            print(e.details['errmsg'])
        
        exit(1)

    except:
        print('Connection error! Try again later')
        exit(1)
        

def list_records(collection):

    # records = collection.find()
    records = collection.find({},{ "_id": 0, "secret": 0 })

    for doc in records:
        print(doc) 


def name_exists(collection,name):

    try:
        collection.find_one({"name": name})["secret"]
        result = True

    except TypeError:
        print(f'Record {name}: not found')
        result = False
        
    return result


def get_secret(collection):
    
    name = input('name: ')
    
    if name_exists(collection,name):

        filter = {"name": name}
        secret = collection.find_one(filter)["secret"]
        pyperclip.copy(secret)
        print(f'{name} secret saved on clipboard!')


def insert_record(collection):

    data = dict()

    data['name'] = input('name: ')
    
    if name_exists(collection,data['name']):
    
        print(f'Record {data["name"]} already exists, choose a different name')
        
    else:
        print('Proceeding...')
        data['url'] = input('url: ')
        data['secret'] = getpass('secret: ')

        response = collection.insert_one(data)

        print('Document saved with id:',response.inserted_id)


def edit_record(collection):

    name = input('name: ')

    if name_exists(collection,name):
    
        url = input('NEW url: ')
        secret = getpass('NEW secret: ')
        filter = { "name": name}
        newvalues = { "$set": { "secret": secret , "url": url} }
        response = collection.update_one(filter, newvalues)
    
        if response.acknowledged:
            print(f'{name} updated!')

  
def delete_record(collection):

    name = input('name: ')
    
    if name_exists(collection,name):

        if input('Type "y" to confirm you want the {name} record deleted:') == 'y':

            filter = { "name": name}
            response = collection.delete_one(filter)

            if response.acknowledged:
                
                print(f'{name} deleted!')
        else:
            print('Record delete cancelled!')
    

if __name__ == '__main__':

    user = input('username: ')
    pwd = getpass('password: ')
    collection = connect_mongo(user,pwd)

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

        if option in ['1','2','3','4','5','6']:

            if option == '1':
                list_records(collection)

            elif option == '2':
                get_secret(collection)

            elif option == '3':
                insert_record(collection)
                
            elif option == '4':
                edit_record(collection)

            elif option == '5':
                delete_record(collection)

            elif option == '6':
                finish = True

        else:
            
            print('INVALID OPTION! Please try again')
