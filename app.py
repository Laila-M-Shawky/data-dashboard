import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Arabic:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans Arabic', sans-serif;
}
.stApp { background-color: #0f1117; }

.metric-card {
    background: linear-gradient(135deg, #1a1d27 0%, #12151f 100%);
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 20px;
    margin: 6px 0;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #4f8ef7; }
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #4f8ef7;
    margin: 0;
}
.metric-label {
    font-size: 0.85rem;
    color: #8891a4;
    margin: 4px 0 0 0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #c8cdd8;
    border-left: 3px solid #4f8ef7;
    padding-left: 12px;
    margin: 24px 0 16px 0;
}
div[data-testid="stSidebar"] {
    background-color: #12151f;
    border-right: 1px solid #2a2d3e;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Data Dashboard")
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "ارفع ملف CSV",
        type=["csv"],
        help="الملف لازم يكون بصيغة CSV"
    )

    st.markdown("---")
    st.markdown("<span style='color:#8891a4; font-size:0.8rem'>Made with Streamlit ⚡</span>",
                unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

def get_sample_data():
    np.random.seed(42)
    n = 200
    return pd.DataFrame({
        "التاريخ": pd.date_range("2024-01-01", periods=n, freq="D"),
        "المبيعات": np.random.randint(1000, 9000, n),
        "الأرباح": np.random.randint(200, 3000, n),
        "المنطقة": np.random.choice(["القاهرة", "الإسكندرية", "الجيزة", "أسوان"], n),
        "الفئة": np.random.choice(["إلكترونيات", "ملابس", "أغذية", "أثاث"], n),
        "التقييم": np.round(np.random.uniform(2.5, 5.0, n), 1),
    })

if uploaded_file:
    df = load_data(uploaded_file)
    st.toast("✅ تم تحميل الملف بنجاح!", icon="✅")
else:
    df = get_sample_data()
    st.info("💡 لا يوجد ملف محمّل — يتم عرض **بيانات تجريبية**. ارفع ملف CSV من الشريط الجانبي.", icon="ℹ️")

# ── Header ───────────────────────────────────────────────────
st.markdown("# 📊 لوحة تحليل البيانات")
st.markdown(f"<span style='color:#8891a4'>{df.shape[0]:,} صف · {df.shape[1]} عمود</span>",
            unsafe_allow_html=True)

st.markdown("---")

# ── KPI Cards ────────────────────────────────────────────────
num_cols = df.select_dtypes(include="number").columns.tolist()

if num_cols:
    st.markdown('<div class="section-header">المؤشرات الرئيسية</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(num_cols), 4))
    for i, col in enumerate(num_cols[:4]):
        val = df[col].sum()
        mean = df[col].mean()
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{val:,.0f}</p>
                <p class="metric-label">إجمالي {col}</p>
                <p style="color:#4f8ef7; font-size:0.8rem; margin:6px 0 0 0">متوسط: {mean:,.1f}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("")

# ── Charts row ───────────────────────────────────────────────
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
date_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

CHART_BG = "#12151f"
GRID_COLOR = "#2a2d3e"
FONT_COLOR = "#c8cdd8"

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=FONT_COLOR, family="IBM Plex Sans Arabic"),
        margin=dict(l=16, r=16, t=40, b=16),
        legend=dict(bgcolor=CHART_BG, bordercolor=CHART_BG),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig

col1, col2 = st.columns(2)

# Chart 1: Line / Bar over time or index
with col1:
    st.markdown('<div class="section-header">التوزيع الزمني</div>', unsafe_allow_html=True)
    if num_cols:
        y_col = st.selectbox("اختر العمود", num_cols, key="line_y")
        if date_cols:
            fig = px.line(df, x=date_cols[0], y=y_col,
                          color_discrete_sequence=["#4f8ef7"])
        else:
            fig = px.bar(df.reset_index(), x="index", y=y_col,
                         color_discrete_sequence=["#4f8ef7"])
        st.plotly_chart(style_fig(fig), use_container_width=True)

# Chart 2: Category breakdown
with col2:
    st.markdown('<div class="section-header">التوزيع حسب الفئة</div>', unsafe_allow_html=True)
    if cat_cols and num_cols:
        cat_col = st.selectbox("اختر الفئة", cat_cols, key="cat_col")
        val_col = st.selectbox("اختر القيمة", num_cols, key="cat_val")
        grp = df.groupby(cat_col)[val_col].sum().reset_index().sort_values(val_col, ascending=False)
        fig2 = px.bar(grp, x=cat_col, y=val_col,
                      color=val_col,
                      color_continuous_scale=["#1a2a4a", "#4f8ef7"],
                      text_auto=True)
        fig2.update_traces(textfont_color=FONT_COLOR)
        st.plotly_chart(style_fig(fig2), use_container_width=True)

# ── Second row ───────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">التوزيع (Histogram)</div>', unsafe_allow_html=True)
    if num_cols:
        hist_col = st.selectbox("اختر العمود", num_cols, key="hist")
        fig3 = px.histogram(df, x=hist_col, nbins=30,
                            color_discrete_sequence=["#34d399"])
        st.plotly_chart(style_fig(fig3), use_container_width=True)

with col4:
    st.markdown('<div class="section-header">Pie Chart</div>', unsafe_allow_html=True)
    if cat_cols and num_cols:
        pie_cat = st.selectbox("الفئة", cat_cols, key="pie_cat")
        pie_val = st.selectbox("القيمة", num_cols, key="pie_val")
        pie_data = df.groupby(pie_cat)[pie_val].sum().reset_index()
        fig4 = px.pie(pie_data, names=pie_cat, values=pie_val,
                      color_discrete_sequence=px.colors.sequential.Blues_r,
                      hole=0.4)
        fig4.update_layout(paper_bgcolor=CHART_BG, font=dict(color=FONT_COLOR))
        st.plotly_chart(fig4, use_container_width=True)

# ── Correlation heatmap ───────────────────────────────────────
if len(num_cols) >= 2:
    st.markdown('<div class="section-header">مصفوفة الارتباط</div>', unsafe_allow_html=True)
    corr = df[num_cols].corr()
    fig5 = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale=[[0, "#1a2a4a"], [0.5, "#0f1117"], [1, "#4f8ef7"]],
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        showscale=True,
    ))
    fig5.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                       font=dict(color=FONT_COLOR), margin=dict(l=16, r=16, t=16, b=16))
    st.plotly_chart(fig5, use_container_width=True)

# ── Raw data table ────────────────────────────────────────────
with st.expander("📋 عرض البيانات الخام"):
    st.dataframe(df, use_container_width=True, height=300)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="⬇️ تحميل CSV",
        data=csv,
        file_name="data_export.csv",
        mime="text/csv",
    )
