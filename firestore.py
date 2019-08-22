from google.cloud import firestore

firestore = firestore.Client.from_service_account_json('./service-account.json')

db = firestore.collection(u'one-time-password')

def add_new_token(token, name):
    db.document(name).set({
        u'token': token
    })

def get_token(name):
    try:
        doc = db.document(name).get()
        token = doc.to_dict()['token']
        return token
    except:
        raise