# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-11-12

### Added
- Initial release of SolrWayback Query History Parser
- `parse_solrwayback_params()` function to extract query parameters from search URLs
- `parse_archived_url()` function to extract archive date and original URL from playback URLs
- `print_search_results()` function to display parsed search query information
- `print_playback_info()` function to display archived page access information
- Support for parsing multiple filter queries (`fq`) from encoded facets parameter
- Global counter to track sequential actions in browsing history
- Detection of click patterns (search result clicks vs. playback page navigation)
- Command-line interface accepting history file path as argument
- README.md with usage instructions, examples, and citation information
- DOI badge integration with Zenodo (10.5281/zenodo.17539852)
- Citation formats: BibTeX, Plain Text, APA Style, and Chicago Style
- MIT License
- Test history file (`test-history.txt`) for demonstration

[Unreleased]: https://github.com/WEB-CHILD/SolrWaybackQueryHistory/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/WEB-CHILD/SolrWaybackQueryHistory/releases/tag/v1.0.0
