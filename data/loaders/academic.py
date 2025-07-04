"""Academic and IMF research papers data loader."""

# Import the real implementations
from .imf_real import IMFLoader
from .academic_real import AcademicPapersLoader

__all__ = ['IMFLoader', 'AcademicPapersLoader']