import ssl
import pathlib
from model import WebResponse,HTTPVersion,SSLErrorType
from exception import SSLHandshakeException
import ipaddress
import socket
import psutil
import asyncio
import certifi
from datetime import datetime,timezone
from cryptography import x509
from cryptography.x509.oid import ExtensionOID,NameOID
from cryptography.hazmat.backends import default_backend

_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile=certifi.where())

_context.minimum_version = ssl.TLSVersion.TLSv1_2

_context.maximum_version = ssl.TLSVersion.TLSv1_3

_context.verify_mode = ssl.CERT_NONE

_context.check_hostname = False

class WebTransport:
    def __init__(self,max):
        pass
    def request():
        pass


class ProxyTransport(WebTransport):
    def __init__():
        pass

class Sock5Transport(ProxyTransport):
    pass

class WebConnectionPool:
    def __init__():
        pass

class WebConnection:
    def __init__(self,host:str,port:int,timeout:int = 25000):
        self.port = port
        self.timeout = timeout
        try:
            self.addr = ipaddress.ip_address(host)
        except:
            for adapter in psutil.net_if_addrs().items():
                for addr in adapter[1]:
                    if addr.address.startswith("fe80::") or addr.address == "::1":
                        continue
                    self.ipv6_support = True
            ip_list = socket.getaddrinfo(host)
            self.ipv4 = []
            self.ipv6 = []
            for ip in ip_list:
                family, _, _, _, sockaddr = ip
                if family == socket.AF_INET:
                    self.ipv4.append(sockaddr)
                elif family == socket.AF_INET6:
                    self.ipv6.append(sockaddr)
    async def open_v6_connection(self):
        connect_task = []
        for ipv6 in self.ipv6:
            connect_task.append(asyncio.open_connection(ipv6,self.port))
        return await asyncio.wait(connect_task,return_when=asyncio.FIRST_COMPLETED,timeout=self.timeout)
    async def open_v4_connection(self):
        connect_task = []
        for ipv4 in self.ipv4:
            connect_task.append(asyncio.open_connection(ipv4,self.port))
        result = await asyncio.wait(connect_task,return_when=asyncio.FIRST_COMPLETED,timeout=self.timeout)
    async def open_connection(self):
        v6_task = asyncio.create_task(self.open_v6_connection())
        await asyncio.sleep(40)
        if v6_task.done():
            v6_result = v6_task.result()[0][0]
            return v6_result
        v4_task = asyncio.create_task(self.open_v4_connection())
        asyncio.wait([v6_task,v4_task],return_when=asyncio.FIRST_COMPLETED,timeout=self.timeout - 40)
    async def upgrade_to_tls():
        """let WebConnection upgrade to TLSWebConnection"""
        pass

class TLSWebConnection(WebConnection):
    def __init__(self,host:str,port:int,timeout:int = 25000,ssl_validate_callback = None):
        self.port = port
        self.timeout = timeout
        self.ssl_validate_callback = ssl_validate_callback
        try:
            self.addr = ipaddress.ip_address(host)
        except:
            for adapter in psutil.net_if_addrs().items():
                for addr in adapter[1]:
                    if addr.address.startswith("fe80::") or addr.address == "::1":
                        continue
                    self.ipv6_support = True
            ip_list = socket.getaddrinfo(host)
            self.ipv4 = []
            self.ipv6 = []
            for ip in ip_list:
                family, _, _, _, sockaddr = ip
                if family == socket.AF_INET:
                    self.ipv4.append(sockaddr)
                elif family == socket.AF_INET6:
                    self.ipv6.append(sockaddr)
                
    def handle_ssl_validate(self,socket):
        if self.ssl_validate_callback:
            ok,error_type = self.ssl_validate_callback(socket)
            if not ok:
                raise SSLHandshakeException(self.__get_message_by_error__(error_type))

    def validate_ssl(self,socket,request_host:str) -> tuple[bool,SSLErrorType,ssl.SSLSocket]:
        ssl_sock = None
        ssl_sock = _context.wrap_socket(socket)
        ssl_sock.do_handshake()
        certs = ssl_sock.getpeercert(True)
        cert_chain = []
        for cert in certs:
            cert_chain.append(x509.load_der_x509_certificate(cert,default_backend()))
        leaf_cert = cert_chain[0]
        if not cert_chain:
            return False,SSLErrorType.ProtocolError,ssl_sock
        current_time = datetime.now(timezone.utc)
        sans = None
        if not leaf_cert.not_valid_before_utc < current_time < leaf_cert.not_valid_after_utc:
            return False,SSLErrorType.Expired,ssl_sock
        try:
            sans = leaf_cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        except x509.ExtensionNotFound:
            pass
        if sans:
            for san in sans.value:
                if san.value.startswith("*"):
                    if not san.endswith(request_host.split(".",1).pop()):
                        return False,SSLErrorType.SubjectAlternativeNameMismatched,ssl_sock
        else:
            try:
                cn = cert.extensions.get_attributes_for_oid(NameOID.COMMON_NAME):
                if cn.startswith("*"):
                    if not cn.endswith(request_host.split(".",1).pop()):
                        return False,SSLErrorType.SubjectAlternativeNameMismatched,ssl_sock
            except IndexError:
                return False,SSLErrorType.Invalid,ssl_sock
        leaf_cert
            
    def __check_algorithm__(self,cert):
        return cert.signature_hash_algorithm.name.upper() in ["MD5","SHA-1"]
        
                        

            
        
    def __get_message_by_error__(self,error:SSLErrorType):
        if error == SSLErrorType.Expired:
            return "The certificate specified by the remote server has expired."
        elif error == SSLErrorType.CertificateRevoked:
            return "The certificate specified by the remote server has been revoked by the issuer."
        elif error == SSLErrorType.InsecureAlgorithm:
            return "The algorithm used by this certificate has been deprecated."
        elif error == SSLErrorType.IncompletedTrustChain:
            return "This certificate contains one or more untrusted (or revoked) issuers."
        elif error == SSLErrorType.SubjectAlternativeNameMismatched or error == SSLErrorType.CommonNameMismatched:
            return "This certificate is not valid for this remote server."
        elif error == SSLErrorType.Invalid:
            return "The certificate specified by the remote server is invalid."
        elif error == SSLErrorType.ProtocolError:
            return "The remote server does not support (or has not provided) the certificate required for an encrypted connection."
        
connection = TLSWebConnection("1",0)