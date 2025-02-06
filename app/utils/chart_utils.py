import plotly.graph_objs as go
import plotly.io as pio

def create_price_comparison_chart(stock_data):
    """Creates a bar chart comparing Open, High, Low, and Previous Close prices."""
    fig = go.Figure()

    categories = ["Open", "High", "Low", "Previous Close"]
    values = [stock_data["open"], stock_data["high"], stock_data["low"], stock_data["previous_close"]]

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker=dict(color=["blue", "green", "red", "purple"]),
        name="Price Comparison"
    ))

    fig.update_layout(
        title="Stock Price Comparison",
        xaxis_title="Price Type",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )

    return pio.to_json(fig)

def create_gauge_chart(stock_data):
    """Creates a gauge chart for stock price percentage change."""
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=stock_data["change_percent"],
        title={"text": "Price Change (%)"},
        delta={"reference": 0},
        gauge={
            "axis": {"range": [-10, 10]},  # Adjust range as needed
            "bar": {"color": "blue"},
            "steps": [
                {"range": [-10, 0], "color": "red"},
                {"range": [0, 10], "color": "green"},
            ],
        }
    ))

    fig.update_layout(template="plotly_dark")

    return pio.to_json(fig)

def create_historical_chart(chart_data, time_period):
    """Creates a line chart for stock price history (weekly or monthly)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_data["labels"],
        y=chart_data["prices"],
        mode='lines',
        name=f'{time_period.capitalize()} Stock Price'
    ))
    fig.update_layout(
        title=f"{time_period.capitalize()} Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )
    return pio.to_json(fig)
