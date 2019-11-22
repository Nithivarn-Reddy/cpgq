from celery.task import task
from celery import signature, group

contacts=[ ]

@task
def add(x,y):
    return x + y

@task
def double(x):
    return x * 2

@task
def triple(x):
    return x * 3

@task
def test_grouping(x,y):
    chain = (add.s(x,y) | group(double.s(), triple.s()))
    chain.delay()
    return "Kicked Off tasks"

@task
def user_create(username,first,last,email):
    
    return [{ 'username' : username , 'first' : first ,'last':last ,'email':email }]

@task
def import_contacts(l):
    global contacts
    contacts.append(l)
    #return '\t new user added ' + contacts[-1].username + 'length of contacts ' +len(contacts)

@task
def insert_user(username,first,last,email):
    result = (user_create.s(username,first,last,email) | import_contacts.s()).apply_async()
    return result.get()

