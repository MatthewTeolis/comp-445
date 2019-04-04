import ipaddress
import socket

# class SelectiveRepeat:
#     _window_size = 5
#     _sequence_size = 2 * _window_size
#     _buffer = list()
#
#
from common.Connection import Connection
from common.Packet import Packet, MAX_LEN, MIN_LEN, DATA, SYN, SYN_ACK, ACK


class Receiver:

    # def __init__(self, address, port, router_address, router_port, window_size=2):
    def __init__(self):
        # self._address = address
        # self._port = port
        # self._router_address = router_address
        # self._router_port = router_port
        # self._window_size = window_size
        # self._sequence_size = 2 * window_size
        # self._buffer = list()
        # self._sequence_number = 0

        self._conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def listen(self, port):
        self._conn.bind(('', port))

    def accept(self):
        packet, sender = self._recv_packet()
        if packet.packet_type == SYN:
            response_packet = Packet(SYN_ACK, packet.seq_num + 1, packet.peer_ip_addr, packet.peer_port, None)
            self._conn.sendto(response_packet.to_bytes(), (sender[0], sender[1]))
            packet_ack, sender_ack = self._recv_packet()
            if packet_ack.packet_type == ACK:
                return Connection(packet_ack.peer_ip_addr, packet_ack.peer_port), sender_ack

    def _recv_packet(self):
        data, sender = self._conn.recvfrom(MAX_LEN)
        packet = Packet.from_bytes(data)
        return packet, sender

    def handle_window(self):
        while True:
            pass

    def send_data(self, data: str):
        # if the data is too big, split data into multiple packets
        packets = self.create_packets(data)
        self._buffer.extend(packets)
        # for each packet, send packet and start timer for each
        # if timer times out for given packet, send packet again
        # if packet is NAK, send packet again
        pass

    def _get_and_increment_sequence_number(self):
        number = self._sequence_number
        self._sequence_number += 1

        if self._sequence_number >= self._sequence_size:
            self._sequence_number = 0

        return number

    def create_packets(self, data: str):
        packets = list()
        chunks = Receiver.chunk_data(data.encode('utf-8'), MAX_LEN - MIN_LEN)

        for chunk in chunks:
            packets.append(Packet(DATA, self._get_and_increment_sequence_number(), self._address, self._port, chunk))

        return packets

    def send_packet(self, packet: Packet):
        """
        Sends a packet a minimum number of times
        :param packet: Packet being sent
        :return: void
        """
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        max_tries = 5
        count = 0

        while count < max_tries:
            try:
                conn.sendto(packet.to_bytes(), (self._router_address, self._router_port))
                conn.settimeout(timeout)
                response, sender = conn.recvfrom(MAX_LEN)
                print(response, sender)
            except socket.timeout:
                count += 1

        conn.close()

    @staticmethod
    def chunk_data(data, length):
        return (data[0+i:length+i] for i in range(0, len(data), length))


def run_server(port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))
        print('Echo server is listening at', port)
        while True:
            data, sender = conn.recvfrom(1024)
            handle_client(conn, data, sender)

    finally:
        conn.close()


def handle_client(conn, data, sender):
    try:
        p = Packet.from_bytes(data)
        print("Router: ", sender)
        print("Packet: ", p)
        print("Payload: ", p.payload.decode("utf-8"))

        # How to send a reply.
        # The peer address of the packet p is the address of the client already.
        # We will send the same payload of p. Thus we can re-use either `data` or `p`.
        conn.sendto(p.to_bytes(), sender)

    except Exception as e:
        print("Error: ", e)


if __name__ == '__main__':
    r = Receiver()
    r.listen(8007)
    r.accept()
