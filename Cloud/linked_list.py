class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListCircular:

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
        if(self.size == 1):
            print(current.data)
        elif(self.size > 1):      
            print(current.data)  
            while(current.next != self.head):  
                current = current.next    
                print(current.data)
        else:
            print("A lista está vazia")
          
            
    '''
    Encontra o nó e o retorna
    '''
    def find_node(self,server):
        current = self.head
        
        for i in range(self.size):
            if(current.data.get("name") == server):
                return current
            current = current.next
        return None 
        
    '''
    Insere em uma lista vazia
    '''
    def __insert_list_empty(self, data): 
        node = Node(data)
        self.head = node
        self.tail = node
        self.size += 1

        
    '''
    Insere no ínicio da lista
    '''
    def insert_init(self, data):
        if self.size == 0:
            self.__insert_list_empty(data)
        else:
            node = Node(data)
            node.next = self.head
            self.tail.next = node
            self.head = node
            self.size += 1
            

       
