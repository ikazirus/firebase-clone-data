# by Kaz
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase Admin SDK with your service account credentials
credPull = credentials.Certificate("./keys/pull-key.json")
credPush = credentials.Certificate("./keys/push-key.json")

pullApp= firebase_admin.initialize_app(credPull,name="pull")
pushApp= firebase_admin.initialize_app(credPush)

dbPull = firestore.client(app=pullApp)
dbPush = firestore.client(app=pushApp)


def pull_collection_data(collection_list,version):  
    os.mkdir(f"data/version_{version+1}")
    for collection_name in collection_list:
        collection_ref = dbPull.collection(collection_name)
        documents = collection_ref.stream()

        data_dict = {}

        for document in documents:
            data_dict[document.id] = document.to_dict()

        with open(f"data/version_{version+1}/{collection_name}.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=4)
            
        print(f"{collection_name}: Dumped successfully")       


def push_collection_data(collection_list,version):
    for collection_name in collection_list:
        with open(f"data/version_{version}/{collection_name}.json", "r") as json_file:
            data_dict = json.load(json_file)
            
        # collection_ref = dbPush.collection(collection_name)

        # for document_id, document_data in data_dict.items():
        #     doc_ref = collection_ref.document(document_id)
        #     doc_ref.set(document_data)
            
        print(f"{collection_name}: Uploaded successfully") 


def pull_auth_data():
    try:
        # Retrieve all users from Firebase Authentication
        users = auth.list_users(app=pullApp)

        user_data = []
        for user in users.users:
            user_info = user._data
            user_data.append(user_info)

        # Write user data to a JSON file
        with open(f"data/auth.json", 'w') as json_file:
            json.dump(user_data, json_file, indent=4)

        print(f"Total of {len(user_data)} users exported")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        
        
def push_auth_data():
    try:
        # Open the JSON file and load user data
        with open(f"data/auth.json", 'r') as json_file:
            user_data = json.load(json_file)

        # Upload each user to Firebase Authentication
        for user_info in user_data:
            user = auth.create_user(
                email=user_info.get('email'),
                password=user_info.get('password'),
                display_name=user_info.get('displayName'),
                phone_number=user_info.get('phoneNumber')
                # Add more user attributes as needed
            )
            print(f"User {user.uid} uploaded to Firebase Authentication")

        print(f"{len(user_data)} Users uploaded successfully")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    index=len(next(os.walk('data'))[1])
    
    # Specify the Firestore collection name
    collectionList = ["apps", "food_item_collection","food_collection"]
    
    # Firestore
    # pull_collection_data(collectionList,index)
    # push_collection_data(["apps"],index)
    
    #auth
    pull_auth_data()
    