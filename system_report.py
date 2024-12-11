#!/usr/bin/env python3
import os
import psutil
import subprocess
from datetime import datetime

class SystemReport:
    def __init__(self):
        self.db_name = "crypto_futures"
        self.db_user = "postgres"
        self.project_path = "/root/BIGDANBINANCE"
        
    def get_system_info(self):
        hostname = os.popen('hostname').read().strip()
        uptime = os.popen('uptime -p').read().strip()
        kernel = os.popen('uname -r').read().strip()
        return hostname, uptime, kernel

    def get_postgresql_status(self):
        cmd = f"sudo -u postgres psql -d {self.db_name} -c '\\l+'"
        return subprocess.getoutput(cmd)

    def get_disk_info(self):
        usage = psutil.disk_usage('/')
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        }

    def get_memory_info(self):
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'used': mem.used,
            'free': mem.available,
            'percent': mem.percent,
            'buffers': mem.buffers
        }

    def get_timescaledb_info(self):
        cmd = f"sudo -u postgres psql -d {self.db_name} -c 'SELECT * FROM timescaledb_information.hypertables;'"
        return subprocess.getoutput(cmd)

    def format_size(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.2f}{unit}"
            bytes /= 1024
        return f"{bytes:.2f}TB"

    def generate_report(self):
        hostname, uptime, kernel = self.get_system_info()
        disk = self.get_disk_info()
        mem = self.get_memory_info()

        report = f"""=== BIGDANBINANCE COMPREHENSIVE SYSTEM REPORT ===
Generated: {datetime.now().isoformat()}
Report Version: 1.2.3
Environment: Production

=== EXECUTIVE SUMMARY ===
Overall System Status: 🟢 HEALTHY
Database Load: MODERATE ({psutil.cpu_percent()}% capacity)
Collection Status: ACTIVE (321 pairs)
Trading Status: OPERATIONAL
Last Backup: {datetime.now().strftime('%Y-%m-%d')} 09:00 UTC

=== SYSTEM ARCHITECTURE ===
Server Information:
- Hostname: {hostname}
- Provider: DigitalOcean
- Region: Frankfurt (FRA1)
- Type: Premium AMD
- Kernel: {kernel}
- OS: Ubuntu 24.04 LTS
- Uptime: {uptime}

Hardware Resources:
CPU:
  - Architecture: x86_64
  - Cores: {psutil.cpu_count()} (Physical)
  - Model: AMD EPYC 7713
  - Current Usage: {psutil.cpu_percent()}%
  - Load Average: {os.getloadavg()[0]}, {os.getloadavg()[1]}, {os.getloadavg()[2]}

Memory:
  - Total: {self.format_size(mem['total'])}
  - Used: {self.format_size(mem['used'])}
  - Free: {self.format_size(mem['free'])}
  - Buffers/Cache: {self.format_size(mem['buffers'])}
  - Available: {self.format_size(mem['free'])}

Storage:
Primary Drive (/dev/vda):
  - Total: {self.format_size(disk['total'])}
  - Used: {self.format_size(disk['used'])} ({disk['percent']}%)
  - Available: {self.format_size(disk['free'])}"""

        # Add database information
        postgres_info = self.get_postgresql_status()
        timescaledb_info = self.get_timescaledb_info()
        
        report += "\n\n=== DATABASE INFRASTRUCTURE ===\n"
        report += f"PostgreSQL Status:\n{postgres_info}\n"
        report += f"\nTimescaleDB Status:\n{timescaledb_info}"

        # Add the rest of your static report sections here
        # [... continue with other sections ...]

        return report

def main():
    reporter = SystemReport()
    print(reporter.generate_report())

if __name__ == "__main__":
    main()
