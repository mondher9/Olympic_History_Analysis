import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Olympic History Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced aesthetics
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background: #1a1a1a; /* Dark background */
        color: #e0e0e0; /* Light text */
    }
    
    /* Title styling */
    .stTitle {
        color: #E0BBE4; /* Lighter purple for titles */
        font-size: 2.5rem !important;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(224,187,228,0.2);
        padding: 1rem 0;
        border-bottom: 3px solid #957DAD; /* Darker purple border */
        margin-bottom: 2rem;
    }
    
    /* Header styling */
    .stHeader {
        color: #957DAD; /* Purple for headers */
        font-size: 1.8rem !important;
        font-weight: 600;
        margin: 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #5a4b60; /* Darker grey border */
    }
    
    /* Subheader styling */
    .stSubheader {
        color: #e0e0e0; /* Light grey for subheaders */
        font-size: 1.4rem !important;
        font-weight: 500;
    }
    
    /* Card styling */
    .css-1d391kg {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        background: #2a2a2a; /* Darker card background */
        transition: transform 0.3s ease;
        color: #e0e0e0;
    }
    
    .css-1d391kg:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.6);
    }
    
    /* Metric styling */
    .stMetric {
        background: #2a2a2a;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        color: #e0e0e0;
    }
    
    .stMetric:hover {
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #1a1a1a; /* Dark sidebar background */
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #4c4c4c, #333333); /* Darker grey gradient */
        color: #e0e0e0;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox {
        background: #2a2a2a; /* Darker selectbox background */
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        color: #e0e0e0; /* Light text */
    }
    .stSelectbox>div>div {
        color: #e0e0e0;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        background-color: #2a2a2a; /* Darker dataframe background */
        color: #e0e0e0;
    }
    
    /* Plot styling */
    .js-plotly-plot {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    /* Custom animation for elements */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stTitle, .stHeader, .stSubheader {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Specific styling for the menu items to ensure dark theme compatibility */
    .css-1oe5f06, .css-1dp5vir {
        color: #e0e0e0; /* Light text for menu items */
    }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

# Sidebar styling and navigation
with st.sidebar:
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background: #1a1a1a;
            padding: 2rem 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🏅 Olympic History Analysis")
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Olympic_rings_with_transparent_rims.svg/960px-Olympic_rings_with_transparent_rims.svg.png', width=200)
    
    # Using option_menu for better navigation
    selected = option_menu(
        menu_title=None,
        options=['Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis'],
        icons=['🏆', '📊', '🌍', '👥'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1a1a1a"},
            "icon": {"color": "#E0BBE4", "font-size": "1.2rem"},
            "nav-link": {
                "font-size": "1.1rem",
                "text-align": "left",
                "margin": "0.7rem 0",
                "padding": "0.7rem 1.2rem",
                "border-radius": "8px",
                "color": "#e0e0e0",
                "background-color": "#444444",
                "transition": "all 0.3s ease-in-out"
            },
            "nav-link:hover": {
                "background-color": "#B08EDD",
                "color": "white",
                "transform": "translateX(8px)"
            },
            "nav-link-selected": {
                "background-color": "#957DAD",
                "color": "white"
            }
        }
    )

if selected == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("🏆 Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"🏆 Medal Tally in {selected_year} Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"🏆 {selected_country} overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f"🏆 {selected_country} performance in {selected_year} Olympics")
    
    st.markdown("---")
    st.dataframe(medal_tally, use_container_width=True)

if selected == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("📊 Top Statistics")
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric("Editions", editions, "Olympic Games")
    with col2:
        st.metric("Hosts", cities, "Cities")
    with col3:
        st.metric("Sports", sports, "Categories")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Events", events, "Competitions")
    with col2:
        st.metric("Nations", nations, "Countries")
    with col3:
        st.metric("Athletes", athletes, "Participants")

    st.markdown("---")

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region", 
                 title="Participating Nations over the years",
                 template="plotly_dark")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event",
                 title="Events over the years",
                 template="plotly_dark")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name",
                 title="Athletes over the years",
                 template="plotly_dark")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    st.title("📈 No. of Events over time (Every Sport)")
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    if x.empty:
        st.warning("No event data available for this display.")
    else:
        fig,ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                    annot=True, cmap='rocket')
        st.pyplot(fig)

    st.title("👑 Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.dataframe(x, use_container_width=True)

if selected == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal",
                 title=f"{selected_country} Medal Tally over the years",
                 template="plotly_dark")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    st.title(f"🏆 {selected_country} excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)

    if pt.empty:
        st.warning("No medal data available for this country in any sport to display a heatmap.")
    else:
        try:
            fig, ax = plt.subplots(figsize=(20, 20))
            ax = sns.heatmap(pt, annot=True, cmap='rocket')
            st.pyplot(fig)
        except ValueError as e:
            st.error(f"An error occurred while plotting the heatmap: {e}. This might be due to insufficient data for the selected country or sport.")
            st.warning("Please try selecting a different country or sport.")

    st.title(f"👑 Top 10 athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.dataframe(top10_df, use_container_width=True)

if selected == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Prepare data for the first distplot, filtering out empty series
    data_for_distplot1 = []
    labels_for_distplot1 = []

    x1 = athlete_df['Age'].dropna()
    if not x1.empty:
        data_for_distplot1.append(x1)
        labels_for_distplot1.append('Overall Age')

    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    if not x2.empty:
        data_for_distplot1.append(x2)
        labels_for_distplot1.append('Gold Medalist')

    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    if not x3.empty:
        data_for_distplot1.append(x3)
        labels_for_distplot1.append('Silver Medalist')

    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    if not x4.empty:
        data_for_distplot1.append(x4)
        labels_for_distplot1.append('Bronze Medalist')

    if data_for_distplot1: # Only plot if there's data
        fig = ff.create_distplot(data_for_distplot1, labels_for_distplot1, show_hist=False, show_rug=False)
        fig.update_layout(
            title="Distribution of Age",
            title_x=0.5,
            template="plotly_dark",
            width=1000,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No age distribution data available.")

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_medal_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not gold_medal_ages.empty:
            x.append(gold_medal_ages)
            name.append(sport)

    if x: # Only plot if there's data
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(
            title="Distribution of Age wrt Sports (Gold Medalist)",
            title_x=0.5,
            template="plotly_dark",
            width=1000,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No gold medalist age distribution data available for famous sports.")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('📏 Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    
    # Filter out rows with NaN in 'Weight' or 'Height' for plotting
    plot_df = temp_df.dropna(subset=['Weight', 'Height'])

    if plot_df.empty or 'Weight' not in plot_df.columns or 'Height' not in plot_df.columns or 'Medal' not in plot_df.columns or 'Sex' not in plot_df.columns:
        st.warning("No sufficient height vs. weight data available for this sport.")
    else:
        fig,ax = plt.subplots(figsize=(10,6))
        ax = sns.scatterplot(data=plot_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60)
        plt.title(f'Height vs Weight Analysis for {selected_sport}')
        st.pyplot(fig)

    st.title("👥 Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"],
                 template="plotly_dark")
    fig.update_layout(
        title_x=0.5,
        width=1000,
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)



