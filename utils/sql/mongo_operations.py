from client.mongo_client import db
from bson.objectid import ObjectId

from core.settings import settings


def get_collection(collection_name:str):
    return db[collection_name]

# ---------------- CREATE ----------------
def create_document(collection_name, data):
    collection = get_collection(collection_name)
    result = collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}

# ---------------- GET ----------------
def get_all_documents(collection_name):
    collection = get_collection(collection_name)
    documents = collection.find()
    return documents

def get_document_by_id(doc_id, collection_name):
    collection = get_collection(collection_name)
    document = collection.find_one({"_id": ObjectId(doc_id)})
    return document

def get_user_by_email(email):
    collection = get_collection("users")
    user = collection.find_one({"email": email})
    return user

def authernticate_user(email, password):
    collection = get_collection("users")
    user = collection.find_one({"email": email, "password": password})
    return user

def get_all_threads(user_id):
    collection = get_collection("threads")
    threads = list(collection.find({"user_id": user_id}))
    return threads

def get_all_thread_messages(thread_id, user_id):
    collection = get_collection("messages")
    messages = list(
        collection.find({"thread_id": thread_id, "user_id": user_id})
        .sort("timestamp", -1)
    )
    return messages

def get_latest_messages(user_id, thread_id):
    collection = get_collection("messages")
    messages = list(
        collection.find({"user_id": user_id, "thread_id": thread_id})
        .sort("timestamp", -1)
        .limit(settings.N_MESSAGES)
    )
    return messages

def get_all_message_uuids():
    collection = get_collection("messages")
    message_uuids = list(collection.find({}, {"message_id": 1}))
    return message_uuids

def get_all_thread_uuids():
    collection = get_collection("threads")
    thread_uuids = list(collection.find({}, {"thread_id": 1}))
    return thread_uuids

# ---------------- UPDATE ----------------
def update_document(doc_id, updated_fields, collection_name):
    collection = get_collection(collection_name)
    result = collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": updated_fields}
    )
    return {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }

# ---------------- DELETE ----------------
def delete_document(doc_id, collection_name):
    collection = get_collection(collection_name)
    result = collection.delete_one({"_id": ObjectId(doc_id)})
    return {"deleted_count": result.deleted_count}
