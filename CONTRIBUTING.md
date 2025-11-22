# Contributing to Wikidata Identifier Extractor

Thank you for your interest in contributing to Wikidata Identifier Extractor! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/wikidata-identifier-extractor.git
   cd wikidata-identifier-extractor
   ```

3. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

1. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure:
   - Code follows Python best practices
   - New features include documentation
   - Tests are added for new functionality

3. **Format your code**:
   ```bash
   black .
   ```

4. **Run tests**:
   ```bash
   pytest
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Adding New Properties

To add support for new Wikidata properties:

1. Find the property ID on Wikidata (e.g., P6127 for Letterboxd)
2. Add to `PROPERTIES` dict in `extractor.py`
3. Add URL template to `URL_TEMPLATES` if applicable
4. Update SPARQL queries in `_build_main_query()` and `_get_item_by_wikidata_id()`
5. Update `_build_response()` to include the new field
6. Add tests and documentation

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Add docstrings to all public methods

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good code coverage

## Documentation

- Update README.md if adding new features
- Update CHANGELOG.md with your changes
- Add examples for new functionality

## Questions?

Feel free to open an issue for:
- Questions about contributing
- Feature requests
- Bug reports
- General discussion

Thank you for contributing! 🎉
