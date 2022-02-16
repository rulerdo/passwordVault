from pymongo import MongoClient
from getpass import getpass
import pyperclip

def connect_mongo(user,pwd):

    host = "mongodb+srv://{}:{}@cluster0.pk2u7.mongodb.net/"
    client = MongoClient(host.format(user,pwd))
    db = client["Boveda"]
    collection = db["passwords"]
    
    print('Connected to MongoDB!')
    
    return collection


def list_records(collection):

    # records = collection.find()
    records = collection.find(projection={"_id": False, "secret": False })

    print('All records:')
    for doc in records:
        print(doc) 


def get_secret(collection):
    
    name = input('name: ')
    filter = {"name": name}
    secret = collection.find_one(filter)["secret"]
    # print(f'secret: {secret}')
    pyperclip.copy(secret)
    print(f'{name} secret saved on clipboard!')


def insert_record(collection):

    data = dict()

    data['name'] = input('name: ')
    data['url'] = input('url: ')
    data['secret'] = getpass('secret: ')

    response = collection.insert_one(data)

    print('ID:',response.inserted_id)


def edit_record(collection):

    name = input('name: ')
    url = input('NEW url: ')
    secret = getpass('NEW secret: ')

    filter = { "name": name}
    newvalues = { "$set": { "secret": secret , "url": url} }
    response = collection.update_one(filter, newvalues)
    
    if response.acknowledged:
        print(f'{name} updated!')

  
def delete_record(collection):

    name = input('name: ')
    filter = { "name": name}
    response = collection.delete_one(filter)
    
    if response.acknowledged:
        print(f'{name} deleted!')

    

if __name__ == '__main__':

    user = input('username: ')
    pwd = getpass('password: ')

    collection = connect_mongo(user,pwd)

    list_records(collection)
    # get_secret(collection)
    # insert_record(collection)
    # edit_record(collection)
    # delete_record(collection)
