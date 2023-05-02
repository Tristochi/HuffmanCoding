class TheTree:
    def __init__(self, value=None, character=None):
        self.left = None
        self.right = None 
        self.value = value
        self.character = character

    def children(self):
        return (self.left, self.right)