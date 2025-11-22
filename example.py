"""
Example usage of Wikidata Identifier Extractor
"""

from wikidata_identifier_extractor import WikidataIdentifierExtractor


def main():
    # Initialize the extractor
    extractor = WikidataIdentifierExtractor()
    
    print("=" * 60)
    print("Wikidata Identifier Extractor - Examples")
    print("=" * 60)
    
    # Example 1: Search by IMDb ID
    print("\n📽️  Example 1: Search by IMDb ID")
    print("-" * 60)
    result = extractor.get_identifiers(imdb_id="tt1375666")
    
    if result:
        print(f"Title: {result['title']}")
        print(f"Wikidata ID: {result['wikidata_id']}")
        print(f"IMDb: {result['imdb']}")
        print(f"Trakt: {result['trakt']}")
        print(f"TMDB: {result['tmdb_movie']}")
        print(f"\nURLs:")
        print(f"  IMDb: {result['urls']['imdb']}")
        print(f"  Trakt: {result['urls']['trakt']}")
    
    # Example 2: Search by Trakt slug
    print("\n\n🎬 Example 2: Search by Trakt Slug")
    print("-" * 60)
    result = extractor.get_identifiers(trakt_slug="shows/breaking-bad")
    
    if result:
        print(f"Title: {result['title']}")
        print(f"IMDb: {result['imdb']}")
        print(f"TMDB Series: {result['tmdb_series']}")
    
    # Example 3: Movie with sequels (Lord of the Rings)
    print("\n\n🎭 Example 3: Movie in a Series")
    print("-" * 60)
    result = extractor.get_identifiers(imdb_id="tt0167261")
    
    if result:
        print(f"Title: {result['title']}")
        
        if result.get('follows'):
            print(f"\n⬅️  Previous: {result['follows']['title']}")
            print(f"   IMDb: {result['follows']['imdb']}")
        
        if result.get('followed_by'):
            print(f"\n➡️  Next: {result['followed_by']['title']}")
            print(f"   IMDb: {result['followed_by']['imdb']}")
        
        if result.get('series'):
            print(f"\n📚 Part of: {result['series']['title']}")
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
