from flask import Flask, request, jsonify
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from distance_calculator import calcular_matriz_distancias

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto permite CORS para todas las rutas


@app.route('/optimizar_ruta', methods=['POST'])
def optimizar_ruta():
    data = request.json  
    direcciones = data.get('direcciones', [])  
    num_vehiculos = data.get('vehiculos_disponibles', 1) 

    # Verificar que haya al menos dos direcciones (incluyendo el depot)
    if len(direcciones) < 2:
        return jsonify({"error": "Se requieren al menos dos direcciones para optimizar una ruta"}), 400

    
    distance_matrix = calcular_matriz_distancias(direcciones)

   
    resultado = calcular_ruta_optima(distance_matrix, num_vehiculos)
    if 'error' in resultado:
        return jsonify({"error": resultado['error']}), 400
    else:
        return jsonify(resultado)

def calcular_ruta_optima(distance_matrix, num_vehiculos):
    try:
        
        num_nodos = len(distance_matrix)
        depot = 0
        manager = pywrapcp.RoutingIndexManager(num_nodos, num_vehiculos, depot)

        
        routing = pywrapcp.RoutingModel(manager)

        def distancia(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(distance_matrix[from_node][to_node])

        # Registrar la función de distancia y establecerla como costo
        transit_callback_index = routing.RegisterTransitCallback(distancia)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # parametros de búsqueda
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.time_limit.seconds = 20 
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

       
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            rutas = {}
            distancia_total = 0
            for vehicle_id in range(num_vehiculos):
                index = routing.Start(vehicle_id)
                ruta_vehiculo = []
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    ruta_vehiculo.append(node_index)
                    previous_index = index
                    index = solution.Value(routing.NextVar(index))
                    distancia_total += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
                
                
                depot_index = manager.IndexToNode(index)
                if depot_index != depot:
                    ruta_vehiculo.append(depot)

                if len(ruta_vehiculo) > 1:
                    rutas[vehicle_id] = ruta_vehiculo

            return {
                "rutas": rutas,
                "distancia_total": distancia_total,
                "mensaje": "Rutas optimizadas calculadas exitosamente"
            }
        else:
            return {"error": "No se pudo encontrar una solución"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(debug=True)