##  Resolve to the same IP address
This Python tool helps you analyze a file containing subdomains and identify those that resolve to the same IP address. It utilizes the dnspython library for DNS lookups.

### Features:

- Analyzes subdomains from a text file (one per line).
- Uses DNS lookups to determine IP addresses.
- Groups subdomains that resolve to the same IP address.
- Provides results in either text or JSON format (user-selectable).
- Suppresses errors by default (optional verbose mode for error messages).
  
### Installation:
1. Ensure you have Python 3 installed.
2. Install the required library:
```bash
pip3 install dnspython
```
### Usage:
1. git clone the project.
2. Place your subdomains list in a text file (e.g., subdomains.txt). Each line should contain a single subdomain.
3. Run the script with the subdomain file path:
```bash
python sameIP-finder.py path/to/your/subdomains.txt
```
4. Optional arguments:

`-f`, `--format`: Specify output format (text or JSON). Defaults to "text".
`-v`, `--verbose`: Enable error messages (default: suppressed).

#### Example Output (Text Format):
```bash
10.0.0.1
---------------
subdomain1.example.com
subdomain2.example.com

192.168.1.1
---------------
subdomain3.example.com
```
#### Example Output (JSON Format with -f json):
```bash
{
  "10.0.0.1": [
    "subdomain1.example.com",
    "subdomain2.example.com"
  ],
  "192.168.1.1": [
    "subdomain3.example.com"
  ]
}
```
