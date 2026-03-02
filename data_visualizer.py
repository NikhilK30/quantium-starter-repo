import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load dataset
DATA_PATH = "./final_sales.csv"
df = pd.read_csv(DATA_PATH)

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Initialize Dash app
app = dash.Dash(__name__)

# -------- Layout -------- #

app.layout = html.Div(

    style={
        "backgroundColor": "#F2F4F7",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "fontFamily": "Arial"
    },

    children=[

        html.Div(

            style={
                "width": "900px",
                "backgroundColor": "white",
                "padding": "30px",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 15px rgba(0,0,0,0.15)"
            },

            children=[

                html.H1(
                    "Soul Foods Pink Morsel Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "color": "#2C3E50",
                        "marginBottom": "25px"
                    }
                ),

                html.Div(
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px"
                    },
                    children=[

                        dcc.RadioItems(
                            id="region-filter",

                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"}
                            ],

                            value="all",

                            labelStyle={
                                "display": "inline-block",
                                "marginRight": "25px",
                                "fontSize": "16px",
                                "cursor": "pointer"
                            }
                        )

                    ]
                ),

                dcc.Graph(id="sales-chart")

            ]
        )

    ]
)

# -------- Callback -------- #

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):

    # Filter region
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # Aggregate sales
    daily_sales = filtered_df.groupby("date", as_index=False)["sales"].sum()

    # Create chart
    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={"date": "Date", "sales": "Total Sales ($)"}
    )

    # Improve chart appearance
    fig.update_traces(line=dict(width=3))

    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=True, gridcolor="#E5E7E9")
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7E9")

    # Price increase marker
    price_change_date = "2021-01-15"

    fig.add_shape(
        type="line",
        x0=price_change_date,
        x1=price_change_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", width=2, dash="dash")
    )

    fig.add_annotation(
        x=price_change_date,
        y=1,
        xref="x",
        yref="paper",
        text="Price Increase (15 Jan 2021)",
        showarrow=False,
        yanchor="bottom",
        font=dict(color="red")
    )

    return fig


# -------- Run App -------- #

if __name__ == "__main__":
    app.run(debug=True)