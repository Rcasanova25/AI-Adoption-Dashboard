"""Data loaders for the Economics of AI Dashboard."""

from .base import BaseDataLoader, DataSource
from .ai_index import AIIndexLoader
from .mckinsey import McKinseyLoader
from .oecd import OECDLoader
from .federal_reserve import RichmondFedLoader, StLouisFedLoader
from .goldman_sachs import GoldmanSachsLoader
from .nvidia import NVIDIATokenLoader
from .academic import IMFLoader, AcademicPapersLoader

__all__ = [
    'BaseDataLoader',
    'DataSource',
    'AIIndexLoader',
    'McKinseyLoader', 
    'OECDLoader',
    'RichmondFedLoader',
    'StLouisFedLoader',
    'GoldmanSachsLoader',
    'NVIDIATokenLoader',
    'IMFLoader',
    'AcademicPapersLoader'
]