# SolrWayback Query History Parser

A small utility to extract SolrWayback search queries (and optional facets / filter queries) from a browser history text file.

This repository contains a single script, `query-checker.py`, which reads a history file with one URL per line (in inverted chronological order) and prints parsed SolrWayback search queries in chronological order.

## Why

If you use SolrWayback and want to analyze or revisit past searches recorded by your browser, this script parses the search URL parameters and prints the query, facets, and filter queries in a readable format.

## Requirements

- Python 3.6+
- No external Python packages required (uses the standard library)

## Expected input format

- A plain text file with one URL per line. The file should be in inverted chronological order (newest entry first), which is the typical order exported by many browser history tools.

Example (lines are URLs):

    https://localhost:8080/solrwayback/search?query=example+term&facets=...&fq=...
    https://localhost:8080/solrwayback/search?query=another+search

The script only processes lines that contain `localhost:8080/solrwayback/search?query=` and will decode URL-encoded strings before parsing.

## Usage

Run the script with the path to your history text file:

```bash
python3 query-checker.py path/to/your-history.txt
```

For example, if you're using the included test file:

```bash
python3 query-checker.py test-history.txt
```

## Output

For each SolrWayback search URL found in the history file, the script prints an iteration number and the parsed parameters. Example output:

```
Iteration:  1
Query:  example term
Facets:  facetParam
Filter Query:  field:value
-----------------------
```

Notes:
- The script extracts the first `query`, the first `facets` parameter, and the first `fq` parameter from the URL query string.
- URL-decoding is performed using `urllib.parse.unquote_plus`, so `+` and percent-encodings will be converted to readable text.

## Limitations and possible improvements

- The script currently looks for `localhost:8080/solrwayback/search?query=`. If your SolrWayback instance runs on a different host or port, update the script or use a preprocessed history file.

## Contributing

Small fixes or clarifications are welcome. For code changes, please create a branch and open a pull request with a short description.


