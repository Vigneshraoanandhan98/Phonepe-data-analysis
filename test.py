# ===============================================
# 📱 PHONEPE PULSE STREAMLIT DASHBOARD
# ===============================================

import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="PhonePe Pulse Dashboard", layout="wide")

# ---------- DB CONNECTION ----------
def get_conn():
    return pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=VIGNESH\SQLEXPRESS;"
    r"DATABASE=phonepe;"
    r"Trusted_Connection=yes;"
)

# ---------- SIDEBAR ----------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Analysis"])

# =========================================================
# 🏠 HOME PAGE WITH INDIA MAP VISUALIZATION
# =========================================================
if page == "Home":
    st.title("📱 PhonePe Pulse – Interactive Analytics Dashboard")
    st.write("Explore India's digital transaction insights powered by PhonePe Pulse Data.")

    conn = get_conn()

    # Fetch State wise Transaction Amount
    query_map = """
    SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount 
    FROM dbo.aggregated_transaction
    GROUP BY State
    ORDER BY Total_Transaction_Amount DESC
    """
    df_map = pd.read_sql(query_map, conn)
    df_map["State"] = df_map["State"].replace({ 
'andaman-&-nicobar-islands': "Andaman & Nicobar",
'andhra-pradesh': "Andhra Pradesh",
'arunachal-pradesh': "Arunachal Pradesh",
'assam': 'Assam',
'bihar': 'Bihar',
'chandigarh': 'Chandigarh',
'chhattisgarh': 'Chhattisgarh',
'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
'delhi': 'Delhi',
'goa': 'Goa',
'gujarat':'Gujarat',
'haryana': 'Haryana',
'himachal-pradesh': 'Himachal Pradesh',
'jammu-&-kashmir': 'Jammu & Kashmir',
'jharkhand': 'Jharkhand',
'karnataka': 'Karnataka',
'kerala': 'Kerala',
'ladakh':'Ladakh',
'madhya-pradesh': 'Madhya Pradesh',
'maharashtra': 'Maharashtra',
'manipur': 'Manipur',
'meghalaya': 'Meghalaya',
'mizoram': 'Mizoram',
'nagaland': 'Nagaland',
'odisha': 'Odisha',
'puducherry': 'Puducherry',
'punjab': 'Punjab',
'rajasthan': 'Rajasthan',
'sikkim': 'Sikkim',
'tamil-nadu': 'Tamil Nadu',
'telangana': 'Telangana',
'tripura': 'Tripura',
'uttar-pradesh': 'Uttar Pradesh',
'uttarakhand': 'Uttarakhand',
'west-bengal': 'West Bengal'
    })

    # GeoJSON URL for India States
    india_geojson = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    st.markdown("<h3 style='text-align:Center;'>🗺 India State-wise Transaction Amount Overview</h3>", unsafe_allow_html=True)
    fig = px.choropleth(
        df_map,
        geojson=india_geojson,
        featureidkey="properties.ST_NM",
        locations="State",
        color="Total_Transaction_Amount",
        color_continuous_scale="Reds",
        
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)
    st.write(df_map)

# =========================================================
# 📊 BUSINESS CASE STUDIES (ANALYSIS PAGE)
# =========================================================
else:
    st.title("📈 Business Case Study Analysis")

    case = st.selectbox(
        "Choose a Case Study",
        [
            "1. Decoding Transaction Dynamics on PhonePe",
            "2. Device Dominance and User Engagement",
            "3. Insurance Penetration and Growth Potential",
            "4. Transaction Analysis Across States and Districts",
            "5. User Registration Analysis"
        ]
    )

    conn = get_conn()

    # =====================================================
    # 1️⃣ SCENARIO 1
    # =====================================================
    if case.startswith("1."):
        st.header("1️⃣ Decoding Transaction Dynamics on PhonePe")

        States_df = pd.read_sql("SELECT DISTINCT State FROM dbo.aggregated_transaction", conn)
        State_sel = st.selectbox("Select a State", States_df["State"].sort_values())

        

        # Q1 — State-wise trend
        q1 = f"""
        SELECT Year, SUM(Transaction_count) AS total_transaction_count, SUM(Transaction_amount) AS total_transaction_amount
        FROM dbo.aggregated_transaction
        WHERE State = '{State_sel}'
        GROUP BY Year ORDER BY Year
        """
        
        df1 = pd.read_sql(q1, conn)
        
       
        col1, col2 = st.columns(2)
        with col1:
                

            fig = px.line(
                df1,
                x="Year",
                y="total_transaction_count",
                markers=True,
                title="Transaction Count Over Years",
                )

            # Customize marker and line
            fig.update_traces(marker=dict(size=10, symbol="square", line=dict(width=2)),
                            line=dict(width=3, color="#7E57C2"))

            # Show values on hover
            fig.update_layout(hovermode="x unified")

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.line(
                df1,
                x="Year",
                y="total_transaction_amount",
                markers=True,
                title="Transaction Amount Over Years",
                )

            # Customize marker and line
            fig.update_traces(marker=dict(size=10, symbol="square", line=dict(width=2)),
                            line=dict(width=3, color="#7E57C2"))

            # Show values on hover
            fig.update_layout(hovermode="x unified")

            st.plotly_chart(fig, use_container_width=True)
            
        Years_df = pd.read_sql("SELECT DISTINCT Year FROM dbo.aggregated_transaction ORDER BY Year", conn)
        Year_sel = st.selectbox("Select a Year", Years_df["Year"])    
            

        # Q2 — Quarter-wise
        q2 = f"""
        SELECT Quarter, SUM(Transaction_count) AS Total_Transaction_Count, SUM(Transaction_amount) AS Total_Transaction_Amount
        FROM dbo.aggregated_transaction
        WHERE State = '{State_sel}' AND Year = {Year_sel}
        GROUP BY Quarter ORDER BY Quarter
        """
        df2 = pd.read_sql(q2, conn)
        
        df2["Quarter"] = df2["Quarter"].astype(str)
        
    
        phonepe_colors = ["#5A31F4", "#7B4DFF", "#A78BFA", "#7E57C2"]

        fig = px.bar(
            df2,
            x="Quarter",
            y="Total_Transaction_Amount",
            title="Quarter-wise Transaction Amount",
            color="Quarter",
            color_discrete_sequence=phonepe_colors,
        )

        # Force x-axis to show only 1,2,3,4
        fig.update_xaxes(
            tickmode="array",
            tickvals=[1, 2, 3, 4],
            ticktext=["1", "2", "3", "4"]
        )

        # Improve layout and visuals
        fig.update_traces(marker=dict(line=dict(width=1)))
        fig.update_layout(
            hovermode="x unified",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)



        # Q3 — Category-wise
        q3 = f"""
        SELECT Transaction_type, SUM(Transaction_count) AS Count, SUM(Transaction_amount) AS Amount
        FROM dbo.aggregated_transaction
        WHERE State='{State_sel}' AND Year={Year_sel}
        GROUP BY Transaction_type
        """
        df3 = pd.read_sql(q3, conn)
        df3 ["Transaction_type"] = df3["Transaction_type"].astype(str)
        
        phonepe_colors = ["#5A31F4", "#7B4DFF", "#A78BFA", "#7E57C2"]

        col3, col4 = st.columns(2)
        with col3:
        # Create interactive pie chart
            fig = px.pie(
            df3,
            names="Transaction_type",
            values="Count",
            title="Category-wise Count",
            color="Transaction_type",
            color_discrete_sequence=phonepe_colors
            )

        # Show label + percent on the chart and detailed hover (value + percent)
            fig.update_traces(
            textinfo="label+percent",           # label and percentage shown on slices
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Percent: %{percent}", 
            marker=dict(line=dict(color="white", width=1))  # white separators between slices
            )

        # Optional: make it a donut by setting hole (0.3 - 0.5)
        # fig.update_traces(hole=0.35)

            fig.update_layout(margin=dict(t=60, b=20, l=20, r=20), showlegend=True)

        # Render in Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
        df3["Transaction_type"] = df3["Transaction_type"].astype(str)
        phonepe_colors = ["#5A31F4", "#7B4DFF", "#A78BFA", "#D8CCFF"]

        with col4:
            fig = px.pie(
            df3,
            names="Transaction_type",
            values="Amount",
            title="Category Share Amount",
            color="Transaction_type",
            color_discrete_sequence=phonepe_colors
            )

            fig.update_traces(
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Amount: %{value:,}<br>Share: %{percent}",
                marker=dict(line=dict(color="white", width=1))
            )

            fig.update_layout(margin=dict(t=60, b=20, l=20, r=20))

            st.plotly_chart(fig, use_container_width=True)


        # Q4 — Top 5 States
        
        q4 = f"""
        SELECT TOP 5 State, SUM(Transaction_amount) AS Transaction_amount
        FROM dbo.aggregated_transaction
        WHERE Year={Year_sel}
        GROUP BY State ORDER BY Transaction_amount DESC
        """
        df4 = pd.read_sql(q4, conn)
        # df4: DataFrame with 'State' and 'Transaction_amount' columns (numeric)
        df4['Transaction_amount'] = pd.to_numeric(df4['Transaction_amount'], errors='coerce').fillna(0)

        phonepe_colors = ["#7E57C2", "#5E35B1", "#26C6DA", "#4E79A7", "#59A14F"]  # will cycle as needed

        fig = px.bar(
            df4,
            x='State',
            y='Transaction_amount',
            text=df4['Transaction_amount'].apply(lambda v: f"{int(v):,}"),
            title=f"Top {len(df4)} States in {Year_sel}",
            color_discrete_sequence=phonepe_colors
        )

        fig.update_layout(
            template='plotly_dark',          # dark background
            xaxis_tickangle=-45,
            margin=dict(l=40, r=20, t=60, b=120),
            hovermode='x',
            showlegend=True
        )
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Amount: %{y:,}<extra></extra>',
                        marker_line_color='black', marker_line_width=0.5, textposition='inside')

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # 2️⃣ SCENARIO 2
    # =====================================================
    
    elif case.startswith("2."): 
            st.header("📱 Device Dominance & User Engagement Analysis")
            q = """  
            SELECT 
                user_brand, 
                SUM(user_count) AS total_users
            FROM dbo.aggregated_user
            GROUP BY user_brand
            ORDER BY total_users DESC
            """
            
            from matplotlib.ticker import FuncFormatter

            df = pd.read_sql(q, conn)

            if not df.empty:
                # aggregate in case query returned duplicates, sort desc
                df = df.groupby('user_brand', as_index=False)['total_users'].sum().sort_values('total_users', ascending=False)

                # choose how many brands to show (top N)
                top_n = 20
                df_top = df.head(top_n).copy()

                phonepe_colors = ["#7E57C2", "#5E35B1", "#26C6DA", "#4E79A7", "#59A14F",
                                "#AB47BC", "#8E24AA", "#6A1B9A"]

                plt.style.use("dark_background")
                fig, ax = plt.subplots(figsize=(10, 7))
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                # horizontal bars
                y_pos = range(len(df_top))
                colors = (phonepe_colors * ((len(df_top) // len(phonepe_colors)) + 1))[:len(df_top)]
                bars = ax.barh(y_pos, df_top['total_users'], color=colors, edgecolor='white', height=0.7)

                # invert y axis so largest on top
                ax.invert_yaxis()

                # format function to show billions/millions nicely
                def human_format(x, pos):
                    if x >= 1_000_000_000:
                        return f"{x/1_000_000_000:.2f}B"
                    if x >= 1_000_000:
                        return f"{x/1_000_000:.2f}M"
                    if x >= 1_000:
                        return f"{x/1_000:.1f}K"
                    return f"{int(x)}"
                ax.xaxis.set_major_formatter(FuncFormatter(human_format))

                # labels & title
                ax.set_yticks(y_pos)
                ax.set_yticklabels(df_top['user_brand'], fontsize=11, color='white')
                ax.set_xlabel("Total Users", fontsize=12, color='white')
                ax.set_title("Total Users by Device Brand (Top {})".format(top_n), fontsize=16, color='white')

                # remove grid completely (you said remove background grid)
                ax.grid(False)

                # make spines and ticks visible/white for dark BG
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # annotate values at the end of bars (non-overlapping)
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    label = human_format(width, None)
                    # place annotation slightly to the right of the bar
                    ax.text(width + max(df_top['total_users']) * 0.005, bar.get_y() + bar.get_height()/2,
                            label, va='center', ha='left', fontsize=9, color='white', weight='bold', clip_on=False)

                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

            else:
                st.warning("No user data available.")
            
                
            q = """
            SELECT 
                State, 
                SUM(m_registered_Users) AS registered_users
            FROM dbo.map_user
            GROUP BY State
            ORDER BY registered_users DESC
            """
            def human_format(num):
                
                num = float(num)
                
                for unit in ['', 'K', 'M', 'B', 'T']:
                    if abs(num) < 1000.0:
                        return f"{num:.1f}{unit}"
                    num /= 1000.0
                return f"{num:.1f}P"
        
            df = pd.read_sql(q, conn)

            if not df.empty:

                top10 = df.sort_values('registered_users', ascending=False).head(10)

                fig, ax = plt.subplots(figsize=(5, 3))
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)
                
                
                bars = sns.barplot( data=top10, x='registered_users', y='State', palette='viridis', ax=ax)
            
                ax.set_title("Top 10 States — Registered Users", fontsize=12)
                ax.set_xlabel("Registered Users", fontsize=10)
                ax.set_ylabel("")
                ax.tick_params(axis='y', labelsize=7)
                ax.tick_params(axis='x', labelsize=5)


                # --- Place annotation slightly to the RIGHT of each bar ---
                for bar in ax.patches:
                    width = bar.get_width()
                    y = bar.get_y() + bar.get_height() / 2
                    
                    ax.text(
                        width + (width * 0.02), y, human_format(width) , va='center', ha='left', fontsize=5, fontweight='bold' )         # <-- 2% to the RIGHT of bar
                st.pyplot(fig, use_container_width=True)
            else:
                st.warning("No data available.")
            q = """ 
            SELECT
                State,
                SUM(CAST(COALESCE(m_app_Opens, 0) AS BIGINT)) AS app_opens
            FROM dbo.map_user
            GROUP BY State
            ORDER BY app_opens DESC
            """

            df = pd.read_sql(q, conn)

            if not df.empty:
                df = df.sort_values("app_opens", ascending=False).reset_index(drop=True)

                # Top 10 + Others
                top = df.head(10).copy()
                others_sum = df.iloc[10:]["app_opens"].sum()
                if others_sum > 0:
                    top = pd.concat(
                        [top, pd.DataFrame([{"State": "Others", "app_opens": others_sum}])],
                        ignore_index=True
                    )

                fig, ax = plt.subplots(figsize=(4, 4))
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                phonepe_colors = [
                    "#7E57C2", "#5E35B1", "#A966A9", "#4E79A7", "#DB55CB",
                    "#AB47BC", "#8E24AA", "#6A1B9A", "#EFDFEE","#4B2C5E","#500845"
                ]

                # --- Percentage ONLY inside donut ---
                def inside_labels_only_pct(pct):
                    return f"{pct:.1f}%"

                wedges, texts, autotexts = ax.pie(
                    top["app_opens"],
                    labels=None,
                    autopct=lambda pct: inside_labels_only_pct(pct),
                    pctdistance=0.75,
                    startangle=90,
                    wedgeprops=dict(width=0.45),
                    colors=phonepe_colors,
                )

                plt.setp(autotexts, size=8, weight="bold", color="black")

                # Legend
                ax.legend(
                    wedges,
                    top["State"],
                    title="State",
                    bbox_to_anchor=(1.05, 1),
                    loc="upper left",
                    fontsize=6
                )

                # Donut center
                centre_circle = plt.Circle((0, 0), 0.45, fc="black")
                fig.gca().add_artist(centre_circle)

                ax.set_title("State Share by App Opens", fontsize=12)
                st.pyplot(fig, use_container_width=False)

            else:
                st.warning("No data available.")

    # =====================================================
    # 3️⃣ SCENARIO 3
    # =====================================================
    elif case.startswith("3."):
        
        st.header("🛡 Insurance Penetration & Growth Potential")


# --- query (you already have conn) ---
        q = """
        SELECT State, Year, SUM(insurance_count) AS total_count, SUM(insurance_amount) AS total_amount
        FROM dbo.aggregated_insurance
        GROUP BY State, Year
        ORDER BY Year;
        """
        df = pd.read_sql(q, conn)

        if df.empty:
            st.warning("No insurance data available.")
        else:
            # normalize
            df.columns = [c.lower() for c in df.columns]   # state, year, total_count, total_amount

            # selectors
            states = ["All"] + sorted(df['state'].dropna().unique().tolist())
            years = ["All"] + sorted(df['year'].dropna().astype(int).unique().tolist())

            sel_state = st.sidebar.selectbox("State", states, index=0)
            sel_year = st.sidebar.selectbox("Year", years, index=0)

            # filtered frames for charts
            def df_for_amount_count(state=None):
                d = df.copy()
                if state and state != "All":
                    d = d[d['state'] == state]
                # aggregate by year
                return d.groupby('year', as_index=False).agg(
                    total_amount = ('total_amount','sum'),
                    total_count  = ('total_count','sum')
                ).sort_values('year')

            df_time = df_for_amount_count(None if sel_state=="All" else sel_state)

            # Chart colors
            colors = ["#7E57C2", "#26C6DA", "#4E79A7", "#59A14F"]

            # Layout: two rows x two cols
            col1, col2 = st.columns(2)

            # 1) Line - total_amount over years (for selected state or aggregated)
            with col1:
                title = f"Total Insurance Amount — {'All states' if sel_state=='All' else sel_state}"
                fig1 = px.line(df_time, x='year', y='total_amount', markers=True,
                            title=title, labels={'year':'Year','total_amount':'Amount'},
                            color_discrete_sequence=[colors[0]])
                fig1.update_traces(hovertemplate='Year: %{x}<br>Amount: %{y:,.0f}<extra></extra>')
                st.plotly_chart(fig1, use_container_width=True)

            # 2) Line - total_count over years
            with col2:
                title = f"Total Insurance Count — {'All states' if sel_state=='All' else sel_state}"
                fig2 = px.line(df_time, x='year', y='total_count', markers=True,
                            title=title, labels={'year':'Year','total_count':'Count'},
                            color_discrete_sequence=[colors[1]])
                fig2.update_traces(hovertemplate='Year: %{x}<br>Count: %{y:,.0f}<extra></extra>')
                st.plotly_chart(fig2, use_container_width=True)

            # For year-based rankings (bar + pie) we need per-state aggregates for the selected year
            if sel_year == "All":
                # default: use the latest year available
                use_year = df['year'].max()
            else:
                use_year = int(sel_year)

            df_year = df[df['year'] == use_year].groupby('state', as_index=False).agg(
                total_amount=('total_amount','sum'),
                total_count=('total_count','sum')
            ).sort_values('total_amount', ascending=False)

            # 3) Bar - top states by amount
            col3, col4 = st.columns(2)
            with col3:
                top_n = 10
                df_top = df_year.head(top_n)
                fig3 = px.bar(df_top, x='state', y='total_amount', title=f"Top {top_n} States by Amount — {use_year}",
                            labels={'state':'State','total_amount':'Amount'},
                            color_discrete_sequence=colors)
                fig3.update_traces(hovertemplate='%{x}<br>Amount: %{y:,.0f}<extra></extra>')
                fig3.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig3, use_container_width=True)

            # 4) Pie - bottom 5 states (lowest total_amount)
            with col4:
                df_bottom = df_year[df_year['total_amount']>0].sort_values('total_amount').head(5)
                if df_bottom.empty:
                    st.info("No data for pie chart (no positive amounts).")
                else:
                    fig4 = px.pie(df_bottom, names='state', values='total_amount', hole=0.45,
                                title=f"Bottom 5 States by Amount — {use_year}",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl)
                    fig4.update_traces(hovertemplate='%{label}<br>Amount: %{value:,.0f} (%{percent})<extra></extra>')
                    st.plotly_chart(fig4, use_container_width=True)

            # optional: show dataframe
            with st.expander("Show data (preview)"):
                st.dataframe(df.sort_values("total_amount", ascending=False).head(200))

        

    # =====================================================
    # 4️⃣ SCENARIO 4
    # =====================================================
    elif case.startswith("4."):
        st.header("📌 Transaction Analysis Across States & Districts") 

        PHONEPE = ["#7E57C2","#5E35B1","#26C6DA","#4E79A7","#59A14F","#EDC948","#E15759"]
        st.sidebar.title("View")
        mode = st.sidebar.radio("Show top by", ["Year", "State", "District", "Pincode"])
        years = ["All"] + sorted(pd.read_sql("SELECT DISTINCT Year FROM dbo.aggregated_transaction", conn)['Year'].astype(int).tolist())
        sel_year = st.sidebar.selectbox("Year", years, index=0)
        # <-- removed sel_state selectbox here

        top_n = st.sidebar.slider("Top Levels", 5, 25, 10)

        # build SQL + params quickly depending on mode
        if mode == "Year":
            q_top = f"""SELECT Year, SUM(Transaction_amount) AS total_amount
                        FROM dbo.aggregated_transaction
                        {f"WHERE Year={sel_year}" if sel_year!="All" else ""}
                        GROUP BY Year ORDER BY total_amount DESC"""
            q_pivot = """SELECT Year, State, SUM(Transaction_amount) AS total_amount FROM dbo.aggregated_transaction GROUP BY Year,State"""
            df_top = pd.read_sql(q_top, conn)
            df_line = pd.read_sql(q_pivot, conn).groupby('Year', as_index=False).total_amount.sum()
            x_col, y_col = 'Year','total_amount'

        elif mode == "State":
            q_top = f"""SELECT TOP {top_n} State AS name, SUM(Transaction_amount) AS total_amount
                        FROM dbo.top_state_transaction
                        {f"WHERE Year={sel_year}" if sel_year!="All" else ""}
                        GROUP BY State ORDER BY total_amount DESC"""
            # removed state filter from pivot query
            q_pivot = f"""SELECT Year, State, SUM(Transaction_amount) AS total_amount FROM dbo.aggregated_transaction
                        {f"WHERE Year={sel_year}" if sel_year!="All" else ""}
                        GROUP BY Year,State"""
            df_top = pd.read_sql(q_top, conn)
            df_line = pd.read_sql(q_pivot, conn).groupby('Year', as_index=False).total_amount.sum()
            x_col, y_col = 'name','total_amount'

        elif mode == "District":
            q_top = f"""SELECT TOP {top_n} District AS name, SUM(Transaction_amount) AS total_amount
                        FROM dbo.top_district_transaction
                        {f"WHERE Year={sel_year}" if sel_year!="All" else ""}
                        GROUP BY District ORDER BY total_amount DESC"""
            # removed dependency on sel_state; only filter by Year when provided
            q_pivot = f"""SELECT Year, SUM(Transaction_amount) AS total_amount FROM dbo.top_district_transaction
                        {f"WHERE Year={sel_year}" if sel_year!="All" else ""}
                        GROUP BY Year"""
            df_top = pd.read_sql(q_top, conn)
            df_line = pd.read_sql(q_pivot, conn).groupby('Year', as_index=False).total_amount.sum()
            x_col, y_col = 'name','total_amount'

        else:  # Pincode
            q_top = f"""SELECT TOP {top_n} Pincode AS name, SUM(Transaction_amount) AS total_amount
                        FROM dbo.top_pincode_transaction
                        {f"WHERE Year={sel_year}" if sel_year!="All" else ""}
                        GROUP BY Pincode ORDER BY total_amount DESC"""
            q_pivot = f"""SELECT Year, SUM(Transaction_amount) AS total_amount FROM dbo.top_pincode_transaction
                        {f"WHERE Year={sel_year}" if sel_year!="All" else ""} GROUP BY Year"""
            df_top = pd.read_sql(q_top, conn)
            df_line = pd.read_sql(q_pivot, conn).groupby('Year', as_index=False).total_amount.sum()
            x_col, y_col = 'name','total_amount'

        if df_top.empty:
            st.warning("No data for selection.")
        else:
            # Bar (top N)
            fig_bar = px.bar(df_top.head(top_n), x=x_col, y=y_col, color=x_col,
                            color_discrete_sequence=PHONEPE, title=f"Top {top_n} {mode}s by Amount",
                            labels={x_col:mode, y_col:"Amount"})
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            fig_bar.update_traces(hovertemplate='%{x}<br>Amount: %{y:,.0f}')
            st.plotly_chart(fig_bar, use_container_width=True)

            # Pie (share of top N)
            fig_pie = px.pie(df_top.head(top_n), names=x_col, values=y_col, hole=0.45,
                            color_discrete_sequence=PHONEPE, title=f"Share — Top {top_n}")
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

            # Line (trend over years)
            if not df_line.empty:
                fig_line = px.line(df_line.sort_values('Year'), x='Year', y='total_amount', markers=True,
                                color_discrete_sequence=[PHONEPE[0]], title=f"Trend — Amount over Years")
                fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                fig_line.update_traces(hovertemplate='Year: %{x}<br>Amount: %{y:,.0f}')
                st.plotly_chart(fig_line, use_container_width=True)


 

    # =====================================================
    # 5️⃣ SCENARIO 5
    # =====================================================
    elif case.startswith("5."):
        st.header("🧑‍🤝‍🧑 User Registration Analysis")

        # ----- COLORS & STYLE -----
        PHONEPE = ["#7E57C2","#5E35B1","#26C6DA","#4E79A7","#59A14F","#EDC948","#E15759"]
       

        # Sidebar: Year / Quarter / None radio (left side)
        filter_mode = st.sidebar.radio("Filter by", ["None", "Year", "Quarter"], index=0)

        # Helper to safely get distinct filter values from DB tables (if present)
        def get_distinct_values(conn, table, col):
            try:
                q = f"SELECT DISTINCT {col} FROM {table} ORDER BY {col} DESC"
                return [r[0] for r in pd.read_sql(q, conn).values.tolist()]
            except Exception:
                return []

        # attempt to fetch available years/quarters (fallback to empty list)
        available_years = get_distinct_values(conn, "dbo.top_user_state", "Year")
        available_quarters = get_distinct_values(conn, "dbo.top_user_state", "Quarter")

        # Choose actual filter value if requested
        selected_year = None
        selected_quarter = None
        if filter_mode == "Year" and available_years:
            selected_year = st.sidebar.selectbox("Select Year", ["All"] + available_years, index=0)
        elif filter_mode == "Quarter" and available_quarters:
            selected_quarter = st.sidebar.selectbox("Select Quarter", ["All"] + available_quarters, index=0)

        # Helper: build WHERE clause only if the table actually has Year/Quarter columns
        def build_where(table_alias=""):
            clauses = []
            # try to apply year/quarter filters — if these columns don't exist, SQL will fail and we fallback
            if selected_year and selected_year != "All":
                clauses.append(f"Year = '{selected_year}'")
            if selected_quarter and selected_quarter != "All":
                clauses.append(f"Quarter = '{selected_quarter}'")
            return (" WHERE " + " AND ".join(clauses)) if clauses else ""

        # ------------------------------
        # 1) State-wise bar chart
        # ------------------------------
        q_state = f"""
        SELECT TOP 10 State, SUM(registeredUsers) AS total_users
        FROM dbo.top_user_state
        {build_where()}
        GROUP BY State
        ORDER BY total_users DESC
        """
        df_state = pd.read_sql(q_state, conn)

        st.header("🧑‍🤝‍🧑 Registered Users — STATE WISE")
        if not df_state.empty:
            fig_state = px.bar(
                df_state,
                x="State",
                y="total_users",
                title="Top 10 States by Registered Users",
                color="State",                     # color by state so each bar can pick from palette
                color_discrete_sequence=PHONEPE,
                labels={"total_users":"Registered Users", "State":"State"}
            )
            fig_state.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig_state.update_xaxes(tickangle=45)
            st.plotly_chart(fig_state, use_container_width=True)

            # selection box under state chart
            chosen_state = st.selectbox("Inspect state (select to view details):", ["All"] + df_state["State"].tolist())
            if chosen_state != "All":
                st.write(df_state[df_state["State"] == chosen_state].reset_index(drop=True))
        else:
            st.warning("No state-level registration data available.")

        # ------------------------------
        # 2) District-wise line chart
        # ------------------------------
        q_district = f"""
        SELECT TOP 10 District, SUM(registeredUsers) AS total_users
        FROM dbo.top_user_district
        {build_where()}
        GROUP BY District
        ORDER BY total_users DESC
        """
        df_district = pd.read_sql(q_district, conn)

        st.header("📈 Registered Users — DISTRICT WISE (Line)")
        if not df_district.empty:
            # for readability: sort by total_users so the line flows by rank
            df_district = df_district.sort_values("total_users", ascending=False).reset_index(drop=True)
            fig_district = px.line(
                df_district,
                x="District",
                y="total_users",
                markers=True,
                title="Top 10 Districts by Registered Users (ranked)",
                labels={"total_users":"Registered Users", "District":"District"}
            )
            # apply color palette cyclically to markers/lines
            fig_district.update_traces(line=dict(color=PHONEPE[0]), marker=dict(size=8))
            fig_district.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig_district.update_xaxes(tickangle=45)
            st.plotly_chart(fig_district, use_container_width=True)

            # selection box under district chart
            chosen_district = st.selectbox("Inspect district (select to view details):", ["All"] + df_district["District"].tolist())
            if chosen_district != "All":
                st.write(df_district[df_district["District"] == chosen_district].reset_index(drop=True))
        else:
            st.warning("No district-level registration data available.")

        # ------------------------------
        # 3) Pincode-wise pie chart
        # ------------------------------
        q_pincode = f"""
        SELECT TOP 10 Pincode, SUM(registeredUsers) AS total_users
        FROM dbo.top_user_pincode
        {build_where()}
        GROUP BY Pincode
        ORDER BY total_users DESC
        """
        df_pincode = pd.read_sql(q_pincode, conn)

        st.header("🥧 Registered Users — PINCODE WISE (Pie)")
        if not df_pincode.empty:
            fig_pincode = px.pie(
                df_pincode,
                names="Pincode",
                values="total_users",
                title="Top 10 Pincodes by Registered Users",
                color_discrete_sequence=PHONEPE
            )
            fig_pincode.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pincode, use_container_width=True)

            # selection box under pincode chart
            chosen_pincode = st.selectbox("Inspect pincode (select to view details):", ["All"] + df_pincode["Pincode"].astype(str).tolist())
            if chosen_pincode != "All":
                st.write(df_pincode[df_pincode["Pincode"].astype(str) == chosen_pincode].reset_index(drop=True))
        else:
            st.warning("No pincode-level registration data available.")
