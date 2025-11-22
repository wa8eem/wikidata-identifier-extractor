# Publishing to PyPI Guide

This guide walks you through publishing the Wikidata Identifier Extractor to PyPI (Python Package Index).

## Prerequisites

### 1. Create PyPI Account

1. Go to https://pypi.org/ and create an account
2. Verify your email address
3. (Optional but recommended) Set up 2FA for security

### 2. Create TestPyPI Account

TestPyPI is a separate instance for testing package uploads:

1. Go to https://test.pypi.org/ and create an account
2. Verify your email address

### 3. Install Build Tools

```bash
pip install --upgrade pip
pip install --upgrade build twine
```

## Step-by-Step Publishing Process

### Step 1: Prepare Your Package

Ensure all files are ready:

```bash
cd /Users/waseemmac/Documents/traktflix/wikidata-identifier-extractor

# Verify package structure
ls -la
```

You should see:
- `wikidata_identifier_extractor/` (package directory)
- `docs/` (documentation)
- `README.md`
- `LICENSE`
- `pyproject.toml`
- `setup.py`
- `MANIFEST.in`
- `CHANGELOG.md`
- `.gitignore`

### Step 2: Update Version Number

Before each release, update the version in:

1. `pyproject.toml`:
   ```toml
   [project]
   version = "0.1.0"  # Update this
   ```

2. `wikidata_identifier_extractor/__init__.py`:
   ```python
   __version__ = "0.1.0"  # Update this
   ```

3. `CHANGELOG.md` - Add entry for new version

**Version Numbering**: Follow [Semantic Versioning](https://semver.org/)
- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Step 3: Update Your Email

Edit `pyproject.toml` and replace the email addresses:

```toml
authors = [
    {name = "Waseem", email = "your.actual.email@example.com"}
]
maintainers = [
    {name = "Waseem", email = "your.actual.email@example.com"}
]
```

### Step 4: Build the Distribution

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates two files in `dist/`:
- `wikidata_identifier_extractor-0.1.0.tar.gz` (source distribution)
- `wikidata_identifier_extractor-0.1.0-py3-none-any.whl` (wheel distribution)

### Step 5: Test with TestPyPI (Recommended)

#### Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for:
- Username: Your TestPyPI username
- Password: Your TestPyPI password (or token)

#### Test Installation from TestPyPI

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ wikidata-identifier-extractor

# Test the package
python -c "from wikidata_identifier_extractor import WikidataIdentifierExtractor; print('Success!')"

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

### Step 6: Upload to PyPI (Production)

Once you've verified everything works on TestPyPI:

```bash
python -m twine upload dist/*
```

You'll be prompted for:
- Username: Your PyPI username
- Password: Your PyPI password (or token)

### Step 7: Verify the Upload

1. Visit https://pypi.org/project/wikidata-identifier-extractor/
2. Check that the README displays correctly
3. Verify all metadata is correct

### Step 8: Test Installation from PyPI

```bash
# In a fresh environment
pip install wikidata-identifier-extractor

# Test it
python -c "from wikidata_identifier_extractor import WikidataIdentifierExtractor; print('Success!')"
```

## Using API Tokens (Recommended)

Instead of using passwords, use API tokens for better security.

### Create PyPI Token

1. Log in to https://pypi.org/
2. Go to Account Settings
3. Scroll to "API tokens"
4. Click "Add API token"
5. Name it (e.g., "wikidata-identifier-extractor-upload")
6. Scope: "Entire account" or specific project
7. Copy the token (starts with `pypi-`)

### Create TestPyPI Token

Same process at https://test.pypi.org/

### Configure .pypirc

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_ACTUAL_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

**Security**: Keep this file private!

```bash
chmod 600 ~/.pypirc
```

Now you can upload without entering credentials:

```bash
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```

## GitHub Release (Optional but Recommended)

After publishing to PyPI, create a GitHub release:

1. **Push to GitHub** (if you haven't already):
   ```bash
   cd wikidata-identifier-extractor
   git init
   git add .
   git commit -m "Initial release v0.1.0"
   git branch -M main
   git remote add origin https://github.com/wa8eem/wikidata-identifier-extractor.git
   git push -u origin main
   ```

2. **Create a tag**:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

3. **Create GitHub Release**:
   - Go to your GitHub repository
   - Click "Releases" → "Create a new release"
   - Choose the tag `v0.1.0`
   - Add release notes from `CHANGELOG.md`
   - Publish release

## Updating the Package

When releasing a new version:

1. **Make your changes**
2. **Update version numbers** in `pyproject.toml` and `__init__.py`
3. **Update `CHANGELOG.md`**
4. **Clean and rebuild**:
   ```bash
   rm -rf build/ dist/ *.egg-info
   python -m build
   ```
5. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```
6. **Create GitHub release** with the new tag

## Common Issues and Solutions

### Issue: "File already exists"

**Problem**: You're trying to upload a version that already exists on PyPI.

**Solution**: You cannot replace a version once uploaded. Increment the version number.

### Issue: "Invalid distribution"

**Problem**: Package structure or metadata is incorrect.

**Solution**: 
- Check `pyproject.toml` for syntax errors
- Ensure all required files are present
- Validate with: `python -m build --check`

### Issue: README not rendering on PyPI

**Problem**: Markdown syntax not supported or incorrect content-type.

**Solution**: 
- Use standard Markdown (not GitHub-flavored)
- Ensure `readme = "README.md"` in `pyproject.toml`

### Issue: Dependencies not installing

**Problem**: Dependencies specified incorrectly.

**Solution**: Check `dependencies` in `pyproject.toml`:
```toml
dependencies = [
    "requests>=2.25.0",
]
```

## Verification Checklist

Before publishing, verify:

- [ ] All tests pass
- [ ] Documentation is complete and accurate
- [ ] README renders correctly locally
- [ ] Version number is updated everywhere
- [ ] CHANGELOG is updated
- [ ] License file is included
- [ ] .gitignore is configured
- [ ] Email addresses are correct
- [ ] Package builds without errors
- [ ] Tested on TestPyPI first
- [ ] All files are included in MANIFEST.in

## Useful Commands

```bash
# Check package metadata
python -m build --check

# Check what will be included in the distribution
python setup.py sdist --dry-run

# Validate README
python -m readme_renderer README.md

# Check package with twine
twine check dist/*

# View package info
pip show wikidata-identifier-extractor

# Uninstall package
pip uninstall wikidata-identifier-extractor
```

## Resources

- **PyPI**: https://pypi.org/
- **TestPyPI**: https://test.pypi.org/
- **Packaging Guide**: https://packaging.python.org/
- **Twine Docs**: https://twine.readthedocs.io/
- **Semantic Versioning**: https://semver.org/

## Support

If you encounter issues:
- Check PyPI's [help documentation](https://pypi.org/help/)
- Ask on [Python Packaging Discourse](https://discuss.python.org/c/packaging/)
- Open an issue on GitHub

---

**Congratulations!** 🎉 You've successfully published your package to PyPI!

Users can now install it with:
```bash
pip install wikidata-identifier-extractor
```
