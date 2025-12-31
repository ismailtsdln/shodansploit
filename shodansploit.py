#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys
import argparse
from src.config import Config
from src.api import ShodanAPI
from src.ui import UI
from src.export import Exporter
from src.dorks import DORKS, get_all_dorks, get_categories
from src.history import History

# shodansploit v2.0.0

def signal_handler(signal, frame):
    UI.print_error("Exiting...")
    sys.exit(0)

def show_dorks_menu(api):
    """Display and handle the Shodan Dorks menu."""
    categories = get_categories()
    
    UI.print_success("\n=== Shodan Dorks Library ===\n")
    
    for idx, category in enumerate(categories, 1):
        print(f"[{idx}] {category}")
    print(f"[{len(categories) + 1}] Search all dorks")
    print(f"[{len(categories) + 2}] Back to main menu")
    
    choice = UI.get_input("\nSelect category: ")
    
    try:
        choice_num = int(choice)
        
        if choice_num == len(categories) + 2:
            return None
        elif choice_num == len(categories) + 1:
            # Search all dorks
            keyword = UI.get_input("Enter search keyword: ")
            from src.dorks import search_dorks
            dorks = search_dorks(keyword)
        elif 1 <= choice_num <= len(categories):
            category = categories[choice_num - 1]
            dorks = DORKS[category]
        else:
            UI.print_error("Invalid choice")
            return None
        
        if not dorks:
            UI.print_error("No dorks found")
            return None
        
        # Display dorks in selected category
        UI.print_success(f"\nAvailable Dorks:\n")
        for idx, dork in enumerate(dorks, 1):
            print(f"[{idx}] {dork['name']}")
            print(f"    Query: {dork['query']}\n")
        
        dork_choice = UI.get_input("Select dork to execute (or 0 to cancel): ")
        dork_num = int(dork_choice)
        
        if dork_num == 0:
            return None
        elif 1 <= dork_num <= len(dorks):
            selected_dork = dorks[dork_num - 1]
            UI.print_success(f"\nExecuting: {selected_dork['name']}")
            UI.print_success(f"Query: {selected_dork['query']}\n")
            return api.host_search(selected_dork['query'])
        else:
            UI.print_error("Invalid choice")
            return None
            
    except ValueError:
        UI.print_error("Please enter a valid number")
        return None

def show_history_menu(history):
    """Display search history."""
    recent = history.get_recent(20)
    
    if not recent:
        UI.print_error("No history found")
        return
    
    UI.print_success("\n=== Recent Search History ===\n")
    for entry in reversed(recent):
        print(f"[{entry['timestamp']}] {entry['type']}: {entry['query']}")
        if entry.get('result_count'):
            print(f"    Results: {entry['result_count']}")
        print()

def run_cli(args, api, exporter, history):
    """Handle CLI mode."""
    result = None
    query_type = None
    query = None
    
    # Host operations
    if args.host:
        result = api.host(args.host)
        query_type = "host"
        query = args.host
    elif args.search:
        result = api.host_search(args.search)
        query_type = "host_search"
        query = args.search
    elif args.count:
        result = api.host_count(args.count)
        query_type = "host_count"
        query = args.count
    
    # Exploit operations
    elif args.exploit_cve:
        result = api.exploit_search("cve", args.exploit_cve)
        query_type = "exploit_cve"
        query = args.exploit_cve
    elif args.exploit_author:
        result = api.exploit_search("author", args.exploit_author)
        query_type = "exploit_author"
        query = args.exploit_author
    
    # DNS operations
    elif args.dns_resolve:
        result = api.dns_resolve(args.dns_resolve)
        query_type = "dns_resolve"
        query = args.dns_resolve
    elif args.dns_reverse:
        result = api.dns_reverse(args.dns_reverse)
        query_type = "dns_reverse"
        query = args.dns_reverse
    
    # Tools
    elif args.myip:
        result = api.myip()
        query_type = "myip"
        query = "myip"
    elif args.profile:
        result = api.profile()
        query_type = "profile"
        query = "profile"
    
    # Dorks
    elif args.dork:
        all_dorks = get_all_dorks()
        matching_dorks = [d for d in all_dorks if args.dork.lower() in d['name'].lower()]
        
        if matching_dorks:
            dork = matching_dorks[0]
            UI.print_success(f"Using dork: {dork['name']}")
            result = api.host_search(dork['query'])
            query_type = "dork"
            query = dork['name']
        else:
            UI.print_error(f"Dork not found: {args.dork}")
            return
    
    if result:
        UI.print_result(result)
        
        # Add to history
        result_count = None
        if isinstance(result, dict):
            result_count = result.get('total') or len(result.get('matches', []))
        
        history.add_entry(query_type, query, result_count)
        
        # Export if requested
        if args.output:
            try:
                filepath = exporter.export(result, args.output, args.format)
                UI.print_success(f"Results exported to: {filepath}")
            except Exception as e:
                UI.print_error(f"Export failed: {e}")

def run_interactive(api, exporter, history):
    """Handle interactive menu mode."""
    while True:
        UI.show_banner()
        UI.show_menu()
        
        try:
            choice_input = UI.get_input("Which option number : ")
            if not choice_input.strip():
                continue
            
            try:
                choice = int(choice_input)
            except ValueError:
                UI.print_error("Please enter a valid number.")
                UI.get_input("\nPress <ENTER> to continue...")
                continue

            result = None
            query_type = None
            query = None

            if choice == 1:
                target = UI.get_input("Shodan Host IP : ")
                result = api.host(target)
                query_type = "host"
                query = target
            elif choice == 2:
                q = UI.get_input("Shodan Host Count Query : ")
                result = api.host_count(q)
                query_type = "host_count"
                query = q
            elif choice == 3:
                q = UI.get_input("Shodan Host Search Query : ")
                result = api.host_search(q)
                query_type = "host_search"
                query = q
            elif choice == 4:
                q = UI.get_input("Shodan Token Search : ")
                result = api.host_tokens(q)
                query_type = "host_tokens"
                query = q
            elif choice == 5:
                result = api.ports()
                query_type = "ports"
                query = "all"
            
            # Exploits
            elif choice == 6:
                q = UI.get_input("Exploit Author : ")
                result = api.exploit_search("author", q)
                query_type = "exploit_author"
                query = q
            elif choice == 7:
                q = UI.get_input("Exploit CVE : ")
                result = api.exploit_search("cve", q)
                query_type = "exploit_cve"
                query = q
            elif choice == 8:
                q = UI.get_input("Exploit Microsoft Security Bulletin ID : ")
                result = api.exploit_search("msb", q)
                query_type = "exploit_msb"
                query = q
            elif choice == 9:
                q = UI.get_input("Exploit Bugtraq ID : ")
                result = api.exploit_search("bid", q)
                query_type = "exploit_bid"
                query = q
            elif choice == 10:
                q = UI.get_input("Exploit OSVDB ID : ")
                result = api.exploit_search("osvdb", q)
                query_type = "exploit_osvdb"
                query = q
            elif choice == 11:
                q = UI.get_input("Exploit Title : ")
                result = api.exploit_search("title", q)
                query_type = "exploit_title"
                query = q
            elif choice == 12:
                q = UI.get_input("Exploit Description : ")
                result = api.exploit_search("description", q)
                query_type = "exploit_description"
                query = q
            elif choice == 13:
                q = UI.get_input("Exploit Date : ")
                result = api.exploit_search("date", q)
                query_type = "exploit_date"
                query = q
            elif choice == 14:
                q = UI.get_input("Exploit Code : ")
                result = api.exploit_search("code", q)
                query_type = "exploit_code"
                query = q
            elif choice == 15:
                q = UI.get_input("Exploit Platform : ")
                result = api.exploit_search("platform", q)
                query_type = "exploit_platform"
                query = q
            elif choice == 16:
                q = UI.get_input("Exploit Port : ")
                result = api.exploit_search("port", q)
                query_type = "exploit_port"
                query = q

            # DNS & Labs
            elif choice == 17:
                q = UI.get_input("DNS Resolve (hostnames) : ")
                result = api.dns_resolve(q)
                query_type = "dns_resolve"
                query = q
            elif choice == 18:
                q = UI.get_input("DNS Reverse (IPs) : ")
                result = api.dns_reverse(q)
                query_type = "dns_reverse"
                query = q
            elif choice == 19:
                q = UI.get_input("Honeyscore IP : ")
                result = api.honeyscore(q)
                query_type = "honeyscore"
                query = q

            # Tools
            elif choice == 20:
                result = api.profile()
                query_type = "profile"
                query = "profile"
            elif choice == 21:
                result = api.myip()
                query_type = "myip"
                query = "myip"
            elif choice == 22:
                result = api.httpheaders()
                query_type = "httpheaders"
                query = "httpheaders"
            elif choice == 23:
                result = api.api_info()
                query_type = "api_info"
                query = "api_info"

            # New features
            elif choice == 24:
                UI.print_success("Exiting...")
                sys.exit(0)
            elif choice == 25:
                result = show_dorks_menu(api)
                query_type = "dork"
                query = "dork_search"
            elif choice == 26:
                show_history_menu(history)
                UI.get_input("\nPress <ENTER> to continue...")
                continue
            
            else:
                UI.print_error("Invalid option.")

            if result:
                UI.print_result(result)
                
                # Add to history
                result_count = None
                if isinstance(result, dict):
                    result_count = result.get('total') or len(result.get('matches', []))
                
                history.add_entry(query_type, query, result_count)
                
                # Ask to export
                save = UI.get_input("\nSave result to file? (y/N): ").lower()
                if save.startswith('y'):
                    filename = UI.get_input("Filename (press ENTER for auto): ").strip()
                    format_choice = UI.get_input("Format (json/csv/txt) [json]: ").strip() or "json"
                    
                    try:
                        filepath = exporter.export(
                            result, 
                            filename if filename else None, 
                            format_choice
                        )
                        UI.print_success(f"Results exported to: {filepath}")
                    except Exception as e:
                        UI.print_error(f"Export failed: {e}")

            UI.get_input("\nPress <ENTER> to continue...")

        except Exception as e:
            UI.print_error(f"An unexpected error occurred: {e}")
            option = UI.get_input('[*] Would you like to change API Key? <Y/n>: ').lower()
            if option.startswith('y'):
                new_key = UI.get_input('[*] Please enter valid Shodan.io API Key: ')
                Config.save_api_key(new_key)
                api.api_key = new_key
                UI.print_success("API Key updated.")
            else:
                UI.print_error("Exiting...")
                sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse CLI arguments
    parser = argparse.ArgumentParser(
        description="Shodansploit - Shodan API CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python shodansploit.py                          # Interactive mode
  python shodansploit.py --host 8.8.8.8           # Get host info
  python shodansploit.py --search "port:22"       # Search hosts
  python shodansploit.py --exploit-cve CVE-2021-1234  # Search exploits
  python shodansploit.py --dork webcam            # Use a dork
  python shodansploit.py --search "nginx" --output results.json
        """
    )
    
    # Host operations
    parser.add_argument('--host', help='Get information about a host')
    parser.add_argument('--search', help='Search Shodan')
    parser.add_argument('--count', help='Count search results')
    
    # Exploit operations
    parser.add_argument('--exploit-cve', help='Search exploits by CVE')
    parser.add_argument('--exploit-author', help='Search exploits by author')
    
    # DNS operations
    parser.add_argument('--dns-resolve', help='Resolve hostnames')
    parser.add_argument('--dns-reverse', help='Reverse DNS lookup')
    
    # Tools
    parser.add_argument('--myip', action='store_true', help='Get your IP address')
    parser.add_argument('--profile', action='store_true', help='Get account profile')
    
    # Dorks
    parser.add_argument('--dork', help='Use a Shodan dork (e.g., "webcam", "camera")')
    
    # Export
    parser.add_argument('--output', help='Output file for results')
    parser.add_argument('--format', choices=['json', 'csv', 'txt'], default='json', 
                        help='Output format (default: json)')
    
    args = parser.parse_args()

    # 1. Load API Key
    api_key = Config.get_api_key()
    if not api_key:
        api_key = UI.get_input("[*] Please enter a valid Shodan.io API Key: ")
        if Config.save_api_key(api_key):
            UI.print_success("File written: ./api.txt")
        else:
            UI.print_error("Failed to write api.txt")

    # 2. Initialize components
    api = ShodanAPI(api_key)
    exporter = Exporter()
    history = History()
    
    # 3. Determine mode (CLI vs Interactive)
    has_cli_args = any([
        args.host, args.search, args.count,
        args.exploit_cve, args.exploit_author,
        args.dns_resolve, args.dns_reverse,
        args.myip, args.profile, args.dork
    ])
    
    if has_cli_args:
        run_cli(args, api, exporter, history)
    else:
        run_interactive(api, exporter, history)

if __name__ == "__main__":
    main()
