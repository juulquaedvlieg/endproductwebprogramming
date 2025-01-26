import streamlit as st
import pandas as pd
import plotly.express as px
import mediamarkt
import coolblue

st.set_page_config(page_title="Elektronica Dashboard", layout="wide")

st.title("📊 Elektronica Dashboard")

# Sidebar: keuze voor Coolblue, MediaMarkt of Vergelijking
keuze = st.sidebar.radio("Selecteer een weergave", ["Overzicht", "Coolblue", "MediaMarkt", "Vergelijking"])

# Basis URL's en pagina's invoeren
if keuze in ["Coolblue", "MediaMarkt"]:
    base_url = st.text_input(f"Voer de {keuze} categorie-URL in")
    pages = st.number_input("Aantal pagina's om te scrapen", min_value=1, max_value=10, value=1, step=1)

    if base_url:
        df = coolblue.get_data(base_url, pages) if keuze == "Coolblue" else mediamarkt.get_data(base_url, pages)

        if not df.empty:
            # Filter op merk
            merken = df["Merk"].unique()
            gekozen_merk = st.selectbox("Selecteer een merk om te filteren", ["Alle"] + list(merken))
            if gekozen_merk != "Alle":
                df = df[df["Merk"] == gekozen_merk]
            
            st.dataframe(df)
            
            # Grafiek: Verdeling per merk
            st.subheader("📌 Verdeling van Elektronica per merk")
            brand_counts = df["Merk"].value_counts().reset_index()
            brand_counts.columns = ["Merk", "Aantal"]
            fig = px.bar(brand_counts, x="Merk", y="Aantal", labels={"Merk": "Merk", "Aantal": "Aantal Elektronica"})
            st.plotly_chart(fig)

            # Grafiek: Gemiddelde prijs per merk
            st.subheader("💰 Gemiddelde prijs per merk")
            avg_price = df.groupby("Merk")["Prijs"].mean().dropna().reset_index()
            fig = px.bar(avg_price, x="Merk", y="Prijs", labels={"Prijs": "Gemiddelde prijs (€)"})
            st.plotly_chart(fig)

            # Prijs vs. beoordeling
            st.subheader("💸 Prijs vs. Beoordeling")
            fig = px.scatter(df, x="Prijs", y="Gemiddelde Beoordeling", labels={"Prijs": "Prijs (€)", "Gemiddelde Beoordeling": "Gemiddelde Beoordeling"})
            st.plotly_chart(fig)

            # Download-knop
            st.download_button("⬇️ Download gegevens als CSV", df.to_csv(index=False), "laptops.csv", "text/csv")
        else:
            st.warning("Geen producten gevonden. Controleer de URL.")

# 🔥 **Vergelijkingspagina: Coolblue vs. MediaMarkt**
elif keuze == "Vergelijking":
    st.subheader("🔍 Coolblue vs. MediaMarkt: Vergelijking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        base_url_coolblue = st.text_input("🔵 Coolblue URL")
        pages_coolblue = st.number_input("Aantal pagina's voor Coolblue", min_value=1, max_value=10, value=1, step=1)

    with col2:
        base_url_mediamarkt = st.text_input("🔴 MediaMarkt URL")
        pages_mediamarkt = st.number_input("Aantal pagina's voor MediaMarkt", min_value=1, max_value=10, value=1, step=1)

    if base_url_coolblue and base_url_mediamarkt:
        df_coolblue = coolblue.get_data(base_url_coolblue, pages_coolblue)
        df_mediamarkt = mediamarkt.get_data(base_url_mediamarkt, pages_mediamarkt)

        if not df_coolblue.empty and not df_mediamarkt.empty:
            df_coolblue["Bron"] = "Coolblue"
            df_mediamarkt["Bron"] = "MediaMarkt"
            df_combined = pd.concat([df_coolblue, df_mediamarkt])

            # Filter op merk
            merken = df_combined["Merk"].unique()
            gekozen_merk = st.selectbox("Selecteer een merk om te filteren", ["Alle"] + list(merken))
            if gekozen_merk != "Alle":
                df_combined = df_combined[df_combined["Merk"] == gekozen_merk]

            # Markeer MediaMarkt als rood in de grafieken
            color_map = {"Coolblue": "blue", "MediaMarkt": "red"}

            st.dataframe(df_combined)

            # 📌 Aantal producten per bron
            st.subheader("🛒 Aantal Elektronica per bron")
            brand_counts = df_combined["Bron"].value_counts().reset_index()
            brand_counts.columns = ["Bron", "Aantal"]
            fig = px.bar(brand_counts, x="Bron", y="Aantal", text="Aantal", labels={"Bron": "Bron", "Aantal": "Aantal Elektronica"}, color="Bron", color_discrete_map=color_map)
            st.plotly_chart(fig)

            # 📊 Gemiddelde prijs per bron
            st.subheader("💰 Gemiddelde prijs per bron")
            avg_price = df_combined.groupby("Bron")["Prijs"].mean().reset_index()
            fig = px.bar(avg_price, x="Bron", y="Prijs", text="Prijs", labels={"Prijs": "Gemiddelde prijs (€)"}, color="Bron", color_discrete_map=color_map)
            st.plotly_chart(fig)

            # ⭐ Beoordelingen vergelijken
            st.subheader("⭐ Beoordelingen per bron")
            avg_rating = df_combined.groupby("Bron")["Gemiddelde Beoordeling"].mean().reset_index()
            fig = px.bar(avg_rating, x="Bron", y="Gemiddelde Beoordeling", text="Gemiddelde Beoordeling", labels={"Gemiddelde Beoordeling": "Gemiddelde Beoordeling"}, color="Bron", color_discrete_map=color_map)
            st.plotly_chart(fig)

            # 💸 Prijs vs. beoordeling per bron
            st.subheader("💸 Prijs vs. Beoordeling per bron")
            fig = px.scatter(df_combined, x="Prijs", y="Gemiddelde Beoordeling", color="Bron", labels={"Prijs": "Prijs (€)", "Gemiddelde Beoordeling": "Gemiddelde Beoordeling"}, color_discrete_map=color_map)
            st.plotly_chart(fig)
