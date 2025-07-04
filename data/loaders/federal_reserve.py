"""Federal Reserve Banks data loaders for AI economic impact studies."""

# Import the real implementations
from .federal_reserve_real import RichmondFedLoader, StLouisFedLoader

__all__ = ['RichmondFedLoader', 'StLouisFedLoader']