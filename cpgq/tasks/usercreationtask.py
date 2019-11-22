from celery.task import task
from celery import signature, group

contacts=[]

@task
def user_create(username,first,last,email):
    
    return [{ 'username' : username , 'first' : first ,'last':last ,'email':email }]

@task
def import_contacts(l):
    global contacts.append(l)
    return '\t new user added ' + l[-1].username + 'length of contacts ' +len(contacts)

@task
def insert_user(username,first,last,email):
    result = (user_create.s(username,first,last,email) | import_contacts.s())
    return result.get()


