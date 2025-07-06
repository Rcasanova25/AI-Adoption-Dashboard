import plotly.graph_objects as go

class ChartFactory:
    @staticmethod
    def create_bar_chart(data, title, **kwargs):
        """Standardized bar chart creation"""
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
    def create_dual_axis_chart(data, title, **kwargs):
        """Standardized dual-axis chart"""
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
