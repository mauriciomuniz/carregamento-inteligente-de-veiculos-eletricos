class Node:

    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None
        self.visited = False


class LinkedListDuple:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_tail(self, node):
        return True if self.tail == node else False
    
    def is_head(self, node):
        return True if self.head == node else False
    
    '''
    Imprimi todos os nós da lista
    '''
    def print_list(self):
        current = self.head
        while(current != None):
            print(current.data)
            current = current.next  
            
    '''
    Encontra o nó e o retorna
    '''
    def find_node(self,server):
        current = self.head
        while(current != None):
            if(current.data.get("name") == server):
                return current
            current = current.next
        return None 
        
    '''
    Insere em uma lista vazia
    '''
    def insert_list_empty(self, data): 
        node = Node(data)
        self.head = node
        self.tail = node
        self.size += 1

       
        
    '''
    Insere no ínicio da lista
    '''
    def insert_init(self, data):
        if self.size == 0:
             self.insert_list_empty(data)
        else:
            node = Node(data)
            node.next = self.head           
            self.head.previous = node
            self.head = node
            self.size += 1

       

