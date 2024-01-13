from enum import Enum

class CONTACTPERM(Enum):
    ASSING = 'contacts.assing'
    DELETE = 'contacts.delete'
    UPDATE = 'contacts.update'
    CREATE = 'contacts.create'
    GET = 'contacts.get'
    GETONE = 'contacts.get_one'
    GETBYUSER = 'contacts.get_by_user'