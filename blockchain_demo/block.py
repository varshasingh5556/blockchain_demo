import hashlib
import datetime
import requests
class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.mine_block()
    def mine_block(self, difficulty=3):
        prefix = '0' * difficulty
        while True:
            value = (
                str(self.index)
                + self.timestamp
                + self.data
                + self.prev_hash
                + str(self.nonce)
            )
            hash_val = hashlib.sha256(value.encode()).hexdigest()
            if hash_val.startswith(prefix):
                return hash_val
            self.nonce += 1
    def calculate_hash(self):
        value = (
            str(self.index)
            + self.timestamp
            + self.data
            + self.prev_hash
            + str(self.nonce)
        )
        return hashlib.sha256(value.encode()).hexdigest()
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nodes = set()
        self.allowed_steps = [
            "Order Placed",
            "Packed",
            "Shipped",
            "Out for Delivery",
            "Delivered"
        ]
    def create_genesis_block(self):
        return Block(0, "Order Created", "0")
    def register_node(self, address):
        self.nodes.add(address)
    def get_last_block(self):
        return self.chain[-1]
    def add_block(self, data, broadcast=True):
        data = data.strip()
        normalized = [step.lower() for step in self.allowed_steps]
        if data.lower() not in normalized:
            return False
        data = self.allowed_steps[normalized.index(data.lower())]
        current_index = len(self.chain) - 1
        if current_index >= len(self.allowed_steps):
            return False
        expected_step = self.allowed_steps[current_index]
        if data != expected_step:
            return False
        prev = self.get_last_block()
        new_block = Block(len(self.chain), data, prev.hash)
        self.chain.append(new_block)
        if broadcast:
            for node in self.nodes:
                try:
                    requests.post(f"{node}/receive_block", json={
                        "index": new_block.index,
                        "timestamp": new_block.timestamp,
                        "data": new_block.data,
                        "prev_hash": new_block.prev_hash,
                        "hash": new_block.hash,
                        "nonce": new_block.nonce
                    })
                except:
                    pass
        return True
    def receive_block(self, block_data):
        last_block = self.get_last_block()
        if block_data['prev_hash'] != last_block.hash:
            print("Rejected: Invalid previous hash ❌")
            return False
        value = (
            str(block_data['index'])
            + block_data['timestamp']
            + block_data['data']
            + block_data['prev_hash']
            + str(block_data['nonce'])
        )
        calculated_hash = hashlib.sha256(value.encode()).hexdigest()
        if calculated_hash != block_data['hash']:
            print("Rejected: Invalid hash ❌")
            return False
        if not block_data['hash'].startswith('000'):
            print("Rejected: Invalid proof of work ❌")
            return False
        b = Block(
            block_data['index'],
            block_data['data'],
            block_data['prev_hash']
        )

        b.timestamp = block_data['timestamp']
        b.nonce = block_data['nonce']
        b.hash = block_data['hash']
        self.chain.append(b)
        print("Block accepted from network ✅")
        return True
    def is_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.prev_hash != prev.hash:
                return False
        return True
    def replace_chain(self):
        longest_chain = None
        max_length = len(self.chain)
        for node in self.nodes:
            try:
                response = requests.get(f"{node}/chain")
                data = response.json()
                if data['length'] > max_length and self.is_chain_valid_external(data['chain']):
                    max_length = data['length']
                    longest_chain = data['chain']
            except:
                pass
        if longest_chain:
            self.chain = self.convert_to_blocks(longest_chain)
            return True
        return False
    def is_chain_valid_external(self, chain):
        for i in range(1, len(chain)):
            curr = chain[i]
            prev = chain[i - 1]
            value = (
                str(curr['index']) +
                curr['timestamp'] +
                curr['data'] +
                curr['prev_hash'] +
                str(curr['nonce'])
            )
            hash_check = hashlib.sha256(value.encode()).hexdigest()
            if curr['hash'] != hash_check:
                return False
            if curr['prev_hash'] != prev['hash']:
                return False
        return True
    def convert_to_blocks(self, chain_data):
        new_chain = []
        for block in chain_data:
            b = Block(block['index'], block['data'], block['prev_hash'])
            b.timestamp = block['timestamp']
            b.nonce = block['nonce']
            b.hash = block['hash']
            new_chain.append(b)
        return new_chain