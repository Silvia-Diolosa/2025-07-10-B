import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self.idMap = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getAllCategories(self):
        return DAO.getAllCategories()


    def buildGraph(self, categoria, anno1, anno2):
        self._graph.clear()
        self.idMap.clear()

        nodes = DAO.getAllNodes(categoria)
        for node in nodes:
            self.idMap[node.product_id] = node
        self._graph.add_nodes_from(nodes)

        edges = DAO.getEdges(categoria, anno1, anno2)
        for edge in edges:
            u = self.idMap[edge[0]]
            venditeU = edge[1]
            pezziU = edge[2]
            v = self.idMap[edge[3]]
            venditeV = edge[4]
            pezziV = edge[5]
            if pezziU < pezziV:
                self._graph.add_edge(u, v, weight=pezziU+pezziV) # v maggiore, arco esce da u entra in v
            elif pezziU > pezziV:
                self._graph.add_edge(v, u, weight=pezziU+pezziV)
            else:
                self._graph.add_edge(u, v, weight=pezziU+pezziV)
                self._graph.add_edge(v, u, weight=pezziU+pezziV)



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getNumNodes(self):
        return len(self._graph.nodes)
    def getNumEdges(self):
        return len(self._graph.edges)

    def getNodes(self):
        return list(self._graph.nodes)
    def getEdges(self):
        return list(self._graph.edges(data=True))


    def getBest5(self):
        bestprodotti = []
        for n in self._graph.nodes:
            score = 0
            for e_out in self._graph.out_edges(n, data=True):
                score -= e_out[2]["weight"]
            for e_in in self._graph.in_edges(n, data=True):
                score += e_in[2]["weight"]

            bestprodotti.append((n, score))

        bestprodotti.sort(reverse=True, key=lambda x: x[1])
        return bestprodotti[0:5]

