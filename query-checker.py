#!/usr/bin/env python3
# Program for extracting solr queries from a txt file of browser history.
# Browswer history file is expected to have one URL per line and be in inverted chronological order.
from urllib.parse import unquote_plus
import argparse
import sys
from pathlib import Path

def extract_query_from_url(url):
    """
    Extracts the query parameter from a SolrWayback search URL.
    """
    keyword = "search?query="
    pos = url.find(keyword)

    if pos != -1:
        semi_sliced_string = url[pos + len(keyword):]
            
        query = semi_sliced_string.split("&")[0] 
        return query

def extract_facets_from_url(url):
    """
    Extracts the facets parameter from a SolrWayback search URL.
    """
    keyword = "facets="
    pos = url.find(keyword)
    if pos != -1:
        semi_sliced_string = url[pos + len(keyword):]  
            
        facets = semi_sliced_string.split("&")[0]  
        return facets

def extract_filterquery_from_url(url):
    """
    Extracts the filter query (fq) parameter from a SolrWayback search URL.
    """
    keyword = "fq="
    pos = url.find(keyword)
    if pos != -1:
        semi_sliced_string = url[pos + len(keyword):]  
            
        fq = semi_sliced_string.split("&")[0]  
        return fq


def print_results(query, facets, filterquery, counter):
    """
    Prints the extracted query, facets, and filter query in a formatted manner.
    """
    print("Iteration: ", counter)
    print("Query: ", query)
    if facets:
        print("Facets: ", facets)
    if filterquery:
        print("Filter Query: ", filterquery)
    print("-----------------------")

def main(history_path):
    """
    Process a browser search history file and print parsed SolrWayback query information.

    Parameters
    ----------
    history_path : str or Path
        Path to the history file to read. File is expected to contain one URL per line
        in inverted chronological order. The function reads the file, reverses the
        lines, and prints parsed query information.
    """
    with open(history_path, "r") as file:
        # Read all lines into a list and reverse it to have search history in chronological order
        lines = file.readlines()  
        lines.reverse()

        counter = 0 # Counter to keep track of amount of iterations

        for line in lines:

            decoded_line = unquote_plus(line)
            # Determine that history entry is a SolrWayback search URL
            if "localhost:8080/solrwayback/search?query=" in decoded_line:
                counter += 1

                query = extract_query_from_url(decoded_line)
                facets = extract_facets_from_url(decoded_line)
                filterquery = extract_filterquery_from_url(decoded_line)
            
                print_results(query, facets, filterquery, counter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract SolrWayback queries from a browser history text file. The text file should be in inverted chronological order."
    )
    parser.add_argument(
        "historyfile",
        help="Path to the history text file (default: test-history.txt)",
    )

    args = parser.parse_args()
    history_file = args.historyfile

    history_path = Path(history_file)
    if not history_path.is_file():
        print(f"Error: history file not found: {history_file}")
        sys.exit(1)

    main(history_path)