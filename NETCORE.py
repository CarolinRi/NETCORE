import networkx as nx

"""
this code is provided as supplemental material to the publication "An Efficiency-Driven, Correlation-Based Feature Elimination Strategy for Small Data Sets" 
by C. A. Rickert, M. Henkel, and O. Lieleg submitted to APL Machine Learning on August, 4th, 2022.

version 1.0.1 (initial setup: 4th August, 2022)

last changed: October 26th, 2022
"""

# input: data as a pandas dataframe, t_corr (desired correlation threshold, a number between 0 and 1); output: reduced feature vector
def run_NETCORE(data, t_corr):

    corrMatrix = create_corr(data)

    global Graph
    Graph = create_network(corrMatrix, minCorrelation = t_corr)

    global reduced_vector
    reduced_vector = []

    reduce_network()

    print(f"final reduced feature vector: {reduced_vector}")
    print(f"length of the final reduced feature vector: {len(reduced_vector)} (from initially {len(corrMatrix.columns)})")

    return reduced_vector

def create_corr(data):

    corrMatrix = data.corr(method='pearson')
    corrMatrix = corrMatrix.astype(float, errors='raise')

    return corrMatrix

def create_network(corrMatrix, minCorrelation):
    G = nx.Graph()

    for n in range(len(corrMatrix.columns)):
        G.add_node(n, feature = corrMatrix.columns[n])

    assert G.number_of_nodes() == len(corrMatrix.columns), f'Number of nodes ({G.number_of_nodes()}) not equal to number features ({len(corrMatrix.columns)})'
  
    for n in range(len(corrMatrix.columns)):
        for i in range(len(corrMatrix.columns)):
            if i < n: continue
            if abs(corrMatrix.iloc[n,i]) >= minCorrelation and n != i:
                G.add_edge(n,i, correlation = corrMatrix.iloc[n,i])     

    return G

def reduce_network():

    while len(Graph.nodes()) > 0:

        eliminate_isolates()
        if len(Graph.nodes()) == 0: break

        global candidate_nodes
        candidate_nodes = []
        candidate_nodes = find_highest_degree()

        if len(candidate_nodes) == 1:
            to_fix = Graph.nodes[candidate_nodes[0]]["feature"]
            fix_feature(candidate_nodes[0])
            continue
        elif len(candidate_nodes) > 1:
            find_highest_remaining_degree()

        if len(candidate_nodes) == 1:
            to_fix = Graph.nodes[candidate_nodes[0]]["feature"]
            fix_feature(candidate_nodes[0])
            continue
        elif len(candidate_nodes) > 1:
            find_highest_correlation()

        if len(candidate_nodes) == 1:
            to_fix = Graph.nodes[candidate_nodes[0]]["feature"]
            fix_feature(candidate_nodes[0])
            continue
        else:
            fix_feature(candidate_nodes[0])

def eliminate_isolates():

    if nx.number_of_isolates(Graph) > 0:
        isol = list(nx.isolates(Graph))
        for node in isol:
            node_2 = Graph.nodes[node]["feature"]
            fix_feature(node)

def find_highest_degree():

    nodes_max_degree = []
    sorted_nodes = sorted(Graph.degree, key=lambda x: x[1], reverse=True)

    for n1 in sorted_nodes:
        if n1[1] == sorted_nodes[0][1]:
            nodes_max_degree.append(n1[0])
        else: break

    return nodes_max_degree

def find_highest_remaining_degree():

    remaining_degrees = {}

    for node in candidate_nodes:
        global to_simulate
        to_simulate = node
        view = nx.subgraph_view(Graph,filter_node=filter_node)
        try: 
            remaining_degrees[node] = max([x[1] for x in view.degree])
        except:
            remaining_degrees[node] = 0

    for key, val in remaining_degrees.items():
        if val < max(remaining_degrees.values()):
            candidate_nodes.remove(key)

def find_highest_correlation():

    mean_corr = {}

    for n3 in candidate_nodes:
        indiv_corr = []
        for nbrs in Graph.adj[n3]:
            indiv_corr.append(Graph.edges[n3, nbrs]['correlation'])
    
        mean_corr[n3] = sum(abs(number) for number in indiv_corr)/len(indiv_corr)

    for key, val in mean_corr.items():
        if val < max(mean_corr.values()):
            candidate_nodes.remove(key)

def filter_node(n1):
    return n1 not in Graph.adj[to_simulate] and n1 is not to_simulate

def fix_feature(node):
    
    reduced_vector.append(Graph.nodes[node]["feature"])

    for n4 in Graph.adj[node].copy():
        Graph.remove_node(n4)

    Graph.remove_node(node)
