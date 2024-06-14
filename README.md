##  Resolve to the same IP address
This Python tool helps you analyze a file containing subdomains and identify those that resolve to the same IP address. It utilizes the dnspython library for DNS lookups.

### Features:

* Outputs results in JSON format (default) or text format.
* Add option for summery report
* Get subdomains in pipe (cat subdomains | python3 resolved_mapper.py )
  
### Installation:
1. Ensure you have Python 3 installed.

### Usage:
1. git clone the project.
2. `cd resolved_mapper`
3. `pip3 install -r requirements.txt`
4. Run the script with the subdomain file path:
```bash
python3 resolved_mapper.py -f subdomains.txt
```

## Optional arguments:

```bash
options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the text file containing subdomains (one per line)
  -o {json,text}, --output {json,text}
                        Output format (JSON or text (default))
  -r, --report          Show a summery report
  -v, --verbose         Enable error messages (default: suppressed)
```

#### Example Output (Text Format):

![resolved_mapper-text](https://github.com/miladkeivanfar/resolved_mapper/assets/129506375/67c14441-cd45-46ab-8d22-22ede7f8a9a9)



#### Example Output (JSON Forma):

![resolved_mapper-json](https://github.com/miladkeivanfar/resolved_mapper/assets/129506375/79ff5bcf-ce38-447b-b9c4-0388bed02456)


