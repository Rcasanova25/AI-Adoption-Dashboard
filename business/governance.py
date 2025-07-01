"""
AI Governance Framework for AI Adoption Dashboard
Provides comprehensive governance, compliance, and ethical AI management capabilities
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class GovernanceLevel(Enum):
    BOARD = "Board Level"
    EXECUTIVE = "Executive Level" 
    OPERATIONAL = "Operational Level"
    TECHNICAL = "Technical Level"

class ComplianceFramework(Enum):
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    SOX = "Sarbanes-Oxley"
    ISO27001 = "ISO 27001"
    NIST = "NIST AI Framework"
    EU_AI_ACT = "EU AI Act"

class AIRiskLevel(Enum):
    MINIMAL = "Minimal Risk"
    LIMITED = "Limited Risk"
    HIGH = "High Risk"
    UNACCEPTABLE = "Unacceptable Risk"

@dataclass
class GovernancePolicy:
    """AI governance policy definition"""
    policy_id: str
    name: str
    description: str
    governance_level: GovernanceLevel
    compliance_frameworks: List[ComplianceFramework]
    risk_level: AIRiskLevel
    requirements: List[str]
    monitoring_metrics: List[str]
    review_frequency: str
    responsible_roles: List[str]
    enforcement_mechanisms: List[str]

@dataclass
class ComplianceAssessment:
    """Compliance assessment results"""
    framework: ComplianceFramework
    overall_score: float
    compliant_controls: List[str]
    non_compliant_controls: List[str]
    risk_areas: List[str]
    remediation_plan: List[str]
    assessment_date: datetime
    next_review_date: datetime

@dataclass
class GovernanceFramework:
    """Complete AI governance framework"""
    organization_profile: Dict[str, str]
    governance_policies: List[GovernancePolicy]
    compliance_assessments: List[ComplianceAssessment]
    risk_register: List[Dict[str, Any]]
    governance_maturity_score: float
    recommendations: List[str]
    implementation_roadmap: List[Dict[str, str]]

class AIGovernanceEngine:
    """Comprehensive AI governance and compliance management engine"""
    
    def __init__(self):
        self.governance_templates = self._load_governance_templates()
        self.compliance_standards = self._load_compliance_standards()
        self.best_practices = self._load_governance_best_practices()
    
    def create_governance_framework(
        self,
        industry: str,
        company_size: str,
        ai_maturity_level: str,
        regulatory_requirements: List[str],
        geographic_scope: List[str],
        ai_use_cases: List[str]
    ) -> GovernanceFramework:
        """
        Create comprehensive AI governance framework tailored to organization
        """
        
        # Create organization profile
        org_profile = {
            'industry': industry,
            'company_size': company_size,
            'ai_maturity_level': ai_maturity_level,
            'regulatory_scope': ', '.join(regulatory_requirements),
            'geographic_scope': ', '.join(geographic_scope),
            'primary_use_cases': ', '.join(ai_use_cases)
        }
        
        # Generate governance policies
        governance_policies = self._generate_governance_policies(
            industry, company_size, ai_maturity_level, regulatory_requirements, ai_use_cases
        )
        
        # Perform compliance assessments
        compliance_assessments = self._perform_compliance_assessments(
            regulatory_requirements, industry, ai_use_cases
        )
        
        # Create risk register
        risk_register = self._create_ai_risk_register(
            industry, ai_use_cases, regulatory_requirements
        )
        
        # Calculate governance maturity score
        maturity_score = self._calculate_governance_maturity(
            governance_policies, compliance_assessments, ai_maturity_level
        )
        
        # Generate recommendations
        recommendations = self._generate_governance_recommendations(
            maturity_score, compliance_assessments, industry
        )
        
        # Create implementation roadmap
        implementation_roadmap = self._create_implementation_roadmap(
            governance_policies, maturity_score, company_size
        )
        
        return GovernanceFramework(
            organization_profile=org_profile,
            governance_policies=governance_policies,
            compliance_assessments=compliance_assessments,
            risk_register=risk_register,
            governance_maturity_score=maturity_score,
            recommendations=recommendations,
            implementation_roadmap=implementation_roadmap
        )
    
    def assess_ai_ethics_compliance(
        self,
        ai_system_description: str,
        data_types: List[str],
        decision_impact: str,
        stakeholder_groups: List[str]
    ) -> Dict[str, Any]:
        """
        Assess AI system for ethics and fairness compliance
        """
        
        ethics_assessment = {
            'fairness_score': 0,
            'transparency_score': 0,
            'accountability_score': 0,
            'privacy_score': 0,
            'safety_score': 0,
            'overall_ethics_score': 0,
            'identified_risks': [],
            'mitigation_strategies': [],
            'monitoring_requirements': []
        }
        
        # Assess fairness
        fairness_score = self._assess_fairness(ai_system_description, stakeholder_groups)
        ethics_assessment['fairness_score'] = fairness_score
        
        # Assess transparency
        transparency_score = self._assess_transparency(ai_system_description, decision_impact)
        ethics_assessment['transparency_score'] = transparency_score
        
        # Assess accountability
        accountability_score = self._assess_accountability(ai_system_description, decision_impact)
        ethics_assessment['accountability_score'] = accountability_score
        
        # Assess privacy
        privacy_score = self._assess_privacy(data_types, stakeholder_groups)
        ethics_assessment['privacy_score'] = privacy_score
        
        # Assess safety
        safety_score = self._assess_safety(ai_system_description, decision_impact)
        ethics_assessment['safety_score'] = safety_score
        
        # Calculate overall score
        scores = [fairness_score, transparency_score, accountability_score, privacy_score, safety_score]
        ethics_assessment['overall_ethics_score'] = sum(scores) / len(scores)
        
        # Identify risks and mitigation strategies
        if ethics_assessment['overall_ethics_score'] < 7.0:
            ethics_assessment['identified_risks'] = self._identify_ethics_risks(scores)
            ethics_assessment['mitigation_strategies'] = self._generate_ethics_mitigations(scores)
        
        # Define monitoring requirements
        ethics_assessment['monitoring_requirements'] = self._define_ethics_monitoring(
            ethics_assessment['overall_ethics_score'], decision_impact
        )
        
        return ethics_assessment
    
    def _generate_governance_policies(
        self,
        industry: str,
        company_size: str,
        ai_maturity_level: str,
        regulatory_requirements: List[str],
        ai_use_cases: List[str]
    ) -> List[GovernancePolicy]:
        """Generate industry and risk-specific governance policies"""
        
        policies = []
        
        # Core governance policies (required for all organizations)
        core_policies = [
            GovernancePolicy(
                policy_id="GOV-001",
                name="AI Strategy and Oversight",
                description="Board-level AI strategy oversight and governance structure",
                governance_level=GovernanceLevel.BOARD,
                compliance_frameworks=[ComplianceFramework.NIST],
                risk_level=AIRiskLevel.HIGH,
                requirements=[
                    "Establish AI governance committee",
                    "Define AI strategy and objectives",
                    "Approve high-risk AI initiatives",
                    "Review AI performance quarterly"
                ],
                monitoring_metrics=["AI ROI", "Risk incidents", "Compliance violations"],
                review_frequency="Quarterly",
                responsible_roles=["Board of Directors", "Chief AI Officer", "Chief Risk Officer"],
                enforcement_mechanisms=["Board resolutions", "Executive compensation", "Audit findings"]
            ),
            
            GovernancePolicy(
                policy_id="GOV-002",
                name="AI Risk Management",
                description="Comprehensive AI risk identification, assessment, and mitigation",
                governance_level=GovernanceLevel.EXECUTIVE,
                compliance_frameworks=[ComplianceFramework.NIST, ComplianceFramework.ISO27001],
                risk_level=AIRiskLevel.HIGH,
                requirements=[
                    "Conduct AI risk assessments",
                    "Implement risk mitigation controls",
                    "Monitor risk indicators",
                    "Report risk incidents"
                ],
                monitoring_metrics=["Risk assessment scores", "Mitigation effectiveness", "Incident frequency"],
                review_frequency="Monthly",
                responsible_roles=["Chief Risk Officer", "AI Risk Manager", "Business Unit Heads"],
                enforcement_mechanisms=["Risk reporting", "Escalation procedures", "Corrective actions"]
            ),
            
            GovernancePolicy(
                policy_id="GOV-003",
                name="AI Ethics and Fairness",
                description="Ensure AI systems are ethical, fair, and non-discriminatory",
                governance_level=GovernanceLevel.TECHNICAL,
                compliance_frameworks=[ComplianceFramework.EU_AI_ACT],
                risk_level=AIRiskLevel.HIGH,
                requirements=[
                    "Implement bias detection and mitigation",
                    "Ensure algorithmic transparency",
                    "Conduct fairness assessments",
                    "Establish ethics review board"
                ],
                monitoring_metrics=["Bias metrics", "Fairness scores", "Ethics violations"],
                review_frequency="Continuous",
                responsible_roles=["AI Ethics Officer", "Data Scientists", "Legal Counsel"],
                enforcement_mechanisms=["Model approval gates", "Ethics reviews", "Audit trails"]
            )
        ]
        
        policies.extend(core_policies)
        
        # Industry-specific policies
        if industry == "Healthcare":
            policies.append(GovernancePolicy(
                policy_id="GOV-H01",
                name="Clinical AI Governance",
                description="Governance for AI systems in clinical decision-making",
                governance_level=GovernanceLevel.OPERATIONAL,
                compliance_frameworks=[ComplianceFramework.HIPAA],
                risk_level=AIRiskLevel.HIGH,
                requirements=[
                    "Clinical validation of AI systems",
                    "Healthcare professional oversight",
                    "Patient consent management",
                    "Clinical audit trails"
                ],
                monitoring_metrics=["Clinical accuracy", "Patient outcomes", "Provider adoption"],
                review_frequency="Monthly",
                responsible_roles=["Chief Medical Officer", "Clinical AI Committee"],
                enforcement_mechanisms=["Clinical protocols", "Quality assurance", "Regulatory compliance"]
            ))
        
        elif industry == "Financial Services":
            policies.append(GovernancePolicy(
                policy_id="GOV-F01",
                name="Financial AI Model Risk Management",
                description="Model risk management for AI in financial services",
                governance_level=GovernanceLevel.EXECUTIVE,
                compliance_frameworks=[ComplianceFramework.SOX],
                risk_level=AIRiskLevel.HIGH,
                requirements=[
                    "Model validation and testing",
                    "Regulatory approval processes",
                    "Model performance monitoring",
                    "Stress testing requirements"
                ],
                monitoring_metrics=["Model accuracy", "Regulatory compliance", "Financial impact"],
                review_frequency="Monthly",
                responsible_roles=["Chief Risk Officer", "Model Risk Committee"],
                enforcement_mechanisms=["Regulatory reporting", "Model approval", "Internal audit"]
            ))
        
        # Add data protection policies if handling personal data
        if any("personal" in use_case.lower() or "customer" in use_case.lower() for use_case in ai_use_cases):
            policies.append(GovernancePolicy(
                policy_id="GOV-004",
                name="AI Data Protection and Privacy",
                description="Protect personal data in AI systems and ensure privacy compliance",
                governance_level=GovernanceLevel.OPERATIONAL,
                compliance_frameworks=[ComplianceFramework.GDPR],
                risk_level=AIRiskLevel.HIGH,
                requirements=[
                    "Data minimization principles",
                    "Purpose limitation compliance",
                    "Data subject rights implementation",
                    "Privacy impact assessments"
                ],
                monitoring_metrics=["Data usage compliance", "Privacy incidents", "Data subject requests"],
                review_frequency="Monthly",
                responsible_roles=["Data Protection Officer", "Privacy Team"],
                enforcement_mechanisms=["Privacy audits", "Consent management", "Data deletion"]
            ))
        
        return policies
    
    def _perform_compliance_assessments(
        self,
        regulatory_requirements: List[str],
        industry: str,
        ai_use_cases: List[str]
    ) -> List[ComplianceAssessment]:
        """Perform compliance assessments for relevant frameworks"""
        
        assessments = []
        
        # Map regulatory requirements to frameworks
        framework_mapping = {
            "GDPR": ComplianceFramework.GDPR,
            "HIPAA": ComplianceFramework.HIPAA,
            "SOX": ComplianceFramework.SOX,
            "ISO 27001": ComplianceFramework.ISO27001,
            "NIST": ComplianceFramework.NIST,
            "EU AI Act": ComplianceFramework.EU_AI_ACT
        }
        
        for req in regulatory_requirements:
            framework = framework_mapping.get(req)
            if framework:
                assessment = self._assess_framework_compliance(framework, industry, ai_use_cases)
                assessments.append(assessment)
        
        # Always include NIST AI Framework assessment
        if ComplianceFramework.NIST not in [a.framework for a in assessments]:
            nist_assessment = self._assess_framework_compliance(
                ComplianceFramework.NIST, industry, ai_use_cases
            )
            assessments.append(nist_assessment)
        
        return assessments
    
    def _assess_framework_compliance(
        self,
        framework: ComplianceFramework,
        industry: str,
        ai_use_cases: List[str]
    ) -> ComplianceAssessment:
        """Assess compliance with specific framework"""
        
        # Framework-specific control assessments
        if framework == ComplianceFramework.NIST:
            return self._assess_nist_compliance(industry, ai_use_cases)
        elif framework == ComplianceFramework.GDPR:
            return self._assess_gdpr_compliance(industry, ai_use_cases)
        elif framework == ComplianceFramework.EU_AI_ACT:
            return self._assess_eu_ai_act_compliance(industry, ai_use_cases)
        else:
            # Generic assessment
            return ComplianceAssessment(
                framework=framework,
                overall_score=7.5,
                compliant_controls=["Basic governance", "Risk management"],
                non_compliant_controls=["Advanced monitoring", "Continuous assessment"],
                risk_areas=["Regulatory changes", "Technical complexity"],
                remediation_plan=["Implement monitoring", "Update policies"],
                assessment_date=datetime.now(),
                next_review_date=datetime.now() + timedelta(days=90)
            )
    
    def _assess_nist_compliance(self, industry: str, ai_use_cases: List[str]) -> ComplianceAssessment:
        """Assess NIST AI Framework compliance"""
        
        # NIST AI Framework core functions assessment
        compliant_controls = [
            "AI system documentation",
            "Risk identification",
            "Stakeholder engagement",
            "AI system testing"
        ]
        
        non_compliant_controls = [
            "Continuous monitoring",
            "Bias assessment",
            "Explainability measures",
            "Third-party risk management"
        ]
        
        # Calculate score based on compliant vs non-compliant
        total_controls = len(compliant_controls) + len(non_compliant_controls)
        score = (len(compliant_controls) / total_controls) * 10
        
        return ComplianceAssessment(
            framework=ComplianceFramework.NIST,
            overall_score=score,
            compliant_controls=compliant_controls,
            non_compliant_controls=non_compliant_controls,
            risk_areas=["Model drift", "Data quality", "Algorithmic bias"],
            remediation_plan=[
                "Implement continuous monitoring system",
                "Develop bias detection capabilities",
                "Enhance model explainability"
            ],
            assessment_date=datetime.now(),
            next_review_date=datetime.now() + timedelta(days=90)
        )
    
    def _assess_gdpr_compliance(self, industry: str, ai_use_cases: List[str]) -> ComplianceAssessment:
        """Assess GDPR compliance for AI systems"""
        
        compliant_controls = [
            "Data processing lawful basis",
            "Privacy notice provisions",
            "Data subject consent",
            "Data retention policies"
        ]
        
        non_compliant_controls = [
            "Automated decision-making safeguards",
            "Data portability for AI models",
            "Right to explanation implementation",
            "Privacy by design in AI"
        ]
        
        score = 6.5  # GDPR compliance is typically challenging for AI
        
        return ComplianceAssessment(
            framework=ComplianceFramework.GDPR,
            overall_score=score,
            compliant_controls=compliant_controls,
            non_compliant_controls=non_compliant_controls,
            risk_areas=["Automated decision-making", "Data subject rights", "Cross-border transfers"],
            remediation_plan=[
                "Implement right to explanation",
                "Enhance automated decision-making controls",
                "Develop data portability for AI systems"
            ],
            assessment_date=datetime.now(),
            next_review_date=datetime.now() + timedelta(days=60)
        )
    
    def _assess_eu_ai_act_compliance(self, industry: str, ai_use_cases: List[str]) -> ComplianceAssessment:
        """Assess EU AI Act compliance"""
        
        # Determine risk level based on use cases
        high_risk_indicators = ["hiring", "credit", "healthcare", "education", "law enforcement"]
        is_high_risk = any(indicator in ' '.join(ai_use_cases).lower() for indicator in high_risk_indicators)
        
        if is_high_risk:
            compliant_controls = [
                "Risk management system",
                "Data governance measures",
                "Technical documentation"
            ]
            
            non_compliant_controls = [
                "Conformity assessment",
                "CE marking process",
                "Post-market monitoring",
                "Fundamental rights impact assessment"
            ]
            score = 5.5
        else:
            compliant_controls = [
                "Transparency obligations",
                "Basic risk measures",
                "User information"
            ]
            non_compliant_controls = [
                "Enhanced transparency",
                "User training requirements"
            ]
            score = 8.0
        
        return ComplianceAssessment(
            framework=ComplianceFramework.EU_AI_ACT,
            overall_score=score,
            compliant_controls=compliant_controls,
            non_compliant_controls=non_compliant_controls,
            risk_areas=["High-risk AI classification", "Regulatory uncertainty"],
            remediation_plan=[
                "Conduct conformity assessment",
                "Implement post-market monitoring",
                "Prepare for regulatory updates"
            ],
            assessment_date=datetime.now(),
            next_review_date=datetime.now() + timedelta(days=180)
        )
    
    def _create_ai_risk_register(
        self,
        industry: str,
        ai_use_cases: List[str],
        regulatory_requirements: List[str]
    ) -> List[Dict[str, Any]]:
        """Create comprehensive AI risk register"""
        
        risk_register = [
            {
                'risk_id': 'AI-001',
                'risk_name': 'Algorithmic Bias',
                'description': 'AI models may exhibit unfair bias leading to discriminatory outcomes',
                'category': 'Ethical',
                'probability': 'Medium',
                'impact': 'High',
                'risk_level': 'High',
                'mitigation_strategies': [
                    'Implement bias detection tools',
                    'Diverse training datasets',
                    'Regular fairness audits'
                ],
                'monitoring_indicators': ['Fairness metrics', 'Outcome disparities', 'Complaint rates'],
                'responsible_party': 'AI Ethics Officer',
                'status': 'Active'
            },
            {
                'risk_id': 'AI-002',
                'risk_name': 'Model Drift',
                'description': 'AI model performance degrades over time due to data or environment changes',
                'category': 'Technical',
                'probability': 'High',
                'impact': 'Medium',
                'risk_level': 'Medium',
                'mitigation_strategies': [
                    'Continuous monitoring systems',
                    'Automated retraining pipelines',
                    'Performance threshold alerts'
                ],
                'monitoring_indicators': ['Model accuracy', 'Prediction variance', 'Data drift metrics'],
                'responsible_party': 'ML Engineering Team',
                'status': 'Active'
            },
            {
                'risk_id': 'AI-003',
                'risk_name': 'Data Privacy Violations',
                'description': 'AI systems may process personal data in violation of privacy regulations',
                'category': 'Regulatory',
                'probability': 'Medium',
                'impact': 'High',
                'risk_level': 'High',
                'mitigation_strategies': [
                    'Privacy impact assessments',
                    'Data minimization techniques',
                    'Privacy-preserving AI methods'
                ],
                'monitoring_indicators': ['Privacy incidents', 'Data usage compliance', 'Regulatory audits'],
                'responsible_party': 'Data Protection Officer',
                'status': 'Active'
            }
        ]
        
        # Add industry-specific risks
        if industry == "Healthcare":
            risk_register.append({
                'risk_id': 'AI-H01',
                'risk_name': 'Clinical Decision Support Errors',
                'description': 'AI recommendations may lead to incorrect clinical decisions',
                'category': 'Safety',
                'probability': 'Low',
                'impact': 'Critical',
                'risk_level': 'High',
                'mitigation_strategies': [
                    'Clinical validation studies',
                    'Healthcare professional oversight',
                    'Continuous monitoring of outcomes'
                ],
                'monitoring_indicators': ['Clinical accuracy', 'Patient outcomes', 'Provider feedback'],
                'responsible_party': 'Chief Medical Officer',
                'status': 'Active'
            })
        
        return risk_register
    
    def _calculate_governance_maturity(
        self,
        policies: List[GovernancePolicy],
        assessments: List[ComplianceAssessment],
        ai_maturity_level: str
    ) -> float:
        """Calculate governance maturity score"""
        
        # Base score from policies (40% weight)
        policy_score = min(len(policies) / 5.0, 1.0) * 4.0  # Max 4 points
        
        # Compliance scores (40% weight)
        if assessments:
            avg_compliance = sum(a.overall_score for a in assessments) / len(assessments)
            compliance_score = (avg_compliance / 10.0) * 4.0  # Max 4 points
        else:
            compliance_score = 2.0  # Default if no assessments
        
        # AI maturity adjustment (20% weight)
        maturity_scores = {
            "Exploring (0-10%)": 0.5,
            "Piloting (10-25%)": 1.0,
            "Implementing (25-50%)": 1.5,
            "Scaling (50-80%)": 1.8,
            "Leading (80%+)": 2.0
        }
        maturity_score = maturity_scores.get(ai_maturity_level, 1.0)
        
        total_score = policy_score + compliance_score + maturity_score
        return min(total_score, 10.0)  # Cap at 10
    
    def _generate_governance_recommendations(
        self,
        maturity_score: float,
        assessments: List[ComplianceAssessment],
        industry: str
    ) -> List[str]:
        """Generate governance improvement recommendations"""
        
        recommendations = []
        
        if maturity_score < 6.0:
            recommendations.extend([
                "Establish formal AI governance committee",
                "Develop comprehensive AI policies and procedures",
                "Implement basic risk management processes",
                "Conduct governance maturity assessment"
            ])
        elif maturity_score < 8.0:
            recommendations.extend([
                "Enhance continuous monitoring capabilities",
                "Implement advanced compliance frameworks",
                "Develop specialized governance roles",
                "Create governance metrics dashboard"
            ])
        else:
            recommendations.extend([
                "Achieve governance excellence through automation",
                "Lead industry best practices development",
                "Implement predictive governance analytics",
                "Share governance expertise externally"
            ])
        
        # Add compliance-specific recommendations
        for assessment in assessments:
            if assessment.overall_score < 7.0:
                recommendations.extend(assessment.remediation_plan[:2])
        
        return recommendations[:8]  # Limit to top 8 recommendations
    
    def _create_implementation_roadmap(
        self,
        policies: List[GovernancePolicy],
        maturity_score: float,
        company_size: str
    ) -> List[Dict[str, str]]:
        """Create governance implementation roadmap"""
        
        roadmap = []
        
        # Phase 1: Foundation (0-3 months)
        roadmap.append({
            'phase': 'Phase 1: Foundation',
            'timeline': '0-3 months',
            'objectives': 'Establish basic governance structure',
            'deliverables': 'Governance committee, core policies, risk register',
            'success_criteria': 'Governance framework approved by board'
        })
        
        # Phase 2: Implementation (3-9 months)
        roadmap.append({
            'phase': 'Phase 2: Implementation',
            'timeline': '3-9 months',
            'objectives': 'Deploy governance processes and controls',
            'deliverables': 'Policy implementation, training programs, monitoring systems',
            'success_criteria': 'All policies implemented and operational'
        })
        
        # Phase 3: Optimization (9-18 months)
        roadmap.append({
            'phase': 'Phase 3: Optimization',
            'timeline': '9-18 months',
            'objectives': 'Optimize and mature governance capabilities',
            'deliverables': 'Advanced analytics, automation, continuous improvement',
            'success_criteria': 'Governance maturity score >8.0'
        })
        
        return roadmap
    
    def _assess_fairness(self, ai_system: str, stakeholders: List[str]) -> float:
        """Assess AI system fairness"""
        # Simplified assessment - would be more sophisticated in practice
        base_score = 7.0
        
        # Adjust based on stakeholder diversity
        if len(stakeholders) > 3:
            base_score += 1.0
        
        # Adjust based on system complexity
        if "decision" in ai_system.lower():
            base_score -= 0.5
        
        return min(base_score, 10.0)
    
    def _assess_transparency(self, ai_system: str, decision_impact: str) -> float:
        """Assess AI system transparency"""
        base_score = 6.5
        
        if "high" in decision_impact.lower():
            base_score -= 1.0
        
        if "explainable" in ai_system.lower():
            base_score += 1.5
        
        return min(base_score, 10.0)
    
    def _assess_accountability(self, ai_system: str, decision_impact: str) -> float:
        """Assess AI system accountability"""
        base_score = 7.5
        
        if "automated" in ai_system.lower() and "high" in decision_impact.lower():
            base_score -= 1.0
        
        return min(base_score, 10.0)
    
    def _assess_privacy(self, data_types: List[str], stakeholders: List[str]) -> float:
        """Assess privacy compliance"""
        base_score = 8.0
        
        sensitive_data = ["personal", "health", "financial", "biometric"]
        if any(sensitive in ' '.join(data_types).lower() for sensitive in sensitive_data):
            base_score -= 1.5
        
        return max(base_score, 5.0)
    
    def _assess_safety(self, ai_system: str, decision_impact: str) -> float:
        """Assess AI system safety"""
        base_score = 8.5
        
        if "critical" in decision_impact.lower():
            base_score -= 2.0
        
        return max(base_score, 6.0)
    
    def _identify_ethics_risks(self, scores: List[float]) -> List[str]:
        """Identify ethics risks based on assessment scores"""
        risks = []
        
        if scores[0] < 7.0:  # Fairness
            risks.append("Potential algorithmic bias and discrimination")
        if scores[1] < 7.0:  # Transparency
            risks.append("Lack of explainability and transparency")
        if scores[2] < 7.0:  # Accountability
            risks.append("Unclear accountability and responsibility")
        if scores[3] < 7.0:  # Privacy
            risks.append("Privacy and data protection concerns")
        if scores[4] < 7.0:  # Safety
            risks.append("Safety and security vulnerabilities")
        
        return risks
    
    def _generate_ethics_mitigations(self, scores: List[float]) -> List[str]:
        """Generate ethics mitigation strategies"""
        mitigations = []
        
        if scores[0] < 7.0:  # Fairness
            mitigations.append("Implement bias detection and mitigation tools")
        if scores[1] < 7.0:  # Transparency
            mitigations.append("Develop model explainability capabilities")
        if scores[2] < 7.0:  # Accountability
            mitigations.append("Establish clear governance and oversight")
        if scores[3] < 7.0:  # Privacy
            mitigations.append("Implement privacy-preserving techniques")
        if scores[4] < 7.0:  # Safety
            mitigations.append("Enhance testing and validation processes")
        
        return mitigations
    
    def _define_ethics_monitoring(self, overall_score: float, decision_impact: str) -> List[str]:
        """Define ethics monitoring requirements"""
        requirements = [
            "Regular bias and fairness assessments",
            "Model performance monitoring",
            "Stakeholder feedback collection"
        ]
        
        if overall_score < 7.0:
            requirements.extend([
                "Enhanced continuous monitoring",
                "Regular ethics committee reviews",
                "Third-party audits"
            ])
        
        if "high" in decision_impact.lower():
            requirements.append("Real-time monitoring with human oversight")
        
        return requirements
    
    def _load_governance_templates(self) -> Dict:
        """Load governance policy templates"""
        return {
            "board_oversight": "Board-level AI governance template",
            "risk_management": "AI risk management template",
            "ethics_framework": "AI ethics framework template"
        }
    
    def _load_compliance_standards(self) -> Dict:
        """Load compliance standards and requirements"""
        return {
            "nist_ai": "NIST AI Risk Management Framework",
            "eu_ai_act": "EU AI Act compliance requirements",
            "gdpr_ai": "GDPR requirements for AI systems"
        }
    
    def _load_governance_best_practices(self) -> List[str]:
        """Load AI governance best practices"""
        return [
            "Establish clear AI governance structure",
            "Implement risk-based approach to AI oversight",
            "Ensure transparency and explainability",
            "Promote ethical AI development",
            "Enable continuous monitoring and improvement"
        ]

# Global AI governance engine instance
governance_engine = AIGovernanceEngine()

# Export functions
__all__ = [
    'GovernanceLevel',
    'ComplianceFramework',
    'AIRiskLevel',
    'GovernancePolicy',
    'ComplianceAssessment',
    'GovernanceFramework',
    'AIGovernanceEngine',
    'governance_engine'
]