# by Kaz
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with your service account credentials
credPull = credentials.Certificate("./keys/pull-key.json")
credPush = credentials.Certificate("./keys/push-key.json")

pullApp= firebase_admin.initialize_app(credPull,name="pull")
pushApp= firebase_admin.initialize_app(credPush)

dbPull = firestore.client(app=pullApp)
dbPush = firestore.client(app=pushApp)


def pullData(collection_list,version):  
    os.mkdir(f"data/version_{version}")
    for collection_name in collection_list:
        collection_ref = dbPull.collection(collection_name)
        documents = collection_ref.stream()

        data_dict = {}

        for document in documents:
            data_dict[document.id] = document.to_dict()

        with open(f"data/version_{version}/{collection_name}.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=4)
            
        print(f"{collection_name}: Dumped successfully")       


def pushData(collection_list,version):
    for collection_name in collection_list:
        with open(f"data/version_{version}/{collection_name}.json", "r") as json_file:
            data_dict = json.load(json_file)
            
        # collection_ref = dbPush.collection(collection_name)

        # for document_id, document_data in data_dict.items():
        #     doc_ref = collection_ref.document(document_id)
        #     doc_ref.set(document_data)
            
        print(f"{collection_name}: Uploaded successfully") 


if __name__ == "__main__":
    index=len(next(os.walk('data'))[1])
    
    # Specify the Firestore collection name
    collectionList = ["apps", "food_item_collection","food_collection"]
    
    pullData(collectionList,index+1)
    # pushData(["apps"],index)