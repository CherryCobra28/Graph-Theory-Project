import networkx as nx
def barabasi_albert_graph(n, m, seed-None, initial_graph=None):
	if m < 1 or m >= n:
		raise nx.NetworkXError(f"Barabási Albert network must have m >= 1 and m <n, m = {m}, n = {n}"
	if initial graph is None:
	# Default initial graph: star graph on (m + 1) nodes
		G = star_graph (m)
	else:
		if len(initial_graph) < m or len(initial_graph) > n:
			raise nx.NetworkXError(
			f"Barabási Albert initial graph needs between m={m} and n={n} nodes"
			)
		G = initial_graph.copy()
		# List of existing nodes, with nodes repeated once for each adjacent edge
		repeated_nodes = [n for n, d in G.degree() for in range(d)]
		# Start adding the other n - me nodes.
		source = len (G)
		while source < n:
			# Now choose m unique nodes from the existing nodes
			# Pick uniformly from repeated_nodes (preferential attachment)
			targets _random_subset (repeated_nodes, m, seed)
			# Add edges to m nodes from the source.
			G.add_edges_from(zip ([source] * m, targets))
			# Add one node to the list for each new edge just created.
			repeated_nodes.extend (targets)
			# And the new node "source" has m edges to add to the list.
			repeated_nodes.extend([source] * m)
			source += 1
		return G
