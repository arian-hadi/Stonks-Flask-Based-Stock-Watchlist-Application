# import plotly.graph_objs as go
# import plotly.io as pio
# from flask import Blueprint, render_template,jsonify
# from flask_login import login_required
# from app.utils.finnhub_utils import get_stock_quote
# from app.utils.stock_chart import get_stock_chart_data

# stock_details_bp = Blueprint('stock_details', __name__)


# def create_stock_chart(chart_data):
#     fig = go.Figure()

#     fig.add_trace(go.Scatter(
#         x=chart_data["labels"], 
#         y=chart_data["prices"], 
#         mode='lines',
#         name='Stock Price'
#     ))

#     fig.update_layout(
#         title="Stock Price Trend",
#         xaxis_title="Date",
#         yaxis_title="Price (USD)",
#         template="plotly_dark"
#     )

#     return pio.to_json(fig) 

# @stock_details_bp.route('/stock/<symbol>', methods=['GET'])
# @login_required
# def stock_details(symbol):
#     stock_data = get_stock_quote(symbol)
#     chart_data = get_stock_chart_data(symbol, resolution="D", days=30)   
#     if stock_data.get("error"):
#         return render_template("stock_details.html", error=f"Unable to retrieve data for {symbol}.")
#     if chart_data.get("error"):
#         return render_template("stock_details.html", stock=stock_data, symbol=symbol, error=chart_data["error"])

#     plotly_chart_json = create_stock_chart(chart_data)

#     return render_template("stock_details.html", stock=stock_data, chart_json=plotly_chart_json, symbol=symbol)
import plotly.graph_objs as go
import plotly.io as pio
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.utils.stock_chart import fetch_stock_details

stock_details_bp = Blueprint('stock_details', __name__)

def create_stock_chart(stock_data):
    fig = go.Figure()
    
    # Line Chart (Real-time stock price trend)
    fig.add_trace(go.Scatter(
        x=["Now"],  # Only current time available in free API
        y=[stock_data["current_price"]],
        mode='lines+markers',
        name='Stock Price'
    ))

    fig.update_layout(
        title="Real-Time Stock Price Trend",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )

    return pio.to_json(fig)

def create_price_comparison_chart(stock_data):
    fig = go.Figure()

    # Bar Chart (Comparing High, Low, Open, Close prices)
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
    fig = go.Figure()

    # Gauge Chart (Price change percentage)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=stock_data["percent_change"],
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

@stock_details_bp.route('/stock/<symbol>', methods=['GET'])
@login_required
def stock_details(symbol):
    stock_data = fetch_stock_details(symbol)
    
    if stock_data.get("error"):
        return render_template("stock_details.html", error=f"Unable to retrieve data for {symbol}.")

    line_chart_json = create_stock_chart(stock_data)
    bar_chart_json = create_price_comparison_chart(stock_data)
    gauge_chart_json = create_gauge_chart(stock_data)

    return render_template(
        "stock_details.html",
        stock=stock_data,
        line_chart_json=line_chart_json,
        bar_chart_json=bar_chart_json,
        gauge_chart_json=gauge_chart_json,
        symbol=symbol
    )
