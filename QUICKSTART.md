# Quick Start - Publishing to PyPI

## TL;DR - Fast Track

```bash
# 1. Navigate to package directory
cd /Users/waseemmac/Documents/wikidata-identifier-extractor

# 2. Update your email in pyproject.toml (IMPORTANT!)
# Edit: authors email and maintainers email

# 3. Install build tools
pip install --upgrade build twine

# 4. Clean and build
rm -rf build/ dist/ *.egg-info
python -m build

# 5. Test on TestPyPI first (optional but recommended)
python -m twine upload --repository testpypi dist/*

# 6. Upload to PyPI
python -m twine upload dist/*
```

## What You Get

Your package is now ready to publish! It includes:

✅ **Package Code**: Clean, well-structured Python package  
✅ **Documentation**: Comprehensive README and guide  
✅ **Examples**: Working example script  
✅ **License**: MIT License  
✅ **Build Config**: Modern pyproject.toml setup  
✅ **Publishing Guide**: Step-by-step instructions  

## Package Structure

```
wikidata-identifier-extractor/
├── wikidata_identifier_extractor/  # Main package
│   ├── __init__.py                 # Package initialization
│   └── extractor.py                # Core functionality
├── docs/
│   └── GUIDE.md                    # Complete documentation
├── README.md                       # PyPI package description
├── LICENSE                         # MIT License
├── CHANGELOG.md                    # Version history
├── CONTRIBUTING.md                 # Contribution guidelines
├── PUBLISHING.md                   # Detailed publishing guide
├── pyproject.toml                  # Package configuration
├── setup.py                        # Build compatibility
├── MANIFEST.in                     # Distribution files
├── .gitignore                      # Git ignore rules
└── example.py                      # Usage examples
```

## Before Publishing

### 1. Update Email Address

Edit `pyproject.toml` and replace with your actual email:

```toml
authors = [
    {name = "Muhammad Waseem", email = "muhammadwaseem220@gmail.com"}  
]
maintainers = [
    {name = "Muhammad Waseem", email = "muhammadwaseem220@gmail.com"} 
]
```

### 2. Create PyPI Account

- **PyPI** (production): https://pypi.org/account/register/
- **TestPyPI** (testing): https://test.pypi.org/account/register/

## Installation After Publishing

Once published, users install with:

```bash
pip install wikidata-identifier-extractor
```

## Usage

```python
from wikidata_identifier_extractor import WikidataIdentifierExtractor

extractor = WikidataIdentifierExtractor()
result = extractor.get_identifiers(imdb_id="tt1375666")
print(result['title'])  # "Inception"
```

## Test Locally First

```bash
# Run the example
cd /Users/waseemmac/Documents/traktflix/wikidata-identifier-extractor
python example.py
```

## Need Help?

- **Quick Guide**: Read this file
- **Detailed Guide**: See `PUBLISHING.md`
- **API Documentation**: See `docs/GUIDE.md`
- **Examples**: Run `example.py`

## Next Steps

1. **Test locally**: `python example.py`
2. **Update email**: Edit `pyproject.toml`
3. **Build package**: `python -m build`
4. **Upload**: `twine upload dist/*`
5. **Celebrate**: 🎉 Your package is live!

---

For detailed instructions, see **[PUBLISHING.md](PUBLISHING.md)**
