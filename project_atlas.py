import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from sklearn.cluster import KMeans
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Atlas | Logistics Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ENTERPRISE CSS INJECTION
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

/* ── Reset & Root ── */
:root {
    --bg-base:        #080C14;
    --bg-surface:     #0D1421;
    --bg-elevated:    #111827;
    --bg-card:        #141D2E;
    --bg-card-hover:  #182236;
    --border:         rgba(255,255,255,0.06);
    --border-accent:  rgba(0,209,162,0.35);
    --text-primary:   #F0F4FF;
    --text-secondary: #8B9BB8;
    --text-muted:     #6B7A99;
    --accent:         #00D1A2;
    --accent-dim:     rgba(0,209,162,0.12);
    --accent-glow:    rgba(0,209,162,0.25);
    --warn:           #F5A623;
    --danger:         #FF4D6A;
    --info:           #4E9AF1;
    --radius-sm:      6px;
    --radius-md:      10px;
    --radius-lg:      16px;
    --shadow-card:    0 1px 3px rgba(0,0,0,0.4), 0 4px 20px rgba(0,0,0,0.3);
    --shadow-accent:  0 0 30px rgba(0,209,162,0.12);
    --font-sans:      'DM Sans', sans-serif;
    --font-mono:      'DM Mono', monospace;
    --font-display:   'Syne', sans-serif;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: var(--font-sans);
    background-color: var(--bg-base);
    color: var(--text-primary);
}

/* Remove default Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header {
    height: 0px;
    overflow: visible;
}
.block-container {
    padding: 1.5rem 2.5rem 3rem 2.5rem;
    max-width: 1600px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: #2A3550; border-radius: 4px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.25rem;
}
[data-testid="stSidebar"] * {
    font-family: var(--font-sans) !important;
}

/* ── Sidebar collapse/expand arrow — broad selectors to catch all Streamlit versions ── */
/* The floating arrow button when sidebar is collapsed */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapsedControl"] button {
    background: #1A2540 !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    color: #F0F4FF !important;
}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] button svg {
    fill: #F0F4FF !important;
    color: #F0F4FF !important;
    stroke: #F0F4FF !important;
}
/* The close arrow inside the sidebar */
[data-testid="stSidebarCollapseButton"] button {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
    color: #F0F4FF !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stSidebarCollapseButton"] button svg {
    fill: #F0F4FF !important;
    color: #F0F4FF !important;
    stroke: #F0F4FF !important;
}
/* Fallback: any button directly inside the sidebar wrapper divs */
section[data-testid="stSidebar"] > div:first-child > button,
section[data-testid="stSidebar"] > div > div > button {
    color: #F0F4FF !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] > div:first-child > button svg,
section[data-testid="stSidebar"] > div > div > button svg {
    fill: #F0F4FF !important;
    color: #F0F4FF !important;
}
/* Universal: any SVG inside sidebar that looks like a nav arrow */
[data-testid="stSidebar"] button:not([aria-label*="collapse"]) svg {
    fill: #F0F4FF !important;
}
/* Widget labels */
label, .stTextInput label, .stSelectbox label,
.stMultiSelect label, .stSlider label,
[data-testid="stWidgetLabel"] {
    color: #8B9BB8 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}

/* Widget inputs */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius-sm) !important;
    color: #F0F4FF !important;
}

/* Multiselect tags */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(0,209,162,0.15) !important;
    color: #00D1A2 !important;
}

/* Dropdown options */
[data-testid="stSelectbox"] ul li,
[data-testid="stMultiSelect"] ul li {
    color: #F0F4FF !important;
    background: #111827 !important;
}

/* Selectbox arrow icon */
[data-testid="stSelectbox"] svg {
    color: #8B9BB8 !important;
    fill: #8B9BB8 !important;
}

/* Sidebar section label class */
.sidebar-section {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8B9BB8;
    padding: 1.25rem 0 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0.85rem;
}

/* Expander */
[data-testid="stExpander"] summary {
    background: #0D1421 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: var(--radius-md) !important;
    color: #F0F4FF !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stExpander"] summary svg {
    color: #8B9BB8 !important;
    fill: #8B9BB8 !important;
}

.stDownloadButton > button {
    background: var(--accent-dim) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,209,162,0.2) !important;
    box-shadow: 0 0 20px var(--accent-glow) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--bg-elevated) !important;
    color: var(--text-secondary) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}
[data-testid="stDataFrame"] td {
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
    color: var(--text-primary) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem 1.4rem;
    box-shadow: var(--shadow-card);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,209,162,0.04) 0%, transparent 60%);
    pointer-events: none;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-card), var(--shadow-accent);
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    font-family: var(--font-mono) !important;
}

/* ── Info/Alert boxes ── */
[data-testid="stInfo"] {
    background: rgba(78,154,241,0.08) !important;
    border: 1px solid rgba(78,154,241,0.25) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}
[data-testid="stInfo"] svg { color: var(--info) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 0.5rem 0 !important; }

/* ── selectbox label ── */
.stSelectbox label, .stMultiSelect label, .stSlider label {
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}


/* ── FORCE SIDEBAR TOGGLE VISIBILITY ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 9999 !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_delivery_data():
    np.random.seed(42)
    base_lat, base_lon = 6.4281, 3.4215
    n = 80
    data = pd.DataFrame({
        'order_id':        [f"ORD-{i:04d}" for i in range(1, n+1)],
        'lat':             base_lat + np.random.uniform(-0.07, 0.07, n),
        'lon':             base_lon + np.random.uniform(-0.07, 0.07, n),
        'weight_kg':       np.random.randint(5, 120, n),
        'priority':        np.random.choice(['Critical', 'High', 'Medium', 'Low'], n,
                               p=[0.1, 0.3, 0.4, 0.2]),
        'delivery_status': np.random.choice(['Pending', 'In-Transit', 'Delayed'], n,
                               p=[0.45, 0.40, 0.15]),
        'eta_minutes':     np.random.randint(15, 180, n),
        'customer':        [f"Client-{np.random.randint(100,999)}" for _ in range(n)],
    })
    return data

df_raw = load_delivery_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo / Brand
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding-bottom:1.25rem;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:0.5rem;">
        <div style="width:34px;height:34px;background:linear-gradient(135deg,#00D1A2,#007AFF);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">🛰️</div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1rem;color:#F0F4FF;letter-spacing:0.03em;">ATLAS</div>
            <div style="font-size:0.62rem;color:#6B7A99;letter-spacing:0.1em;text-transform:uppercase;">Logistics Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Operations Filter</div>', unsafe_allow_html=True)
    priority_filter = st.multiselect(
        "Priority Tier",
        options=['Critical', 'High', 'Medium', 'Low'],
        default=['Critical', 'High', 'Medium', 'Low']
    )
    status_filter = st.multiselect(
        "Delivery Status",
        options=['Pending', 'In-Transit', 'Delayed'],
        default=['Pending', 'In-Transit', 'Delayed']
    )

    st.markdown('<div class="sidebar-section">Fleet Configuration</div>', unsafe_allow_html=True)
    num_trucks = st.slider("Active Trucks", min_value=2, max_value=12, value=6)
    map_style = st.selectbox("Map Mode", ["3D Density Heatmap", "Zone Scatter"])

    st.markdown('<div class="sidebar-section">Export</div>', unsafe_allow_html=True)
    # Download button rendered after data is processed (see bottom)

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
df = df_raw[
    df_raw['priority'].isin(priority_filter) &
    df_raw['delivery_status'].isin(status_filter)
].copy()

if df.empty:
    st.warning("No orders match current filters. Adjust your sidebar selections.")
    st.stop()

# ─────────────────────────────────────────────
# ZONE OPTIMIZATION
# ─────────────────────────────────────────────
@st.cache_data
def optimize_zones(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    data = data.copy()
    data['zone_id'] = kmeans.fit_predict(data[['lat', 'lon']])
    return data

df = optimize_zones(df, min(num_trucks, len(df)))

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:1.75rem;">
    <div style="display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
        <div>
            <h1 style="font-family:'Syne',sans-serif;font-size:1.85rem;font-weight:800;
                       margin:0;color:#F0F4FF;letter-spacing:-0.01em;line-height:1.1;">
                Fleet &amp; Route Command Center
            </h1>
            <p style="margin:0.35rem 0 0;color:#8B9BB8;font-size:0.85rem;font-weight:400;">
                Lagos Metro · Live Simulation · <span style="color:#00D1A2;font-family:'DM Mono',monospace;">●</span> Operational
            </p>
        </div>
        <div style="display:flex;align-items:center;gap:0.5rem;background:#0D1421;
                    border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:0.45rem 0.85rem;">
            <span style="width:7px;height:7px;background:#00D1A2;border-radius:50%;
                         box-shadow:0 0 8px #00D1A2;display:inline-block;"></span>
            <span style="font-size:0.75rem;color:#8B9BB8;font-family:'DM Mono',monospace;">
                LIVE · {t}
            </span>
        </div>
    </div>
</div>
""".format(t=pd.Timestamp.now().strftime("%H:%M:%S")), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

pending   = len(df[df['delivery_status']=='Pending'])
intransit = len(df[df['delivery_status']=='In-Transit'])
delayed   = len(df[df['delivery_status']=='Delayed'])

with k1:
    st.metric("Total Orders", len(df), f"+{np.random.randint(2,8)} today")
with k2:
    st.metric("Total Payload", f"{df['weight_kg'].sum():,} kg", f"{df['weight_kg'].mean():.0f} kg avg")
with k3:
    st.metric("In-Transit", intransit, f"{intransit/len(df)*100:.0f}% of fleet")
with k4:
    st.metric("Est. Fuel Cost", "₦450,000", "-5.2% vs last wk")
with k5:
    st.metric("Fleet Efficiency", "92.4%", "+2.1%")

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATUS BADGE ROW
# ─────────────────────────────────────────────
PRIORITY_COLORS = {'Critical':'#FF4D6A','High':'#F5A623','Medium':'#4E9AF1','Low':'#8B9BB8'}
STATUS_COLORS   = {'Pending':'#F5A623','In-Transit':'#00D1A2','Delayed':'#FF4D6A'}

priority_counts = df['priority'].value_counts()
status_counts   = df['delivery_status'].value_counts()

badges_html = "<div style='display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:1.5rem;'>"
for p, c in priority_counts.items():
    color = PRIORITY_COLORS.get(p, '#8B9BB8')
    badges_html += f"""
    <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);
                border-radius:6px;padding:0.35rem 0.7rem;display:flex;align-items:center;gap:0.4rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:{color};display:inline-block;"></span>
        <span style="font-size:0.75rem;color:#8B9BB8;">{p}</span>
        <span style="font-size:0.78rem;font-weight:600;font-family:'DM Mono',monospace;color:#F0F4FF;">{c}</span>
    </div>"""
badges_html += "<div style='width:1px;background:rgba(255,255,255,0.08);margin:0 0.2rem;'></div>"
for s, c in status_counts.items():
    color = STATUS_COLORS.get(s, '#8B9BB8')
    badges_html += f"""
    <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);
                border-radius:6px;padding:0.35rem 0.7rem;display:flex;align-items:center;gap:0.4rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:{color};display:inline-block;"></span>
        <span style="font-size:0.75rem;color:#8B9BB8;">{s}</span>
        <span style="font-size:0.78rem;font-weight:600;font-family:'DM Mono',monospace;color:#F0F4FF;">{c}</span>
    </div>"""
badges_html += "</div>"
st.markdown(badges_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAP SECTION
# ─────────────────────────────────────────────
map_col, insight_col = st.columns([3, 1])

with map_col:
    st.markdown("""
    <div style="margin-bottom:0.6rem;display:flex;align-items:center;justify-content:space-between;">
        <div>
            <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#F0F4FF;">
                Delivery Density Map
            </span>
            <span style="margin-left:0.6rem;font-size:0.72rem;color:#6B7A99;font-family:'DM Mono',monospace;">
                Lagos Metro · {n} active nodes
            </span>
        </div>
    </div>
    """.format(n=len(df)), unsafe_allow_html=True)

    if map_style == "3D Density Heatmap":
        layer = pdk.Layer(
            "HexagonLayer", df,
            get_position=["lon", "lat"],
            auto_highlight=True,
            elevation_scale=60,
            pickable=True,
            elevation_range=[0, 1200],
            extruded=True,
            coverage=1,
            color_range=[
                [0, 30, 60, 200],
                [0, 80, 120, 210],
                [0, 140, 160, 220],
                [0, 200, 162, 230],
                [80, 240, 200, 240],
                [200, 255, 230, 255],
            ]
        )
    else:
        # Scatter colored by zone
        zone_colors = [
            [0,209,162],[78,154,241],[245,166,35],[255,77,106],
            [165,105,255],[255,165,0],[0,200,255],[255,100,200]
        ]
        df['color'] = df['zone_id'].apply(lambda z: zone_colors[z % len(zone_colors)])
        layer = pdk.Layer(
            "ScatterplotLayer", df,
            get_position=["lon", "lat"],
            get_color="color",
            get_radius=100,
            pickable=True,
            auto_highlight=True,
        )

    view_state = pdk.ViewState(
        latitude=6.4281, longitude=3.4215,
        zoom=11.5, pitch=45 if map_style == "3D Density Heatmap" else 20
    )
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Orders: {elevationValue}" if map_style == "3D Density Heatmap" else "Order: {order_id}\nZone: {zone_id}"},
        map_style="mapbox://styles/mapbox/dark-v11",
    )
    st.pydeck_chart(deck, use_container_width=True)

with insight_col:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
                color:#F0F4FF;margin-bottom:0.75rem;">
        Network Insights
    </div>
    """, unsafe_allow_html=True)

    # Insight cards
    def insight_card(icon, label, value, sub="", color="#00D1A2"):
        return f"""
        <div style="background:var(--bg-card,#141D2E);border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:0.85rem 1rem;margin-bottom:0.6rem;
                    border-left:3px solid {color};">
            <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;
                        color:#6B7A99;font-weight:500;margin-bottom:0.2rem;">{icon} {label}</div>
            <div style="font-family:'DM Mono',monospace;font-size:1.05rem;
                        font-weight:500;color:#F0F4FF;">{value}</div>
            {f'<div style="font-size:0.7rem;color:#6B7A99;margin-top:0.15rem;">{sub}</div>' if sub else ''}
        </div>"""

    delayed_pct  = f"{delayed/len(df)*100:.1f}%"
    avg_eta      = f"{df['eta_minutes'].mean():.0f} min"
    critical_cnt = len(df[df['priority']=='Critical'])
    heaviest     = df.nlargest(1,'weight_kg').iloc[0]

    st.markdown(
        insight_card("⚡","Critical Orders", str(critical_cnt), "require immediate dispatch", "#FF4D6A") +
        insight_card("⏱","Avg ETA", avg_eta, "across active routes", "#4E9AF1") +
        insight_card("⚠️","Delayed Rate", delayed_pct, f"{delayed} shipments affected", "#F5A623") +
        insight_card("🏋","Heaviest Load", f"{heaviest['weight_kg']} kg", heaviest['order_id'], "#00D1A2"),
        unsafe_allow_html=True
    )

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ZONE OPTIMIZATION TABLE
# ─────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.85rem;">
    <div style="width:3px;height:1.4rem;background:linear-gradient(180deg,#00D1A2,#007AFF);border-radius:2px;"></div>
    <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#F0F4FF;">
        Automated Zone Assignment — {n} Trucks
    </span>
</div>
""".format(n=num_trucks), unsafe_allow_html=True)

zone_col, table_col = st.columns([1, 1])

with zone_col:
    zone_stats = df.groupby('zone_id').agg(
        Orders=('order_id','count'),
        Total_Load_kg=('weight_kg','sum'),
        Avg_ETA_min=('eta_minutes','mean'),
        Critical=('priority', lambda x: (x=='Critical').sum()),
        Delayed=('delivery_status', lambda x: (x=='Delayed').sum()),
    ).reset_index()
    zone_stats.columns = ['Zone','Orders','Load (kg)','Avg ETA (min)','Critical','Delayed']
    zone_stats['Zone'] = zone_stats['Zone'].apply(lambda z: f"Truck {z+1:02d}")
    zone_stats['Avg ETA (min)'] = zone_stats['Avg ETA (min)'].round(0).astype(int)
    st.dataframe(zone_stats, use_container_width=True, hide_index=True)

with table_col:
    # Per-zone efficiency gauge - build full HTML string first, then render once
    max_orders = zone_stats['Orders'].max()
    gauge_rows = ""
    for _, row in zone_stats.iterrows():
        pct = int(row['Orders'] / max_orders * 100)
        bar_color = "#FF4D6A" if row['Critical'] > 0 else "#00D1A2"
        zone_name = row['Zone']
        orders_val = row['Orders']
        load_val = row['Load (kg)']
        gauge_rows += (
            '<div style="margin-bottom:0.65rem;">'
            '<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.25rem;">'
            f'<span style="font-size:0.75rem;color:#8B9BB8;font-family:\'DM Sans\',sans-serif;">{zone_name}</span>'
            f'<span style="font-size:0.72rem;font-family:\'DM Mono\',monospace;color:#F0F4FF;">{orders_val} orders · {load_val} kg</span>'
            '</div>'
            '<div style="height:6px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;">'
            f'<div style="width:{pct}%;height:100%;background:{bar_color};border-radius:3px;"></div>'
            '</div>'
            '</div>'
        )
    gauge_full = (
        '<div style="background:#0D1421;border:1px solid rgba(255,255,255,0.06);'
        'border-radius:10px;padding:1.1rem 1.2rem;margin-top:0.15rem;">'
        '<div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;'
        'color:#8B9BB8;font-weight:600;margin-bottom:0.9rem;">Load Distribution</div>'
        + gauge_rows +
        '</div>'
    )
    st.markdown(gauge_full, unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAVINGS FORECAST
# ─────────────────────────────────────────────
def calculate_efficiency(data):
    std_vals = data.groupby('zone_id')[['lat','lon']].std().mean()
    savings = (1 / (std_vals.sum() + 1e-9)) * 100
    return min(savings, 99.9)

savings_val = calculate_efficiency(df)

st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(0,209,162,0.07) 0%,rgba(0,122,255,0.05) 100%);
            border:1px solid rgba(0,209,162,0.2);border-radius:12px;
            padding:1.1rem 1.4rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:1rem;">
    <div style="font-size:1.6rem;">💡</div>
    <div>
        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                    color:#00D1A2;font-weight:600;margin-bottom:0.2rem;">Optimization Insight</div>
        <div style="color:#F0F4FF;font-size:0.88rem;line-height:1.5;">
            Grouping deliveries into <strong style="color:#00D1A2;">{num_trucks} optimized zones</strong> 
            reduces deadhead miles by an estimated <strong style="color:#00D1A2;">{savings_val:.1f}%</strong> 
            this week — saving approximately <strong>₦{int(savings_val * 4500):,}</strong> in fuel overhead.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DISPATCH CONTROL CENTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.85rem;">
    <div style="width:3px;height:1.4rem;background:linear-gradient(180deg,#4E9AF1,#00D1A2);border-radius:2px;"></div>
    <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#F0F4FF;">
        Dispatch Control &amp; Order Deep-Dive
    </span>
</div>
""", unsafe_allow_html=True)

search_col, detail_col = st.columns([1, 2])

with search_col:
    selected_order = st.selectbox("Select Order ID", df['order_id'].tolist(), label_visibility="collapsed")
    order_info = df[df['order_id'] == selected_order].iloc[0]

    # Mini order list (top 8) - build full string then render once
    list_rows = ""
    for _, row in df.head(8).iterrows():
        sc = STATUS_COLORS.get(row['delivery_status'], '#8B9BB8')
        pc = PRIORITY_COLORS.get(row['priority'], '#8B9BB8')
        is_sel = row['order_id'] == selected_order
        bg = "rgba(0,209,162,0.07)" if is_sel else "transparent"
        oid = row['order_id']
        list_rows += (
            f'<div style="padding:0.45rem 0.85rem;border-bottom:1px solid rgba(255,255,255,0.04);'
            f'background:{bg};display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-family:\'DM Mono\',monospace;font-size:0.75rem;color:#F0F4FF;">{oid}</span>'
            f'<div style="display:flex;gap:0.35rem;align-items:center;">'
            f'<span style="width:6px;height:6px;border-radius:50%;background:{pc};display:inline-block;"></span>'
            f'<span style="width:6px;height:6px;border-radius:50%;background:{sc};display:inline-block;"></span>'
            f'</div>'
            f'</div>'
        )
    list_full = (
        '<div style="margin-top:0.75rem;background:#0D1421;border:1px solid rgba(255,255,255,0.06);border-radius:10px;overflow:hidden;">'
        '<div style="padding:0.55rem 0.85rem;background:rgba(255,255,255,0.03);font-size:0.65rem;'
        'text-transform:uppercase;letter-spacing:0.1em;color:#8B9BB8;font-weight:600;'
        'border-bottom:1px solid rgba(255,255,255,0.05);">Recent Orders</div>'
        + list_rows +
        '</div>'
    )
    st.markdown(list_full, unsafe_allow_html=True)

with detail_col:
    pc   = PRIORITY_COLORS.get(order_info['priority'], '#8B9BB8')
    sc   = STATUS_COLORS.get(order_info['delivery_status'], '#8B9BB8')
    zone = int(order_info['zone_id'])

    # Convert hex colors to rgba for transparent backgrounds (avoids broken {pc}1A CSS hack)
    def hex_to_rgba(hex_color, alpha):
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return f"rgba({r},{g},{b},{alpha})"

    pc_bg     = hex_to_rgba(pc, 0.12)
    pc_border = hex_to_rgba(pc, 0.35)
    sc_bg     = hex_to_rgba(sc, 0.12)
    sc_border = hex_to_rgba(sc, 0.35)

    oid        = order_info['order_id']
    priority   = order_info['priority']
    status     = order_info['delivery_status']
    customer   = order_info['customer']
    weight     = order_info['weight_kg']
    eta        = order_info['eta_minutes']
    truck_num  = f"{zone+1:02d}"
    lat_str    = f"{order_info['lat']:.6f}"
    lon_str    = f"{order_info['lon']:.6f}"

    ticket_html = (
        '<div style="background:linear-gradient(135deg,#111827 0%,#0D1421 100%);'
        'border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.4rem 1.6rem;">'

        # Corner glow
        '<div style="position:relative;">'
        '<div style="position:absolute;top:-1.4rem;right:-1.6rem;width:120px;height:120px;'
        'background:radial-gradient(circle at top right,rgba(0,209,162,0.08),transparent 70%);'
        'pointer-events:none;border-radius:14px;"></div>'
        '</div>'

        # Header row
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.1rem;">'
        '<div>'
        '<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.12em;color:#6B7A99;margin-bottom:0.25rem;">Dispatch Ticket</div>'
        f'<div style="font-family:\'Syne\',sans-serif;font-size:1.3rem;font-weight:800;color:#F0F4FF;">{oid}</div>'
        '</div>'
        '<div style="display:flex;flex-direction:column;align-items:flex-end;gap:0.35rem;">'
        f'<span style="background:{pc_bg};border:1px solid {pc_border};border-radius:5px;'
        f'padding:0.2rem 0.65rem;font-size:0.72rem;color:{pc};font-weight:600;">{priority}</span>'
        f'<span style="background:{sc_bg};border:1px solid {sc_border};border-radius:5px;'
        f'padding:0.2rem 0.65rem;font-size:0.72rem;color:{sc};font-weight:600;">{status}</span>'
        '</div>'
        '</div>'

        # Fields grid
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem 1.25rem;">'

        '<div>'
        '<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:#6B7A99;margin-bottom:0.2rem;">Assigned Truck</div>'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.9rem;color:#00D1A2;font-weight:500;">Truck {truck_num} &middot; Zone {zone}</div>'
        '</div>'

        '<div>'
        '<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:#6B7A99;margin-bottom:0.2rem;">Customer</div>'
        f'<div style="font-size:0.88rem;color:#F0F4FF;">{customer}</div>'
        '</div>'

        '<div>'
        '<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:#6B7A99;margin-bottom:0.2rem;">Payload</div>'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.9rem;color:#F0F4FF;">{weight} kg</div>'
        '</div>'

        '<div>'
        '<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:#6B7A99;margin-bottom:0.2rem;">ETA</div>'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.9rem;color:#4E9AF1;">~{eta} min</div>'
        '</div>'

        '<div style="grid-column:span 2;">'
        '<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:#6B7A99;margin-bottom:0.2rem;">GPS Coordinates</div>'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.82rem;color:#8B9BB8;">{lat_str}, {lon_str}</div>'
        '</div>'

        '</div>'  # end grid
        '</div>'  # end card
    )
    st.markdown(ticket_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ORDER TABLE
# ─────────────────────────────────────────────
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

with st.expander("📋  Full Order Manifest", expanded=False):
    display_df = df[['order_id','customer','priority','delivery_status',
                     'weight_kg','eta_minutes','lat','lon','zone_id']].copy()
    display_df['zone_id'] = display_df['zone_id'].apply(lambda z: f"Truck {z+1:02d}")
    display_df.columns = ['Order ID','Customer','Priority','Status',
                          'Weight (kg)','ETA (min)','Lat','Lon','Zone']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# SIDEBAR DOWNLOAD (needs df to be ready)
# ─────────────────────────────────────────────
@st.cache_data
def convert_df(d):
    return d.to_csv(index=False).encode('utf-8')

with st.sidebar:
    st.download_button(
        label="↓  Download Dispatch Schedule",
        data=convert_df(df),
        file_name='atlas_dispatch_log.csv',
        mime='text/csv',
    )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-top:2.5rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.05);
            display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
    <div style="display:flex;align-items:center;gap:0.6rem;">
        <div style="width:18px;height:18px;background:linear-gradient(135deg,#00D1A2,#007AFF);
                    border-radius:4px;"></div>
        <span style="font-family:'Syne',sans-serif;font-size:0.78rem;font-weight:700;
                     color:#8B9BB8;letter-spacing:0.05em;">ATLAS</span>
        <span style="font-size:0.72rem;color:#6B7A99;">by Nexus Tech Analytics</span>
    </div>
    <div style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#6B7A99;letter-spacing:0.05em;">
        Framework v2.0 · Lagos Metro Simulation
    </div>
</div>
""", unsafe_allow_html=True)
