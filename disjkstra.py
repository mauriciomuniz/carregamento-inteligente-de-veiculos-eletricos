# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph
 
# Library for INT_MAX
import sys
import random as rd
 
class Graph():
 
    def __init__(self, vertices):
        self.vet_str = ['A','B','C','D','E','F','P1','P2','P3']
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
        
        self.generate_random_num()

    def printSolution(self, dist, src):
        print("Vertex -> Distance from Source")
        for node in range(self.V):
            print(self.vet_str[src], "->" ,self.vet_str[node], "=",dist[node])
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = sys.maxsize
 
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    # Funtion that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum  distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
 
        self.printSolution(dist, src)
        
        # Gerar o números aleatórios para compor a matriz. 
        # Grafo bi-direcionado.
    def generate_random_num(self):
        for i in range(self.V):
            for j in range(self.V):
                rand = rd.randint(1,50)
                self.graph[i][j] = rand
                self.graph[j][i] = rand
                if i == j:
                    self.graph[i][j] = 0
                  
# Driver program
#g = Graph(9)

#print(g.graph)
#g.dijkstra(1)
 
# This code is contributed by Divyanshu Mehta