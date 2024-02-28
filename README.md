# Firebase Repo Cloner

This script clones firebase data such as specific documents/collections in firestore and authentication data from one project to another project. 

## Setup

```sh
python -m venv .env
source .env/bin/activate
pip install firebase-admin
```

Add Server keys from firebase to the keys folder.

Initialize Firebase Admin SDK with your service account credentials.

```py
credPull = credentials.Certificate("./keys/pull-key.json")
credPush = credentials.Certificate("./keys/push-key.json")
```

```sh
python app/main.py
```
