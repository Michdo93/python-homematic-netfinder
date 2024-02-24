import concurrent.futures
import socket
import ipaddress
import ping3
import platform
import subprocess

class Netfinder(object):
    def __init__(self, ip=None, target_ports=[80, 443, 9293], timeout=1):
        if ip is None:
            self.ip = self.__get_own_ip()
        else:
            self.ip = ip
        self.target_ports = target_ports
        self.timeout = timeout
        self.ip_range = self.__get_ip_range_by_ip(self.ip)

    def __get_own_ip(self):
        try:
            # Verbindung zu einem externen Server aufbauen
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Hier wird der Google DNS-Server als Beispiel verwendet
            own_ip = s.getsockname()[0]
            s.close()
            return own_ip
        except socket.error:
            print("Could not detect own ip.")

    def __get_ip_range_by_ip(self, ip):
        if self.__is_valid_ipv4(ip):
            network_parts = ip.split('.')[:3]
            ip_range = '.'.join(network_parts)
            return ip_range
        else:
            print("Invalid IPv4 address")
        
    def __is_valid_ipv4(self, ip):
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    def __check_ping(self, host):
        ping_result = ping3.ping(dest_addr=host)

        if ping_result is not None:
            return ping_result
        else:
            return None
        
    def __get_hostname_by_ip_address(self, ip):
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except socket.herror as e:
            return "n/a"
        
    def __check_os(self):
        system = platform.system()
        version = platform.version()

        return "{} {}".format(system, version)
    
    def __get_mac_address_by_ip(self, ip):
        os = self.__check_os()
        mac_address = None  # Initialisiere die Variable vor dem if-else-Block

        if "Windows" in os:
            command = ["arp", "-a", ip]
            result = subprocess.run(command, capture_output=True, text=True)
            
            lines = result.stdout.splitlines()
            if len(lines) > 3:
                mac_address = lines[3].split()[1].replace('-', ':')

        elif "Linux" in os:
            command = ["arp", "-n", ip]
            result = subprocess.run(command, capture_output=True, text=True)
            
            lines = result.stdout.splitlines()
            if len(lines) > 1:
                mac_address = lines[1].split()[2].replace(':', '-')

        if mac_address:
            return mac_address
        else:
            return "n/a"

    def find_homematic_devices(self):
        devices = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            for i in range(1, 255):
                host = "{}.{}".format(self.ip_range, i)
                future = executor.submit(self.__check_device, host)
                futures.append((host, future))

            for host, future in futures:
                result = future.result()
                if result is not None:
                    devices.append(result)

        return devices

    def __check_device(self, host):
        ping_result = self.__check_ping(host)
        hostname = None
        mac = None
        ports = self.target_ports
        check = []

        if ping_result is not None:
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))

                if result == 0:
                    check.append(True)
                else:
                    check.append(False)

                sock.close()

            if all(check):
                hostname = self.__get_hostname_by_ip_address(host)
                mac = self.__get_mac_address_by_ip(host)

                return {
                    'ip_address': host,
                    'hostname': hostname,
                    'mac_address': mac
                }

        return None
        
if __name__ == "__main__":
    pass
