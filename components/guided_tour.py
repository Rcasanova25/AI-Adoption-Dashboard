"""Interactive guided tour system for new users."""

from enum import Enum
from typing import Callable, List, Optional

import streamlit as st


class TourStep:
    """Represents a single step in the guided tour."""

    def __init__(
        self,
        element_id: str,
        title: str,
        description: str,
        position: str = "bottom",
        action: Optional[Callable] = None,
        highlight: bool = True,
    ):
        """Initialize tour step.

        Args:
            element_id: ID of the element to highlight
            title: Step title
            description: Step description
            position: Tooltip position (top, bottom, left, right)
            action: Optional action to perform on this step
            highlight: Whether to highlight the element
        """
        self.element_id = element_id
        self.title = title
        self.description = description
        self.position = position
        self.action = action
        self.highlight = highlight


class UserLevel(Enum):
    """User experience levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class GuidedTour:
    """Manages interactive guided tours for the dashboard."""

    def __init__(self):
        """Initialize guided tour system."""
        # Initialize session state
        if "tour_completed" not in st.session_state:
            st.session_state.tour_completed = False

        if "tour_step" not in st.session_state:
            st.session_state.tour_step = 0

        if "user_level" not in st.session_state:
            st.session_state.user_level = UserLevel.BEGINNER

        if "show_tooltips" not in st.session_state:
            st.session_state.show_tooltips = True

        # Define tour steps
        self.tours = {
            "main_dashboard": self._create_main_tour(),
            "competitive_position": self._create_competitive_tour(),
            "roi_calculator": self._create_roi_tour(),
        }

    def _create_main_tour(self) -> List[TourStep]:
        """Create the main dashboard tour."""
        return [
            TourStep(
                "welcome",
                "Welcome to the Economics of AI Dashboard! 🎯",
                "This dashboard helps you understand the economic impact of AI on your organization. Let's take a quick tour!",
                position="center",
            ),
            TourStep(
                "persona_selector",
                "Choose Your Perspective",
                "Select your role to get personalized insights and recommendations tailored to your needs.",
                position="right",
            ),
            TourStep(
                "key_metrics",
                "Key Metrics at a Glance",
                "These cards show the most important AI metrics for your industry and role.",
                position="bottom",
            ),
            TourStep(
                "competitive_position",
                "Your Competitive Position",
                "See how you compare to industry peers and leaders in AI adoption.",
                position="top",
            ),
            TourStep(
                "action_plan",
                "Personalized Action Plan",
                "Get specific recommendations based on your current position and goals.",
                position="left",
            ),
            TourStep(
                "export_options",
                "Export and Share",
                "Download reports and insights to share with your team.",
                position="top",
            ),
        ]

    def _create_competitive_tour(self) -> List[TourStep]:
        """Create the competitive position tour."""
        return [
            TourStep(
                "assessment_inputs",
                "Quick Assessment",
                "Enter your organization's details to get a personalized competitive analysis.",
                position="right",
            ),
            TourStep(
                "position_matrix",
                "Competitive Position Matrix",
                "See where you stand compared to industry leaders and peers.",
                position="bottom",
            ),
            TourStep(
                "gap_analysis",
                "Gap Analysis",
                "Understand what separates you from industry leaders.",
                position="top",
            ),
            TourStep(
                "recommendations",
                "Strategic Recommendations",
                "Get actionable steps to improve your competitive position.",
                position="bottom",
            ),
        ]

    def _create_roi_tour(self) -> List[TourStep]:
        """Create the ROI calculator tour."""
        return [
            TourStep(
                "investment_inputs",
                "Investment Parameters",
                "Enter your planned AI investment details.",
                position="right",
            ),
            TourStep(
                "roi_projection",
                "ROI Projection",
                "See projected returns over time based on industry benchmarks.",
                position="bottom",
            ),
            TourStep(
                "scenario_analysis",
                "What-If Scenarios",
                "Explore different investment scenarios and their impacts.",
                position="top",
            ),
        ]

    def should_show_tour(self) -> bool:
        """Check if tour should be shown."""
        # Show tour for first-time users or if requested
        return (
            not st.session_state.tour_completed
            and st.session_state.user_level == UserLevel.BEGINNER
        )

    def start_tour(self, tour_name: str = "main_dashboard"):
        """Start a specific tour."""
        st.session_state.tour_step = 0
        st.session_state.current_tour = tour_name
        st.session_state.tour_active = True

    def render_tour_controls(self):
        """Render tour control buttons in sidebar."""
        st.sidebar.markdown("### 🎓 Learning Center")

        col1, col2 = st.sidebar.columns(2)

        with col1:
            if st.button("Start Tour", key="start_tour_btn", use_container_width=True):
                self.start_tour()
                st.rerun()

        with col2:
            if st.button(
                "Tips On" if st.session_state.show_tooltips else "Tips Off",
                key="toggle_tips_btn",
                use_container_width=True,
            ):
                st.session_state.show_tooltips = not st.session_state.show_tooltips
                st.rerun()

        # User level selector
        st.sidebar.selectbox(
            "Experience Level",
            options=[level.value for level in UserLevel],
            index=[level.value for level in UserLevel].index(st.session_state.user_level.value),
            key="user_level_select",
            on_change=self._on_level_change,
        )

    def _on_level_change(self):
        """Handle user level change."""
        new_level = st.session_state.user_level_select
        st.session_state.user_level = UserLevel(new_level)

    def render_tour_step(self):
        """Render the current tour step."""
        if not hasattr(st.session_state, "tour_active") or not st.session_state.tour_active:
            return

        tour_name = st.session_state.get("current_tour", "main_dashboard")
        tour_steps = self.tours.get(tour_name, [])

        if st.session_state.tour_step >= len(tour_steps):
            self.complete_tour()
            return

        current_step = tour_steps[st.session_state.tour_step]

        # Create tour overlay
        with st.container():
            st.markdown(
                """
            <div style='position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                        background-color: rgba(0,0,0,0.5); z-index: 999;'>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Create tour tooltip
            self._render_tooltip(current_step)

    def _render_tooltip(self, step: TourStep):
        """Render tour tooltip."""
        # Calculate position based on step.position
        position_styles = {
            "center": "top: 50%; left: 50%; transform: translate(-50%, -50%);",
            "top": "top: 20%; left: 50%; transform: translateX(-50%);",
            "bottom": "bottom: 20%; left: 50%; transform: translateX(-50%);",
            "left": "top: 50%; left: 20%; transform: translateY(-50%);",
            "right": "top: 50%; right: 20%; transform: translateY(-50%);",
        }

        style = position_styles.get(step.position, position_styles["center"])

        # Create tooltip container
        tooltip_html = f"""
        <div style='position: fixed; {style} background-color: white; 
                    padding: 20px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                    z-index: 1000; max-width: 400px;'>
            <h3 style='margin-top: 0; color: #1f77b4;'>{step.title}</h3>
            <p style='margin: 10px 0; color: #495057;'>{step.description}</p>
            <div style='margin-top: 20px; text-align: right;'>
                <span style='color: #6c757d; font-size: 14px;'>
                    Step {st.session_state.tour_step + 1} of {len(self.tours[st.session_state.current_tour])}
                </span>
            </div>
        </div>
        """

        st.markdown(tooltip_html, unsafe_allow_html=True)

        # Tour navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("Skip Tour", key="skip_tour"):
                self.complete_tour()
                st.rerun()

        with col2:
            if st.session_state.tour_step > 0:
                if st.button("← Previous", key="prev_step"):
                    st.session_state.tour_step -= 1
                    st.rerun()

        with col3:
            if st.session_state.tour_step < len(self.tours[st.session_state.current_tour]) - 1:
                if st.button("Next →", key="next_step"):
                    st.session_state.tour_step += 1
                    st.rerun()
            else:
                if st.button("Finish ✓", key="finish_tour"):
                    self.complete_tour()
                    st.rerun()

    def complete_tour(self):
        """Complete the current tour."""
        st.session_state.tour_completed = True
        st.session_state.tour_active = False
        st.success("🎉 Tour completed! You're ready to explore the dashboard.")

    def render_contextual_help(self, help_id: str, content: str):
        """Render contextual help tooltip.

        Args:
            help_id: Unique identifier for the help item
            content: Help content to display
        """
        if not st.session_state.show_tooltips:
            return

        # Create help icon with popover
        if st.button("ℹ️", key=f"help_{help_id}", help=content):
            pass

    def render_onboarding_wizard(self):
        """Render initial onboarding wizard for new users."""
        if "onboarding_complete" in st.session_state and st.session_state.onboarding_complete:
            return

        # Create modal-style onboarding
        st.markdown(
            """
        <div style='position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                    background-color: rgba(0,0,0,0.8); z-index: 1000;
                    display: flex; align-items: center; justify-content: center;'>
            <div style='background-color: white; padding: 40px; border-radius: 20px;
                        max-width: 600px; text-align: center;'>
                <h1 style='color: #1f77b4; margin-bottom: 20px;'>
                    Welcome to the Economics of AI Dashboard! 🚀
                </h1>
                <p style='font-size: 18px; color: #495057; margin-bottom: 30px;'>
                    Let's get you started with a personalized experience.
                </p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Onboarding questions
        with st.form("onboarding_form"):
            st.markdown("### Tell us about yourself")

            role = st.selectbox(
                "What's your role?", ["Executive", "Manager", "Analyst", "Researcher", "Other"]
            )

            objective = st.selectbox(
                "What's your primary objective?",
                [
                    "Assess competitive position",
                    "Calculate ROI",
                    "Explore market trends",
                    "Build investment case",
                    "General exploration",
                ],
            )

            experience = st.radio(
                "How familiar are you with AI?", ["New to AI", "Some experience", "Very familiar"]
            )

            if st.form_submit_button("Get Started", type="primary", use_container_width=True):
                # Store preferences
                st.session_state.user_role = role
                st.session_state.user_objective = objective
                st.session_state.user_experience = experience
                st.session_state.onboarding_complete = True

                # Set appropriate user level
                if experience == "New to AI":
                    st.session_state.user_level = UserLevel.BEGINNER
                elif experience == "Some experience":
                    st.session_state.user_level = UserLevel.INTERMEDIATE
                else:
                    st.session_state.user_level = UserLevel.ADVANCED

                st.rerun()


class InteractiveTutorial:
    """Provides interactive tutorials for specific features."""

    def __init__(self):
        """Initialize tutorial system."""
        self.tutorials = {
            "roi_calculator": self._roi_calculator_tutorial,
            "competitive_matrix": self._competitive_matrix_tutorial,
            "scenario_planner": self._scenario_planner_tutorial,
        }

    def render_tutorial(self, tutorial_name: str):
        """Render a specific tutorial.

        Args:
            tutorial_name: Name of the tutorial to render
        """
        if tutorial_name in self.tutorials:
            self.tutorials[tutorial_name]()

    def _roi_calculator_tutorial(self):
        """ROI calculator tutorial."""
        with st.expander("📚 How to use the ROI Calculator", expanded=False):
            st.markdown(
                """
            ### ROI Calculator Tutorial
            
            **Step 1: Enter Investment Details**
            - Specify your planned AI investment amount
            - Select the implementation timeline
            - Choose your industry sector
            
            **Step 2: Review Projections**
            - The calculator uses industry benchmarks to project returns
            - Conservative, expected, and optimistic scenarios are shown
            - Break-even point is highlighted
            
            **Step 3: Explore Scenarios**
            - Use the what-if analysis to test different assumptions
            - Adjust parameters to see impact on ROI
            - Compare multiple scenarios side-by-side
            
            **Tips:**
            - Start with conservative estimates
            - Consider both direct and indirect benefits
            - Factor in implementation risks
            """
            )

    def _competitive_matrix_tutorial(self):
        """Competitive matrix tutorial."""
        with st.expander("📚 Understanding the Competitive Matrix", expanded=False):
            st.markdown(
                """
            ### Competitive Position Matrix Guide
            
            **Reading the Matrix:**
            - **X-axis**: AI Adoption Rate (%)
            - **Y-axis**: AI Investment Level ($M)
            - **Bubble size**: GenAI adoption rate
            - **Color**: ROI performance
            
            **Quadrants:**
            1. **Leaders** (Top-Right): High adoption, high investment
            2. **Efficient Adopters** (Bottom-Right): High adoption, low investment
            3. **Over-investors** (Top-Left): Low adoption, high investment
            4. **Laggards** (Bottom-Left): Low adoption, low investment
            
            **Your Position:**
            - Red star indicates your current position
            - Compare to industry average (dotted lines)
            - Identify gaps to leaders
            """
            )

    def _scenario_planner_tutorial(self):
        """Scenario planner tutorial."""
        with st.expander("📚 Scenario Planning Guide", expanded=False):
            st.markdown(
                """
            ### What-If Scenario Planning
            
            **Available Scenarios:**
            1. **Adoption Acceleration**: Impact of faster implementation
            2. **Investment Levels**: ROI at different investment scales
            3. **Competitive Response**: Market dynamics modeling
            
            **How to Use:**
            - Select a scenario type
            - Adjust parameters using sliders
            - Compare outcomes across scenarios
            - Export results for presentations
            
            **Best Practices:**
            - Test both optimistic and pessimistic cases
            - Consider external factors (market, competition)
            - Update scenarios quarterly
            """
            )


def render_help_system():
    """Render the integrated help system."""
    tour = GuidedTour()

    # Check if onboarding needed
    if "onboarding_complete" not in st.session_state:
        tour.render_onboarding_wizard()
        return

    # Render tour controls in sidebar
    tour.render_tour_controls()

    # Render active tour step if any
    tour.render_tour_step()

    # Show welcome message for new users
    if st.session_state.user_level == UserLevel.BEGINNER and not st.session_state.tour_completed:
        st.info(
            """
        👋 **New to the dashboard?** Click 'Start Tour' in the sidebar for a 
        guided walkthrough of key features!
        """
        )

    return tour
