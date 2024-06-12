import json
import dns.resolver
import re
import argparse
from urllib.parse import urlparse

def find_subdomains_with_same_ip(subdomains_file, output_format="text", verbose=False):

  results = {}
  resolver = dns.resolver.Resolver()

  with open(subdomains_file, "r") as f:
    for subdomain in f:
      subdomain = subdomain.strip()  # Remove leading/trailing whitespace

      if subdomain.startswith("http://") or subdomain.startswith("https://"):
        subdomain = urlparse(subdomain).hostname

      try:
        # Use dnspython to resolve A record (using updated method)
        answers = resolver.resolve(subdomain, "A")
        ip_address = answers[0].to_text()  # Get the first A record IP
        if ip_address not in results:
          results[ip_address] = []
        results[ip_address].append(subdomain)
      except dns.resolver.NXDOMAIN:
        pass  # Silently handle non-existent domains by default
      except dns.resolver.Timeout:
        pass  # Silently handle timeouts by default
      except Exception as e:
        if verbose:  # Only print errors if verbose is explicitly set to True
          print(f"Error: Unknown error for '{subdomain}': {e}. Skipping.")

  if output_format == "json":
    return json.dumps(results, indent=4)
  else:
    # Convert results to human-readable text format
    output = ""
    for ip, subdomains in results.items():
      output += f"{ip}\n"
      output += "---------------\n"
      output += "\n".join(subdomains)
      output += "\n\n"  # Add blank lines between results
    return output

if __name__ == "__main__":
  # Get subdomains file path and output format from user using argparse
  parser = argparse.ArgumentParser(description="Find subdomains with same IP")
  parser.add_argument("subdomains_file", help="Path to the text file containing subdomains (one per line)")
  parser.add_argument("-f", "--format", choices=["json", "text"], default="text",
                      help="Output format (JSON or text)")
  parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                      help="Enable error messages (default: suppressed)")
  args = parser.parse_args()

  same_ip_results = find_subdomains_with_same_ip(args.subdomains_file, output_format=args.format, verbose=args.verbose)

  if same_ip_results:
    print(same_ip_results)
  else:
    print("No subdomains found with the same IP address.")
