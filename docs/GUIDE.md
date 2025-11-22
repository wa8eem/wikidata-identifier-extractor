# Wikidata Identifier Extractor

## Overview

The Wikidata Identifier Extractor is a powerful tool for retrieving cross-platform media identifiers from [Wikidata](https://www.wikidata.org/), the free knowledge base that acts as central storage for structured data of Wikimedia projects.

**Location:** `playground/wikidata.py`

## What is Wikidata?

Wikidata is a collaborative, multilingual knowledge base that stores structured data. For media content (movies, TV shows, episodes), Wikidata links various platform-specific identifiers together, making it an excellent source for cross-referencing content across different services.

### Why Use Wikidata?

- **Cross-Platform Mapping**: Find IMDb, Trakt, TMDB, Rotten Tomatoes IDs for the same content
- **Free and Open**: No API keys required for basic queries
- **Comprehensive**: Covers millions of movies, TV shows, and episodes
- **Relationship Data**: Includes sequels, prequels, series information
- **Community Maintained**: Constantly updated by contributors worldwide

## How Wikidata APIs Work

### SPARQL Endpoint

Wikidata provides a **SPARQL endpoint** for querying its data:

```
https://query.wikidata.org/sparql
```

SPARQL (SPARQL Protocol and RDF Query Language) is a query language designed for RDF databases. Think of it as SQL for linked data.

### Basic Query Structure

```sparql
SELECT ?item ?itemLabel ?property1 ?property2 WHERE {
  # Filter clause - find the item
  ?item wdt:P345 "tt1375666".  # Search by IMDb ID
  
  # Optional properties - get additional data
  OPTIONAL { ?item wdt:P345 ?imdb. }
  OPTIONAL { ?item wdt:P8013 ?trakt. }
  
  # Service to get human-readable labels
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 1
```

### Key Components

1. **SELECT Clause**: Specifies what variables to return
2. **WHERE Clause**: Contains the query patterns
3. **OPTIONAL Blocks**: Properties that may or may not exist
4. **SERVICE wikibase:label**: Converts Wikidata IDs to readable names
5. **LIMIT**: Restricts number of results

### Wikidata Properties

Properties in Wikidata are identified by P-numbers. Common media properties:

| Property ID | Name | Example Value |
|-------------|------|---------------|
| P345 | IMDb ID | tt1375666 |
| P8013 | Trakt.tv slug | movies/inception-2010 |
| P12492 | Trakt film ID | inception-2010 |
| P4947 | TMDb movie ID | 27205 |
| P4983 | TMDb TV series ID | 1399 |
| P179 | Part of series | Q201 (Lord of the Rings) |
| P155 | Follows (previous) | Q127367 (previous movie) |
| P156 | Followed by (next) | Q164963 (next movie) |
| P1258 | Rotten Tomatoes ID | m/inception |
| P4073 | Fandom wiki ID | lotr |
| P2671 | Google Knowledge Graph ID | /g/11b6vxwpkm |

**Full list**: https://www.wikidata.org/wiki/Wikidata:List_of_properties

## Tool Architecture

### Class Structure

```python
WikidataIdentifierExtractor
├── __init__()                    # Initialize session and cache
├── get_identifiers()             # Main entry point
├── _build_main_query()           # Construct SPARQL query
├── _fetch_related_items()        # Fetch series, follows, followed_by
├── _build_response()             # Parse raw data to structured dict
├── _build_urls()                 # Generate URLs from IDs
├── _get_item_by_wikidata_id()   # Fetch any item by Wikidata ID
└── _execute_sparql()             # Execute SPARQL query
```

### Data Flow

```
User Input (IMDb/Trakt ID)
    ↓
get_identifiers()
    ↓
Check Cache → [Hit] → Return cached result
    ↓ [Miss]
_build_main_query()
    ↓
_execute_sparql()
    ↓
_build_response()
    ↓
_fetch_related_items() (if fetch_relations=True)
    ↓
Cache Result
    ↓
Return to User
```

### Caching Strategy

The tool implements in-memory caching with the following keys:
- `imdb:tt1375666` - For IMDb lookups
- `trakt:movies/inception-2010` - For Trakt lookups
- `wd:Q25188` - For Wikidata ID lookups

This prevents redundant API calls and improves performance significantly.

## Usage Examples

### Basic Usage

```python
from playground.wikidata import WikidataIdentifierExtractor

extractor = WikidataIdentifierExtractor()

# Search by IMDb ID
result = extractor.get_identifiers(imdb_id="tt1375666")
print(result['title'])  # "Inception"
print(result['trakt'])  # "movies/inception-2010"
print(result['tmdb_movie'])  # "27205"

# Search by Trakt slug
result = extractor.get_identifiers(trakt_slug="movies/inception-2010")
print(result['imdb'])  # "tt1375666"
```

### Response Structure

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
    'series': None,      # Populated if part_of_series_id exists
    'follows': None,     # Populated if follows_id exists
    'followed_by': None  # Populated if followed_by_id exists
}
```

### Handling Sequels/Series

```python
# Lord of the Rings: The Two Towers
result = extractor.get_identifiers(imdb_id="tt0167261")

print(result['title'])  # "The Lord of the Rings: The Two Towers"

# Previous movie
if result.get('follows'):
    print(result['follows']['title'])  # "The Lord of the Rings: The Fellowship of the Ring"
    print(result['follows']['imdb'])   # "tt0120737"

# Next movie
if result.get('followed_by'):
    print(result['followed_by']['title'])  # "The Lord of the Rings: The Return of the King"
    print(result['followed_by']['imdb'])   # "tt0167260"

# Series information
if result.get('series'):
    print(result['series']['title'])  # "The Lord of the Rings trilogy"
```

### Disable Relation Fetching

```python
# Only get direct identifiers, skip related items
result = extractor.get_identifiers(
    imdb_id="tt0167261",
    fetch_relations=False  # Won't fetch series/follows/followed_by
)
```

## How to Modify the Tool

### Adding New Properties

**Step 1:** Find the property on Wikidata

Visit https://www.wikidata.org/wiki/Special:Search and search for the property (e.g., "Letterboxd film ID").

**Step 2:** Add to PROPERTIES dict

```python
PROPERTIES = {
    # ... existing properties
    'letterboxd': 'P6127',  # Add new property
}
```

**Step 3:** Add URL template (if applicable)

```python
URL_TEMPLATES = {
    # ... existing templates
    'letterboxd': 'https://letterboxd.com/film/{letterboxd}/',
}
```

**Step 4:** Update SPARQL query

In `_build_main_query()` and `_get_item_by_wikidata_id()`:

```python
query = f"""
SELECT ?item ?itemLabel ?imdb ... ?letterboxd WHERE {{
  {filter_clause}
  OPTIONAL {{ ?item wdt:P345 ?imdb. }}
  # ... other properties
  OPTIONAL {{ ?item wdt:P6127 ?letterboxd. }}  # Add here
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
LIMIT 1
"""
```

**Step 5:** Update response builder

In `_build_response()`:

```python
ids = {
    # ... existing IDs
    'letterboxd': data.get('letterboxd'),  # Add new field
}
```

### Adding New Search Methods

To search by a different identifier (e.g., TMDB ID):

```python
def get_identifiers(self, imdb_id: str = None, trakt_slug: str = None, 
                   tmdb_id: str = None, fetch_relations: bool = True) -> Optional[Dict]:
    """Get all identifiers by IMDb ID, Trakt slug, or TMDB ID"""
    
    if imdb_id:
        imdb_id = imdb_id if imdb_id.startswith('tt') else f'tt{imdb_id}'
        cache_key = f'imdb:{imdb_id}'
        filter_clause = f'?item wdt:P345 "{imdb_id}".'
    elif trakt_slug:
        trakt_slug = trakt_slug.split('trakt.tv/')[-1] if 'trakt.tv' in trakt_slug else trakt_slug
        cache_key = f'trakt:{trakt_slug}'
        filter_clause = f'?item wdt:P8013 "{trakt_slug}".'
    elif tmdb_id:  # New search method
        cache_key = f'tmdb:{tmdb_id}'
        filter_clause = f'?item wdt:P4947 "{tmdb_id}".'  # For movies
    else:
        return None
    
    # ... rest of method
```

### Modifying Recursion Depth

Control how deep the tool fetches related items:

In `_get_item_by_wikidata_id()`:

```python
def _get_item_by_wikidata_id(self, wikidata_id: str, depth: int = 0) -> Optional[Dict]:
    if not wikidata_id or depth > 3:  # Change from 2 to 3 for deeper recursion
        return None
    
    # ... rest of method
    
    # Fetch relations only for certain depths
    if depth < 2:  # Change from 1 to 2 for more levels
        # ... fetch follows/followed_by
```

### Adding Custom Filters

Filter results by specific criteria:

```python
def get_identifiers_with_filter(self, imdb_id: str, min_year: int = None) -> Optional[Dict]:
    """Get identifiers with additional SPARQL filters"""
    
    filter_clause = f'?item wdt:P345 "{imdb_id}".'
    
    # Add year filter to SPARQL query
    year_filter = ""
    if min_year:
        year_filter = f"?item wdt:P577 ?pubdate. FILTER(YEAR(?pubdate) >= {min_year})"
    
    query = f"""
    SELECT ?item ?itemLabel ?imdb ... WHERE {{
      {filter_clause}
      {year_filter}
      OPTIONAL {{ ?item wdt:P345 ?imdb. }}
      # ... rest of query
    }}
    """
    
    # ... execute and return
```

### Batch Processing

Process multiple items efficiently:

```python
def get_multiple_identifiers(self, imdb_ids: List[str]) -> List[Dict]:
    """Fetch identifiers for multiple IMDb IDs"""
    results = []
    
    for imdb_id in imdb_ids:
        result = self.get_identifiers(imdb_id=imdb_id)
        if result:
            results.append(result)
    
    return results

# Usage
extractor = WikidataIdentifierExtractor()
ids = ["tt1375666", "tt0468569", "tt0816692"]
results = extractor.get_multiple_identifiers(ids)
```

## Performance Considerations

### Query Optimization

1. **Use OPTIONAL sparingly**: Each OPTIONAL clause adds overhead
2. **LIMIT results**: Always use LIMIT to prevent large result sets
3. **Filter early**: Put filter clauses before OPTIONAL blocks
4. **Cache aggressively**: The built-in cache significantly reduces API calls

### Rate Limiting

Wikidata SPARQL endpoint has rate limits:
- **Timeout**: 60 seconds per query
- **Concurrent connections**: Limit to ~5 simultaneous queries
- **Best practice**: Add delays between bulk requests

```python
import time

def batch_query_with_delay(items: List[str], delay: float = 0.5):
    for item in items:
        result = extractor.get_identifiers(imdb_id=item)
        time.sleep(delay)  # Be nice to the API
        yield result
```

### Error Handling

Add robust error handling for production use:

```python
def safe_get_identifiers(self, imdb_id: str, retries: int = 3) -> Optional[Dict]:
    """Get identifiers with retry logic"""
    for attempt in range(retries):
        try:
            return self.get_identifiers(imdb_id=imdb_id)
        except requests.RequestException as e:
            if attempt == retries - 1:
                print(f"Failed after {retries} attempts: {e}")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff
```

## SPARQL Query Examples

### Find All Movies in a Series

```sparql
SELECT ?movie ?movieLabel ?imdb WHERE {
  ?movie wdt:P179 wd:Q190214.  # Part of "The Matrix" series
  ?movie wdt:P345 ?imdb.       # Has IMDb ID
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

### Find Movies by Director

```sparql
SELECT ?movie ?movieLabel ?imdb WHERE {
  ?movie wdt:P57 wd:Q25191.    # Directed by Christopher Nolan
  ?movie wdt:P345 ?imdb.        # Has IMDb ID
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?movie)
LIMIT 20
```

### Find All Sequels

```sparql
SELECT ?sequel ?sequelLabel ?imdb WHERE {
  wd:Q25188 wdt:P156+ ?sequel.  # All items that follow "Inception" (transitive)
  ?sequel wdt:P345 ?imdb.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

## Troubleshooting

### Common Issues

**Issue**: "No results found"
- **Solution**: Check if the item exists on Wikidata first
- Visit: `https://www.wikidata.org/wiki/Special:Search?search=tt1375666`

**Issue**: Query timeout
- **Solution**: Simplify query, remove OPTIONAL clauses, or add more specific filters

**Issue**: Missing properties
- **Solution**: The property might not be set on Wikidata. Consider contributing!

**Issue**: Rate limiting
- **Solution**: Add delays between requests, use caching, or run queries during off-peak hours

### Testing Queries

Test SPARQL queries interactively:
1. Visit: https://query.wikidata.org/
2. Paste your query
3. Click "Run" to see results
4. Use "Display" dropdown to visualize data differently

## Resources

- **Wikidata Query Service**: https://query.wikidata.org/
- **SPARQL Tutorial**: https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial
- **Property List**: https://www.wikidata.org/wiki/Wikidata:List_of_properties
- **SPARQL Examples**: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples
- **Wikidata API Docs**: https://www.wikidata.org/wiki/Wikidata:Data_access

## Contributing to Wikidata

If you find missing data:
1. Create a Wikidata account
2. Search for the item (movie/show)
3. Click "Add statement"
4. Select the property (e.g., "IMDb ID")
5. Enter the value
6. Add references/sources
7. Save

Your contributions help everyone using Wikidata!

## License

This tool uses Wikidata's SPARQL endpoint, which is freely available. Wikidata content is available under CC0 (public domain).
