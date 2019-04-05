import ipaddress
import socket
import threading

from common.Connection import Connection
from common.Packet import Packet, MAX_LEN, MIN_LEN, DATA, SYN, SYN_ACK, ACK


class Receiver:

    # def __init__(self, address, port, router_address, router_port, window_size=2):
    def __init__(self, port):
        # self._address = address
        self.__port = port
        # self._router_address = router_address
        # self._router_port = router_port
        # self._window_size = window_size
        # self._sequence_size = 2 * window_size
        # self._buffer = list()
        # self._sequence_number = 0
        self._list_of_connections = list()
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_connection(self):
        return self._conn

    def listen(self):
        self._conn.bind(('', self.__port))

    def accept(self):
        packet, sender = self.recv_packet()
        if packet.packet_type == SYN:
            response_packet = Packet(SYN_ACK, packet.seq_num + 1, packet.peer_ip_addr, packet.peer_port, None)
            self._conn.sendto(response_packet.to_bytes(), (sender[0], sender[1]))
            packet_ack, sender_ack = self.recv_packet()
            if packet_ack.packet_type == ACK:
                # Connection established
                connection = Connection(packet_ack.peer_ip_addr, packet_ack.peer_port, self)
                self._list_of_connections.append(connection)
                return connection, sender
        # elif packet.packet_type == DATA:
        #     if Connection(packet.peer_ip_addr, packet.peer_port, self) in self._list_of_connections:
        #         self.handle_data_packet(packet, sender)

    def recv_packet(self):
        data, sender = self._conn.recvfrom(MAX_LEN)
        packet = Packet.from_bytes(data)
        return packet, sender

    def notify_connections(self):
        for connection in self._list_of_connections:
            connection.handle_packet(packet, sender)

    def handle_data_packet(self, packet, sender):
        self._conn.sendto(Packet(ACK, 0, packet.peer_ip_addr, packet.peer_port, None).to_bytes(), sender)


def listen_to_client(client, address):
    data = client.recv(1024).decode('utf-8')
    print(data)


if __name__ == '__main__':
    r = Receiver(8007)
    r.listen()
    while True:
        client, address = r.accept()
        threading.Thread(target=listen_to_client, args=(client, address)).start()
