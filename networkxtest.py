# from model import Profile, db, connect_to_db
# from flask import request
# """
# An example using networkx.Graph().

# miles_graph() returns an undirected graph over the 128 US cities from
# the datafile miles_dat.txt. The cities each have location and population
# data.  The edges are labeled with the distance betwen the two cities.

# This example is described in Section 1.1 in Knuth's book [1,2].

# References.
# -----------

# [1] Donald E. Knuth,
#     "The Stanford GraphBase: A Platform for Combinatorial Computing",
#     ACM Press, New York, 1993.
# [2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html


# """
    
# import networkx as nx
# from networkx.readwrite import json_graph
# import json
# # from NetworkxD3 import simpleNetworkx

# def miles_graph():
#     """ Return the cites example graph in miles_dat.txt
#         from the Stanford GraphBase.
#     """
#     # open file miles_dat.txt.gz (or miles_dat.txt)
#     G=nx.DiGraph()

#     age_min=18
#     age_max=98
#     orientation_tuple=tuple(["Straight","Gay","Bisexual"])
#     gender_tuple=tuple(["Woman","Man"])
    
#     users = db.session.query(Profile.gender, Profile.orientation, Profile.age).filter(
#         Profile.orientation.in_(orientation_tuple)).filter(
#         Profile.gender.in_(gender_tuple)).filter(
#         Profile.age >= age_min).filter(Profile.age <= age_max).order_by(Profile.age).all()





#     G.add_node(1) # root
#     for gender, orientation, age in users:

#         G.add_node(gender)
#         G.add_node(gender+", "+orientation)
#         G.add_node(gender+", "+orientation+", "+str(age))
#         G.add_edge(1, gender)
#         if G.has_edge(gender, gender+", "+orientation):
#             G[gender][gender+", "+orientation]['weight']+=1
#             if G.has_edge(gender+", "+orientation, gender+", "+orientation+", "+str(age)):
#                 G[gender+", "+orientation][gender+", "+orientation+", "+str(age)]['weight']+=1

#             else:
#                 G.add_edge(gender+", "+orientation, gender+", "+orientation+", "+str(age), weight=1)
#             # G[age][orientation]['weight']+=1
#             # G[gender][orientation][age]['weight']+=1
#         else:
#             # G.add_edges(orientation, age, {'weight': 1})
#             G.add_edge(gender, gender+", "+orientation, weight= 1)

#         # print "edges", G.edges()
#         # print "node", G.nodes()
    
#     # print "g",G.nodes()
#     # print G.edges()

#     # G.add_node("gay")
#     # G.add_node("woman")
#     # print "num of nodes:", G.number_of_nodes()
#     # G.add_edge("gay","woman",{'weight':3.1415})
#     # print "num of edges:", G.number_of_edges()
#     # print "num of degree:", G.degree_iter() 
    

#     graph_json = json_graph.node_link_data(G, 'weight')
#     graph_json=json.dumps(graph_json)

#     # graph_json = json.dumps(json_graph.tree_data(G, root=1))

#     # graph_json = json.dumps(json_graph.adjacency_data(G))

#     data = json_graph.node_link_data(G)
#     graph_json = json_graph.node_link_graph(data)

#     print graph_json
#     return graph_json

# if __name__ == '__main__':
#     import networkx as nx
#     import re
#     import sys
#     from flask_app import app
#     connect_to_db(app)

#     miles_graph()