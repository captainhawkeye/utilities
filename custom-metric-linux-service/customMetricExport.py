import subprocess
import re
import os

def get_service_status(service_name):
    result = subprocess.run(['systemctl', 'status', service_name], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def parse_memory_info(status_output):
    memory_info = re.search(r'Memory:\s+([\d.]+[A-Z]) \(min: ([\d.]+[A-Z]) high: ([\d.]+[A-Z]) max: ([\d.]+[A-Z]) available: ([\d.]+[A-Z])\)', status_output)
    if memory_info:
        return {
            'memory_usage': convert_to_bytes(memory_info.group(1)),
            'memory_min': convert_to_bytes(memory_info.group(2)),
            'memory_high': convert_to_bytes(memory_info.group(3)),
            'memory_max': convert_to_bytes(memory_info.group(4)),
            'memory_available': convert_to_bytes(memory_info.group(5))
        }
    return None

def convert_to_bytes(value):
    units = {"K": 1024, "M": 1024**2, "G": 1024**3, "T": 1024**4}
    number = float(re.match(r'([\d.]+)', value).group(1))
    unit = re.match(r'[\d.]+([A-Z])', value).group(1)
    return int(number * units[unit])

def write_prometheus_file(service_name, memory_info):
    file_path = f'/data/metrics/{service_name}_metrics.prom'
    print(f"Writing to file: {file_path}")
    with open(file_path, 'w') as f:
        f.write(f"# HELP {service_name}_memory_min Minimum memory limit of the service\n")
        f.write(f"# TYPE {service_name}_memory_min gauge\n")
        f.write(f"{service_name}_memory_min {memory_info['memory_min']}\n")

        f.write(f"# HELP {service_name}_memory_max Maximum memory limit of the service\n")
        f.write(f"# TYPE {service_name}_memory_max gauge\n")
        f.write(f"{service_name}_memory_max {memory_info['memory_max']}\n")

        f.write(f"# HELP {service_name}_memory_high High memory limit of the service\n")
        f.write(f"# TYPE {service_name}_memory_high gauge\n")
        f.write(f"{service_name}_memory_high {memory_info['memory_high']}\n")

        f.write(f"# HELP {service_name}_memory_available Available memory of the service\n")
        f.write(f"# TYPE {service_name}_memory_available gauge\n")
        f.write(f"{service_name}_memory_available {memory_info['memory_available']}\n")

    # Set file permissions to 755
    os.chmod(file_path, 0o755)

def main():
    service_name = os.environ.get("SERVICE_NAME")
    status_output = get_service_status(service_name)
    print(f"Service status output:\n{status_output}")

    memory_info = parse_memory_info(status_output)
    print(f"Parsed memory info: {memory_info}")

    if memory_info:
        write_prometheus_file(service_name, memory_info)
    else:
        print("Failed to parse necessary information.")

if __name__ == "__main__":
    main()