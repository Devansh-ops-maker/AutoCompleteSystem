class TrieNode:

    def __init__(self):
        self.children=[None] * 26
        self.isEndOfWord=False

    def insert(root,key):
        curr=root
        for c in key:
            index=ord(c)-ord('a')
            if curr.children[index] is None:
                curr.children[index]=TrieNode()
            curr=curr.children[index]
        curr.isEndOfWord=True

    def search(root,key):
        curr=root
        for c in key:
            index=ord(c)-ord('a')
            if curr.children[index] is None:
                return False
            curr=curr.children[index]
        return curr.isEndOfWord
    
    def startsWith(root,prefix):
        curr=root
        for c in prefix:
            index=ord(c)-ord('a')
            if curr.children[index] is None:
                return False
            curr=curr.children[index]
        return True