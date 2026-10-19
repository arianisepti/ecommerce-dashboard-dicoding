import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# Konfigurasi Halaman
# ============================================================
st.set_page_config(
    page_title="E-Commerce Public Dataset Dashboard",
    page_icon="🛒",
    layout="wide"
)

sns.set_style("whitegrid")

# ============================================================
# Load Data
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    date_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date", "shipping_limit_date",
        "review_creation_date", "review_answer_timestamp"
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

all_df = load_data()

# Filter periode analisis (Januari 2017 - Agustus 2018)
start_date = pd.Timestamp("2017-01-01")
end_date = pd.Timestamp("2018-08-31 23:59:59")
all_df = all_df[
    (all_df["order_purchase_timestamp"] >= start_date) &
    (all_df["order_purchase_timestamp"] <= end_date)
].copy()

# ============================================================
# Sidebar - Filter Interaktif
# ============================================================
with st.sidebar:
    st.title("🛒 E-Commerce Dashboard")
    st.markdown("**Periode:** Januari 2017 – Agustus 2018")
    st.markdown("---")

    # Filter state (multi-select)
    all_states = sorted(all_df["customer_state"].dropna().unique())
    selected_states = st.multiselect(
        "Pilih Negara Bagian (customer_state):",
        options=all_states,
        default=all_states
    )

    # Filter kategori (multi-select, opsional)
    all_categories = sorted(all_df["product_category_name_english"].dropna().unique())
    selected_categories = st.multiselect(
        "Pilih Kategori Produk:",
        options=all_categories,
        default=all_categories
    )

# Terapkan filter
filtered_df = all_df[
    (all_df["customer_state"].isin(selected_states)) &
    (
        all_df["product_category_name_english"].isin(selected_categories) |
        all_df["product_category_name_english"].isna()
    )
].copy()

# ============================================================
# Header & Metrik Utama
# ============================================================
st.title("🛒 E-Commerce Public Dataset Dashboard")
st.markdown(
    "Dashboard interaktif hasil analisis data e-commerce periode "
    "**Januari 2017 – Agustus 2018**. Gunakan filter di sidebar untuk "
    "menyesuaikan tampilan."
)

col1, col2, col3, col4 = st.columns(4)
total_revenue = filtered_df["price"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_unique_id"].nunique()
avg_delivery = (
    filtered_df.loc[
        filtered_df["order_status"] == "delivered", "order_delivered_customer_date"
    ].sub(filtered_df.loc[
        filtered_df["order_status"] == "delivered", "order_purchase_timestamp"
    ], fill_value=pd.NaT).dt.total_seconds().mean() / 86400
)

col1.metric("Total Revenue (R$)", f"{total_revenue:,.2f}")
col2.metric("Total Pesanan", f"{total_orders:,}")
col3.metric("Pelanggan Unik", f"{total_customers:,}")
col4.metric("Rata-rata Pengiriman (hari)", f"{avg_delivery:.2f}" if pd.notna(avg_delivery) else "-")

st.markdown("---")

# ============================================================
# TAB 1: Kategori Produk (Pertanyaan 1)
# ============================================================
tab1, tab2, tab3 = st.tabs([
    "📦 Kategori Produk",
    "🚚 Waktu Pengiriman",
    "👥 Segmentasi RFM"
])

with tab1:
    st.subheader("Top 10 Kategori Produk Berdasarkan Revenue")
    st.markdown(
        "Kategori dengan total revenue tertinggi pada periode analisis. "
        "Persentase menunjukkan kontribusi terhadap total revenue."
    )

    category_revenue = (
        filtered_df
        .dropna(subset=["product_category_name_english"])
        .groupby("product_category_name_english", as_index=False)
        .agg(total_revenue=("price", "sum"), total_items=("order_item_id", "count"))
        .sort_values("total_revenue", ascending=False)
    )
    category_revenue["revenue_pct"] = (
        category_revenue["total_revenue"] / category_revenue["total_revenue"].sum() * 100
    ).round(2)

    top10 = category_revenue.head(10).sort_values("total_revenue")

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(
        top10["product_category_name_english"],
        top10["total_revenue"],
        color=sns.color_palette("viridis", len(top10))
    )
    for bar, pct in zip(bars, top10["revenue_pct"]):
        ax.text(
            bar.get_width() * 0.99, bar.get_y() + bar.get_height() / 2,
            f" {pct:.2f}%", va="center", ha="right",
            color="white", fontsize=9, fontweight="bold"
        )
    ax.set_title("Top 10 Kategori Produk Berdasarkan Total Revenue",
                 fontsize=12, fontweight="bold")
    ax.set_xlabel("Total Revenue (R$)")
    ax.set_ylabel("Kategori Produk")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Lihat tabel lengkap kategori"):
        st.dataframe(category_revenue, use_container_width=True)

# ============================================================
# TAB 2: Waktu Pengiriman (Pertanyaan 2)
# ============================================================
with tab2:
    st.subheader("Rata-rata Waktu Pengiriman per Negara Bagian")
    st.markdown(
        "Rata-rata waktu pengiriman (dalam hari) dari pesanan dibuat hingga diterima "
        "pelanggan. Batang **merah** menunjukkan state dengan pengiriman di atas "
        "rata-rata nasional."
    )

    delivered = filtered_df[
        (filtered_df["order_status"] == "delivered") &
        (filtered_df["order_delivered_customer_date"].notna()) &
        (filtered_df["order_purchase_timestamp"].notna())
    ].copy()

    delivered["delivery_days"] = (
        delivered["order_delivered_customer_date"] -
        delivered["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    delivered = delivered[delivered["delivery_days"] >= 0]

    state_delivery = (
        delivered
        .groupby("customer_state", as_index=False)
        .agg(
            avg_delivery_days=("delivery_days", "mean"),
            median_delivery_days=("delivery_days", "median"),
            total_orders=("order_id", "nunique")
        )
        .sort_values("avg_delivery_days", ascending=True)
    )
    state_delivery["avg_delivery_days"] = state_delivery["avg_delivery_days"].round(2)
    state_delivery["median_delivery_days"] = state_delivery["median_delivery_days"].round(2)

    national_avg = delivered["delivery_days"].mean()

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = [
        "#d62728" if v > national_avg else "#2ca02c"
        for v in state_delivery["avg_delivery_days"]
    ]
    bars = ax.barh(
        state_delivery["customer_state"],
        state_delivery["avg_delivery_days"],
        color=colors
    )
    for bar, val in zip(bars, state_delivery["avg_delivery_days"]):
        ax.text(bar.get_width() + 0.3,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", fontsize=8)
    ax.axvline(national_avg, color="black", linestyle="--", linewidth=1.2,
               label=f"Rata-rata nasional: {national_avg:.2f} hari")
    ax.set_title("Rata-rata Waktu Pengiriman per Negara Bagian",
                 fontsize=12, fontweight="bold")
    ax.set_xlabel("Rata-rata Waktu Pengiriman (hari)")
    ax.set_ylabel("Negara Bagian")
    ax.legend(loc="lower right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Lihat tabel lengkap per state"):
        st.dataframe(state_delivery, use_container_width=True)

# ============================================================
# TAB 3: Segmentasi RFM (Pertanyaan 3)
# ============================================================
with tab3:
    st.subheader("Segmentasi Pelanggan dengan RFM Analysis")
    st.markdown(
        "Pelanggan dikelompokkan berdasarkan **Recency**, **Frequency**, dan "
        "**Monetary** menggunakan skor kuantil 1–5 dan aturan bisnis (manual grouping)."
    )

    reference_date = pd.Timestamp("2018-08-31 23:59:59")
    rfm_base = filtered_df[
        filtered_df["customer_unique_id"].notna() &
        filtered_df["order_purchase_timestamp"].notna() &
        filtered_df["payment_value"].notna()
    ].copy()

    rfm = (
        rfm_base
        .groupby("customer_unique_id", as_index=False)
        .agg(
            last_purchase=("order_purchase_timestamp", "max"),
            frequency=("order_id", "nunique"),
            monetary=("payment_value", "sum")
        )
    )
    rfm["recency"] = (reference_date - rfm["last_purchase"]).dt.days

    if len(rfm) >= 5:
        rfm["r_score"] = pd.qcut(rfm["recency"], q=5, labels=[5, 4, 3, 2, 1]).astype(int)
        rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5,
                                 labels=[1, 2, 3, 4, 5]).astype(int)
        rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), q=5,
                                 labels=[1, 2, 3, 4, 5]).astype(int)

        def segment_customer(row):
            r, f, m = row["r_score"], row["f_score"], row["m_score"]
            if r >= 4 and f >= 4 and m >= 4:
                return "Champions"
            elif r >= 3 and f >= 3 and m >= 3:
                return "Loyal Customers"
            elif r >= 4 and f <= 2:
                return "New Customers"
            elif r <= 2 and f >= 3:
                return "At Risk"
            elif r <= 2 and f <= 2 and m <= 2:
                return "Hibernating"
            else:
                return "Potential Loyalist"

        rfm["segment"] = rfm.apply(segment_customer, axis=1)

        seg_summary = (
            rfm.groupby("segment", as_index=False)
            .agg(
                customers=("customer_unique_id", "count"),
                total_monetary=("monetary", "sum"),
                avg_monetary=("monetary", "mean"),
                avg_recency=("recency", "mean")
            )
        )
        seg_summary["customer_pct"] = (
            seg_summary["customers"] / seg_summary["customers"].sum() * 100
        ).round(2)
        seg_summary["monetary_pct"] = (
            seg_summary["total_monetary"] / seg_summary["total_monetary"].sum() * 100
        ).round(2)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        seg_cust = seg_summary.sort_values("customers")
        bars1 = axes[0].barh(seg_cust["segment"], seg_cust["customers"],
                             color=sns.color_palette("Blues_d", len(seg_cust)))
        for bar, pct in zip(bars1, seg_cust["customer_pct"]):
            axes[0].text(bar.get_width() + 300,
                         bar.get_y() + bar.get_height() / 2,
                         f"{pct:.2f}%", va="center", fontsize=9)
        axes[0].set_title("(a) Jumlah Pelanggan per Segmen", fontweight="bold")
        axes[0].set_xlabel("Jumlah Pelanggan")

        seg_rev = seg_summary.sort_values("monetary_pct")
        bars2 = axes[1].barh(seg_rev["segment"], seg_rev["monetary_pct"],
                             color=sns.color_palette("Oranges_d", len(seg_rev)))
        for bar, pct in zip(bars2, seg_rev["monetary_pct"]):
            axes[1].text(bar.get_width() + 0.3,
                         bar.get_y() + bar.get_height() / 2,
                         f"{pct:.2f}%", va="center", fontsize=9)
        axes[1].set_title("(b) Kontribusi Revenue per Segmen", fontweight="bold")
        axes[1].set_xlabel("Kontribusi Revenue (%)")

        plt.suptitle("Segmentasi Pelanggan dengan RFM Analysis",
                     fontsize=13, fontweight="bold", y=1.02)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Lihat tabel lengkap segmen RFM"):
            st.dataframe(seg_summary, use_container_width=True)
    else:
        st.warning("Data pelanggan pada filter ini terlalu sedikit untuk analisis RFM.")

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.caption(
    "Dibuat oleh Ariani Dwi Septi · Proyek Analisis Data Dicoding · "
    "E-Commerce Public Dataset"
)