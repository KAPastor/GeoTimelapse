import osmnx as ox
import networkx as nx
import imageio
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageEnhance
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt




start_location = (43.46713, -79.72782)
G = ox.graph_from_point(start_location, distance=1000, network_type='walk')
nearest_node = ox.get_nearest_node(G, start_location, return_dist=True)[0]
print (nearest_node)
ec = ox.get_edge_colors_by_attr(G, attr='length')
print()
# Starting from the nearest node to the start of the run find all edges
total_distance = 0.0;
running_route = [nearest_node];
images=[]

while total_distance < 5000.0: # 5k run
    # Get the nearest nodes from the last node
    adj_edges = G.edges(running_route[-1])
    # For each edge, find the length
    next_node = []
    next_node_length = 0.;
    for e in adj_edges:
        tmp_next_node = e[1]
        tmp_next_node_length = G[running_route[-1]][e[1]][0]['length']
        if (tmp_next_node_length > next_node_length) & (tmp_next_node not in running_route):
            next_node_length = tmp_next_node_length
            next_node = tmp_next_node

    if next_node == []:
        for e in adj_edges:
            next_node = e[1]
            next_node_length = G[running_route[-1]][e[1]][0]['length']

    # We selected based on longest next edge
    total_distance = total_distance + next_node_length
    running_route.append(next_node)
    fig, ax = ox.plot_graph_route(G, running_route, edge_color=ec,fig_height=6, fig_width=6,show=False, save=True, file_format='png', filename='tmp')
    ax.scatter(start_location[1], start_location[0], c='k', s=30)
    # Now we animate
    im = Image.open('./images/tmp.png').convert("RGBA")
    txt = Image.new('RGBA', im.size, (255,255,255,0))
    font = ImageFont.truetype("./roboto/Roboto-Bold.ttf", 80)
    w, h = im.size
    d = ImageDraw.Draw(txt)
    distance_string = str(round(total_distance/1000.,2))+' KM'
    d.rectangle(((w-400, h-200), (w, h)), fill="white")

    d.text((w-400, h-100),distance_string,(10,10,10,200),font=font)
    combined = Image.alpha_composite(im, txt)
    combined.save("./images/tmp.png")
    images.append(imageio.imread("./images/tmp.png"))
    print (total_distance)

imageio.mimsave("./Animation.gif", images,duration=0.3)

# route = nx.shortest_path(G,nearest_node[0] ,nearest_node[0])
# n = list(G.neighbors(nearest_node[0]))
# next_neighbour = n[0]
# node_info = G.node[next_neighbour]
# print (node_info)
# path = list(nx.all_simple_paths(G, source=nearest_node[0], target=next_neighbour,cutoff=20))
# main_path = path[-1]
# print(main_path)
# Gonna make my own path!
#
# fig, ax = ox.plot_graph_route(G, running_route, edge_color=ec,fig_height=6, fig_width=6,show=False, close=False)
# ax.scatter(start_location[1], start_location[0], c='k', s=30)
# plt.show()

# ox.plot_graph_route(G, main_path,route_color='g',edge_color=ec,fig_height=6, fig_width=6,show=False, save=True, file_format='png', filename='tmp')
#
# print (len(path))










    # # print (G.nodes)
    # # route = nx.shortest_path(G, 779310080,1578921468)
    #
    # # ox.plot_graph_route(G, route,fig_height=6,fig_width=6,edge_color=ec,show=False, save=True, file_format='png', filename=str(i).zfill(4))
    # ox.plot_graph(G, fig_height=6,fig_width=6,edge_color=ec,show=False, save=True, file_format='png', filename=str(i).zfill(7))




# for i in range(200,2000,10):
#     print (i)
#     G = ox.graph_from_point((43.46713, -79.72782), distance=i, network_type='walk')
#     # ox.plot_graph(G)
#     # print (G.nodes)
#     # route = nx.shortest_path(G, 779310080,1578921468)
#     ec = ox.get_edge_colors_by_attr(G, attr='length')
#
#     # ox.plot_graph_route(G, route,fig_height=6,fig_width=6,edge_color=ec,show=False, save=True, file_format='png', filename=str(i).zfill(4))
#     ox.plot_graph(G, fig_height=6,fig_width=6,edge_color=ec,show=False, save=True, file_format='png', filename=str(i).zfill(7))


# images = []
# onlyfiles = [f for f in listdir('./images/') if isfile(join('./images/', f))]
#
# filenames = onlyfiles
# # print filenames
# i=0
# for filename in filenames:
#     print (filename)
#     im = Image.open('./images/' + filename).convert("RGBA")
#     txt = Image.new('RGBA', im.size, (255,255,255,0))
#     font = ImageFont.truetype("./roboto/Roboto-Bold.ttf", 80)
#     w, h = im.size
#     d = ImageDraw.Draw(txt)
#     alpha = 15.0*i
#     d.text((w-400, h-100),'Oakville',(10,10,10,min(int(alpha),200)),font=font)
#     combined = Image.alpha_composite(im, txt)
#     combined.save("./tmp.png")
#
#     images.append(imageio.imread("./tmp.png"))
#
#     # images.append(imageio.imread('./images/' + filename))
#
#     i=i+1
# imageio.mimsave("./Animation.gif", images,duration=0.05)
