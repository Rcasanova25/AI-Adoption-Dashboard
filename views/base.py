import streamlit as st

class BaseView:
    def __init__(self, title: str, description: str):
        """Initializes the BaseView with a title and description.

        Args:
            title (str): The title of the view.
            description (str): A brief description of the view.
        """
        self.title = title
        self.description = description

    def render(self, data: dict) -> None:
        """Renders the complete view by calling setup, render_header, render_content, and render_footer.

        Args:
            data (dict): A dictionary containing all necessary data for the view.
        """
        self.setup()
        self.render_header()
        self.render_content(data)
        self.render_footer()

    def setup(self) -> None:
        """Optional setup method for subclasses to override.
        This method is called before rendering the header.
        """
        pass

    def render_header(self) -> None:
        """Renders the header of the view, including the title and description."""
        st.title(self.title)
        st.markdown(self.description)

    def render_content(self, data: dict) -> None:
        """Abstract method that subclasses must implement to render the main content of the view.

        Args:
            data (dict): A dictionary containing all necessary data for the view.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError

    def render_footer(self) -> None:
        """Optional footer method for subclasses to override.
        This method is called after rendering the content.
        """
        pass
