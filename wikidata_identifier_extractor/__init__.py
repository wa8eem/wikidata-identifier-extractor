"""
Wikidata Identifier Extractor

A Python library for extracting cross-platform media identifiers from Wikidata.
Retrieve IMDb, Trakt, TMDB, Rotten Tomatoes IDs and more for movies, TV shows, and episodes.
"""

__version__ = "0.1.0"
__author__ = "Waseem"
__license__ = "MIT"

from .extractor import WikidataIdentifierExtractor, WikidataItem

__all__ = ["WikidataIdentifierExtractor", "WikidataItem"]
