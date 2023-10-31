from BST import TreeNode
from AVLTree import AVLTree

class AVLTreeUnique(AVLTree):
    def __init__(self):
        super().__init__()

    def _put(self, key, value, current_node):

        if key < current_node.key:
            if current_node.left_child:
                self._put(key, value, current_node.left_child)
            else:
                current_node.left_child = TreeNode(key, value, parent=current_node)
        elif key > current_node.key:
            if current_node.right_child:
                self._put(key, value, current_node.right_child)
            else:
                current_node.right_child = TreeNode(key, value, parent=current_node)

        elif key==current_node.key: 
            current_node.value +=1
            current_node = TreeNode(current_node.key, current_node.value,current_node)

        # Modify this function to make sure that key-value pairs are overwritten
        # in the case of duplicate keys.

    def rotate_right(self, rotation_root):
        # Your solution here
        new_root = rotation_root.right_child
        rotation_root.left_child = new_root.right_child
        if new_root.right_child:
            new_root.right_child.parent = rotation_root
        new_root.parent = rotation_root.parent
        if rotation_root.is_root():
            self._root = new_root
        else:
            if rotation_root.is_right_child():
                rotation_root.parent.right_child = new_root
            else:
                rotation_root.parent.left_child = new_root
        new_root.right_child = rotation_root
        rotation_root.parent = new_root
        rotation_root.balance_factor = (
            rotation_root.balance_factor - 1 + min(new_root.balance_factor, 0)
        )
        new_root.balance_factor = (
            new_root.balance_factor - 1 - max(rotation_root.balance_factor, 0)
        )

def strip(word):
    """strip() removes all non-alphabetic characters from a string. The builtin
    str.split function isn't quite flexible enough for our needs here, so we
    supply a custom version. The string function str.isalpha() may be useful."""
    return "".join([ch for ch in word if str.isalpha(ch)])

def word_count(fname):
    """Opens the file named `fname` and reads each line, creating an AVL tree storing each word
    and its frequency as a key-value pair."""
    my_tree = AVLTreeUnique()
    with open(fname, 'r') as file:
        lines = file.readlines() # now lines is a list of the lines in the file
        # You can read up on file handling in the Python documentation and
        # do things differently here if you want to. My starter code is just
        # a suggestion.
    # Your solution here
        for line in lines:
            words = line.split(' ')
            for word in words: 
                word = strip(word)
                my_tree.put(word,1)
            
    return my_tree

def display_common(freq_map, n):
    """Given a frequency mapping (like that produced by word_count), prints the n most common
    entries and their frequencies to the screen."""
    # Your solution here
    greatest_to_least_map = sorted(freq_map, key= lambda dict_key: freq_map[dict_key], reverse = True)
    common = []
    for i in range(n+1):
        common.append(f"{greatest_to_least_map[i]}: {freq_map [greatest_to_least_map[i]]}")
    return common 


def report(tree, fname): # used word_count
    """Uses sorted() with a custom sort key and file.write() to
    create the lines of the file one by one."""
    srted_tree = sorted(tree)
    with open(fname, "w") as file_:
        for i in range(len(srted_tree)):
            file_.write(srted_tree[i] + ":     " + str((tree[srted_tree[i]])) + "\n")
    return file_


if __name__ == "__main__":
    # Put the code for problem 05 here: that is, the steps of the main program.
    # Guarding the code inside this `if` statement would allow us to import this
    # file as a Python module without executing the main program, were we so inclined.

    # Your solution here
    bk = word_count("/home/user/csc152/HW3WordFrequencies//browne.txt")
    report(bk,"/home/user/csc152/HW3WordFrequencies//report.txt")
    cmn_lst = display_common(bk, 100)
    print(cmn_lst)
    
