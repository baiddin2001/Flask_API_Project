from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "samplemodel"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, Tracer!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

#READ
@app.route("/agents", methods=["GET"])
def get_agents():
    data = data_fetch("""SELECT * FROM agents""")
    return make_response(jsonify(data), 200)

@app.route("/agents/<int:id>", methods=["GET"])
def get_agents_by_id(id):
    data = data_fetch("""SELECT * FROM agents WHERE AGENT_CODE = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/agents/<int:id>/CustOrder", methods=["GET"])
def get_customerOrder_by_agents(id):
    data = data_fetch(
        """
    SELECT AGENT_NAME, CUST_NAME, ORD_AMOUNT, ADVANCE_AMOUNT, ORD_DESCRIPTION FROM agents 
    INNER JOIN  customer
    ON agents.AGENT_CODE = customer.AGENT_CODE 
    INNER JOIN orders 
    ON customer.CUST_CODE = customer.CUST_CODE 
    WHERE agents.AGENT_CODE = {};                
    """.format(
            id
        )
    )
    return make_response(
        jsonify({"AGENT_CODE": id, "count": len(data), "CUSTOMER_ORDER": data}), 200
    )

if __name__ == "__main__":
    app.run(debug=True)