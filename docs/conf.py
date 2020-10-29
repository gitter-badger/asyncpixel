"""Sphinx configuration."""
from datetime import datetime


project = "asyncpixel"
author = "Leon Bowie"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.asyncio",
    # "sphinx-autodoc-typehints",
]

intersphinx_mapping = {
    "python": ("http://docs.python.org/3", None),
    "aiohttp": ("https://aiohttp.readthedocs.io/en/latest/", None),
}
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
