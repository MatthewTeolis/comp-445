import ipaddress
import socket
import threading

from common.Packet import Packet, MAX_LEN, MIN_LEN, DATA, SYN, SYN_ACK, ACK, FIN


class Sender:

    def __init__(self, address, port, router_address, router_port, window_size=2):
        # client address and port
        self.__address = address
        self.__port = port
        # router address and port
        self.__router_address = router_address
        self.__router_port = router_port
        # window and buffer
        self.__window_size = window_size
        self.__sequence_size = 2 * window_size
        self.__buffer = list()
        self.__window = list()
        self.__sequence_number = 0

        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.handshake()

    def handshake(self):
        self.__conn.sendto(Packet(SYN, 0, address, port, None).to_bytes(), (self.__router_address, self.__router_port))
        data, sender = self.__conn.recvfrom(MAX_LEN)
        packet = Packet.from_bytes(data)
        if packet.packet_type == SYN_ACK:
            response_packet = Packet(ACK, packet.seq_num + 1, packet.peer_ip_addr, packet.peer_port, None)
            self.__conn.sendto(response_packet.to_bytes(), (sender[0], sender[1]))

    def close(self):
        pass
        # self._conn.sendto(Packet(FIN, self._sequence_number))

    def send_data(self, data: str):
        packet_generator = self.create_packets(data)

        for packet in packet_generator:
            self.add_packet(packet)

    def _get_and_increment_sequence_number(self):
        number = self.__sequence_number
        self.__sequence_number += 1

        if self.__sequence_number >= self.__sequence_size:
            self.__sequence_number = 0

        return number

    def create_packets(self, data: str):
        chunks = Sender.chunk_data(data.encode('utf-8'), MAX_LEN - MIN_LEN)

        for chunk in chunks:
            yield Packet(DATA, self._get_and_increment_sequence_number(), self.__address, self.__port, chunk)

    def send_packet(self, packet: Packet):
        timeout = 5
        max_tries = 5
        count = 0

        while count < max_tries:
            try:
                self.__conn.sendto(packet.to_bytes(), (self.__router_address, self.__router_port))
                self.__conn.settimeout(timeout)
                response, sender = self.__conn.recvfrom(MAX_LEN)
                response_packet = Packet.from_bytes(response)
                while response_packet.packet_type != ACK:
                    response, sender = self.__conn.recvfrom(MAX_LEN)
                    response_packet = Packet.from_bytes(response)
                return packet, sender
            except socket.timeout:
                count += 1

    def add_packet(self, packet: Packet):
        self.__buffer.append(packet)
        if len(self.__window) < self.__window_size:
            self.__repop()

    def __repop(self):
        """
        Repopulate the window buffer list, and start processing the newly added packet
        """
        packet = self.__buffer.pop(0)
        self.__window.append(packet)
        self.process(packet)

    def process_thread(self, packet):
        response_packet, sender = self.send_packet(packet)
        self.notify()
        # self.handle_response_packet(packet, sender)

    def handle_response_packet(self, response, sender):
        pass

    def process(self, packet):
        threading.Thread(target=self.process_thread, args=(packet,)).start()

    def notify(self):
        while len(self.__window) > 0 and self.__window[0].isAcked():
            self.__window.pop(0)
            if len(self.__buffer) > 0:
                self.__repop()

    @staticmethod
    def chunk_data(data, length):
        return (data[0+i:length+i] for i in range(0, len(data), length))


def test_connection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(10):
        connection.sendto(b'12345678901', ('127.0.0.1', 3000))
    connection.close()


if __name__ == '__main__':
    f = open('../../lorem.txt', 'r')
    file_data = f.read()
    f.close()
    # packet = Packet(0, 0, ipaddress.ip_address(socket.gethostbyname('localhost')), 8007, data.encode('utf-8'))
    # Sender().send_packet(packet)
    address = ipaddress.ip_address(socket.gethostbyname('localhost'))
    port = 8007
    # Sender(address, port, address, 3000).send_data(file_data)
    # c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # c.sendto(Packet(DATA, 0, address, port, b"Hello").to_bytes(), ('localhost', 3000))
    s = Sender(address, port, 'localhost', 3000)
    s.send_data("Hello World!")
    s.send_data("Hello World!!")
    # test_connection()
