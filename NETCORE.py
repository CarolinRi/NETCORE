import networkx as nx
import numpy as np
import pandas as pd

"""
this code is provided as supplemental material to the publication "An Efficiency-Driven, Correlation-Based Feature Elimination Strategy for Small Data Sets" 
by C. A. Rickert, M. Henkel, and O. Lieleg submitted to APL Machine Learning on August, 4th, 2022.

version 1.0.1 (initial setup: 4th August, 2022)

last changed: October 31st, 2022
"""

# input: data as a pandas dataframe, t_corr (desired correlation threshold, a number between 0 and 1); output: reduced feature vector
def run_NETCORE(data, t_corr):

    assert 0 <= t_corr <= 1, "The correlation theshold should be between 0 and 1."

    # create a correlation matrix based on the provided dataset
    corrMatrix = create_corr(data)

    # generate a graph based on the correlation matrix: a node will be added for each feature contained in the dataset and edges are added when the correlation between the two features exceeds the correlation threshold
    global Graph
    Graph = create_network(corrMatrix, minCorrelation = t_corr)

    # initialize the new, reduced feature vector
    global reduced_vector
    reduced_vector = []

    # iteratively reduce the network by finding features of highest centrality
    reduce_network()

    # print the results
    print(f"final reduced feature vector: {reduced_vector}")
    print(f"length of the final reduced feature vector: {len(reduced_vector)} (from initially {len(corrMatrix.columns)})")

    return reduced_vector

def create_corr(data):

    # this function creates a correlation matrix based on the pearsons correlation coefficient.

    corrMatrix = data.corr(method='pearson')
    corrMatrix = corrMatrix.astype(float, errors='raise')

    corrMatrix = corrMatrix.dropna(how='all', axis=1, inplace=False)
    corrMatrix = corrMatrix.dropna(how='all', axis=0, inplace=False)

    assert np.array_equal(corrMatrix.columns.values, corrMatrix.index.values), "Dimension mismatch occuring in the correlation matrix." 

    assert corrMatrix.isnull().values.sum() == 0, "The correlation matrix was not successfully created."

    return corrMatrix

def create_network(corrMatrix, minCorrelation):

    # create an empty graph
    G = nx.Graph()

    # add a node for each feature in the dataset
    for n in range(len(corrMatrix.columns)):
        G.add_node(n, feature = corrMatrix.columns[n])

    # test if number of nodes in the created network matches the number of features in the correlation matrix
    assert G.number_of_nodes() == len(corrMatrix.columns), f'Number of nodes ({G.number_of_nodes()}) not equal to number features ({len(corrMatrix.columns)})'
  
    # add edges between nodes, if the correlation coefficient between the two features equals of exceeds the correlation threshold
    for n in range(len(corrMatrix.columns)):
        for i in range(len(corrMatrix.columns)):
            if i < n: continue
            if abs(corrMatrix.iloc[n,i]) >= minCorrelation and n != i:
                G.add_edge(n,i, correlation = corrMatrix.iloc[n,i])

    return G

def reduce_network():

    # this function iteratively performs the reduction of the network based on the centrality of the nodes

    while len(Graph.nodes()) > 0:
        # continue as long as the graph contains nodes

        # eliminate all isolated nodes (nodes without any edges). Those nodes are added to the new, reduced feature vector.
        eliminate_isolates()
        if len(Graph.nodes()) == 0: break

        # initialize empty list of candidate nodes (nodes that might be fixed during this iteration)
        global candidate_nodes
        candidate_nodes = []
        # add all nodes of highest degree to the list of candidate nodes
        candidate_nodes = find_highest_degree()

        # if only one feature has the highest degree, it is added to the new feature vector and the iteration is terminated. 
        if len(candidate_nodes) == 1:
            fix_feature(candidate_nodes[0])
            continue
        # Otherwise, the features (from the remaining candidates) that keep the network with the highest remaining degree are searched and all others are removed from the candidate list.
        elif len(candidate_nodes) > 1:
            find_highest_remaining_degree()

        # If only one feature leads to the highest remaining degree, it is added to the new feature vector and the iteration is terminated.
        if len(candidate_nodes) == 1:
            fix_feature(candidate_nodes[0])
            continue
        #Otherwise, the feature (from the remaining candidates) with the highest correlation strength is searched
        elif len(candidate_nodes) > 1:
            find_highest_correlation()

        # if only one feature has the highest correlation to its neighbors, it is added to the new feature vector and the iteration is terminated.
        if len(candidate_nodes) == 1:
            fix_feature(candidate_nodes[0])
            continue
        #Otherwise, the first feature of the remaining candidates is added to the new, reduced feature vector and the iteration is terminated.
        else:
            fix_feature(candidate_nodes[0])

def eliminate_isolates():

    # this function detects isolates in the network, eliminates those nodes, and adds the corresponding feature to the new, reduced feature vector

    if nx.number_of_isolates(Graph) > 0:
        isol = list(nx.isolates(Graph))
        for node in isol:
            fix_feature(node)

def find_highest_degree():

    # this function analyzes the created network to find the nodes of highest degree

    nodes_max_degree = []
    sorted_nodes = sorted(Graph.degree, key=lambda x: x[1], reverse=True)

    for n1 in sorted_nodes:
        if n1[1] == sorted_nodes[0][1]:
            nodes_max_degree.append(n1[0])
        else: break

    return nodes_max_degree

def find_highest_remaining_degree():

    # this function analyzes the networks that would remain after adding each cadidate node to the new feature vector and only keeps those that would lead to the maximum remaining degree in the network

    remaining_degrees = {}

    for node in candidate_nodes:
        global to_simulate
        to_simulate = node
        view = nx.subgraph_view(Graph,filter_node=filter_node)

        assert view.number_of_nodes() == Graph.number_of_nodes() - len(Graph.adj[to_simulate]) - 1, "simulated network has incorrect number of nodes"

        try:
            remaining_degrees[node] = max([x[1] for x in view.degree])
        except:
            remaining_degrees[node] = 0

    for key, val in remaining_degrees.items():
        if val < max(remaining_degrees.values()):
            candidate_nodes.remove(key)

def find_highest_correlation():

    # this function determines the average correlation of each candidate node to its neighbors in the network and keeps only the nodes with the highest value among the calculated ones

    mean_corr = {}

    for n3 in candidate_nodes:
        indiv_corr = []
        for nbrs in Graph.adj[n3]:
            indiv_corr.append(Graph.edges[n3, nbrs]['correlation'])

        assert len(indiv_corr) == len(Graph.adj[n3]), "wrong number of correlation values for sorting criterion 3"
    
        mean_corr[n3] = sum(abs(number) for number in indiv_corr)/len(indiv_corr)

    for key, val in mean_corr.items():
        if val < max(mean_corr.values()):
            candidate_nodes.remove(key)

def filter_node(n1):

    # this function masks the graph so that node n1 and its neighbors are not showing in the simulated graph

    return n1 not in Graph.adj[to_simulate] and n1 is not to_simulate

def fix_feature(node):

    # this function fixes a feature: the feature is added to the reduced feature vector and together with its direct neighbors (i.e. connected nodes in the network) it is removed from the network
    
    reduced_vector.append(Graph.nodes[node]["feature"])

    for n4 in Graph.adj[node].copy():
        Graph.remove_node(n4)

    Graph.remove_node(node)
