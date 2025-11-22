# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-22

### Added
- Initial release
- Support for searching by IMDb ID
- Support for searching by Trakt slug
- Automatic fetching of related items (series, sequels, prequels)
- Built-in caching system
- URL generation for all supported platforms
- Support for the following identifiers:
  - IMDb
  - Trakt.tv
  - Trakt Film ID
  - TMDB (Movie, Series, Episode)
  - Rotten Tomatoes
  - Fandom Wiki
  - Google Knowledge Graph
- Relationship properties:
  - Part of series
  - Follows (previous item)
  - Followed by (next item)

### Features
- No API keys required
- Python 3.7+ support
- Comprehensive documentation
- Type hints support
- Memory caching for performance

[0.1.0]: https://github.com/wa8eem/wikidata-identifier-extractor/releases/tag/v0.1.0
