#!/usr/bin/env python3
# Program for extracting solr queries from a txt file of browser history.
# Browswer history file is expected to have one URL per line and be in inverted chronological order.
from urllib.parse import unquote_plus, urlparse, parse_qs
import argparse
import sys
from pathlib import Path

def parse_solrwayback_params(url):
    """
    Parse SolrWayback search URL parameters using urlparse + parse_qs.
    Returns tuple: (query, facets, fq) or (None, None, None) when not present.
    """
    decoded = unquote_plus(url.strip())
    parsed = urlparse(decoded)
    # parse_qs returns lists for each key
    params = parse_qs(parsed.query, keep_blank_values=True)

    query = params.get("query", [None])[0]
    facets = params.get("facets", [None])[0]
    # collect all fq values (parse_qs gives a list if multiple fq are present)
    fqs = params.get("fq", [])

    return query, facets, fqs

def print_results(query, facets, filterquery, counter):
    """
    Prints the extracted query, facets, and filter query in a formatted manner.
    """
    print("Iteration: ", counter)
    print("Query: ", query)
    if facets:
        print("Facets: ", facets)
    # Pretty printing of list of filterqueries
    if filterquery:
        if isinstance(filterquery, list):
            for i, fq in enumerate(filterquery, start=1):
                print(f"Filter Query {i}: ", fq)
        else:
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

                query, facets, filterquery = parse_solrwayback_params(decoded_line)
            
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