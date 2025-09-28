def floyd_warshall(grafo):
# Número de nodos
    nodos = list(grafo.keys())
    n = len(nodos)
    # Inicializar matriz de distancias
    dist = [[float('inf')] * n for _ in range(n)]
    # Distancia a sí mismo = 0
    for i in range(n):
        dist[i][i] = 0
# Llenar con valores del grafo
    for u in grafo:
        for v, peso in grafo[u].items():
            dist[nodos.index(u)][nodos.index(v)] = peso
# Algoritmo principal
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
# Mostrar resultado
    print("Matriz de distancias mínimas:")
    for fila in dist:
        print(fila)
# Grafo de ejemplo
grafo = {
'A': {'B': 3, 'C': 8},
'B': {'C': 2, 'D': 5},
'C': {'D': 1},
'D': {'A': 2}
}
floyd_warshall(grafo)