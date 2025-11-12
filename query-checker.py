#!/usr/bin/env python3
# Program for extracting solr queries from a txt file of browser history.
# Browswer history file is expected to have one URL per line and be in inverted chronological order.
from urllib.parse import unquote_plus, urlparse, parse_qs
import argparse
import sys
from pathlib import Path

PLAYBACK_PREFIX = "http://localhost:8080/solrwayback/services/web/"
QUERY_PREFIX = "http://localhost:8080/solrwayback/search?query="
LAST_ACTION_EQUALS_CLICK = False
COUNTER = 0

def parse_archived_url(decoded_url):
    """
    Parse a SolrWayback archived web URL to extract the date and original URL.
    
    Parameters
    ----------
    decoded_url : str
        A decoded URL in the format:
        http://localhost:8080/solrwayback/services/web/{DATE}/{ORIGINAL_URL}
    
    Returns
    -------
    tuple
        (date, url) where:
        - date: str, the timestamp (e.g., "20001117071800")
        - url: str, the original archived URL
    """
    prefix = PLAYBACK_PREFIX
    
    if not decoded_url.startswith(prefix):
        raise ValueError("URL must start with the playback prefix: " + prefix)

    # Remove the prefix
    remainder = decoded_url[len(prefix):]
    
    # Split on the first '/' to separate date from URL
    parts = remainder.split('/', 1)
    
    if len(parts) != 2:
        raise ValueError("URL does not contain a valid date and original URL after the prefix. It was split into:" + str(parts))
    
    date = parts[0]
    url = parts[1]
    
    return date, url


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

def print_search_results(query, facets, filterquery):
    """
    Prints the extracted query, facets, and filter query in a formatted manner.
    """
    global COUNTER
    print("Action Number: ", COUNTER)
    print("SolrWayback Query changed.")
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

        for line in lines:
            global LAST_ACTION_EQUALS_CLICK

            # Decode the line for easier parsing and better readability
            decoded_line = unquote_plus(line)

            # Determine that history entry is a SolrWayback Playback URL
            if decoded_line.startswith(PLAYBACK_PREFIX):
                handle_playback_entry(decoded_line)

            # Determine that history entry is a SolrWayback search URL
            elif decoded_line.startswith(QUERY_PREFIX):
                handle_search_entry(decoded_line)

def handle_search_entry(decoded_line):
    global LAST_ACTION_EQUALS_CLICK, COUNTER
    COUNTER += 1
    query, facets, filterquery = parse_solrwayback_params(decoded_line)
    print_search_results(query, facets, filterquery)
    LAST_ACTION_EQUALS_CLICK = False

def handle_playback_entry(decoded_line):
    global LAST_ACTION_EQUALS_CLICK, COUNTER
    COUNTER += 1
    archive_date, original_url = parse_archived_url(decoded_line)
    print_playback_info(decoded_line, archive_date, original_url)
    LAST_ACTION_EQUALS_CLICK = True

def print_playback_info(decoded_line, archive_date, original_url):
    """
        Print information about a clicked SolrWayback playback URL.
    """
    global COUNTER
    print(f"Action Number: {COUNTER}")
    if LAST_ACTION_EQUALS_CLICK:
        print("Clicked on a link from a playback page.")
    else:
        print("Found interesting search result and clicked it from search results: ")
    print("SolrWayback Playback URL clicked.")
    print("URL clicked: ", decoded_line)
    print("Archive Date: ", archive_date)
    print("Original URL: ", original_url)
    print("-----------------------")

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