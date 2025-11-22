# Wikidata Identifier Extractor

[![PyPI version](https://badge.fury.io/py/wikidata-identifier-extractor.svg)](https://badge.fury.io/py/wikidata-identifier-extractor)
[![Python Versions](https://img.shields.io/pypi/pyversions/wikidata-identifier-extractor.svg)](https://pypi.org/project/wikidata-identifier-extractor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python library for extracting cross-platform media identifiers from [Wikidata](https://www.wikidata.org/). Find IMDb, Trakt, TMDB, Rotten Tomatoes IDs and more for movies, TV shows, and episodes.

## Features

✨ **Cross-Platform Mapping**: Get identifiers for IMDb, Trakt, TMDB, Rotten Tomatoes, and more  
🔗 **Relationship Data**: Automatically fetch sequels, prequels, and series information  
💾 **Built-in Caching**: Efficient caching to minimize API calls  
🆓 **No API Keys Required**: Uses Wikidata's free SPARQL endpoint  
📊 **Comprehensive Coverage**: Access millions of movies, TV shows, and episodes  
🔄 **Automatic URL Generation**: Get ready-to-use URLs for all platforms  

## Installation

```bash
pip install wikidata-identifier-extractor
```

## Quick Start

```python
from wikidata_identifier_extractor import WikidataIdentifierExtractor

# Initialize the extractor
extractor = WikidataIdentifierExtractor()

# Search by IMDb ID
result = extractor.get_identifiers(imdb_id="tt1375666")

print(f"Title: {result['title']}")           # Inception
print(f"Trakt: {result['trakt']}")           # movies/inception-2010
print(f"TMDB: {result['tmdb_movie']}")       # 27205
print(f"IMDb URL: {result['urls']['imdb']}")  # https://www.imdb.com/title/tt1375666
```

## Usage Examples

### Search by Trakt Slug

```python
result = extractor.get_identifiers(trakt_slug="movies/inception-2010")

print(result['imdb'])          # tt1375666
print(result['wikidata_id'])   # Q25188
```

### Get Movie Sequels/Prequels

```python
# Lord of the Rings: The Two Towers
result = extractor.get_identifiers(imdb_id="tt0167261")

# Get previous movie
if result.get('follows'):
    print(result['follows']['title'])  # The Fellowship of the Ring
    print(result['follows']['imdb'])   # tt0120737

# Get next movie
if result.get('followed_by'):
    print(result['followed_by']['title'])  # The Return of the King
    print(result['followed_by']['imdb'])   # tt0167260

# Get series information
if result.get('series'):
    print(result['series']['title'])  # The Lord of the Rings trilogy
```

### Disable Relation Fetching

For faster queries when you don't need related items:

```python
result = extractor.get_identifiers(
    imdb_id="tt0167261",
    fetch_relations=False  # Skip fetching series/follows/followed_by
)
```

## Response Structure

```python
{
    'wikidata_id': 'Q25188',
    'title': 'Inception',
    'imdb': 'tt1375666',
    'trakt': 'movies/inception-2010',
    'trakt_film': 'inception-2010',
    'tmdb_movie': '27205',
    'rotten_tomatoes': 'm/inception',
    'google_kg': '/g/11b6vxwpkm',
    'fandom_wiki': 'inception',
    'part_of_series_id': None,
    'follows_id': None,
    'followed_by_id': None,
    'urls': {
        'wikidata': 'https://www.wikidata.org/wiki/Q25188',
        'imdb': 'https://www.imdb.com/title/tt1375666',
        'trakt': 'https://trakt.tv/movies/inception-2010',
        'tmdb_movie': 'https://www.themoviedb.org/movie/27205',
        # ... more URLs
    },
    'series': None,        # Populated if part of a series
    'follows': None,       # Populated if there's a previous item
    'followed_by': None    # Populated if there's a next item
}
```

## Supported Identifiers

| Platform | Property | Example |
|----------|----------|---------|
| Wikidata | wikidata_id | Q25188 |
| IMDb | imdb | tt1375666 |
| Trakt.tv | trakt | movies/inception-2010 |
| Trakt Film | trakt_film | inception-2010 |
| TMDB Movie | tmdb_movie | 27205 |
| TMDB Series | tmdb_series | 1399 |
| TMDB Episode | tmdb_episode | 63056 |
| Rotten Tomatoes | rotten_tomatoes | m/inception |
| Fandom Wiki | fandom_wiki | lotr |
| Google Knowledge Graph | google_kg | /g/11b6vxwpkm |

## Advanced Usage

### Batch Processing

```python
def process_multiple_movies(imdb_ids):
    extractor = WikidataIdentifierExtractor()
    results = []
    
    for imdb_id in imdb_ids:
        result = extractor.get_identifiers(imdb_id=imdb_id)
        if result:
            results.append(result)
    
    return results

movies = ["tt1375666", "tt0468569", "tt0816692"]
results = process_multiple_movies(movies)
```

### Error Handling

```python
try:
    result = extractor.get_identifiers(imdb_id="tt1375666")
    if result:
        print(f"Found: {result['title']}")
    else:
        print("No results found")
except Exception as e:
    print(f"Error: {e}")
```

## How It Works

This library uses [Wikidata's SPARQL endpoint](https://query.wikidata.org/) to query structured data about media content. Wikidata is a free, collaborative knowledge base that links various platform-specific identifiers together.

**Key Benefits:**
- 🆓 Free and open - no API keys required
- 🌐 Community-maintained and constantly updated
- 🔗 Comprehensive cross-platform linking
- 📈 Covers millions of movies, TV shows, and episodes

## Performance

- **Caching**: Built-in memory cache prevents redundant API calls
- **Configurable Depth**: Control relationship fetching to balance speed vs data completeness
- **Rate Limiting Friendly**: Respectful of Wikidata's SPARQL endpoint limits

## Requirements

- Python 3.7+
- requests >= 2.25.0

## Documentation

Full documentation is available in the [docs](./docs) folder:

- **[Complete Guide](./docs/GUIDE.md)**: Detailed usage examples and API reference
- **[SPARQL Tutorial](./docs/GUIDE.md#sparql-query-examples)**: Learn how to modify and extend queries
- **[Contributing](./CONTRIBUTING.md)**: How to contribute to the project

## Development

```bash
# Clone the repository
git clone https://github.com/wa8eem/wikidata-identifier-extractor.git
cd wikidata-identifier-extractor

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Wikidata](https://www.wikidata.org/) for providing free access to structured data
- The Wikidata community for maintaining and updating the database

## Support

- 📫 Issues: [GitHub Issues](https://github.com/wa8eem/wikidata-identifier-extractor/issues)
- 📖 Documentation: [Full Guide](./docs/GUIDE.md)
- 💬 Discussions: [GitHub Discussions](https://github.com/wa8eem/wikidata-identifier-extractor/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each version.

---

Made with ❤️ using [Wikidata](https://www.wikidata.org/)
