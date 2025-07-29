# Certificate Monitoring Script

This directoty contains a sample Python script, `certMonitor.py`, designed to fetch certificate information from Windows systems and store the results in a log file using JSON structure. The generated log file can be ingested into Splunk for analysis or used to create Prometheus metrics for monitoring.

## Features

- Fetches certificate details from the Windows certificate store.
- Outputs certificate information (such as subject, issuer, expiration date, etc.) in a structured JSON format.
- Appends results to a log file for easy integration with monitoring tools.
- Supports future integration with Splunk or Prometheus.

## Example Log Entry

```json
{
  "timestamp": "2024-06-01T12:00:00Z",
  "subject": "CN=example.com",
  "issuer": "CN=Example CA",
  "not_before": "2024-05-01T00:00:00Z",
  "not_after": "2025-05-01T00:00:00Z",
  "serial_number": "1234567890ABCDEF"
}
```

## Integration

- **Splunk:**  
  The JSON log file can be ingested into Splunk for searching, alerting, and dashboarding.

- **Prometheus:**  
  The script can be extended to expose metrics in Prometheus format for certificate expiration monitoring.

## Customization

- Modify `certMonitor.py` to adjust which certificate are needed for monitoring.
- Update the log file path or format as needed for your environment.
