"""Economic input validation and confidence assessment module.

This module provides comprehensive validation for economic calculations,
including business logic constraints, sector validation, and confidence
level indicators.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ValidationConstraints:
    """Business logic constraints for economic inputs."""

    # Revenue constraints (in dollars)
    MIN_REVENUE = 1_000_000  # $1M
    MAX_REVENUE = 1_000_000_000_000  # $1T

    # Employee count constraints
    MIN_EMPLOYEES = 10
    MAX_EMPLOYEES = 500_000

    # AI investment constraints (percentage of revenue)
    MIN_AI_INVESTMENT_PCT = 0.1  # 0.1%
    MAX_AI_INVESTMENT_PCT = 10.0  # 10%

    # Timeline constraints (in months)
    MIN_TIMELINE_MONTHS = 6
    MAX_TIMELINE_YEARS = 10
    MAX_TIMELINE_MONTHS = MAX_TIMELINE_YEARS * 12

    # Valid sectors (based on economic models)
    VALID_SECTORS = [
        "Technology",
        "Financial Services",
        "Professional Services",
        "Healthcare",
        "Manufacturing",
        "Retail",
        "Other",
    ]

    # Company size categories
    COMPANY_SIZES = {
        "Small": {"min": 10, "max": 50},
        "Medium": {"min": 50, "max": 999},
        "Large": {"min": 1000, "max": 4999},
        "Enterprise": {"min": 5000, "max": 500000},
    }

    # ROI project types
    VALID_PROJECT_TYPES = [
        "Customer Service Automation",
        "Sales & Marketing Optimization",
        "Supply Chain Optimization",
        "Predictive Maintenance",
        "Fraud Detection",
        "Document Processing",
        "Software Development",
        "HR & Recruitment",
        "Process Automation",
        "Predictive Analytics",
        "Product Development",
        "Marketing Optimization",
    ]

    # Risk tolerance levels
    RISK_LEVELS = ["Conservative", "Moderate", "Aggressive"]

    # Adoption level constraints (percentage)
    MIN_ADOPTION_LEVEL = 0
    MAX_ADOPTION_LEVEL = 100

    # Competitive position categories
    COMPETITIVE_POSITIONS = ["Leader", "Competitive", "Follower", "Laggard"]


class EconomicValidator:
    """Validates economic inputs and provides confidence assessments."""

    def __init__(self, constraints: Optional[ValidationConstraints] = None):
        """Initialize validator with constraints."""
        self.constraints = constraints or ValidationConstraints()

    def validate_economic_inputs(
        self,
        revenue: Optional[float] = None,
        employees: Optional[int] = None,
        ai_investment: Optional[float] = None,
        timeline_months: Optional[int] = None,
        sector: Optional[str] = None,
        adoption_level: Optional[float] = None,
        company_size: Optional[str] = None,
        project_type: Optional[str] = None,
        risk_tolerance: Optional[str] = None,
        competitors_adopting_pct: Optional[float] = None,
    ) -> Tuple[bool, List[str], Dict[str, float]]:
        """Validate all economic inputs with comprehensive business logic.

        Returns:
            Tuple of (is_valid, error_messages, confidence_scores)
        """
        errors = []
        confidence_scores = {}

        # Validate revenue
        if revenue is not None:
            rev_valid, rev_errors, rev_confidence = self._validate_revenue(revenue)
            errors.extend(rev_errors)
            confidence_scores["revenue"] = rev_confidence

        # Validate employees
        if employees is not None:
            emp_valid, emp_errors, emp_confidence = self._validate_employees(employees)
            errors.extend(emp_errors)
            confidence_scores["employees"] = emp_confidence

        # Validate AI investment
        if ai_investment is not None and revenue is not None:
            inv_valid, inv_errors, inv_confidence = self._validate_ai_investment(
                ai_investment, revenue
            )
            errors.extend(inv_errors)
            confidence_scores["ai_investment"] = inv_confidence
        elif ai_investment is not None:
            errors.append("Revenue required to validate AI investment percentage")

        # Validate timeline
        if timeline_months is not None:
            time_valid, time_errors, time_confidence = self._validate_timeline(timeline_months)
            errors.extend(time_errors)
            confidence_scores["timeline"] = time_confidence

        # Validate sector
        if sector is not None:
            sect_valid, sect_errors = self._validate_sector(sector)
            errors.extend(sect_errors)
            confidence_scores["sector"] = 1.0 if sect_valid else 0.0

        # Validate adoption level
        if adoption_level is not None:
            adopt_valid, adopt_errors, adopt_confidence = self._validate_adoption_level(
                adoption_level
            )
            errors.extend(adopt_errors)
            confidence_scores["adoption_level"] = adopt_confidence

        # Validate company size
        if company_size is not None:
            size_valid, size_errors = self._validate_company_size(company_size)
            errors.extend(size_errors)
            confidence_scores["company_size"] = 1.0 if size_valid else 0.0

        # Validate project type
        if project_type is not None:
            proj_valid, proj_errors = self._validate_project_type(project_type)
            errors.extend(proj_errors)
            confidence_scores["project_type"] = 1.0 if proj_valid else 0.0

        # Cross-validation checks
        if revenue is not None and employees is not None:
            cross_valid, cross_errors = self._cross_validate_revenue_employees(revenue, employees)
            errors.extend(cross_errors)

        # Calculate overall confidence
        if confidence_scores:
            confidence_scores["overall"] = np.mean(list(confidence_scores.values()))

        return len(errors) == 0, errors, confidence_scores

    def _validate_revenue(self, revenue: float) -> Tuple[bool, List[str], float]:
        """Validate revenue with confidence scoring."""
        errors = []
        confidence = 1.0

        if revenue <= 0:
            errors.append("Revenue must be positive")
            confidence = 0.0
        elif revenue < self.constraints.MIN_REVENUE:
            errors.append(f"Revenue below minimum threshold (${self.constraints.MIN_REVENUE:,.0f})")
            confidence = 0.3
        elif revenue > self.constraints.MAX_REVENUE:
            errors.append(
                f"Revenue exceeds maximum threshold (${self.constraints.MAX_REVENUE:,.0f})"
            )
            confidence = 0.2
        else:
            # Calculate confidence based on reasonableness
            if revenue < 10_000_000:  # Small company
                confidence = 0.8
            elif revenue < 100_000_000:  # Medium company
                confidence = 0.9
            elif revenue < 1_000_000_000:  # Large company
                confidence = 0.95
            else:  # Very large company
                confidence = 0.85

        return len(errors) == 0, errors, confidence

    def _validate_employees(self, employees: int) -> Tuple[bool, List[str], float]:
        """Validate employee count with confidence scoring."""
        errors = []
        confidence = 1.0

        if employees < self.constraints.MIN_EMPLOYEES:
            errors.append(f"Employee count below minimum ({self.constraints.MIN_EMPLOYEES})")
            confidence = 0.3
        elif employees > self.constraints.MAX_EMPLOYEES:
            errors.append(f"Employee count exceeds maximum ({self.constraints.MAX_EMPLOYEES:,})")
            confidence = 0.2
        else:
            # Confidence based on typical ranges
            if 50 <= employees <= 10000:
                confidence = 0.95
            else:
                confidence = 0.85

        return len(errors) == 0, errors, confidence

    def _validate_ai_investment(
        self, ai_investment: float, revenue: float
    ) -> Tuple[bool, List[str], float]:
        """Validate AI investment as percentage of revenue."""
        errors = []
        confidence = 1.0

        if ai_investment < 0:
            errors.append("AI investment cannot be negative")
            confidence = 0.0
        elif revenue > 0:
            investment_pct = (ai_investment / revenue) * 100

            if investment_pct < self.constraints.MIN_AI_INVESTMENT_PCT:
                errors.append(
                    f"AI investment too low ({investment_pct:.2f}% of revenue, "
                    f"minimum {self.constraints.MIN_AI_INVESTMENT_PCT}%)"
                )
                confidence = 0.5
            elif investment_pct > self.constraints.MAX_AI_INVESTMENT_PCT:
                errors.append(
                    f"AI investment too high ({investment_pct:.2f}% of revenue, "
                    f"maximum {self.constraints.MAX_AI_INVESTMENT_PCT}%)"
                )
                confidence = 0.4
            else:
                # Optimal range is 1-5% of revenue
                if 1.0 <= investment_pct <= 5.0:
                    confidence = 0.95
                else:
                    confidence = 0.85

        return len(errors) == 0, errors, confidence

    def _validate_timeline(self, timeline_months: int) -> Tuple[bool, List[str], float]:
        """Validate implementation timeline."""
        errors = []
        confidence = 1.0

        if timeline_months < self.constraints.MIN_TIMELINE_MONTHS:
            errors.append(
                f"Timeline too short (minimum {self.constraints.MIN_TIMELINE_MONTHS} months)"
            )
            confidence = 0.3
        elif timeline_months > self.constraints.MAX_TIMELINE_MONTHS:
            errors.append(
                f"Timeline too long (maximum {self.constraints.MAX_TIMELINE_YEARS} years)"
            )
            confidence = 0.4
        else:
            # Optimal timeline is 12-36 months
            if 12 <= timeline_months <= 36:
                confidence = 0.95
            else:
                confidence = 0.85

        return len(errors) == 0, errors, confidence

    def _validate_sector(self, sector: str) -> Tuple[bool, List[str]]:
        """Validate industry sector."""
        errors = []

        if sector not in self.constraints.VALID_SECTORS:
            errors.append(
                f"Invalid sector '{sector}'. Valid options: "
                f"{', '.join(self.constraints.VALID_SECTORS)}"
            )

        return len(errors) == 0, errors

    def _validate_adoption_level(self, adoption_level: float) -> Tuple[bool, List[str], float]:
        """Validate AI adoption level percentage."""
        errors = []
        confidence = 1.0

        if adoption_level < self.constraints.MIN_ADOPTION_LEVEL:
            errors.append("Adoption level cannot be negative")
            confidence = 0.0
        elif adoption_level > self.constraints.MAX_ADOPTION_LEVEL:
            errors.append("Adoption level cannot exceed 100%")
            confidence = 0.0
        else:
            # Most companies are between 10-60% adoption
            if 10 <= adoption_level <= 60:
                confidence = 0.95
            else:
                confidence = 0.85

        return len(errors) == 0, errors, confidence

    def _validate_company_size(self, company_size: str) -> Tuple[bool, List[str]]:
        """Validate company size category."""
        errors = []

        if company_size not in self.constraints.COMPANY_SIZES:
            errors.append(
                f"Invalid company size '{company_size}'. Valid options: "
                f"{', '.join(self.constraints.COMPANY_SIZES.keys())}"
            )

        return len(errors) == 0, errors

    def _validate_project_type(self, project_type: str) -> Tuple[bool, List[str]]:
        """Validate AI project type."""
        errors = []

        if project_type not in self.constraints.VALID_PROJECT_TYPES:
            errors.append(
                f"Invalid project type '{project_type}'. Valid options: "
                f"{', '.join(self.constraints.VALID_PROJECT_TYPES)}"
            )

        return len(errors) == 0, errors

    def _cross_validate_revenue_employees(
        self, revenue: float, employees: int
    ) -> Tuple[bool, List[str]]:
        """Cross-validate revenue against employee count."""
        errors = []

        # Calculate revenue per employee
        revenue_per_employee = revenue / employees if employees > 0 else 0

        # Industry reasonable ranges
        min_revenue_per_employee = 50_000  # $50K
        max_revenue_per_employee = 5_000_000  # $5M

        if revenue_per_employee < min_revenue_per_employee:
            errors.append(
                f"Revenue per employee (${revenue_per_employee:,.0f}) seems too low. "
                f"Typical range: ${min_revenue_per_employee:,} - ${max_revenue_per_employee:,}"
            )
        elif revenue_per_employee > max_revenue_per_employee:
            errors.append(
                f"Revenue per employee (${revenue_per_employee:,.0f}) seems too high. "
                f"Typical range: ${min_revenue_per_employee:,} - ${max_revenue_per_employee:,}"
            )

        return len(errors) == 0, errors

    def suggest_valid_ranges(self, field: str) -> Dict[str, Union[str, float, List[str]]]:
        """Suggest valid ranges for a given field."""
        suggestions = {
            "revenue": {
                "min": f"${self.constraints.MIN_REVENUE:,.0f}",
                "max": f"${self.constraints.MAX_REVENUE:,.0f}",
                "typical": "$10M - $1B",
                "description": "Annual company revenue",
            },
            "employees": {
                "min": self.constraints.MIN_EMPLOYEES,
                "max": f"{self.constraints.MAX_EMPLOYEES:,}",
                "typical": "50 - 10,000",
                "description": "Total number of employees",
            },
            "ai_investment": {
                "min": f"{self.constraints.MIN_AI_INVESTMENT_PCT}% of revenue",
                "max": f"{self.constraints.MAX_AI_INVESTMENT_PCT}% of revenue",
                "typical": "1-5% of revenue",
                "description": "Annual AI investment budget",
            },
            "timeline": {
                "min": f"{self.constraints.MIN_TIMELINE_MONTHS} months",
                "max": f"{self.constraints.MAX_TIMELINE_YEARS} years",
                "typical": "12-36 months",
                "description": "AI implementation timeline",
            },
            "sectors": {
                "valid_options": self.constraints.VALID_SECTORS,
                "description": "Industry sectors with AI adoption data",
            },
            "adoption_level": {
                "min": f"{self.constraints.MIN_ADOPTION_LEVEL}%",
                "max": f"{self.constraints.MAX_ADOPTION_LEVEL}%",
                "typical": "10-60%",
                "description": "Current AI adoption percentage",
            },
            "company_sizes": {
                "valid_options": list(self.constraints.COMPANY_SIZES.keys()),
                "ranges": self.constraints.COMPANY_SIZES,
                "description": "Company size by employee count",
            },
            "project_types": {
                "valid_options": self.constraints.VALID_PROJECT_TYPES,
                "description": "Types of AI projects",
            },
        }

        return suggestions.get(field, {})

    def get_confidence_interpretation(self, confidence_score: float) -> Dict[str, str]:
        """Interpret confidence score into human-readable format."""
        if confidence_score >= 0.95:
            return {
                "level": "Very High",
                "color": "green",
                "icon": "✅",
                "description": "Inputs are highly reliable and within typical ranges",
            }
        elif confidence_score >= 0.85:
            return {
                "level": "High",
                "color": "lightgreen",
                "icon": "✓",
                "description": "Inputs are reliable with minor variations from typical",
            }
        elif confidence_score >= 0.70:
            return {
                "level": "Moderate",
                "color": "yellow",
                "icon": "⚠️",
                "description": "Inputs have some unusual values that may affect accuracy",
            }
        elif confidence_score >= 0.50:
            return {
                "level": "Low",
                "color": "orange",
                "icon": "⚠️",
                "description": "Inputs contain significant anomalies - verify data",
            }
        else:
            return {
                "level": "Very Low",
                "color": "red",
                "icon": "❌",
                "description": "Inputs have major issues - results may be unreliable",
            }

    def format_validation_errors(self, errors: List[str]) -> str:
        """Format validation errors for display."""
        if not errors:
            return "✅ All inputs validated successfully"

        formatted = "**Validation Issues:**\n"
        for error in errors:
            formatted += f"• ❌ {error}\n"

        return formatted

    def log_validation_attempt(
        self,
        inputs: Dict[str, any],
        is_valid: bool,
        errors: List[str],
        confidence_scores: Dict[str, float],
    ):
        """Log validation attempts for monitoring."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "inputs": inputs,
            "is_valid": is_valid,
            "error_count": len(errors),
            "errors": errors,
            "confidence_scores": confidence_scores,
        }

        if is_valid:
            logger.info(f"Validation successful: {log_entry}")
        else:
            logger.warning(f"Validation failed: {log_entry}")

        return log_entry
