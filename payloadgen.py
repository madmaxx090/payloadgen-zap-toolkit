# payloadgen.py

print("[DEBUG] Script running...")

import argparse
import json
import pyperclip
from colorama import Fore, Style

# Try importing your modules
try:
    from modules import xss, sqli, cmdinj
    from zap_integration import send_and_scan, export_zap_report
    print("[DEBUG] Modules imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import modules: {e}")
    exit()

# Print payloads
def print_payloads(payloads):
    for p in payloads:
        print(f"{Fore.GREEN}[{p['type']}]{Style.RESET_ALL} {p['payload']}")
        print(f"{Fore.YELLOW}Bypass:{Style.RESET_ALL} {p['bypass']}\n")

# Export to JSON
def export_json(payloads, filename):
    try:
        with open(f"output/{filename}", "w") as f:
            json.dump(payloads, f, indent=2)
        print(f"{Fore.CYAN}✅ Saved to output/{filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to export JSON: {e}{Style.RESET_ALL}")

# Export to TXT (for Burp/ZAP file import)
def export_txt(payloads, filename):
    try:
        with open(f"output/{filename}", "w") as f:
            for p in payloads:
                f.write(p['payload'] + "\n")
        print(f"{Fore.CYAN}✅ Saved to output/{filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to export TXT: {e}{Style.RESET_ALL}")

# Main driver
def main():
    parser = argparse.ArgumentParser(description="🔧 Custom Payload Generator — by Unaiza & Maxx")
    parser.add_argument('--xss', action='store_true', help="Generate XSS payloads")
    parser.add_argument('--sqli', action='store_true', help="Generate SQL Injection payloads")
    parser.add_argument('--cmd', action='store_true', help="Generate Command Injection payloads")
    parser.add_argument('--json', action='store_true', help="Export payloads to JSON")
    parser.add_argument('--txt', action='store_true', help="Export payloads to TXT")
    parser.add_argument('--clip', action='store_true', help="Copy first payload to clipboard")
    parser.add_argument('--zap', action='store_true', help="Send payloads to ZAP and generate report")
    parser.add_argument('--target', type=str, help="Target URL for ZAP attack")

    args = parser.parse_args()

    payloads = []

    if args.xss:
        print("[DEBUG] --xss flag detected")
        payloads = xss.get_xss_payloads()
        print_payloads(payloads)
        if args.json:
            export_json(payloads, "xss_payloads.json")
        if args.txt:
            export_txt(payloads, "xss_payloads.txt")
        if args.clip:
            pyperclip.copy(payloads[0]['payload'])
            print(f"{Fore.MAGENTA}📋 First XSS payload copied to clipboard!{Style.RESET_ALL}")

    elif args.sqli:
        print("[DEBUG] --sqli flag detected")
        payloads = sqli.get_sqli_payloads()
        print_payloads(payloads)
        if args.json:
            export_json(payloads, "sqli_payloads.json")
        if args.txt:
            export_txt(payloads, "sqli_payloads.txt")
        if args.clip:
            pyperclip.copy(payloads[0]['payload'])
            print(f"{Fore.MAGENTA}📋 First SQLi payload copied to clipboard!{Style.RESET_ALL}")

    elif args.cmd:
        print("[DEBUG] --cmd flag detected")
        payloads = cmdinj.get_cmd_payloads()
        print_payloads(payloads)
        if args.json:
            export_json(payloads, "cmd_payloads.json")
        if args.txt:
            export_txt(payloads, "cmd_payloads.txt")
        if args.clip:
            pyperclip.copy(payloads[0]['payload'])
            print(f"{Fore.MAGENTA}📋 First CMDi payload copied to clipboard!{Style.RESET_ALL}")

    else:
        print(f"{Fore.RED}❌ No module selected. Use --xss, --sqli or --cmd to generate payloads.{Style.RESET_ALL}")
        return

    # ZAP attack trigger
    if args.zap:
        if args.target:
            print(f"{Fore.CYAN}[ZAP] Sending payloads to: {args.target}{Style.RESET_ALL}")
            send_and_scan(args.target, payloads)
            export_zap_report()
        else:
            print(f"{Fore.RED}❌ Missing target URL for ZAP. Use --target http://example.com{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

