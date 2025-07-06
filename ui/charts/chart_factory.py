import plotly.graph_objects as go

class ChartFactory:
    @staticmethod
    def create_bar_chart(data: dict, title: str, **kwargs) -> go.Figure:
        """Creates a standardized bar chart.

        Args:
            data (dict): A dictionary containing 'x' and 'y' keys for chart data.
            title (str): The title of the chart.
            **kwargs: Additional keyword arguments to pass to `go.Bar`.

        Returns:
            go.Figure: A Plotly Graph Object figure representing the bar chart.
        """
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=data['x'],
                y=data['y'],
                **kwargs
            )
        )
        fig.update_layout(title_text=title)
        return fig

    @staticmethod
    def create_dual_axis_chart(data: dict, title: str, **kwargs) -> go.Figure:
        """Creates a standardized dual-axis chart.

        Args:
            data (dict): A dictionary containing 'x', 'y1', 'y1_name', 'y2', and 'y2_name' keys for chart data.
            title (str): The title of the chart.
            **kwargs: Additional keyword arguments to pass to `go.Bar` and `go.Scatter`.

        Returns:
            go.Figure: A Plotly Graph Object figure representing the dual-axis chart.
        """
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=data['x'],
                y=data['y1'],
                name=data['y1_name'],
                yaxis='y1',
                **kwargs
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data['x'],
                y=data['y2'],
                name=data['y2_name'],
                yaxis='y2',
                **kwargs
            )
        )
        fig.update_layout(
            title_text=title,
            yaxis=dict(title=data['y1_name']),
            yaxis2=dict(title=data['y2_name'], overlaying='y', side='right')
        )
        return fig
