import requests
from typing import Dict, Optional, List
from dataclasses import dataclass, field

@dataclass
class WikidataItem:
    """Represents a Wikidata item with all its identifiers"""
    wikidata_id: str
    title: str
    imdb: Optional[str] = None
    rotten_tomatoes: Optional[str] = None
    trakt: Optional[str] = None
    trakt_film: Optional[str] = None
    fandom_wiki: Optional[str] = None
    fandom_article: Optional[str] = None
    google_kg: Optional[str] = None
    tmdb_movie: Optional[str] = None
    tmdb_series: Optional[str] = None
    tmdb_episode: Optional[str] = None
    part_of_series_id: Optional[str] = None
    follows_id: Optional[str] = None
    followed_by_id: Optional[str] = None
    urls: Dict[str, str] = field(default_factory=dict)
    series: Optional['WikidataItem'] = None
    follows: Optional['WikidataItem'] = None
    followed_by: Optional['WikidataItem'] = None


class WikidataIdentifierExtractor:
    """Extract identifiers from Wikidata for movies, TV series, and episodes"""
    
    SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
    
    # Property mappings
    PROPERTIES = {
        'imdb': 'P345',
        'rotten_tomatoes': 'P1258',
        'trakt': 'P8013',
        'trakt_film': 'P12492',
        'part_of_series': 'P179',
        'follows': 'P155',
        'followed_by': 'P156',
        'fandom_wiki': 'P4073',
        'fandom_article': 'P6262',
        'google_kg': 'P2671',
        'tmdb_movie': 'P4947',
        'tmdb_series': 'P4983',
        'tmdb_episode': 'P12559',
    }
    
    # URL templates
    URL_TEMPLATES = {
        'wikidata': 'https://www.wikidata.org/wiki/{wikidata_id}',
        'imdb': 'https://www.imdb.com/title/{imdb}',
        'rotten_tomatoes': 'https://www.rottentomatoes.com/{rotten_tomatoes}',
        'trakt': 'https://trakt.tv/{trakt}',
        'trakt_film': 'https://trakt.tv/movies/{trakt_film}',
        'fandom_wiki': 'https://{fandom_wiki}.fandom.com',
        'google_kg': 'https://www.google.com/search?kgmid={google_kg}',
        'tmdb_movie': 'https://www.themoviedb.org/movie/{tmdb_movie}',
        'tmdb_series': 'https://www.themoviedb.org/tv/{tmdb_series}',
        'tmdb_episode': 'https://www.themoviedb.org/episode/{tmdb_episode}',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'WikidataIdentifierExtractor/1.0'})
        self._cache = {}  # Simple cache to avoid re-querying same items
    
    def get_identifiers(self, imdb_id: str = None, trakt_slug: str = None, 
                       fetch_relations: bool = True) -> Optional[Dict]:
        """
        Get all identifiers by IMDb ID or Trakt slug
        
        Args:
            imdb_id: IMDb identifier (e.g., 'tt1375666')
            trakt_slug: Trakt slug (e.g., 'movies/inception-2010')
            fetch_relations: Whether to fetch related items (series, follows, followed_by)
        
        Returns:
            Dictionary with all identifiers and URLs, or None if not found
        """
        if imdb_id:
            imdb_id = imdb_id if imdb_id.startswith('tt') else f'tt{imdb_id}'
            cache_key = f'imdb:{imdb_id}'
            filter_clause = f'?item wdt:P345 "{imdb_id}".'
        elif trakt_slug:
            trakt_slug = trakt_slug.split('trakt.tv/')[-1] if 'trakt.tv' in trakt_slug else trakt_slug
            cache_key = f'trakt:{trakt_slug}'
            filter_clause = f'?item wdt:P8013 "{trakt_slug}".'
        else:
            return None
        
        # Check cache
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        query = self._build_main_query(filter_clause)
        results = self._execute_sparql(query)
        
        if not results:
            return None
        
        response = self._build_response(results[0])
        
        # Fetch related items if requested
        if fetch_relations:
            self._fetch_related_items(response)
        
        # Cache and return
        self._cache[cache_key] = response
        return response
    
    def _build_main_query(self, filter_clause: str) -> str:
        """Build the main SPARQL query"""
        return f"""
        SELECT ?item ?itemLabel ?imdb ?rottenTomatoes ?trakt ?traktFilm ?partOfSeries 
               ?follows ?followedBy ?fandom ?fandomArticle ?googleKG 
               ?tmdbMovie ?tmdbSeries ?tmdbEpisode WHERE {{
          {filter_clause}
          OPTIONAL {{ ?item wdt:P345 ?imdb. }}
          OPTIONAL {{ ?item wdt:P1258 ?rottenTomatoes. }}
          OPTIONAL {{ ?item wdt:P8013 ?trakt. }}
          OPTIONAL {{ ?item wdt:P12492 ?traktFilm. }}
          OPTIONAL {{ ?item wdt:P179 ?partOfSeries. }}
          OPTIONAL {{ ?item wdt:P155 ?follows. }}
          OPTIONAL {{ ?item wdt:P156 ?followedBy. }}
          OPTIONAL {{ ?item wdt:P4073 ?fandom. }}
          OPTIONAL {{ ?item wdt:P6262 ?fandomArticle. }}
          OPTIONAL {{ ?item wdt:P2671 ?googleKG. }}
          OPTIONAL {{ ?item wdt:P4947 ?tmdbMovie. }}
          OPTIONAL {{ ?item wdt:P4983 ?tmdbSeries. }}
          OPTIONAL {{ ?item wdt:P12559 ?tmdbEpisode. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 1
        """
    
    def _fetch_related_items(self, response: Dict) -> None:
        """Fetch all related items (series, follows, followed_by)"""
        # Fetch series info
        if response.get('part_of_series_id'):
            series_info = self._get_item_by_wikidata_id(response['part_of_series_id'])
            if series_info:
                response['series'] = series_info
        
        # Fetch previous item
        if response.get('follows_id'):
            follows_info = self._get_item_by_wikidata_id(response['follows_id'])
            if follows_info:
                response['follows'] = follows_info
        
        # Fetch next item
        if response.get('followed_by_id'):
            followed_by_info = self._get_item_by_wikidata_id(response['followed_by_id'])
            if followed_by_info:
                response['followed_by'] = followed_by_info
    
    def _build_response(self, data: Dict) -> Dict:
        """Build structured response with IDs and URLs"""
        
        ids = {
            'wikidata_id': data.get('item', '').split('/')[-1],
            'title': data.get('itemLabel'),
            'imdb': data.get('imdb'),
            'rotten_tomatoes': data.get('rottenTomatoes'),
            'trakt': data.get('trakt'),
            'trakt_film': data.get('traktFilm'),
            'part_of_series_id': data.get('partOfSeries', '').split('/')[-1] if data.get('partOfSeries') else None,
            'follows_id': data.get('follows', '').split('/')[-1] if data.get('follows') else None,
            'followed_by_id': data.get('followedBy', '').split('/')[-1] if data.get('followedBy') else None,
            'fandom_wiki': data.get('fandom'),
            'fandom_article': data.get('fandomArticle'),
            'google_kg': data.get('googleKG'),
            'tmdb_movie': data.get('tmdbMovie'),
            'tmdb_series': data.get('tmdbSeries'),
            'tmdb_episode': data.get('tmdbEpisode'),
        }
        
        # Build URLs from available IDs
        urls = self._build_urls(ids)
        
        return {**ids, 'urls': urls}
    
    def _build_urls(self, ids: Dict) -> Dict[str, str]:
        """Build URLs from available identifiers"""
        urls = {}
        for key, template in self.URL_TEMPLATES.items():
            id_key = key if key in ids else key.replace('_id', '')
            id_value = ids.get(id_key if id_key != 'wikidata' else 'wikidata_id')
            
            if id_value:
                # Special handling for fandom_article (already full URL)
                if id_key == 'fandom_article':
                    urls[key] = id_value
                else:
                    urls[key] = template.format(**ids)
        
        return urls
    
    def _get_item_by_wikidata_id(self, wikidata_id: str, depth: int = 0) -> Optional[Dict]:
        """
        Get information about an item by its Wikidata ID
        
        Args:
            wikidata_id: Wikidata identifier (e.g., 'Q42')
            depth: Recursion depth to prevent infinite loops
        
        Returns:
            Dictionary with identifiers or None
        """
        if not wikidata_id or depth > 2:  # Prevent deep recursion
            return None
        
        # Check cache first
        cache_key = f'wd:{wikidata_id}'
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        query = f"""
        SELECT ?item ?itemLabel ?imdb ?rottenTomatoes ?trakt ?traktFilm 
               ?follows ?followedBy ?fandom ?fandomArticle ?googleKG 
               ?tmdbMovie ?tmdbSeries WHERE {{
          BIND(wd:{wikidata_id} AS ?item)
          OPTIONAL {{ ?item wdt:P345 ?imdb. }}
          OPTIONAL {{ ?item wdt:P1258 ?rottenTomatoes. }}
          OPTIONAL {{ ?item wdt:P8013 ?trakt. }}
          OPTIONAL {{ ?item wdt:P12492 ?traktFilm. }}
          OPTIONAL {{ ?item wdt:P155 ?follows. }}
          OPTIONAL {{ ?item wdt:P156 ?followedBy. }}
          OPTIONAL {{ ?item wdt:P4073 ?fandom. }}
          OPTIONAL {{ ?item wdt:P6262 ?fandomArticle. }}
          OPTIONAL {{ ?item wdt:P2671 ?googleKG. }}
          OPTIONAL {{ ?item wdt:P4947 ?tmdbMovie. }}
          OPTIONAL {{ ?item wdt:P4983 ?tmdbSeries. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 1
        """
        
        results = self._execute_sparql(query)
        if not results:
            return None
        
        response = self._build_response(results[0])
        
        # For related items, only fetch one level deep to avoid excessive queries
        if depth < 1:
            if response.get('follows_id'):
                follows_info = self._get_item_by_wikidata_id(response['follows_id'], depth + 1)
                if follows_info:
                    response['follows'] = follows_info
            
            if response.get('followed_by_id'):
                followed_by_info = self._get_item_by_wikidata_id(response['followed_by_id'], depth + 1)
                if followed_by_info:
                    response['followed_by'] = followed_by_info
        
        # Cache and return
        self._cache[cache_key] = response
        return response
    
    def _execute_sparql(self, query: str) -> list:
        """Execute SPARQL query"""
        try:
            response = self.session.get(
                self.SPARQL_ENDPOINT,
                params={'query': query, 'format': 'json'},
                timeout=10
            )
            response.raise_for_status()
            
            bindings = response.json().get('results', {}).get('bindings', [])
            return [{k: v.get('value') for k, v in b.items()} for b in bindings]
        except Exception as e:
            print(f"Error: {e}")
            return []
