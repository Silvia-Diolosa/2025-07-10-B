
from model.model import Model
from datetime import date

# oppure date(2016, 1, 1)

myModel = Model()
myModel.buildGraph("Electric Bikes", "2016-01-01", "2018-12-28")
nNodes, nEdges = myModel.getGraphDetails()
print(f"Nodi: {nNodes} --- Archi: {nEdges}")

# test ricorsion
# path, score = myModel.getCamminoR1(nodo_partenza, nodo_arrivo, 5)
# print(f"Score: {score}")
# for n in path:
#     print(n)