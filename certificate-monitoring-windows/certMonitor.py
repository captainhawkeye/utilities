import subprocess
import json

# Manually specify the server names
servers = [
    'Pass the Server Names Here'
]

# Function to fetch certificates with "anuragpoc" in the Subject field
def fetch_certificates(server):
    # PowerShell command to fetch certificates that contain "anuragpoc" in the Subject
    ps_command = f"""
    Invoke-Command -ComputerName {server} -ScriptBlock {{
        try {{
            $certs = Get-ChildItem Cert:\LocalMachine\My | Where-Object {{ $_.Subject -like '*anuragpoc*' }}
            if ($certs) {{
                $certs | Select-Object Subject, Thumbprint, NotBefore, NotAfter, SerialNumber | ConvertTo-Json
            }} else {{
                @{{ Message = "No certificates found with 'anuragpoc' in the Subject." }} | ConvertTo-Json
            }}
        }} catch {{
            @{{ Error = "An error occurred: $_" }} | ConvertTo-Json
        }} finally {{
            Exit  # Ensure PowerShell session terminates properly
        }}
    }}
    """
    
    # Execute the PowerShell command with a timeout to avoid hanging indefinitely
    try:
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True, text=True, timeout=60  # Timeout after 60 seconds
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "PowerShell command timed out."})
    except Exception as e:
        return json.dumps({"error": f"Failed to run PowerShell command: {str(e)}"})

# Open a .log file to write the output
with open('certificates_output.log', 'w') as output_file:
    # Loop through each server and fetch certificate information
    for server in servers:
        try:
            cert_info = fetch_certificates(server)
            output_data = {
                "server": server,
                "certificates": json.loads(cert_info)  # Load the JSON output into a Python dict
            }
            output_file.write(json.dumps(output_data) + "\n")
        except Exception as e:
            error_data = {
                "server": server,
                "error": f"Failed to fetch certificates: {str(e)}"
            }
            output_file.write(json.dumps(error_data) + "\n")

print("Certificate information has been written to certificates_output.log.")