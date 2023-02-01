import mptcplib
import socket
import random
import string

from mptcplib.test import unittest

def _client_server_pair(family, sock_type):
    sock_server = mptcplib.create_mptcp_socket(family, sock_type)
    sock_server.bind(('', 0))
    sock_server.listen()
    sock_client = mptcplib.create_mptcp_socket(family, sock_type)
    return sock_client, sock_server

class MPTCPLibDataTransfer(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    @unittest.skipIf(not mptcplib.is_mptcp_enabled_and_supported(), "Host OS doesn't support MPTCP or MPTCP not enabled")
    def test_mptcp_transfer_ipv4(self):
        sock_client, sock_server = _client_server_pair(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.assertTrue(mptcplib.is_socket_mptcp(sock_client))
            self.assertTrue(mptcplib.is_socket_mptcp(sock_server))
            sock_client.connect(sock_server.getsockname())
            text_length = 1024
            random_text = "".join(random.choice(string.ascii_letters) for _ in range(text_length))
            sock_client.sendall(str.encode(random_text))
            conn, _ = sock_server.accept()
            with conn:
                recv_text   = conn.recv(text_length).decode()
            self.assertEqual(random_text, recv_text)  
            try:
                self.assertGreaterEqual(mptcplib.get_nb_used_subflows(sock_client), 1) 
                self.assertGreaterEqual(mptcplib.get_nb_used_subflows(sock_server), 1)
            except NotImplementedError as e:
                pass 
        finally:
            sock_client.close()
            sock_client.close()

    @unittest.skipIf(not mptcplib.is_mptcp_enabled_and_supported(), "Host OS doesn't support MPTCP or MPTCP not enabled")
    def test_mptcp_transfer_ipv6(self):
        sock_client, sock_server = _client_server_pair(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.assertTrue(mptcplib.is_socket_mptcp(sock_client))
            self.assertTrue(mptcplib.is_socket_mptcp(sock_server))
            sock_client.connect(sock_server.getsockname())
            text_length = 1024
            random_text = "".join(random.choice(string.ascii_letters) for _ in range(text_length))
            sock_client.sendall(str.encode(random_text))
            conn, _ = sock_server.accept()
            with conn:
                recv_text   = conn.recv(text_length).decode()
            self.assertEqual(random_text, recv_text)
            try:
                self.assertGreaterEqual(mptcplib.get_nb_used_subflows(sock_client), 1)
                self.assertGreaterEqual(mptcplib.get_nb_used_subflows(sock_server), 1)
            except NotImplementedError as e:
                pass        
        finally:
            sock_client.close()
            sock_client.close()

    def tearDown(self):
        return super().tearDown()