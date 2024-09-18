
import os
import re
from colorama import Fore, Style, init


init(autoreset=True)

def search_in_file(file_path, search_term):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            if re.search(search_term, line):
                # Highlight the search term in green
                highlighted_line = re.sub(search_term, f"{Fore.GREEN}{search_term}{Style.RESET_ALL}", line.strip())
                results.append((line_number, highlighted_line))
    return results

def search_in_directory(directory_path, search_term):
    search_results = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                results = search_in_file(file_path, search_term)
                if results:
                    search_results[file] = results
    return search_results

if __name__ == "__main__":
    project_dir = "Python"  
    term_to_search = input("Enter term to search (e.g., function name or data type): ")
    
    search_results = search_in_directory(project_dir, term_to_search)
    
    # Print search results with colored function names or terms
    for file, matches in search_results.items():
        print(f"\nFile: {file}")
        for line_number, line in matches:
            print(f" Line {line_number}: {line}")
