import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Style, init
import os
import sys

init(autoreset=True)

USERNAME = "Admiral"
PASSWORD = "Admiral@23"

def banner():
    print(Fore.RED + r"""
██████╗  █████╗ ██████╗  █████╗ ███╗   ███╗███████╗████████╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗ ████║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██████╔╝███████║██████╔╝███████║██╔████╔██║█████╗     ██║   █████╗  ██████╔╝
██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝     ██║   ██╔══╝  ██╔══██╗
██║     ██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║███████╗   ██║   ███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                            
    """ + Style.RESET_ALL)
    print(Fore.CYAN + "╔══════════════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║                      PARAMETER & ADMIN SCANNER TOOL                         ║")
    print(Fore.CYAN + "║                             VERSION 1.0                                     ║")
    print(Fore.CYAN + "║                             MADE BY ZEU$                                    ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════════════════════════════════╝" + Style.RESET_ALL)

def login_screen():
    print(Fore.YELLOW + "╔══════════════════════════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + "║                                 LOGIN SYSTEM                                ║")
    print(Fore.YELLOW + "╠══════════════════════════════════════════════════════════════════════════════╣")
    print(Fore.YELLOW + "║ To access this tool, please enter the correct username and password.        ║")
    print(Fore.YELLOW + "║ Default credentials:                                                        ║")
    print(Fore.YELLOW + "║  Username: Admiral                                                          ║")
    print(Fore.YELLOW + "║  Password: Admiral@23                                                       ║")
    print(Fore.YELLOW + "╚══════════════════════════════════════════════════════════════════════════════╝\n" + Style.RESET_ALL)

    attempts = 3
    while attempts > 0:
        username = input(Fore.CYAN + "Enter Username: " + Style.RESET_ALL).strip()
        password = input(Fore.CYAN + "Enter Password: " + Style.RESET_ALL).strip()

        if username == USERNAME and password == PASSWORD:
            print(Fore.GREEN + "\n[INFO] Login Successful! Access Granted.\n" + Style.RESET_ALL)
            return True
        else:
            attempts -= 1
            print(Fore.RED + f"\n[ERROR] Invalid credentials. You have {attempts} attempt(s) left.\n" + Style.RESET_ALL)

    print(Fore.RED + "\n[INFO] Too many failed attempts. Exiting...\n" + Style.RESET_ALL)
    sys.exit(0)

def show_instructions():
    print(Fore.YELLOW + "╔══════════════════════════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + "║                              HOW TO USE THIS TOOL                            ║")
    print(Fore.YELLOW + "╠══════════════════════════════════════════════════════════════════════════════╣")
    print(Fore.YELLOW + "║ 1. Enter the full URL of the target website (e.g., https://example.com).     ║")
    print(Fore.YELLOW + "║ 2. This tool will scan all internal links within the same domain.            ║")
    print(Fore.YELLOW + "║ 3. If an admin panel is detected, it will display in GREEN.                  ║")
    print(Fore.YELLOW + "║ 4. If SQLi-prone parameters are found, they will display in YELLOW.          ║")
    print(Fore.YELLOW + "║ 5. Follow the on-screen instructions for next steps.                        ║")
    print(Fore.YELLOW + "╚══════════════════════════════════════════════════════════════════════════════╝\n" + Style.RESET_ALL)

def get_links_from_domain(url, domain):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = urljoin(url, a['href'])
            parsed_href = urlparse(href)
            if domain in parsed_href.netloc:
                links.add(href)
        return links
    except Exception as e:
        print(Fore.RED + f"[ERROR] {e}" + Style.RESET_ALL)
        return set()

def get_parameters(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return params if params else None

def is_admin_panel(url):
    admin_keywords = ['admin', 'login', 'dashboard']
    return any(keyword in url.lower() for keyword in admin_keywords)

def scan_site(base_url):
    domain = urlparse(base_url).netloc
    visited = set()
    to_visit = {base_url}
    parameters_found = {}
    admin_pages = []

    while to_visit:
        current_url = to_visit.pop()
        visited.add(current_url)
        links = get_links_from_domain(current_url, domain)
        for link in links:
            if link not in visited:
                to_visit.add(link)
        if is_admin_panel(current_url):
            admin_pages.append(current_url)
        params = get_parameters(current_url)
        if params:
            parameters_found[current_url] = params

    return parameters_found, admin_pages

def display_results(parameters, admins):
    if admins:
        print(Fore.GREEN + "\n[+] Admin Pages Found:" + Style.RESET_ALL)
        for admin in admins:
            print(Fore.GREEN + f"  - {admin}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[INFO] No admin pages found." + Style.RESET_ALL)

    if parameters:
        print(Fore.YELLOW + "\n[+] Parameters Found (Potential SQLi):" + Style.RESET_ALL)
        for url, params in parameters.items():
            print(Fore.BLUE + f"\nURL: {url}" + Style.RESET_ALL)
            for param, values in params.items():
                print(Fore.YELLOW + f"  - Parameter: {param} | Values: {values}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[INFO] No parameters found." + Style.RESET_ALL)

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner()
    if not login_screen():
        return
    show_instructions()

    try:
        base_url = input(Fore.CYAN + "\nEnter the target website (e.g., https://example.com): " + Style.RESET_ALL).strip()
        if not base_url.startswith('http'):
            base_url = 'http://' + base_url

        print(Fore.CYAN + f"\n[INFO] Scanning: {base_url}" + Style.RESET_ALL)
        parameters, admins = scan_site(base_url)
        display_results(parameters, admins)

    except KeyboardInterrupt:
        print(Fore.RED + "\n[INFO] Exiting..." + Style.RESET_ALL)
        sys.exit(0)

if __name__ == "__main__":
    while True:
        main()
        restart = input(Fore.CYAN + "\nDo you want to scan another website? (y/n): " + Style.RESET_ALL).strip().lower()
        if restart != 'y':
            print(Fore.RED + "\n[INFO] Exiting tool. Goodbye!" + Style.RESET_ALL)
            sys.exit(0)
