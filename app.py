from flask import Flask, render_template, request, jsonify
from block import Blockchain
import sys

app = Flask(__name__)
bc = Blockchain()


@app.route('/')
def home():
    return render_template("index.html", chain=bc.chain, valid=bc.is_valid(), message=None, nodes=bc.nodes)


@app.route('/add', methods=['POST'])
def add():
    step = request.form['step']
    result = bc.add_block(step)

    message = "Step added & broadcasted ✅" if result else "Invalid step/order ❌"

    return render_template("index.html", chain=bc.chain, valid=bc.is_valid(), message=message, nodes=bc.nodes)


@app.route('/register', methods=['POST'])
def register():
    node = request.form['node']
    bc.register_node(node)

    return render_template("index.html", chain=bc.chain, valid=bc.is_valid(), message=f"Node {node} added ✅", nodes=bc.nodes)


@app.route('/receive_block', methods=['POST'])
def receive_block():
    data = request.json
    bc.receive_block(data)
    return jsonify({"message": "Processed"}), 200


@app.route('/chain')
def chain():
    chain_data = []

    for block in bc.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "prev_hash": block.prev_hash,
            "hash": block.hash,
            "nonce": block.nonce
        })

    return {"length": len(chain_data), "chain": chain_data}


@app.route('/sync')
def sync():
    replaced = bc.replace_chain()

    message = "Chain updated from network ✅" if replaced else "Already up-to-date ✅"

    return render_template("index.html", chain=bc.chain, valid=bc.is_valid(), message=message, nodes=bc.nodes)


# Attacks
@app.route('/tamper')
def tamper():
    if len(bc.chain) > 1:
        bc.chain[1].data = "Tampered ❌"
    return render_template("index.html", chain=bc.chain, valid=bc.is_valid(), message="Basic attack ❌", nodes=bc.nodes)


@app.route('/smart_attack')
def smart_attack():
    if len(bc.chain) > 1:
        bc.chain[1].data = "Hacked ⚠️"
        bc.chain[1].hash = bc.chain[1].calculate_hash()
    return render_template("index.html", chain=bc.chain, valid=bc.is_valid(), message="Smart attack ⚠️", nodes=bc.nodes)


@app.route('/full_attack')
def full_attack():
    if len(bc.chain) > 1:
        bc.chain[1].data = "Fully Hacked 🚨"
        for i in range(1, len(bc.chain)):
            bc.chain[i].hash = bc.chain[i].calculate_hash()
    return render_template("index.html", chain=bc.chain, valid=bc.is_valid(), message="Full attack 🚨", nodes=bc.nodes)


if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    app.run(debug=True, port=port)