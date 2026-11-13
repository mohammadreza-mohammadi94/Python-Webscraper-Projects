# CIDR to IP Range Converter

This script converts `.zone` files containing CIDR notation to IP ranges and saves them in multiple formats.

## Features

- ✅ Converts CIDR notation (e.g., `192.168.1.0/24`) to IP ranges
- ✅ Processes all `.zone` files in the `ip_zones` directory
- ✅ Supports multiple output formats: **JSON**, **CSV**, and **TXT**
- ✅ Calculates total IP addresses for each range
- ✅ Provides detailed statistics and summary

## Usage

### Basic Usage

```bash
python convert_cidr_to_ranges.py
```

This will:
1. Read all `.zone` files from the `ip_zones` directory
2. Convert each CIDR entry to IP ranges
3. Save the results in the `ip_ranges` directory in all three formats

### Output Formats

#### 1. JSON Format (`*_ranges.json`)
Contains structured data with metadata:
```json
{
  "country_code": "US",
  "total_ranges": 69358,
  "total_ips": 1610095968,
  "ranges": [
    {
      "cidr": "14.1.64.0/19",
      "start_ip": "14.1.64.0",
      "end_ip": "14.1.95.255",
      "total_ips": 8192
    }
  ]
}
```

#### 2. CSV Format (`*_ranges.csv`)
Comma-separated values for easy import into spreadsheets:
```csv
CIDR,Start_IP,End_IP,Total_IPs
14.1.64.0/19,14.1.64.0,14.1.95.255,8192
27.100.36.0/22,27.100.36.0,27.100.39.255,1024
```

#### 3. TXT Format (`*_ranges.txt`)
Simple text format with IP ranges:
```
14.1.64.0 - 14.1.95.255
27.100.36.0 - 27.100.39.255
```

## Configuration

You can modify the script to change the output format by editing the `output_format` variable in the `main()` function:

```python
# Output format options: 'json', 'csv', 'txt', or 'all'
output_format = 'all'  # Change this to your preferred format
```

## Directory Structure

```
IP-Ranges/
├── ip_zones/              # Input directory with .zone files
│   ├── us.zone
│   ├── ir.zone
│   └── ...
├── ip_ranges/             # Output directory (created automatically)
│   ├── us_ranges.json
│   ├── us_ranges.csv
│   ├── us_ranges.txt
│   └── ...
└── convert_cidr_to_ranges.py
```

## Example Output

For Iran (IR) with 1,909 CIDR ranges:
- **JSON**: `ir_ranges.json` (272 KB) - Structured data with metadata
- **CSV**: `ir_ranges.csv` (93 KB) - Spreadsheet-compatible format
- **TXT**: `ir_ranges.txt` (58 KB) - Simple IP range list

## Statistics

The script provides a summary after processing:
```
✅ Conversion Complete!
   Total countries processed: 233
   Total IP ranges: 1,234,567
   Total IP addresses: 3,456,789,012
   
   Output saved to: C:\...\IP-Ranges\ip_ranges
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Error Handling

The script includes robust error handling:
- Skips invalid CIDR entries with a warning
- Handles empty lines and comments in `.zone` files
- Creates output directory automatically if it doesn't exist
- Provides detailed error messages for troubleshooting

## Performance

- Processes **233 countries** in seconds
- Handles large files efficiently (e.g., US with 69,358 ranges)
- Memory-efficient streaming processing

## License

This script is part of the IP-Ranges project.
