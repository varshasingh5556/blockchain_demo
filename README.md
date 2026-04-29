🔗 Blockchain-Based Order Tracking System
📌 Overview
This project is a blockchain-based order tracking system that demonstrates how blockchain ensures data integrity, transparency, and security.
Each step of an order (Placed → Packed → Delivered) is stored as a block. Blocks are linked using cryptographic hashes and secured using Proof of Work (mining with nonce).
The system also supports:
Smart contract-like workflow enforcement
Multi-node network simulation
Attack simulation (to demonstrate security)
Consensus mechanism for synchronization
⚙️ Features
* 🔐 Tamper-resistant blockchain
* ⛏ Proof-of-Work mining (nonce-based)
* 📦 Order tracking workflow enforcement
* 🌐 Multi-node communication
* 🔄 Consensus (longest chain rule)
* ⚠️ Attack simulation (basic, smart, full)
 📁 Project Structure
blockchain_demo/
│
├── app.py              # Flask server (API + UI)
├── block.py            # Blockchain logic
├── templates/
│   └── index.html      # Frontend UI
🚀 How to Run the Project
1. Install dependencies
pip install flask requests
2. Run a node (default)
python3 app.py
Runs on:
http://127.0.0.1:5000
Run multiple nodes (for network)
Open multiple terminals:
python3 app.py 5000
python3 app.py 5001
python3 app.py 5002
 4. Connect nodes
In the UI:
* Enter node address (example):
http://127.0.0.1:5001
 Click Add Node
Repeat for all nodes.
5. Add order steps
Use dropdown:
* Order Placed
* Packed
* Shipped
* Out for Delivery
* Delivered
System enforces correct order.
6. Sync nodes
Click Sync to:
* Fetch longest chain
* Maintain consistency across nodes
 ⚠️ Attack Simulation
| Attack Type  | Description                                       |
| ------------ | ------------------------------------------------- |
| Basic Attack | Changes data without updating hash (fails)        |
| Smart Attack | Updates one hash (still fails)                    |
| Full Attack  | Re-mines entire chain (computationally expensive) |
🧠 How It Works
1. User adds a step
2. Block is mined using nonce (Proof of Work)
3. Block is added to chain
4. Block is broadcast to other nodes
5. Nodes verify hash + previous hash + PoW
6. Chain remains consistent via consensus
 🔐 Key Concepts Demonstrated
* Hashing (SHA-256)
* Proof of Work
* Nonce-based mining
* Blockchain structure
* Distributed nodes
* Consensus mechanism
🎯 Example Use Cases
* E-commerce tracking
* Supply chain management
* Logistics systems
* Secure record keeping
 👩‍💻 Author
Varsha Singh
