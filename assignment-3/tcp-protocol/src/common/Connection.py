

class Connection:
    from receiver.receiver import Receiver

    def __init__(self, address, port, receiver: Receiver):
        self.address = address
        self.port = port
        self.__receiver = receiver

    def recv(self, buffer_size):
        from common.Packet import Packet
        data, sender = self.__receiver.get_connection().recvfrom(buffer_size)
        packet = Packet.from_bytes(data)
        return packet.payload

    def __eq__(self, other):
        return type(self) == type(other) and self.address == other.address and self.port == other.port
