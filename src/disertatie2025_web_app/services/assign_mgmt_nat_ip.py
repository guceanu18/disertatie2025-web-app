import ipaddress
import subprocess
import re


class LANRouter:
    _used_ips = []

    def __init__(self, subnet: str):
        self.subnet = subnet  # Store subnet as instance variable
        self.used_ips = []

    def __search_for_used_ips(self):
        """Run Nmap ping sweep and extract active IPs."""
        try:
            result = subprocess.run(
                ["nmap", "-sn", self.subnet, "-oG", "-"],
                capture_output=True,
                text=True,
                check=True
            )

            ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            active_ips = ip_pattern.findall(result.stdout)
            unique_ips = list(set(active_ips))

            filtered_ips = [ip for ip in unique_ips if not ip.endswith(('.0', '.255'))]
            LANRouter._used_ips += filtered_ips

        except subprocess.CalledProcessError as e:
            print(f"Nmap scan failed: {e.stderr}")
            self.used_ips = []

    def is_ip_in_subnet(self, ip: str) -> bool:
        """Check if IP belongs to the router's subnet."""
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            network = ipaddress.IPv4Network(self.subnet, strict=False)
            return ip_obj in network
        except ValueError:
            return False

    def assign_unused_lan_ip(self):
        """Find the first unused IP in the subnet."""
        self.__search_for_used_ips()
        network = ipaddress.IPv4Network(self.subnet, strict=False)

        for host in network.hosts():
            host_ip = str(host)
            if host_ip not in LANRouter._used_ips:
                LANRouter._used_ips.append(host_ip)
                return host_ip
        return None



if __name__ == "__main__":
    LANRouter.assign_unused_lan_ip(LANRouter('192.168.72.0/24'))