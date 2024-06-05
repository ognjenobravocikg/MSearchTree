#Base exception class
class MTreeException(Exception):
    pass

#Trying to insert a duplicate key, it can and should be implemented in some cases, i chose however not to for this example 
class DuplicateKeyException(Exception):
    def __init__(self, key):
        super().__init__(f"Duplicate key insertion attempted: {key}")

#Usual when using find or search in nodes.py
class NodeNotFoundException(MTreeException):
    def __init__(self, key):
        super().__init__(f"Node with key {key} not found in the tree.")

#Raised when we are using an invalid key
class InvalidKeyException(MTreeException):
    def __init__(self, key):
        super().__init__(f"Invalid key: {key}.")

#Raised when trying to get a subtree from a leaf node or invalid index
class SubtreeNotFoundException(MTreeException):
    def __init__(self, key, subtree_type):
        super().__init__(f"{subtree_type.capitalize()} subtree for key {key} not found or is a leaf node.")
