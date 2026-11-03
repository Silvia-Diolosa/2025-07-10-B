from database.DB_connect import DBConnect
from model.product import Prodotto


class DAO:

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT category_name
FROM categories
ORDER BY category_name"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["category_name"])


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(categoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.* 
FROM products p, categories c
WHERE p.category_id = c.category_id
AND c.category_name = %s """

        cursor.execute(query, (categoria,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(categoria, anno1, anno2):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.product_id as id1, t1.numOrdini as numVend1, t1.pezziVenduti as pezVend1, t2.product_id as id2, t2.numOrdini as numVend2, t2.pezziVenduti as pezVend2
FROM 
(SELECT p.product_id, COUNT(*) as numOrdini, SUM(oi.quantity) AS pezziVenduti
FROM products p, categories c, order_items oi, orders o
WHERE p.category_id = c.category_id
AND c.category_name = %s
AND p.product_id = oi.product_id
AND oi.order_id = o.order_id
AND o.order_date BETWEEN %s AND %s
GROUP BY p.product_id) t1,
(SELECT p.product_id, COUNT(*) as numOrdini, SUM(oi.quantity) AS pezziVenduti
FROM products p, categories c, order_items oi, orders o
WHERE p.category_id = c.category_id
AND c.category_name = %s
AND p.product_id = oi.product_id
AND oi.order_id = o.order_id
AND o.order_date BETWEEN %s AND %s
GROUP BY p.product_id) t2
WHERE t1.product_id < t2.product_id
GROUP By t1.product_id, t2.product_id"""

        cursor.execute(query, (categoria, anno1, anno2, categoria, anno1, anno2))

        for row in cursor:
            results.append((row["id1"], row["numVend1"], row["pezVend1"], row["id2"], row["numVend2"], row["pezVend2"]))

        cursor.close()
        conn.close()
        return results
