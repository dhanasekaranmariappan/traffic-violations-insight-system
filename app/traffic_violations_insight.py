"""
streamlit_app.py - Traffic Violations Insight System Dashboard
Enhanced UI Version
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Traffic Violations Insight System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #2c3e50 !important;
    }

    /* All sidebar text white */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: white !important;
    }

    /* Force ALL input boxes to be white with dark text */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="input"] > div {
        background-color: white !important;
        color: #1a1a2e !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* Dropdown selected value text */
    section[data-testid="stSidebar"] [data-baseweb="select"] span,
    section[data-testid="stSidebar"] [data-baseweb="select"] div,
    section[data-testid="stSidebar"] [class*="ValueContainer"] *,
    section[data-testid="stSidebar"] [class*="singleValue"] {
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }

    /* Date input */
    section[data-testid="stSidebar"] [data-testid="stDateInput"] input {
        color: #1a1a2e !important;
        background-color: white !important;
        font-weight: 600 !important;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #e74c3c, #c0392b);
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        margin: 20px 0 15px 0;
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

    /* Main background */
    .main { background-color: #f8f9fa; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'traffic_violations.db')

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM Violations", conn)
    conn.close()
    df['Date Of Stop'] = pd.to_datetime(df['Date Of Stop'], errors='coerce')
    return df

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def build_sidebar(df):
    st.sidebar.markdown("""
        <div style='text-align:center; padding: 10px 0 5px 0;'>
            <span style='font-size:3rem'>🚦</span>
            <h2 style='color:white; margin:5px 0; font-size:1.1rem;'>
                Traffic Violations<br>Insight System
            </h2>
            <p style='color:#bdc3c7; font-size:0.75rem; margin:0;'>
                2M+ Records | 2012–2025
            </p>
        </div>
        <hr style='border-color:#4a6278; margin:10px 0;'>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🔍 Filter Data")

    # Date range
    min_date = df['Date Of Stop'].min().date()
    max_date = df['Date Of Stop'].max().date()
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.sidebar.markdown("---")

    # Filters
    genders    = ['All'] + sorted(df['Gender'].dropna().unique().tolist())
    categories = ['All'] + sorted(df['ViolationCategory'].dropna().unique().tolist())
    top_makes  = ['All'] + df['Make'].value_counts().head(20).index.tolist()
    agencies   = ['All'] + sorted(df['SubAgency'].dropna().unique().tolist())
    vtypes     = ['All'] + sorted(df['Violation Type'].dropna().unique().tolist())

    gender   = st.sidebar.selectbox("👤 Gender",             genders)
    category = st.sidebar.selectbox("🚦 Violation Category", categories)
    make     = st.sidebar.selectbox("🚗 Vehicle Make",        top_makes)
    agency   = st.sidebar.selectbox("🏢 District",            agencies)
    vtype    = st.sidebar.selectbox("📋 Violation Type",      vtypes)

    st.sidebar.markdown("---")

    # Active filters summary
    active = sum([
        gender != 'All', category != 'All',
        make != 'All', agency != 'All', vtype != 'All'
    ])
    if active > 0:
        st.sidebar.markdown(
            f"<div style='background:#e74c3c;color:white;padding:8px 12px;"
            f"border-radius:8px;text-align:center;font-weight:600;'>"
            f"⚡ {active} active filter{'s' if active>1 else ''}</div>",
            unsafe_allow_html=True
        )

    st.sidebar.markdown("""
        <div style='text-align:center; margin-top:20px;
                    color:#7f8c8d; font-size:0.75rem;'>
            Built with Python & Streamlit<br>
        </div>
    """, unsafe_allow_html=True)

    return date_range, gender, category, make, agency, vtype


def apply_filters(df, date_range, gender, category, make, agency, vtype):
    f = df.copy()
    if len(date_range) == 2:
        f = f[(f['Date Of Stop'].dt.date >= date_range[0]) &
              (f['Date Of Stop'].dt.date <= date_range[1])]
    if gender   != 'All': f = f[f['Gender']           == gender]
    if category != 'All': f = f[f['ViolationCategory'] == category]
    if make     != 'All': f = f[f['Make']              == make]
    if agency   != 'All': f = f[f['SubAgency']         == agency]
    if vtype    != 'All': f = f[f['Violation Type']    == vtype]
    return f

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
def show_kpis(df):
    st.markdown(
        "<div class='section-header'>📊 Summary Statistics</div>",
        unsafe_allow_html=True
    )

    kpis = [
        ("🚦", "Total Violations",  f"{len(df):,}",              "#e74c3c"),
        ("💥", "Accidents",         f"{int(df['Accident'].sum()):,}", "#e67e22"),
        ("☠️", "Fatal",             f"{int(df['Fatal'].sum()):,}",    "#c0392b"),
        ("🍺", "Alcohol-Related",   f"{int(df['Alcohol'].sum()):,}",  "#8e44ad"),
        ("☢️", "HAZMAT",            f"{int(df['HAZMAT'].sum()):,}",   "#2980b9"),
    ]

    cols = st.columns(5)
    for col, (icon, label, value, color) in zip(cols, kpis):
        col.markdown(f"""
            <div style='background:white; border-radius:12px; padding:20px;
                        text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.08);
                        border-left:4px solid {color};'>
                <div style='font-size:1.8rem'>{icon}</div>
                <div style='font-size:1.6rem; font-weight:700;
                            color:#2c3e50;'>{value}</div>
                <div style='font-size:0.78rem; color:#7f8c8d;
                            text-transform:uppercase;
                            letter-spacing:1px;'>{label}</div>
            </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────
def make_chart_container(fig):
    """Wrap a plotly chart in a white card."""
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def show_charts(df):
    st.markdown(
        "<div class='section-header'>📈 Visual Analysis</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        vc = df['ViolationCategory'].value_counts().reset_index()
        vc.columns = ['Category', 'Count']
        fig = px.bar(
            vc, x='Count', y='Category', orientation='h',
            title='🚦 Violations by Category',
            color='Count',
            color_continuous_scale='Reds',
            template='plotly_white'
        )
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            showlegend=False,
            title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig.update_coloraxes(showscale=False)
        make_chart_container(fig)

    with col2:
        hourly = df['Hour'].value_counts().sort_index().reset_index()
        hourly.columns = ['Hour', 'Count']
        fig2 = px.area(
            hourly, x='Hour', y='Count',
            title='⏰ Violations by Hour of Day',
            color_discrete_sequence=['#e74c3c'],
            template='plotly_white'
        )
        fig2.update_layout(
            xaxis=dict(tickmode='linear', dtick=2),
            title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        make_chart_container(fig2)

    col3, col4 = st.columns(2)

    with col3:
        day_order = ['Monday','Tuesday','Wednesday',
                     'Thursday','Friday','Saturday','Sunday']
        daily = df['DayOfWeek'].value_counts().reindex(day_order).reset_index()
        daily.columns = ['Day', 'Count']
        fig3 = px.bar(
            daily, x='Day', y='Count',
            title='📅 Violations by Day of Week',
            color='Count',
            color_continuous_scale='Blues',
            template='plotly_white'
        )
        fig3.update_layout(
            title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig3.update_coloraxes(showscale=False)
        make_chart_container(fig3)

    with col4:
        tod = df['TimeOfDay'].value_counts().reset_index()
        tod.columns = ['TimeOfDay', 'Count']
        fig4 = px.pie(
            tod, names='TimeOfDay', values='Count',
            title='🌅 Violations by Time of Day',
            color_discrete_sequence=['#2ecc71','#e74c3c','#3498db','#f39c12'],
            hole=0.4,
            template='plotly_white'
        )
        fig4.update_layout(
            title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        make_chart_container(fig4)

    col5, col6 = st.columns(2)

    with col5:
        makes = df['Make'].value_counts().head(10).reset_index()
        makes.columns = ['Make', 'Count']
        fig5 = px.bar(
            makes, x='Count', y='Make', orientation='h',
            title='🚗 Top 10 Vehicle Makes',
            color='Count',
            color_continuous_scale='Viridis',
            template='plotly_white'
        )
        fig5.update_layout(
            yaxis={'categoryorder':'total ascending'},
            title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig5.update_coloraxes(showscale=False)
        make_chart_container(fig5)

    with col6:
        # Monthly trend
        monthly = df.groupby('Month').size().reset_index(name='Count')
        month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                       7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        monthly['Month'] = monthly['Month'].map(month_names)
        fig6 = px.line(
            monthly, x='Month', y='Count',
            title='📆 Monthly Violation Trend',
            markers=True,
            color_discrete_sequence=['#2ecc71'],
            template='plotly_white'
        )
        fig6.update_layout(
            title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig6.update_traces(line_width=3, marker_size=8)
        make_chart_container(fig6)

    # Full-width race chart
    st.markdown(
        "<div class='section-header'>👥 Demographics Analysis</div>",
        unsafe_allow_html=True
    )
    col7, col8 = st.columns(2)

    with col7:
        race = df['Race'].value_counts().reset_index()
        race.columns = ['Race', 'Count']
        fig7 = px.bar(
            race, x='Race', y='Count',
            title='🌍 Violations by Race',
            color='Race',
            color_discrete_sequence=px.colors.qualitative.Set2,
            template='plotly_white'
        )
        fig7.update_layout(
            showlegend=False, title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        make_chart_container(fig7)

    with col8:
        gender_df = df['Gender'].value_counts().reset_index()
        gender_df.columns = ['Gender', 'Count']
        fig8 = px.pie(
            gender_df, names='Gender', values='Count',
            title='👤 Violations by Gender',
            color_discrete_sequence=['#3498db','#e74c3c','#95a5a6'],
            hole=0.4,
            template='plotly_white'
        )
        fig8.update_layout(
            title_font_size=14,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig8.update_traces(textposition='inside', textinfo='percent+label')
        make_chart_container(fig8)

# ─────────────────────────────────────────────
# MAP
# ─────────────────────────────────────────────
def show_map(df):
    st.markdown(
        "<div class='section-header'>🗺️ Geographic Hotspot Analysis</div>",
        unsafe_allow_html=True
    )

    map_df = df[['Latitude','Longitude','ViolationCategory','Accident']].dropna()
    map_df = map_df[
        map_df['Latitude'].between(24, 50) &
        map_df['Longitude'].between(-125, -65)
    ]

    col1, col2, col3 = st.columns(3)
    col1.metric("📍 Valid Coordinates", f"{len(map_df):,}")
    col2.metric("💥 Accidents on Map", f"{map_df['Accident'].sum():,.1f}")
    col3.metric("🗺️ Sample Displayed", "50,000")

    st.markdown("<br>", unsafe_allow_html=True)

    # Map type selector
    map_type = st.radio(
        "🗺️ Map Type",
        ["🔥 Density Heatmap", "📍 Scatter Points"],
        horizontal=True
    )

    sample = map_df.sample(min(55000, len(map_df)), random_state=42)

    if "Density" in map_type:
        fig = px.density_mapbox(
            sample,
            lat='Latitude', lon='Longitude',
            radius=6, zoom=9,
            center={"lat": 39.1, "lon": -77.2},
            mapbox_style="open-street-map",
            title="🔥 Traffic Violation Density Heatmap",
            color_continuous_scale="YlOrRd"
        )
    else:
        fig = px.scatter_mapbox(
            sample,
            lat='Latitude', lon='Longitude',
            color='ViolationCategory',
            zoom=9,
            center={"lat": 39.1, "lon": -77.2},
            mapbox_style="open-street-map",
            title="📍 Traffic Violation Scatter Map",
            opacity=0.4,
            size_max=5
        )

    fig.update_layout(
        height=700,
        margin=dict(l=0, r=0, t=40, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# DATA TABLE
# ─────────────────────────────────────────────
def show_table(df):
    st.markdown(
        "<div class='section-header'>🗄️ Raw Data Explorer</div>",
        unsafe_allow_html=True
    )

    # Search box
    search = st.text_input("🔎 Search description or location...", "")

    display_cols = [
        'Date Of Stop','Time Of Stop','SubAgency','Description',
        'ViolationCategory','Violation Type','Make','Model',
        'Color','Year','Gender','Race','Accident','Fatal','Alcohol','HAZMAT'
    ]
    available = [c for c in display_cols if c in df.columns]
    display_df = df[available].copy()

    if search:
        mask = (
            display_df['Description'].astype(str).str.contains(search, case=False, na=False) |
            display_df['SubAgency'].astype(str).str.contains(search, case=False, na=False)
        )
        display_df = display_df[mask]

    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total Rows",    f"{len(df):,}")
    col2.metric("🔍 Filtered Rows", f"{len(display_df):,}")
    col3.metric("📊 Columns",       f"{len(available)}")

    st.dataframe(
        display_df.head(500),
        use_container_width=True,
        height=420
    )

    csv = display_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_violations.csv",
        mime="text/csv",
        use_container_width=True
    )

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #c0392b, #e74c3c);
                    padding: 25px 30px; border-radius: 12px;
                    margin-bottom: 20px;'>
            <h1 style='color:white; margin:0; font-size:2rem;'>
                🚦 Traffic Violations Insight System
            </h1>
            <p style='color:rgba(255,255,255,0.85); margin:5px 0 0 0;
                      font-size:1rem;'>
                Interactive analytics dashboard | Montgomery County, MD |
                2,070,115 records | 2012–2025
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("⏳ Loading data..."):
        df = load_data()

    date_range, gender, category, make, agency, vtype = build_sidebar(df)
    filtered_df = apply_filters(df, date_range, gender, category,
                                make, agency, vtype)

    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches your filters. Please adjust the sidebar.")
        return

    # Filter status bar
    pct = len(filtered_df) / len(df) * 100
    st.markdown(f"""
        <div style='background:#eafaf1; border:1px solid #2ecc71;
                    border-radius:8px; padding:10px 15px;
                    display:flex; align-items:center; gap:10px;
                    margin-bottom:15px;'>
            <span style='color:#27ae60; font-size:1.2rem;'>✅</span>
            <span style='color:#27ae60; font-weight:600;'>
                Showing <strong>{len(filtered_df):,}</strong> records
                ({pct:.1f}% of total dataset)
            </span>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📊  Charts & Insights",
        "🗺️  Geographic Map",
        "🗄️  Raw Data"
    ])

    with tab1:
        show_kpis(filtered_df)
        show_charts(filtered_df)

    with tab2:
        show_map(filtered_df)

    with tab3:
        show_table(filtered_df)


if __name__ == "__main__":
    main()