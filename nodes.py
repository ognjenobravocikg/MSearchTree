from exceptions import NodeNotFoundException, InvalidKeyException, SubtreeNotFoundException, DuplicateKeyException

class MNode:
    def __init__(self, m):
        self.m = m
        self.keys = []
        self.children = []

    def insert(self, key):
        try:
            # Try to search for the key
            self.search(key)
            # If no exception is raised, the key is already in the tree
            raise DuplicateKeyException(key)
        except NodeNotFoundException:
            # If the key is not found, proceed with insertion
            if not self.children:
                self.keys.append(key)
                self.keys.sort()
                if len(self.keys) >= self.m:
                    return self.split()
            else:
                for i, item in enumerate(self.keys):
                    if key < item:
                        res = self.children[i].insert(key)
                        if res:
                            return self.handle_split(res, i)
                        return None
                res = self.children[-1].insert(key)
                if res:
                    return self.handle_split(res, len(self.keys))
            return None
        
    def split(self):
        mid_index = len(self.keys) // 2
        mid_value = self.keys[mid_index]

        left_child = MNode(self.m)
        right_child = MNode(self.m)

        left_child.keys = self.keys[:mid_index]
        right_child.keys = self.keys[mid_index + 1:]

        if self.children:
            left_child.children = self.children[:mid_index + 1]
            right_child.children = self.children[mid_index + 1:]

        return mid_value, left_child, right_child

    def handle_split(self, split_data, index):
        mid_value, left_child, right_child = split_data

        self.keys.insert(index, mid_value)
        self.children[index] = left_child
        self.children.insert(index + 1, right_child)

        if len(self.keys) >= self.m:
            return self.split()
        return None

    def print_tree(self, depth=0, child_type='root', subtree=False):
        result = ""
        if not subtree:
            result += " " * (4 * depth) + f"{child_type.upper()} {self.keys}\n"
        else:
            result += " " * (4 * depth) + f"{child_type.upper()} {self.keys}\n"

        if not subtree:
            for i, child in enumerate(self.children):
                child_type = 'left' if i == 0 else 'right' if i == len(self.children) - 1 else 'middle'
                result += child.print_tree(depth + 1, child_type)
        else:
            for i, child in enumerate(self.children):
                child_type = 'left' if i == 0 else 'middle' if i != len(self.children) - 1 else 'right'
                result += child.print_tree(depth + 1, child_type)

        return result

    def search(self, key, level=0):
        for i, item in enumerate(self.keys):
            if key == item:
                return self
            elif key < item:
                if self.children:
                    return self.children[i].search(key, level + 1)
                raise NodeNotFoundException(f"Key {key} not found in the tree.")
        if self.children:
            return self.children[-1].search(key, level + 1)
        raise NodeNotFoundException(f"Key {key} not found in the tree.")

    def delete(self, key):
        try:
            node = self.search(key)  # Find the node containing the key
            index = node.keys.index(key)
            
            if not node.children:
                # Case 1: Leaf node
                node.keys.pop(index)
            else:
                # Case 2a, 2b & 3: Non-leaf node
                if len(node.children[index].keys) > 0:
                    # Get predecessor (max value in the left subtree)
                    predecessor = node.get_predecessor(index)
                    node.keys[index] = predecessor
                    node.children[index].delete(predecessor)
                else:
                    # Get successor (min value in the right subtree)
                    successor = node.get_successor(index)
                    node.keys[index] = successor
                    node.children[index + 1].delete(successor)
            
            # Fix the node if necessary
            self.fix_node()
            return self
        except NodeNotFoundException:
            # Traverse to find the key
            for i, item in enumerate(self.keys):
                if key < item:
                    if self.children:
                        self.children[i].delete(key)
                    break
            else:
                if self.children:
                    self.children[-1].delete(key)

            # Fix the node if necessary
            self.fix_node()
            return self


    # Helper functions for deletion
    def get_predecessor(self, index):
        current = self.children[index]
        while current.children:
            current = current.children[-1]
        return current.keys[-1]

    def get_successor(self, index):
        current = self.children[index + 1]
        while current.children:
            current = current.children[0]
        return current.keys[0]

    def merge_children(self, index):
        child = self.children.pop(index + 1)
        self.children[index].keys.append(self.keys.pop(index))
        self.children[index].keys.extend(child.keys)
        if child.children:
            self.children[index].children.extend(child.children)

    def borrow_from_left_sibling(self, index):
        child = self.children[index]
        sibling = self.children[index - 1]
        child.keys.insert(0, self.keys[index - 1])
        self.keys[index - 1] = sibling.keys.pop(-1)
        if sibling.children:
            child.children.insert(0, sibling.children.pop(-1))

    def borrow_from_right_sibling(self, index):
        child = self.children[index]
        sibling = self.children[index + 1]
        child.keys.append(self.keys[index])
        self.keys[index] = sibling.keys.pop(0)
        if sibling.children:
            child.children.append(sibling.children.pop(0))

    def fix_node(self):
        for i, child in enumerate(self.children):
            if not child.keys:
                if i > 0 and len(self.children[i - 1].keys) > 1:
                    self.borrow_from_left_sibling(i)
                elif i < len(self.children) - 1 and len(self.children[i + 1].keys) > 1:
                    self.borrow_from_right_sibling(i)
                else:
                    if i > 0:
                        self.merge_children(i - 1)
                    else:
                        self.merge_children(i)
                break

    def get_left_subtree(self, key):
        node = self.search(key)
        if node:
            if node.children:
                index = node.keys.index(key)
                if index >= 0 and index < len(node.children):
                    return node.children[index]
                else:
                    raise SubtreeNotFoundException(key, "left")
            else:
                raise SubtreeNotFoundException(key, "left")
        raise NodeNotFoundException(f"Key {key} not found in the tree.")

    def get_right_subtree(self, key):
        node = self.search(key)
        if node:
            if node.children:
                index = node.keys.index(key)
                if index + 1 < len(node.children):
                    return node.children[index + 1]
                else:
                    raise SubtreeNotFoundException(key, "right")
            else:
                raise SubtreeNotFoundException(key, "right")
        raise NodeNotFoundException(f"Key {key} not found in the tree.")

    def getMaxNum(self, key):
        node = self.search(key)
        if node:
            return node.keys[-1]
        raise NodeNotFoundException(f"Key {key} not found in the tree.")
    
    def getMinNum(self, key):
        node = self.search(key)
        if node:
            return node.keys[0]
        raise NodeNotFoundException(f"Key {key} not found in the tree.")
    
    def isFull(self):
        return len(self.keys) >= self.m - 1

    def isEmpty(self):
        return len(self.keys) == 0
            

class MSearchTree:
    def __init__(self, m):
        self.root = MNode(m)

    def search(self, key):
        return self.root.search(key)
    
    def add(self, key):
        res = self.root.insert(key)
        if res:
            mid_value, left_child, right_child = res
            new_root = MNode(self.root.m)
            new_root.keys = [mid_value]
            new_root.children = [left_child, right_child]
            self.root = new_root

    def remove(self, key):
        self.root.delete(key)
