import os

import subprocess

from rich.console import Console

from rich.prompt import Prompt

import re

import socket

import nmap 



console = Console()



def center_text(text):

    """Center text in the terminal."""

    term_width = os.get_terminal_size().columns

    return text.center(term_width)



def show_banner():

    banner_lines = [

 " _____________________ ____                             _    __  _______ ",

 "                       |  _ \ ___  ___ ___  _ __        / \   \ \/ / ____|",

 "                       | |_) / _ \/ __/ _ \| '_ \      / _ \   \  /|  _|  ",

 "                       |  _ <  __/ (_| (_) | | | |    / ___ \  /  \| |___ ",

 "                       |_| \_\___|\___\___/|_| |_|___/_/   \_\/_/\_\_____|",

  "                                              |_____|                  By Cyberboy.net___________________"

    ]



    term_width = os.get_terminal_size().columns

    for line in banner_lines:

        centered_line = line.center(term_width)

        console.print(centered_line, style="bold cyan")





def create_directory(path):

    """Create a directory if it does not exist."""

    if not os.path.exists(path):

        os.makedirs(path)



def touch_file(filename):

    """Create a file if it does not exist."""

    if not os.path.isfile(filename):

        open(filename, 'a').close()



def run_command(command, capture_output=False):

    """Run a shell command."""

    result = subprocess.run(command, shell=True, text=True, capture_output=capture_output)

    return result.stdout if capture_output else None



def count_lines(file_path):

    """Count the number of lines in a file."""

    with open(file_path, 'r') as file:

        return len(file.readlines())

def center_text_with_asterisks(text):

    """Center text in the terminal with asterisks."""

    term_width = os.get_terminal_size().columns

    padded_text = f" {text} ".center(term_width)

    asterisk_line = '*' * term_width

    return f"{asterisk_line}\n{padded_text}\n{asterisk_line}"



def subdomain_enum(url):

    console.print(center_text_with_asterisks("Performing Subdomain Enumeration"), style="bold magenta")



    # Create directories and files

    create_directory(url)

    create_directory(f"{url}/recon")

    create_directory(f"{url}/recon/httprobe")

    touch_file(f"{url}/recon/httprobe/alive.txt")

    touch_file(f"{url}/recon/final.txt")



    # Run assetfinder

    console.print("[+] Finding subdomains with Assetfinder...", style="bold green")

    run_command(f"assetfinder {url} >> {url}/recon/assets.txt")



    # Combine results for unique count

    run_command(f"cat {url}/recon/assets.txt >> {url}/recon/final.txt")

    run_command(f"rm {url}/recon/assets.txt")



    # Run subfinder

    console.print("[+] Finding subdomains with Subfinder...", style="bold green")

    run_command(f"subfinder -d {url} --silent >> {url}/recon/subfinder.txt")

    run_command(f"cat {url}/recon/subfinder.txt >> {url}/recon/final.txt")

    run_command(f"rm {url}/recon/subfinder.txt")



    # Run amass

    console.print("[+] Harvesting Subdomains with Amass...", style="bold green")

    run_command(f"amass enum -d {url} --silent >> {url}/recon/f.txt")

    run_command(f"cat {url}/recon/f.txt >> {url}/recon/final.txt")

    run_command(f"sort -u {url}/recon/final.txt >> {url}/recon/temp.txt")

    os.rename(f"{url}/recon/temp.txt", f"{url}/recon/final.txt")

    final_count = count_lines(f"{url}/recon/final.txt")

    console.print(f"Total Unique Domains Found: {final_count}", style="yellow")



    # Probing for alive domains

    console.print("[+] Probing for alive domains...", style="bold green")

    run_command(f"cat {url}/recon/final.txt | sort -u | httpx -silent >> {url}/recon/httprobe/a.txt")

    run_command(f"sort -u {url}/recon/httprobe/a.txt > {url}/recon/httprobe/alive.txt")

    os.remove(f"{url}/recon/httprobe/a.txt")

    alive_count = count_lines(f"{url}/recon/httprobe/alive.txt")

    console.print(f"Alive Domains: {alive_count}", style="yellow")



def collect_urls(url):

    console.print(center_text_with_asterisks("Collecting Urls With Waybackurls and Gau"), style="bold magenta")



    # Prepare filenames

    domains_filename = 'domains.txt'

    gau_filename = f"gau_{url}.txt"

    wayback_filename = f"wayback_{url}.txt"

    combined_filename = f"combined_{url}.txt"



    # Create and write to domains.txt

    touch_file(domains_filename)

    with open(domains_filename, 'w') as file:

        file.write(url + '\n')



    # Run gau command and save output

    console.print("[+] Running gau...", style="bold green")

    gau_command = f"cat {domains_filename} | gau --threads 5 > {gau_filename}"

    run_command(gau_command)



    # Run waybackurls command and save output

    console.print("[+] Running waybackurls...", style="bold green")

    waybackurls_command = f"cat {domains_filename} | waybackurls > {wayback_filename}"

    run_command(waybackurls_command)



    # Combine files

    console.print("[+] Combining output files...", style="bold green")

    with open(combined_filename, 'w') as outfile:

        for fname in [gau_filename, wayback_filename]:

            with open(fname) as infile:

                for line in infile:

                    outfile.write(line)



    # Count lines in the combined file

    line_count = count_lines(combined_filename)

    console.print(f"[+] Total URLs collected: {line_count}", style="bold yellow")





def port_service_scan(url):

    console.print(center_text_with_asterisks("Starting port scan"), style="bold magenta")



    # Check if url is a valid domain name using regex (optional)

    if not re.match(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$', url):

        console.print(f"Invalid domain format: {url}", style="bold red")

        return



    try:

        # Resolving domain to IP

        ip_address = socket.gethostbyname(url)

    except socket.gaierror:

        console.print(f"Failed to resolve IP for domain: {url}", style="bold red")

        return



    scanner = nmap.PortScanner()

    scanner.scan(ip_address, arguments='-sV')  # -sV for version detection



    for host in scanner.all_hosts():

        console.print(f'Host: {host} ({scanner[host].hostname()})', style="bold blue")

        console.print(f'State: {scanner[host].state()}', style="bold blue")



        for proto in scanner[host].all_protocols():

            console.print(f'Protocol: {proto}', style="bold blue")



            lport = scanner[host][proto].keys()

            for port in lport:

                console.print(f'Port: {port}\tState: {scanner[host][proto][port]["state"]}\tService: {scanner[host][proto][port]["name"]}\tVersion: {scanner[host][proto][port]["version"]}', style="bold blue")



def do_all(url):

    # Call all functions for 'Do All'

    console.print(center_text_with_asterisks("Performing All tasks"), style="bold magenta")

    subdomain_enum(url)

    collect_urls(url)

    port_service_scan(url)



def exit_script():

    console.print("Exiting the script...", style="bold red")

    exit()



def main(url=None):

    show_banner()

    if url is None:

        url = console.input("[bold green][align=center]Please enter the domain name:[/align][/bold green]")



    while True:

        console.print("\n[bold magenta][align=center]1. Subdomain Enumeration[/align][/bold magenta]")

        console.print("[bold green][align=center]2. Collect Possible URLs[/align][/bold green]")

        console.print("[bold cyan][align=center]3. Port and Service Scan[/align][/bold cyan]")

        console.print("[bold yellow][align=center]4. Do All[/align][/bold yellow]")

        console.print("[bold red][align=center]5. Exit[/align][/bold red]\n")



        choice = console.input("[bold green][align=center]Choose an option [1/2/3/4/5]: [/align][/bold green]")





        if choice == "1":

            subdomain_enum(url)

        elif choice == "2":

            collect_urls(url)

        elif choice == "3":

            port_service_scan(url)

        elif choice == "4":

            do_all(url)

        elif choice == "5":

            exit_script()



if __name__ == "__main__":

    import sys

    url_arg = sys.argv[1] if len(sys.argv) > 1 else None

    main(url_arg)

