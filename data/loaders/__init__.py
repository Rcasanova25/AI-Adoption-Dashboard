"""Data loaders for the Economics of AI Dashboard."""

from .base import BaseDataLoader, DataSource
from .ai_index import AIIndexLoader
from .mckinsey import McKinseyLoader
from .oecd import OECDLoader
from .federal_reserve import FederalReserveLoader

__all__ = [
    'BaseDataLoader',
    'DataSource',
    'AIIndexLoader',
    'McKinseyLoader', 
    'OECDLoader',
    'FederalReserveLoader'
]