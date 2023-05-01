import variables as vb
import random as rd

# Python3 program to find the shortest
# path between any two nodes using
# Floyd Warshall Algorithm.

class Warshall():

    def __init__(self) -> None:
        self.V = len(vb.VERTICES)
        self.graph = [[0 for column in range(self.V)]
                      for row in range(self.V)]
        self.INF = 1000
        self.dis = [[-1 for i in range(self.V)] for i in range(self.V)]
        self.Next = [[-1 for i in range(self.V)] for i in range(self.V)]
        self.generate_random_num()
        self.initialise()
        self.floydWarshall()


    #Gerar o números aleatórios para compor a matriz. 
    # Grafo bi-direcionado.
    def generate_random_num(self):
        for i in range(self.V):
            for j in range(self.V):
                rand = rd.randint(1,50)
                self.graph[i][j] = rand
                self.graph[j][i] = rand
                if i == j:
                    self.graph[i][j] = 0

    # Initializing the distance and
    # Next array
    def initialise(self):
        global dis, Next
        for i in range(self.V):
            for j in range(self.V):
                self.dis[i][j] = self.graph[i][j]
    
                # No edge between node
                # i and j
                if (self.graph[i][j] == self.INF):
                    self.Next[i][j] = -1
                else:
                    self.Next[i][j] = j
    
    # Function construct the shortest
    # path between u and v
    def constructPath(self, u, v):
        global graph, Next
        
        # If there's no path between
        # node u and v, simply return
        # an empty array
        if (self.Next[u][v] == -1):
            return {}
    
        # Storing the path in a vector
        path = [u]
        while (u != v):
            u = self.Next[u][v]
            path.append(u)

        return path
    

    # Standard Floyd Warshall Algorithm
    # with little modification Now if we find
    # that dis[i][j] > dis[i][k] + dis[k][j]
    # then we modify next[i][j] = next[i][k]
    def floydWarshall(self):
        global dist, Next
        
        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    
                    # We cannot travel through
                    # edge that doesn't exist
                    if (self.dis[i][k] == self.INF or self.dis[k][j] == self.INF):
                        continue
                    if (self.dis[i][j] > self.dis[i][k] + self.dis[k][j]):
                        self.dis[i][j] = self.dis[i][k] + self.dis[k][j]
                        self.Next[i][j] = self.Next[i][k]
  

    # Print the shortest path
    def printPath(self,path):
        n = len(path)
        str_p = ''
        for i in range(n - 1):
            str_p += str(path[i]) + " -> "
        
        return str_p + str(path[n - 1])

'''
if __name__ == '__main__':

    w = Warshall()
    # Function to initialise the
    # distance and Next array
    w.initialise()
    print(w.graph)
    # Calling Floyd Warshall Algorithm,
    # this will update the shortest
    # distance as well as Next array
    w.floydWarshall()
   

    # Path from node 0 to 2
    org,dest = 2,1
    print("Shortest path from 0 to 1: ", end = "")
    path = w.constructPath(org, dest)
    w.printPath(path)
    print(w.dis[org][dest])
   
 
    # This code is contributed by mohit kumar 29'''