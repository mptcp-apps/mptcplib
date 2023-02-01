import mptcplib
import socket 

from mptcplib.test import unittest

# TODO add tests

class MPTCPLibSocketCreation(unittest.TestCase):

    def setUp(self) -> None:
        self._ctx = {}
        return super().setUp()

    @unittest.skipIf(not mptcplib.is_mptcp_enabled_and_supported(), "Host OS doesn't support MPTCP or MPTCP not enabled")
    def test_initialisation_on_supported_os_ipv4(self):
        sock = mptcplib.create_mptcp_socket(socket.AF_INET, socket.SOCK_STREAM)
        try:    
            self.assertTrue(mptcplib.is_socket_mptcp(sock))
        except NotImplementedError as error:
            pass
        self.assertEqual(sock.family, socket.AF_INET)
        self.assertEqual(sock.proto, mptcplib.IPPROTO_MPTCP)
        sock.close()

    @unittest.skipIf(mptcplib.is_mptcp_enabled_and_supported(), "MPTCP capable host")
    def test_initialisation_on_unsupported_os_ipv4(self):
        sock = mptcplib.create_mptcp_socket(socket.AF_INET, socket.SOCK_STREAM)
        try:    
            self.assertFalse(mptcplib.is_socket_mptcp(sock))
        except NotImplementedError as error:
            pass
        # We fallback to TCP
        self.assertEqual(sock.family, socket.AF_INET)
        self.assertEqual(sock.proto, socket.IPPROTO_TCP)
        sock.close()
    
    def tearDown(self) -> None:
        return super().tearDown()