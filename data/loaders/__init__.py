"""Data loaders for the Economics of AI Dashboard."""

from .academic import AcademicPapersLoader, IMFLoader
from .ai_index import AIIndexLoader
from .base import BaseDataLoader, DataSource
from .federal_reserve import RichmondFedLoader, StLouisFedLoader
from .goldman_sachs import GoldmanSachsLoader
from .mckinsey import McKinseyLoader
from .nvidia import NVIDIATokenLoader
from .oecd import OECDLoader

__all__ = [
    "BaseDataLoader",
    "DataSource",
    "AIIndexLoader",
    "McKinseyLoader",
    "OECDLoader",
    "RichmondFedLoader",
    "StLouisFedLoader",
    "GoldmanSachsLoader",
    "NVIDIATokenLoader",
    "IMFLoader",
    "AcademicPapersLoader",
]
