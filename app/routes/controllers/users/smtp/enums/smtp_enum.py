from enum import Enum

class SMTPERMISSION(Enum):
    CREATE_SERVER = 'create_server'
    GET_SERVER = 'get_server'
    UPDATE_SERVER = 'update_server'
    DELETE_SERVER = 'delete_server'
    MODIFY_SERVER = 'modify_server'