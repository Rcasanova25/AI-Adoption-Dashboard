import streamlit as st

class BaseView:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def render(self, data):
        """Template method for rendering"""
        self.setup()
        self.render_header()
        self.render_content(data)
        self.render_footer()

    def setup(self):
        """Optional setup method for subclasses"""
        pass

    def render_header(self):
        st.title(self.title)
        st.markdown(self.description)

    def render_content(self, data):
        """Subclasses must implement this method"""
        raise NotImplementedError

    def render_footer(self):
        """Optional footer method for subclasses"""
        pass
