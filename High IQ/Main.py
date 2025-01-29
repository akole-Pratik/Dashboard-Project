from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
from map import generate_map


# Load data
data = pd.read_csv("shopping_trends.csv")
data_copy = data.copy()

################################################ Data calculations ############################################################
# 1: Frequency of Purchase by Gender
frequency_by_gender = data.groupby("Gender")["Frequency of Purchases"].value_counts().unstack(fill_value=0)
frequency_by_gender = frequency_by_gender.reset_index()

# 2: Count purchases by Category and Item
count_by_category = data['Category'].value_counts().reset_index()
count_by_category.columns = ['Category', 'Count']  # Rename columns properly


# 3: Top Categories Purchased in Each Season
top_categories_by_season = data.groupby("Season")["Category"].value_counts().unstack(fill_value=0)
top_categories_by_season = top_categories_by_season.reset_index()

# 4: Most Popular Categories in Different Locations
popular_categories_by_location = data.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()

map_fig = generate_map(popular_categories_by_location)

################################################ filters & KPIs #####################################################################
categories = list(data["Category"].unique())   
selected_category = "Clothing"

season = list(data['Season'].unique())
selected_season = "Winter"

# KPI Calculations
total_revenue = data['Purchase Amount (USD)'].sum()
total_customers = data['Customer ID'].nunique()
avg_purchase_value = sum(data['Purchase Amount (USD)']) / len(data['Purchase Amount (USD)'])


def apply_changes(state):
    state.data_copy = state.data[
        state.data["Category"].isin(state.selected_category) 
        & 
        state.data["Season"].isin(state.selected_season)]
    
    state.total_revenue = total_revenue
    state.total_customers = total_customers
    state.avg_purchase_value = avg_purchase_value

    
    state.frequency_by_gender = (
        state.data_copy.groupby('Gender')['Frequency of Purchases']
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )
    state.count_by_category = (
        state.data_copy['Category']
        .value_counts()
        .reset_index()
    )

    state.count_by_category.columns = ["Category", "Count"]

    state.top_categories_by_season = (
        state.data_copy.groupby("Season")["Category"]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )
    
    state.popular_categories_by_location = (
        state.data_copy.groupby("Location")["Purchase Amount (USD)"]
        .sum()
        .reset_index()
    )
    state.map_fig = generate_map(state.popular_categories_by_location)

    # Update KPIs
    state.total_revenue = state.data_copy['Purchase Amount (USD)'].sum()
    state.total_customers = state.data_copy['Customer ID'].nunique()
    state.avg_purchase_value = sum(state.data_copy['Purchase Amount (USD)']) / len(state.data_copy['Purchase Amount (USD)'])


    print("Filtered Data:")
    print(state.data_copy.head())   

# Reset function to reset all filters and KPI Data
def reset_filter_data(state):
    state.selected_category = categories 
    state.selected_season = season
    state.data_copy = state.data.copy()
    

    state.frequency_by_gender = frequency_by_gender
    state.count_by_category = count_by_category
    state.top_categories_by_season = top_categories_by_season
    state.popular_categories_by_location = popular_categories_by_location
    #state.map_fig = generate_map(state.popular_categories_by_location)

    state.total_revenue = total_revenue
    state.total_customers = total_customers
    state.avg_purchase_value = avg_purchase_value

    print("Reset filters and data.")


############################################ Page Layout ############################################
# Page Layout
with tgb.Page() as page:
    # Filters and KPIs
    with tgb.layout("1"):
        with tgb.part(class_name='header-container'):
            tgb.text('### Customer Purchase Pattern Dashboard', mode='md', class_name='dashboard-title')
        with tgb.part(class_name='card'):

            with tgb.layout('1 1'):
            # Filters
                with tgb.part(class_name='filter-container'):
                    tgb.text("###### Filters", mode='md', class_name='filter-title')
                    with tgb.layout("1 1"):
                        with tgb.part(class_name='card', style='height : 100px'):
                            tgb.text("**Category**", mode='md', class_name='filter-label')
                            tgb.selector(value="{selected_category}",
                                     lov=categories,
                                     dropdown=True,
                                     multiple=True,
                                     checkbox=True,
                                     class_name='dropdown'
                                    )
                        with tgb.part(class_name='card', style='height : 100px'):
                            tgb.text("**Select Season**", mode='md', class_name='filter-label')
                            tgb.selector(value="{selected_season}",
                                     lov=season,
                                     dropdown=True,
                                     multiple=True,
                                     checkbox=True,
                                     class_name='dropdown'
                                    )
                        with tgb.part(class_name='button-container'):
                            with tgb.layout('1 1'):
                                tgb.button('Apply', class_name='apply-button', on_action=apply_changes)
                                tgb.button('Reset', class_name='reset-button', on_action=reset_filter_data)

            # KPIs
                with tgb.part(class_name='kpi-container'):
                        tgb.text("###### KPI Cards", mode='md', class_name='kpi-title')
                        with tgb.layout("1 1 1"):
                            with tgb.part(class_name='card'):
                                tgb.text("**Total Revenue:**", mode='md', class_name='kpi-card')
                                tgb.text(value="${total_revenue}", mode='md',class_name='kpi-value')

                            with tgb.part(class_name='card'):
                                tgb.text("**Total Customers:**", mode='md', class_name='kpi-card')
                                tgb.text(value="{total_customers}", mode='md',class_name='kpi-value')

                            with tgb.part(class_name='card'):
                                tgb.text("**Avg Purchase Value:**", mode='md', class_name='kpi-card')
                                tgb.text(value="${avg_purchase_value:,.2f}", mode='md',class_name='kpi-value')
    
################################################# Visual charts ##################################################
        # Dashboard Visuals
        # Chart 1: Frequency of Purchase by Gender
        with tgb.layout("1"):
            with tgb.part(class_name='chart-container'):
                with tgb.part(class_name='chart-container'):
                    tgb.text('###### Insights', mode='md')
                    #tgb.html("br")
                    with tgb.layout("1 1"):
                        tgb.chart(data="{frequency_by_gender}",
                            type='bar',
                            x='Gender',
                            y__1="Annually",
                            y__2="Bi-Weekly",
                            y__3="Every 3 Months",
                            y__4="Fortnightly",
                            y__5="Monthly",
                            y__6="Quarterly",
                            y__7="Weekly",
                            title="Frequency of Purchases by Gender",
                            layout={"showlegend": True, "barmode": "group", "xaxis": {"title": "Gender"}, "yaxis": {"title": "Frequency"}}
                        )
            
            # chart 2: Count purchases by Category.
                        tgb.chart(data="{count_by_category}",
                            type='pie',
                            hole=0.4,
                            label='Category',
                            values='Count',
                            title='Purchase Distribution by Category',
                            layout={"showlegend": True, "title": "Purchase Distribution by Category"},
                        )
            
            # Chart 3: Top Categories by Season
                        tgb.chart(data='{top_categories_by_season}',
                                  type='bar',
                                  x='Season',
                                  y=['Accessories', 'Clothing', 'Footwear', 'Outerwear'],
                                  title='Top Categories Purchased During Each Season',
                                  layout={
                                          "showlegend": True,
                                          "barmode": "group",
                                          "xaxis": {"title": "Season", "type": "category"}, 
                                          "yaxis": {"title": "Count"}  
                                        }
                        )
            
            # Chart 4: Map Chart for Most Popular Categories by Location
                        tgb.chart(figure='{map_fig}', color='85A947', layout={"showlegend":False})

#tgb.text("Dashboard by Pratik Akole | © 2025", mode='md', class_name="footer")     


if __name__ == "__main__":
    app = Gui(page)
    app.run(use_reloader=True, title="Customer Purchase Pattern Dashborad",dark_mode=False, debug=True)
