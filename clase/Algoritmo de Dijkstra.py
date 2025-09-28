
import heapq
def dijkstra(grafo, inicio):
# Distancias iniciales: infinito para todos menos el nodo de inicio
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
# Cola de prioridad para elegir el nodo más cercano
    cola_prioridad = [(0, inicio)]
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
    # Si encontramos una distancia mayor, no es óptima y la ignoramos
        if distancia_actual > distancias[nodo_actual]:
            continue
# Explorar vecinos
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
# Si encontramos una ruta más corta, actualizamos
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola_prioridad, (distancia, vecino))
    return distancias
grafo = {
'A': {'B': 2, 'C': 5},
'B': {'A': 2, 'C': 6, 'D': 1},
'C': {'A': 5, 'B': 6, 'D': 2, 'E': 5},
'D': {'B': 1, 'C': 2, 'E': 1},
'E': {'C': 5, 'D': 1}
}
resultado = dijkstra(grafo, 'A')
print("Distancias mínimas desde A:")
for nodo, distancia in resultado.items():
    print(f"A → {nodo}: {distancia}")