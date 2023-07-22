from graphv2 import Graph
from flask import Flask, render_template, request, redirect, url_for, jsonify
import networkx as nx
import matplotlib.pyplot as plt
import os
import matplotlib
import json
from geopy.geocoders import Nominatim
import requests
matplotlib.use('Agg')
import numpy as np
from geopy.distance import geodesic
import random

main_screen = Flask(__name__,
                    template_folder="templates",
                    static_url_path="/static")
ob = Graph()
graph_object = None
pos = None
dpos = None
static_folder_path = None


base_url = "https://api.tomtom.com"
version_number = "4"
style = "relative"
zoom = "12"
format = "json"
api_key = "L0Xj943A4jttdtCPohFfcuoVOuuudYFq"
thickness = '5'


app = Flask(__name__)
geolocator = Nominatim(user_agent="geoapiExercises")

d = {}
places = ['alandur','ambattur','purasawalkam','egmore','kalavakkam','madhuravoyal','avadi','kilpauk','adyar','vellore','guindy']
dic = {}

@app.route('/')
def index():
    return render_template('mainscreen.html')

def construct_graph():

    global places,dic

    for i in places:
        location = geolocator.geocode(i)
        latitude = location.latitude
        longitude = location.longitude

        url = f"{base_url}/traffic/services/{version_number}/flowSegmentData/{style}/{zoom}/{format}?key={api_key}&point={latitude},{longitude}&thickness={thickness}"
        params = {
            "key": api_key,
        }
        response = requests.get(url, params=params)
        
        flow_segment_data = response.json()

        ob.insert_node(i,int(flow_segment_data["flowSegmentData"]["freeFlowSpeed"]))
        dic[i]={'lat':latitude,'lon':longitude}


    for j in places:
        count = 0
        while(1):
            a = random.randint(0,10)
            if places[a] != j :
                location1 = (dic[places[a]]['lat'], dic[places[a]]['lon']) 
                location2 = (dic[j]['lat'], dic[j]['lon'])  

                distance = geodesic(location1, location2).miles
                print("Distance:", distance, "miles")
                ob.insert_edge_twoway(j,places[a], distance)
                if count == 1:
                   break
                else:
                   count+=1

    global graph_object, pos
    graph_object = nx.DiGraph()
    for node in ob.nodes:
        graph_object.add_node(node.name, traffic_no=node.traffic_no)
    for edge in ob.edges_lst:
        graph_object.add_edge(edge.frm.name, edge.to.name, weight=int(edge.wt))

    k = 21 / np.sqrt(len(graph_object.nodes())
                    )  # Adjust the spring constant based on the number of nodes
    pos = nx.spring_layout(graph_object, k=k, seed=42)


def draw_graph():
  plt.figure(figsize=(6.5, 5.1))
  node_labels = {node: node for node in graph_object.nodes()}
  edge_labels = nx.get_edge_attributes(graph_object, 'weight')

  nx.draw_networkx(graph_object,
                   pos,
                   with_labels=False,
                   node_size=500,
                   node_color='lightblue',
                   edge_color='black')

  nx.draw_networkx_labels(graph_object,
                          pos,
                          labels=node_labels,
                          font_size=8,
                          verticalalignment='center')

  edge_labels = nx.draw_networkx_edge_labels(graph_object,
                                             pos,
                                             edge_labels=edge_labels,
                                             font_size=6)

  plt.title('Graph Visualization')
  plt.axis('off')
  plt.savefig(os.path.join(static_folder_path, 'graph_before_dijkstra.png'))


@main_screen.route('/')
def main_index():
  draw_graph()
  return render_template('mainscreen.html')


@main_screen.route('/graphwindow.html')
def graph_window():
  return render_template('graphwindow.html')


@main_screen.route('/add_node', methods=['POST'])
def add_node():
  if request.method == 'POST':
    nodename = request.form['nodename']

    location = geolocator.geocode(nodename)
    latitude = location.latitude
    longitude = location.longitude

    url = f"{base_url}/traffic/services/{version_number}/flowSegmentData/{style}/{zoom}/{format}?key={api_key}&point={latitude},{longitude}&thickness={thickness}"
    params = {
        "key": api_key,
    }
    response = requests.get(url, params=params)
    
    flow_segment_data = response.json()
    splim = int(flow_segment_data["flowSegmentData"]["freeFlowSpeed"])
    global places,dic
    places.append(nodename)
    dic[nodename]={'lat':latitude,'lon':longitude}

    draw_graph()  # Redraw the graph with the new node

    return redirect(
      url_for('add_nodeforcustom', nodename=nodename, splim=splim))


@main_screen.route('/samplenode', methods=['POST','GET'])
def add_nodeforcustom():
    nodename = request.args.get('nodename')
    splim = request.args.get('splim')
    global places,dic, ob

    draw_graph()  # Redraw the graph with the new node
    print('ok')
    # Perform basic validation
    if nodename.strip() == '':
        return "Error: Please enter the name of the location."

    # Add the sample node to the graph
    ob.insert_node(nodename, int(splim))
    global graph_object, pos
    graph_object = nx.DiGraph()
    for node in ob.nodes:
        graph_object.add_node(node.name, traffic_no=node.traffic_no)
    for edge in ob.edges_lst:
        graph_object.add_edge(edge.frm.name, edge.to.name, weight=int(edge.wt))

    k = 21 / np.sqrt(len(graph_object.nodes())
                    )  # Adjust the spring constant based on the number of nodes
    pos = nx.spring_layout(graph_object, k=k, seed=42)

    draw_graph()

    # Save the updated graph visualization
    plt.title('Graph Visualization with New Node')
    plt.axis('off')
    plt.savefig(os.path.join(static_folder_path, 'graph_before_dijkstra.png'))
    # plt.savefig(os.path.join(static_folder_path, 'graph_before_dijkstra.png'))
    return "Success: Sample node '{}' with speed limit '{}' added to the graph.".format(
        nodename, splim)


@main_screen.route('/add_edge', methods=['POST'])
def add_edge():
  if request.method == 'POST':
    frm = request.form['frm']
    to = request.form['to']

    location1 = (dic[frm]['lat'], dic[frm]['lon']) 
    location2 = (dic[to]['lat'], dic[to]['lon'])  

    distance = geodesic(location1, location2).miles

    draw_graph()  # Redraw the graph with the new node

    return redirect(
      url_for('add_edgeforcustom', distance=distance, frm=frm, to=to))

@main_screen.route('/sampleedge' ,methods=['POST','GET'])
def add_edgeforcustom():
    frm = request.args.get('frm')
    to = request.args.get('to')
    global graph_object, pos,ob
    ob.insert_edge_twoway(frm, to, request.args.get('distance'))
  
    graph_object = nx.DiGraph()
    for node in ob.nodes:
        graph_object.add_node(node.name, traffic_no=node.traffic_no)
    for edge in ob.edges_lst:
        graph_object.add_edge(edge.frm.name, edge.to.name, weight=int(edge.wt))

    k = 21 / np.sqrt(len(graph_object.nodes())
                    )  # Adjust the spring constant based on the number of nodes
    pos = nx.spring_layout(graph_object, k=k, seed=42)

    # Redraw the graph with the new node
    draw_graph()

    # Save the updated graph visualization
    plt.title('Graph Visualization with New Node')
    plt.axis('off')
    plt.savefig(os.path.join(static_folder_path, 'graph_beforedijkstra.png'))
    # plt.savefig(os.path.join(static_folder_path, 'graph_before_dijkstra.png'))
    return "Success: Sample edge added to the graph."


@main_screen.route('/resetmap', methods=['POST'])
def reset():
    return redirect(url_for('reset_graph'))


@main_screen.route('/resetthemap')
def reset_graph():

  return "Success: Map has been reset!"


@main_screen.route('/dij')
def dij():
  start = request.args.get('start')
  end = request.args.get('end')

  draw_graph()

  path, dist = ob.dijkstra(start, end)
  path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
  edge_labels = nx.get_edge_attributes(graph_object, 'weight')
  edge_colors = [
    'springgreen' if (edge[0], edge[1]) in path_edges or
    (edge[1], edge[0]) in path_edges else 'red' for edge in graph_object.edges
  ]
  weights = [edge_labels[edge] / 5.5 for edge in graph_object.edges]
  nx.draw_networkx_edges(graph_object,
                         pos,
                         edgelist=graph_object.edges,
                         edge_color=edge_colors,
                         width=weights)

  nx.draw_networkx_edge_labels(graph_object, pos, edge_labels=edge_labels)

  plt.title('Shortest Path Visualization')
  plt.axis('off')
  plt.savefig(os.path.join(static_folder_path, 'graph_after_dijkstra.png'))

  response = {'distance': dist, 'path': path}
  return jsonify(response)


@main_screen.route('/process_input', methods=['POST'])
def process_input():

  start = request.form['start']
  end = request.form['end']
  return redirect(url_for('dij', start=start, end=end))


if __name__ == "__main__":
    static_folder_path = os.path.join(os.getcwd(), 'static')
    if not os.path.exists(static_folder_path):
        os.makedirs(static_folder_path)

    construct_graph()
    main_screen.run(debug=True, host="0.0.0.0", port=8080)