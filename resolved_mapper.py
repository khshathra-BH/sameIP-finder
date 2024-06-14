import json
import dns.resolver
import re
import argparse
import dns.exception
import time
import sys
from tabulate import tabulate
from colorama import Fore, Style
from urllib.parse import urlparse


def convert_duration(duration):
    # Convert the duration to seconds
    total_seconds = duration

    # Calculate hours, minutes, and seconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    # Format the duration
    if hours > 0:
        formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    elif minutes > 0:
        formatted_duration = f"{minutes:02d}:{seconds:02d}"
    else:
        formatted_duration = f"00:00:{seconds:02d}"

    return formatted_duration

def output(final_results,output_format=None):
    if output_format == "json":
        return json.dumps(final_results, indent=4)
    else:
    # Convert results to human-readable text format
        output = ""
        for ip, subdomains in final_results.items():
          output += f"{ip}\n"
          output += "---------------\n"
          output += "\n".join(subdomains)
          output += "\n\n"  # Add blank lines between results
        return output

def report(all_subs,duration_process=None):
    print("\n")
    print(Fore.GREEN + 'Summery Report:\n' + Style.RESET_ALL)

    table = [["Duration", duration_process, "Duration of process"],["","" , ""],["All Subdomains", all_subs, "Number of subdomains in input file."]]

    print(tabulate(table, headers=["Name", "Quantity", "Description"],tablefmt="github"))

def main():
    # Get subdomains file path and output format from user using argparse
    parser = argparse.ArgumentParser(description="analyze a file containing subdomains and identify those that resolve to the same IP address.\n")
    parser.add_argument("-f","--file", help="Path to the text file containing subdomains (one per line)")
    parser.add_argument("-o", "--output", choices=["json", "text"], default="text", help="Output format (JSON or text (default))")
    parser.add_argument("-r", "--report", action="store_true", dest="report", help="Show a summery report")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Enable error messages (default: suppressed)")
    args = parser.parse_args()

    start = time.time()
    results = {}
    resolver = dns.resolver.Resolver()

    try:
        if not sys.stdin.isatty():
            lines = sys.stdin
            all_subs = 0
            for subdomain in sys.stdin:
                all_subs += 1

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
                    print("except dns.resolver.NXDOMAIN")
                    pass  # Silently handle non-existent domains by default
                except dns.resolver.Timeout:
                    print("except dns.resolver.Timeout")
                    pass  # Silently handle timeouts by default
                except Exception as e:
                    if verbose:  # Only print errors if verbose is explicitly set to True
                        print(f"Error: Unknown error for '{subdomain}': {e}. Skipping.")
        else:
            with open(args.file, "r") as f:
                lines = f.readlines()
                all_subs = len(lines) # find number of subs in input file

                for subdomain in lines:
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
                        print("except dns.resolver.NXDOMAIN")
                        pass  # Silently handle non-existent domains by default
                    except dns.resolver.Timeout:
                        print("except dns.resolver.Timeout")
                        pass  # Silently handle timeouts by default
                    except Exception as e:
                        if verbose:  # Only print errors if verbose is explicitly set to True
                            print(f"Error: Unknown error for '{subdomain}': {e}. Skipping.")

    except ValueError:
        print(f"Invalid URL: {subdomain}")
        sys.exit(1)

    final_output= output(results,args.output)

    if final_output:
        print(final_output)
    else:
        print("There is'nt any output.")

    end = time.time()
    duration = end - start
    duration_process = convert_duration(duration)

    if args.report:
        report(all_subs,duration_process)

if __name__ == '__main__':
    main()
