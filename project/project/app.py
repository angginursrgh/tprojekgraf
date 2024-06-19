from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import heapq

app = Flask(__name__, template_folder='templates')
CORS(app)


# Define your graph (copy from your Python code)
graph = {
    'A': {'B': 0.51},
    'B': {'A': 0.51, 'C': 0.44, 'N': 0.56},
    'C': {'B': 0.44, 'D': 0.35, 'O': 0.61},
    'D': {'C': 0.35, 'E': 0.2},
    'E': {'D': 0.2, 'F': 0.17,'R':0.61},
    'F': {'E': 0.17, 'G': 0.17, 'S': 0.61},
    'G': {'F': 0.17, 'H': 0.06, 'T': 0.61},
    'H': {'G': 0.06, 'I': 0.06,'U':0.61},
    'I': {'H': 0.06, 'J': 0.12, 'V': 0.61},
    'J': {'I': 0.12, 'K': 0.17, 'W': 0.61},
    'K': {'J': 0.17, 'L': 0.07,'X':0.61},
    'L': {'K': 0.07, 'M': 0.2, 'Y': 0.61},
    'M': {'L': 0.2, 'Z': 0.61},
    'N': {'B': 0.56, 'O': 0.36},
    'O': {'C': 0.61, 'N': 0.36, 'P': 0.22},
    'P': {'O': 0.22, 'Q': 0.12},
    'Q': {'P': 0.12, 'R': 0.31},
    'R': {'E': 0.61, 'Q': 0.31, 'S': 0.19,'AA':0.31},
    'S': {'F': 0.61, 'R': 0.19, 'T': 0.18},
    'T': {'G': 0.61, 'S': 0.18,'U':0.06,'AC':0.14},
    'U': {'H': 0.61, 'T': 0.06, 'V': 0.06},
    'V': {'I': 0.61, 'U': 0.06, 'W': 0.12},
    'W': {'J': 0.61, 'V': 0.12,'X':0.17},
    'X': {'K': 0.61, 'W': 0.17, 'Y': 0.07},
    'Y': {'L': 0.61, 'X': 0.07, 'Z': 0.2},
    'Z': {'M': 0.61, 'Y': 0.2,'AD':0.14},
    'AA': {'R': 0.31, 'AB': 0.36, 'AH': 0.35},
    'AB': {'AA': 0.36, 'AC': 0.18, 'AE': 0.29,'AJ':0.36},
    'AC': {'T': 0.14, 'AD': 0.65,'AB':0.18},
    'AD': {'Z': 0.14, 'AC': 0.65, 'AG': 0.1},
    'AE': {'AB': 0.29, 'AF': 0.17},
    'AF': {'AE': 0.17, 'AG': 0.41},
    'AG': {'AD': 0.1, 'AF': 0.41, 'AL': 0.05},
    'AH': {'AA': 0.35, 'AI': 0.21, 'AM': 0.85},
    'AI': {'AH': 0.21, 'AJ': 0.16,'AO':0.51},
    'AJ': {'AB': 0.36, 'AI': 0.31, 'AK': 0.71},
    'AK': {'AJ': 0.31, 'AL': 0.71, 'AO': 0.66},
    'AL': {'AG': 0.05, 'AR': 1.2},
    'AM': {'AH': 0.85, 'AN': 0.89, 'AS': 0.16},
    'AN': {'AM': 0.89, 'AO': 0.35, 'AP': 0.04},
    'AO': {'AI': 0.51, 'AK': 0.66,'AN':0.35,'AP':0.31},
    'AP': {'AN': 0.04, 'AO': 0.31,'AQ':0.36,'AU':0.36},
    'AQ': {'AP': 0.36, 'AR': 1.2, 'AV': 0.56},
    'AR': {'AL': 1.2, 'AQ': 1.2,'AW':0.5},
    'AS': {'AM': 0.16, 'AN': 0.2, 'AT': 0.04},
    'AT': {'AS': 0.03, 'AU': 0.4},
    'AU': {'AT': 0.4, 'AV': 0.3,'AP':0.36},
    'AV': {'AU': 0.3, 'AW': 0.7, 'AQ': 0.56},
    'AW': {'AR': 0.5, 'AX': 0.1},
    'AX':{}
}

def dijkstra(graph, start, end):
    import heapq
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    shortest_path = {}
    while queue:
        (current_distance, current_node) = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_path[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    path = []
    while end:
        path.append(end)
        end = shortest_path.get(end)
    path = path[::-1]
    return distances, path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dijkstra', methods=['POST'])
def dijkstra_route():
    data = request.get_json()
    print(f"Received data: {data}")  # Logging data received from client
    start_node = data['start']
    end_node = data['end']
    distances, path = dijkstra(graph, start_node, end_node)
    response = {'distance': distances[end_node], 'path': path}
    print(f"Sending response: {response}")  # Logging response data
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)