class MNode:
    def __init__(self, m):
        self.m = m
        self.keys = []
        self.children = []

    def insert(self, key):
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

    def print_tree(self, depth=0, child_type='root'):
        result = " " * (4 * depth) + f"{child_type.upper()} {self.keys}\n"
        for i, child in enumerate(self.children):
            child_type = 'left' if i == 0 else 'right' if i == len(self.children) - 1 else 'middle'
            result += child.print_tree(depth + 1, child_type)
        return result

    def search(self, key, level=0):
        for i, item in enumerate(self.keys):
            if key == item:
                return f"Found {key} at level {level}"
            elif key < item:
                if self.children:
                    return self.children[i].search(key, level + 1)
                return None
        if self.children:
            return self.children[-1].search(key, level + 1)
        return None

    def delete(self, key):
        if key in self.keys:
            index = self.keys.index(key)
            if not self.children:
                # Case 1: Leaf node
                self.keys.pop(index)
            else:
                # Case 2 & 3: Non-leaf node
                if len(self.children[index].keys) > 0:
                    # Get predecessor (max value in the left subtree)
                    predecessor = self.get_predecessor(index)
                    self.keys[index] = predecessor
                    self.children[index].delete(predecessor)
                else:
                    # Get successor (min value in the right subtree)
                    successor = self.get_successor(index)
                    self.keys[index] = successor
                    self.children[index + 1].delete(successor)
        else:
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

class MSearchTree:
    def __init__(self, m):
        self.root = MNode(m)

    def search(self, key):
        return self.root.search(key)
