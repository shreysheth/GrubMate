import uuid

from utils.sql.mongo_operations import get_all_message_uuids, get_all_thread_uuids

def generate_message_uuid():
    uuid = str(uuid.uuid4())
    while (uuid in get_all_message_uuids()):
        uuid = str(uuid.uuid4())
    return uuid

def generate_thread_uuid():
    uuid = str(uuid.uuid4())
    while (uuid in get_all_thread_uuids()):
        uuid = str(uuid.uuid4())
    return uuid