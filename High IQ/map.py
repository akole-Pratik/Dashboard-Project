import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("shopping_trends.csv")

state_codes = {
    "Kentucky": "KY",
    "Maine": "ME",
    "Massachusetts": "MA",
    "Rhode Island": "RI",
    "Oregon": "OR",
    "Wyoming": "WY",
    "Montana": "MT",
    "Louisiana": "LA",
    "West Virginia": "WV",
    "Missouri": "MO",
    "Arkansas": "AR",
    "Hawaii": "HI",
    "Delaware": "DE",
    "New Hampshire": "NH",
    "New York": "NY",
    "Alabama": "AL",
    "Mississippi": "MS",
    "North Carolina": "NC",
    "California": "CA",
    "Oklahoma": "OK",
    "Florida": "FL",
    "Texas": "TX",
    "Nevada": "NV",
    "Kansas": "KS",
    "Colorado": "CO",
    "North Dakota": "ND",
    "Illinois": "IL",
    "Indiana": "IN",
    "Arizona": "AZ",
    "Alaska": "AK",
    "Tennessee": "TN",
    "Ohio": "OH",
    "New Jersey": "NJ",
    "Maryland": "MD",
    "Vermont": "VT",
    "New Mexico": "NM",
    "South Carolina": "SC",
    "Idaho": "ID",
    "Pennsylvania": "PA",
    "Connecticut": "CT",
    "Utah": "UT",
    "Virginia": "VA",
    "Georgia": "GA",
    "Nebraska": "NE",
    "Iowa": "IA",
    "South Dakota": "SD",
    "Minnesota": "MN",
    "Washington": "WA",
    "Wisconsin": "WI",
    "Michigan": "MI"
}

def generate_map(popular_categories_by_location: pd.DataFrame) -> go.Figure:
    popular_categories_by_location = data.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()
    popular_categories_by_location['text'] =(
        popular_categories_by_location['Location'] + "<br>" + "Purchase Amount (USD):"+ popular_categories_by_location['Purchase Amount (USD)'].astype(str)
    )
    popular_categories_by_location['codes'] = popular_categories_by_location['Location'].map(state_codes)
    
    fig = go.Figure(data=go.Choropleth(locations=popular_categories_by_location['codes'],
                                       z = popular_categories_by_location['Purchase Amount (USD)'],
                                       locationmode = 'USA-states',
                                       colorscale = 'Reds',
                                       colorbar_title = "Number of Records",
                                       hoverinfo='none',
                                       )
    )

    for i, row in popular_categories_by_location.iterrows():
        fig.add_trace(
            go.Scattergeo(locationmode="USA-states",
                          locations=[row["codes"]],
                          text=f"{row['codes']}",
                          hovertext=f"{row['Location']}<br>{row['Purchase Amount (USD)']}",
                          hoverinfo="text",
                          mode="text",
                          textfont=dict(size=10),
            )
        )
                                    
    fig.update_layout(title_text = 'Number of Records by State',
                      geo_scope='usa',
                      showlegend = False,
    )
    return fig

if __name__ == "__main__":
    fig = generate_map(data)
    fig.show()
