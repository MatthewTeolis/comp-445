import ipaddress
import socket

# class SelectiveRepeat:
#     _window_size = 5
#     _sequence_size = 2 * _window_size
#     _buffer = list()
#
#
from common.Packet import Packet, MAX_LEN, MIN_LEN, DATA


class Sender:

    def __init__(self, address, port, router_address, router_port, window_size=5):
        self._address = address
        self._port = port
        self._router_address = router_address
        self._router_port = router_port
        self._window_size = window_size
        self._sequence_size = 2 * window_size
        self._buffer = list()
        self._sequence_number = 0

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
        chunks = Sender.chunk_data(data.encode('utf-8'), MAX_LEN - MIN_LEN)

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

        while True:
            try:
                conn.sendto(packet.to_bytes(), (self._router_address, self._router_port))
                conn.settimeout(timeout)
                response, sender = conn.recvfrom(MAX_LEN)
                print(response, sender)
            except socket.timeout:
                count += 1
                if count >= max_tries:
                    break

    @staticmethod
    def chunk_data(data, length):
        return (data[0+i:length+i] for i in range(0, len(data), length))


def send_packet_raw(router_addr, router_port, server_addr, server_port):
        peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            msg = "Hello World"
            # p = Packet(packet_type=0,
            #            seq_num=1,
            #            peer_ip_addr=peer_ip,
            #            peer_port=server_port,
            #            payload=msg.encode("utf-8"))
            conn.sendto(b'12345678900', (router_addr, router_port))
            print('Send "{}" to router'.format(msg))

            # Try to receive a response within timeout
            conn.settimeout(timeout)
            print('Waiting for a response')
            # response, sender = conn.recvfrom(1024)
            # p = Packet.from_bytes(response)
            # print('Router: ', sender)
            # print('Packet: ', p)
            # print('Payload: ' + p.payload.decode("utf-8"))

        except socket.timeout:
            print('No response after {}s'.format(timeout))
        finally:
            conn.close()


if __name__ == '__main__':
    f = open('../../lorem.txt', 'r')
    file_data = f.read()
    f.close()
    # packet = Packet(0, 0, ipaddress.ip_address(socket.gethostbyname('localhost')), 8007, data.encode('utf-8'))
    # Sender().send_packet(packet)
    address = ipaddress.ip_address(socket.gethostbyname('localhost'))
    port = 8007
    Sender(address, port, address, 3000).send_data(file_data)
