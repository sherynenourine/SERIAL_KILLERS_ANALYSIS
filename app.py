import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Serial Killers — Data Investigation",
    page_icon="🩸",
    layout="wide",
)

# =======================================================
#  DESIGN SYSTEM
#  Direction : "dossier d'enquête criminelle"
#  Palette  : encre #0a0908 · sang #8B0000 · braise #ff3b3b
#             os #ece7df · acier #8a9099
#  Typo     : Oswald (display) · Inter (corps) · JetBrains Mono (data)
# =======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --ink:      #0a0908;
    --ink-2:    #121010;
    --panel:    rgba(22,19,19,0.86);
    --blood:    #8B0000;
    --crimson:  #B00020;
    --ember:    #ff3b3b;
    --bone:     #ece7df;
    --text:     #d8d3cb;
    --muted:    #8a8079;
    --steel:    #9aa0a8;
    --hair:     rgba(236,231,223,0.10);
}

/* ----- base ----- */
.stApp {
    background:
        radial-gradient(900px 600px at 12% -5%, rgba(139,0,0,0.30), transparent 60%),
        radial-gradient(700px 500px at 100% 0%, rgba(120,0,0,0.12), transparent 55%),
        linear-gradient(180deg, #0c0a0a 0%, #070606 100%);
    color: var(--text);
}
html, body, [class*="css"], .stApp, p, div, span, label, input, button, select, textarea {
    font-family: 'Inter', system-ui, sans-serif;
}
.block-container { padding-top: 1.5rem; padding-bottom: 5rem; max-width: 1180px; }

/* hide streamlit chrome for a cleaner deliverable */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* ----- HERO ----- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 56px 48px 50px;
    border-radius: 22px;
    background:
        linear-gradient(135deg, rgba(80,0,0,0.55), rgba(10,9,8,0.96) 62%);
    border: 1px solid var(--hair);
    box-shadow: 0 30px 80px rgba(0,0,0,0.6), inset 0 0 80px rgba(139,0,0,0.10);
    margin-bottom: 14px;
    animation: rise .7s cubic-bezier(.2,.7,.2,1) both;
}
/* bande "scène de crime" en haut du hero */
.hero::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 8px;
    background: repeating-linear-gradient(45deg,
        var(--ember) 0 16px, #1a0000 16px 32px);
    opacity: .9;
}
.hero .fp {
    position: absolute; right: -10px; top: 40px;
    width: 230px; height: 280px;
    color: var(--ember); opacity: .10; pointer-events: none;
}
.hero .eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; letter-spacing: .32em; text-transform: uppercase;
    color: var(--ember); margin-bottom: 20px;
}
.hero h1 {
    font-family: 'Oswald', sans-serif;
    font-weight: 700; font-size: 78px; line-height: .94;
    letter-spacing: -0.5px; text-transform: uppercase;
    color: #fff; margin: 0 0 8px;
}
.hero h1 .thin { display:block; font-weight: 300; font-size: 30px; letter-spacing: .12em;
    color: var(--steel); text-transform: uppercase; margin-top: 14px; }
.hero p {
    font-size: 18px; line-height: 1.6; color: var(--text);
    max-width: 720px; margin-top: 22px;
}

/* ----- SECTION HEADERS ----- */
.section-head { margin: 58px 0 18px; animation: rise .6s ease both; }
.section-head .eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; letter-spacing: .28em; text-transform: uppercase;
    color: var(--ember); display: flex; align-items: center; gap: 12px;
}
.section-head .snum {
    color: var(--bone); background: rgba(139,0,0,0.35);
    border: 1px solid rgba(255,59,59,.35);
    padding: 3px 9px; border-radius: 6px; font-weight: 700;
}
.section-head h2 {
    font-family: 'Oswald', sans-serif; font-weight: 600;
    font-size: 40px; line-height: 1.05; letter-spacing: .2px;
    color: #fff; margin: 10px 0 0;
    padding-left: 16px; border-left: 5px solid var(--blood);
}

/* ----- CARDS ----- */
.case-card {
    background: var(--panel);
    border: 1px solid var(--hair);
    border-radius: 16px; padding: 24px 26px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.45);
    font-size: 16px; line-height: 1.65;
}
.case-card b { color: #fff; }
.case-card .src { font-size: 12.5px; color: var(--muted); font-family:'JetBrains Mono',monospace; }

/* ----- KPI / METRICS ----- */
.metric-card {
    position: relative;
    background: linear-gradient(180deg, #161313, #0c0a0a);
    border: 1px solid var(--hair);
    border-radius: 14px; padding: 22px 18px 18px;
    transition: transform .25s ease, box-shadow .25s ease, border-color .25s;
}
.metric-card::before {
    content: ""; position:absolute; top:0; left:18px; right:18px; height:2px;
    background: linear-gradient(90deg, var(--ember), transparent);
}
.metric-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255,59,59,.35);
    box-shadow: 0 22px 44px rgba(139,0,0,.28);
}
.metric-idx {
    font-family:'JetBrains Mono',monospace; font-size: 11px;
    color: var(--muted); letter-spacing:.15em;
}
.metric-value {
    font-family:'JetBrains Mono',monospace; font-weight:700;
    font-size: 40px; color:#fff; line-height:1; margin: 8px 0 6px;
}
.metric-value .sub { font-size:17px; color: var(--steel); font-weight:500; }
.metric-label {
    font-size: 12px; color: var(--muted);
    text-transform: uppercase; letter-spacing:.10em;
}

/* ----- VERDICT (conclusion) ----- */
.verdict {
    position: relative;
    background: linear-gradient(135deg, rgba(139,0,0,0.22), rgba(10,9,8,0.95));
    border: 1px solid rgba(255,59,59,.22);
    border-radius: 18px; padding: 34px 32px;
    box-shadow: 0 24px 60px rgba(0,0,0,.5);
    font-size: 16.5px; line-height: 1.7;
}
.verdict .stamp {
    font-family:'Oswald',sans-serif; font-weight:700; letter-spacing:.18em;
    color: var(--ember); text-transform: uppercase; font-size: 14px;
    margin-bottom: 12px; display:block;
}

/* widgets */
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border:1px solid var(--hair); }
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
    background: var(--ink-2) !important; border-color: var(--hair) !important;
}

/* motion */
@keyframes rise { from { opacity:0; transform: translateY(14px);} to {opacity:1; transform:none;} }
@media (prefers-reduced-motion: reduce) {
    .hero, .section-head { animation: none; }
    .metric-card { transition: none; }
}
</style>
""", unsafe_allow_html=True)

# =======================================================
#  COUCHE D'IMMERSION (overlay cinéma + overrides esthétiques)
#  S'empile par-dessus le design existant sans toucher aux graphes.
# =======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

/* overlay cinéma : grain animé + lignes de balayage + vignette */
.fx-overlay { position: fixed; inset: 0; pointer-events: none; z-index: 9998;
  background:
    repeating-linear-gradient(0deg, rgba(0,0,0,0.05) 0 1px, transparent 1px 3px),
    radial-gradient(130% 130% at 50% 35%, transparent 52%, rgba(0,0,0,0.55) 100%); }
.fx-overlay::before { content:""; position:absolute; inset:-50%;
  background-image: url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='160'%20height='160'%3E%3Cfilter%20id='n'%3E%3CfeTurbulence%20type='fractalNoise'%20baseFrequency='0.85'%20numOctaves='2'%20stitchTiles='stitch'/%3E%3C/filter%3E%3Crect%20width='100%25'%20height='100%25'%20filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: .045; animation: grain 5s steps(5) infinite; }
@keyframes grain { 0%{transform:translate(0,0)} 20%{transform:translate(-4%,3%)}
  40%{transform:translate(3%,-3%)} 60%{transform:translate(-2%,2%)}
  80%{transform:translate(2%,-1%)} 100%{transform:translate(0,0)} }

/* police "rapport tapé" pour les libellés d'enquête */
.section-head .eyebrow, .hero .eyebrow, .metric-idx, .verdict .stamp, .stamp-rot, .hero-meta {
  font-family: 'Special Elite','JetBrains Mono',monospace !important; }

/* hero renforcé : halo, léger flicker, tampon + ligne de méta */
.hero { box-shadow: 0 30px 90px rgba(0,0,0,.7), inset 0 0 120px rgba(139,0,0,.14); }
.hero h1 { text-shadow: 0 0 28px rgba(176,0,32,.45), 0 2px 0 rgba(0,0,0,.5);
  animation: flicker 7s infinite; }
@keyframes flicker { 0%,90%,100%{opacity:1} 93%{opacity:.78} 94%{opacity:1}
  96%{opacity:.86} 97%{opacity:1} }
.stamp-rot { position:absolute; top:42px; right:64px; z-index:3; transform:rotate(-11deg);
  color: rgba(255,59,59,.55); border:3px double rgba(255,59,59,.5); border-radius:8px;
  padding:6px 16px; font-size:21px; letter-spacing:.16em; text-transform:uppercase;
  font-weight:700; opacity:.85; }
.hero-meta { margin-top:22px; font-size:12px; letter-spacing:.18em; text-transform:uppercase;
  color: var(--muted); border-top:1px solid var(--hair); padding-top:14px; display:inline-block; }

/* en-têtes de section : onglet de dossier */
.section-head .eyebrow { background: rgba(20,18,18,.9); border:1px solid var(--hair);
  border-left:3px solid var(--ember); border-radius:6px 6px 0 0; padding:7px 14px; }

/* KPI : faux scellé code-barres */
.metric-card::after { content:"▮▯▮▮▯▮▯▯▮▮▯▮"; position:absolute; bottom:8px; right:12px;
  font-size:9px; letter-spacing:-1px; color: rgba(236,231,223,.16); font-family:monospace; }

/* verdict : tampon "affaire classée" */
.verdict { overflow:hidden; }
.verdict::after { content:"Affaire classée"; position:absolute; top:22px; right:24px;
  transform:rotate(8deg); color: rgba(255,59,59,.5); border:3px double rgba(255,59,59,.45);
  border-radius:8px; padding:6px 14px; font-family:'Special Elite',monospace;
  text-transform:uppercase; letter-spacing:.12em; font-size:15px; font-weight:700; }

/* sélection + barre de défilement */
::selection { background: rgba(176,0,32,.55); color:#fff; }
::-webkit-scrollbar { width:11px; }
::-webkit-scrollbar-track { background:#0a0908; }
::-webkit-scrollbar-thumb { background: linear-gradient(#5a0000,#2a0000); border-radius:6px; }

/* fiche dossier interactive (explorateur) */
.dossier { background: linear-gradient(180deg, rgba(24,21,20,.95), rgba(12,10,9,.96));
  border:1px solid var(--hair); border-left:5px solid var(--blood); border-radius:14px;
  padding:24px 26px; margin-top:14px; box-shadow:0 20px 50px rgba(0,0,0,.5);
  animation: rise .4s ease both; }
.dossier-head { display:flex; justify-content:space-between; align-items:baseline;
  flex-wrap:wrap; gap:8px; border-bottom:1px dashed var(--hair);
  padding-bottom:14px; margin-bottom:16px; }
.dossier-name { font-family:'Oswald',sans-serif; font-size:30px; font-weight:600; color:#fff;
  text-transform:uppercase; letter-spacing:.5px; }
.dossier-id { font-family:'Special Elite',monospace; font-size:13px; letter-spacing:.15em;
  color: var(--ember); }
.dossier-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:14px; margin-bottom:16px; }
.fld { display:flex; flex-direction:column; gap:4px; background:rgba(0,0,0,.25);
  border:1px solid var(--hair); border-radius:10px; padding:12px 14px; }
.fld .k { font-family:'Special Elite',monospace; font-size:10.5px; letter-spacing:.12em;
  text-transform:uppercase; color: var(--muted); }
.fld .v { font-family:'JetBrains Mono',monospace; font-size:19px; color:#fff; }
.fld .v.vred { color: var(--ember); }
.dossier-notes { background:rgba(0,0,0,.25); border:1px solid var(--hair); border-radius:10px;
  padding:14px 16px; font-size:15px; line-height:1.6; color: var(--text); }
.dossier-notes .k { display:block; font-family:'Special Elite',monospace; font-size:10.5px;
  letter-spacing:.12em; text-transform:uppercase; color: var(--muted); margin-bottom:8px; }

@media (prefers-reduced-motion: reduce) {
  .hero h1 { animation:none; } .fx-overlay::before { animation:none; } }
</style>
<div class="fx-overlay"></div>
""", unsafe_allow_html=True)


# Empreinte digitale SVG (décor du hero) — une seule ligne pour éviter
# qu'un retour à la ligne ne casse le bloc HTML interprété par Streamlit.
FINGERPRINT = (
    '<svg class="fp" viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<g stroke="currentColor" stroke-width="2.4" stroke-linecap="round">'
    '<path d="M100 30 C55 30 38 70 40 115 C41 150 55 185 70 210"/>'
    '<path d="M100 48 C66 48 56 82 58 118 C60 150 70 178 84 205" opacity=".9"/>'
    '<path d="M100 66 C76 66 72 92 74 120 C76 148 84 172 96 198" opacity=".8"/>'
    '<path d="M100 84 C86 84 86 104 88 124 C90 146 96 166 106 188" opacity=".7"/>'
    '<path d="M100 102 C95 102 98 116 100 130 C102 146 106 160 114 178" opacity=".6"/>'
    '<path d="M118 40 C150 52 162 92 160 130 C159 158 150 186 138 208" opacity=".85"/>'
    '<path d="M132 60 C156 78 162 108 158 138 C156 160 150 180 142 200" opacity=".7"/>'
    '</g></svg>'
)


# =======================================================
#  DATA  (chargé une seule fois grâce au cache)
# =======================================================
@st.cache_data(show_spinner=False)
def load_data():
    sources = {
        "df":            "serial_killers_clean.csv",
        "timeline":      "timeline_killers.csv",
        "decade":        "decade_analysis.csv",
        "country":       "country_analysis.csv",
        "crime_profile": "crime_profile.csv",
        "victim_profile":"victim_profile.csv",
        "word_freq":     "word_frequency.csv",
        "aces":          "aces_comparison.csv",
        "bio_cov":       "bio_coverage.csv",
    }
    data = {}
    for key, path in sources.items():
        try:
            data[key] = pd.read_csv(path)
        except FileNotFoundError:
            data[key] = None
    return data

data = load_data()
df = data["df"]

if df is None:
    st.error("Fichier introuvable : place `serial_killers_clean.csv` dans le dossier de app.py.")
    st.stop()


# =======================================================
#  HELPERS
# =======================================================
PLOT_FONT = "Inter, sans-serif"
HEAD_FONT = "Oswald, sans-serif"

def style_fig(fig, title_size=20):
    """Applique le thème sombre transparent à toutes les figures (DRY)."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=PLOT_FONT, color="#cfcac2", size=13),
        title_font=dict(family=HEAD_FONT, size=title_size, color="#f3efe9"),
        margin=dict(t=58, l=8, r=8, b=8),
        legend_title_text="",
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="rgba(236,231,223,0.06)", zerolinecolor="rgba(236,231,223,0.10)"),
        yaxis=dict(gridcolor="rgba(236,231,223,0.06)", zerolinecolor="rgba(236,231,223,0.10)"),
    )
    return fig

def section(num, eyebrow, title):
    st.markdown(
        f'<div class="section-head">'
        f'<div class="eyebrow"><span class="snum">{num}</span>{eyebrow}</div>'
        f'<h2>{title}</h2></div>',
        unsafe_allow_html=True,
    )

# Normalisation des pays pour la cartographie :
# on retient le pays principal (1er listé) et on convertit les États
# historiques en équivalents modernes reconnus par Plotly.
_HIST = {
    "West Germany": "Germany", "East Germany": "Germany", "German Empire": "Germany",
    "Allied-occupied Germany": "Germany", "Soviet Union": "Russia",
    "Czechoslovakia": "Czech Republic", "Austria-Hungary": "Austria",
    "Ottoman Empire": "Turkey", "Imperial State of Iran": "Iran",
    "Kingdom of Yugoslavia": "Serbia", "Republic of Macedonia": "North Macedonia",
    "SR Croatia": "Croatia", "SR Slovenia": "Slovenia", "Kingdom of Romania": "Romania",
    "Belgian Congo": "Democratic Republic of the Congo", "Portuguese Angola": "Angola",
    "Swaziland": "Eswatini",
}

@st.cache_data(show_spinner=False)
def geo_counts(country_series):
    def norm(c):
        if pd.isna(c):
            return None
        first = str(c).split(",")[0].strip()
        return _HIST.get(first, first)
    s = country_series.map(norm).dropna().value_counts()
    return s.rename_axis("Country").reset_index(name="Killers")


# =======================================================
#  HERO
# =======================================================
st.markdown(f"""
<div class="hero">
{FINGERPRINT}
<div class="stamp-rot">Confidentiel</div>
<div class="eyebrow">⦿ Dossier N° SK-757 · Accès restreint · True Crime / NLP</div>
<h1>Serial<br>Killers<span class="thin">Une enquête par les données</span></h1>
<p>757 dossiers criminels documentés, passés au crible : évolution historique, géographie de la peur, modes opératoires extraits par text-mining, et une dernière question — <b>pourquoi&nbsp;?</b></p>
<div class="hero-meta">Ouvert le 17.06.2026 · 757 sujets · 10 sources croisées · NLP</div>
</div>
""", unsafe_allow_html=True)

# ----- KPI -----
total_killers   = int(df["Name"].nunique())
proven_victims  = int(df["Proven victims"].sum())
possible_victims= int(df["Possible victims"].sum())
peak = int(data["timeline"]["active_killers"].max()) if data["timeline"] is not None else 0

kpis = [
    ("N°01", f"{total_killers}",                              "dossiers recensés"),
    ("N°02", f"{proven_victims:,}".replace(",", " "),         "victimes confirmées"),
    ("N°03", f"{possible_victims:,}".replace(",", " "),       "victimes potentielles"),
    ("N°04", f"{peak}",                                       "pic de tueurs actifs"),
]
cols = st.columns(4)
for col, (idx, value, label) in zip(cols, kpis):
    with col:
        st.markdown(f"""
<div class="metric-card">
<div class="metric-idx">{idx}</div>
<div class="metric-value">{value}</div>
<div class="metric-label">{label}</div>
</div>
""", unsafe_allow_html=True)


# =======================================================
#  01 · PROBLEMATIQUE
# =======================================================
section("01", "L'enquête", "La problématique")
st.markdown("""
<div class="case-card">
Peut-on retracer l'évolution du phénomène des serial killers à travers le <b>temps</b>,
l'<b>espace</b> et leurs <b>méthodes</b> grâce à l'analyse de données historiques et textuelles —
et au-delà du « comment », approcher le <b>pourquoi</b> ?
</div>
""", unsafe_allow_html=True)


# =======================================================
#  02 · CHRONOLOGIE
# =======================================================
section("02", "Quand", "L'année la plus dangereuse")
if data["timeline"] is not None:
    fig = px.line(data["timeline"], x="year", y="active_killers",
                  title="Nombre de serial killers actifs par année")
    fig.update_traces(line_color="#B00020", line_width=3,
                      fill="tozeroy", fillcolor="rgba(176,0,32,0.15)")
    st.plotly_chart(style_fig(fig, 22), use_container_width=True)


# =======================================================
#  03 · DECENNIES
# =======================================================
section("03", "L'âge d'or", "Le pic du phénomène")
if data["decade"] is not None:
    c1, c2 = st.columns(2)
    with c1:
        f = px.bar(data["decade"], x="Decade", y="Killers",
                   title="Serial killers par décennie")
        f.update_traces(marker_color="#8B0000")
        st.plotly_chart(style_fig(f), use_container_width=True)
    with c2:
        f = px.bar(data["decade"], x="Decade", y="Proven_Victims",
                   title="Victimes confirmées par décennie")
        f.update_traces(marker_color="#9aa0a8")
        st.plotly_chart(style_fig(f), use_container_width=True)


# =======================================================
#  04 · GEOGRAPHIE
# =======================================================
section("04", "Où", "La géographie de la peur")
geo = geo_counts(df["Country"])
if not geo.empty:
    # --- Carte mondiale (choropleth) ---
    fig_map = px.choropleth(
        geo, locations="Country", locationmode="country names",
        color="Killers", color_continuous_scale=["#2a0000", "#8B0000", "#ff3b3b"],
        title="Répartition mondiale des dossiers documentés")
    fig_map.update_geos(
        bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=False,
        showland=True, landcolor="#15110f",
        showocean=True, oceancolor="#0a0807",
        showcountries=True, countrycolor="rgba(236,231,223,0.10)",
        projection_type="natural earth", lataxis_range=[-56, 82])
    fig_map = style_fig(fig_map, 21)
    fig_map.update_layout(
        height=470, margin=dict(t=58, l=0, r=0, b=0),
        coloraxis_colorbar=dict(title="", thickness=10, len=0.55,
                                tickfont=dict(color="#cfcac2")))
    st.plotly_chart(fig_map, use_container_width=True)

    # --- Top pays (barres) ---
    top_country = geo.sort_values("Killers", ascending=False).head(15)
    f = px.bar(top_country, x="Killers", y="Country", orientation="h",
               title="Pays les plus représentés", color="Killers",
               color_continuous_scale=["#3a0000", "#8B0000", "#ff3b3b"])
    f.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(style_fig(f), use_container_width=True)
    st.markdown("""
<div class="case-card src">
À lire avec prudence : cette carte reflète la <b>documentation</b> (sources anglophones, archives en ligne), pas la prévalence réelle pays par pays. Les pays sont normalisés (État historique → équivalent moderne, pays principal retenu).
</div>
""", unsafe_allow_html=True)


# =======================================================
#  05 · METHODES (NLP)
# =======================================================
section("05", "Comment", "Les modes opératoires")
n1, n2 = st.columns(2)
with n1:
    if data["crime_profile"] is not None:
        f = px.bar(data["crime_profile"].sort_values("Count"),
                   x="Count", y="Profile", orientation="h",
                   title="Méthodes détectées dans les descriptions")
        f.update_traces(marker_color="#8B0000")
        st.plotly_chart(style_fig(f), use_container_width=True)
with n2:
    if data["victim_profile"] is not None:
        f = px.treemap(data["victim_profile"], path=["Victim_Type"], values="Count",
                       title="Victimes les plus ciblées",
                       color="Count", color_continuous_scale=["#2a0000", "#B00020"])
        f.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_fig(f), use_container_width=True)

if data["word_freq"] is not None:
    f = px.bar(data["word_freq"].sort_values("Frequency").tail(20),
               x="Frequency", y="Word", orientation="h",
               title="Termes les plus fréquents dans les descriptions")
    f.update_traces(marker_color="#9aa0a8")
    f.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(style_fig(f), use_container_width=True)


# =======================================================
#  06 · LE POURQUOI
# =======================================================
section("06", "Pourquoi", "L'enfance derrière le crime")
aces, bio_cov = data["aces"], data["bio_cov"]

st.markdown("""
<div class="case-card">
Jusqu'ici : <b>quand</b>, <b>où</b>, <b>comment</b>. Reste la question la plus difficile.
Nos 757 dossiers décrivent les crimes, presque jamais les trajectoires : seuls <b>1,6&nbsp;%</b>
des résumés évoquent un abus durant l'enfance. Ce silence est une limite de <i>nos</i> données,
pas une réalité. Pour approcher le « pourquoi », nous connectons une <b>source externe</b> :
l'étude de Mitchell &amp; Aamodt (2005, Radford University), qui a codé la maltraitance infantile
chez les tueurs en série <i>et</i> dans la population générale.
</div>
""", unsafe_allow_html=True)

g1, g2, g3 = st.columns(3)
for col, (lbl, sk, gp) in zip(
    [g1, g2, g3],
    [("Abus psychologique", 50, 2), ("Abus physique", 36, 6), ("Abus sexuel", 26, 3)]
):
    with col:
        st.markdown(f"""
<div class="metric-card">
<div class="metric-idx">Tueurs vs population</div>
<div class="metric-value">{sk}% <span class="sub">vs {gp}%</span></div>
<div class="metric-label">{lbl}</div>
</div>
""", unsafe_allow_html=True)

st.write("")
if aces is not None:
    aces_long = aces.melt(id_vars="Abuse_Type",
                          value_vars=["Serial_Killers", "General_Population"],
                          var_name="Population", value_name="Prevalence")
    aces_long["Population"] = aces_long["Population"].map(
        {"Serial_Killers": "Tueurs en série", "General_Population": "Population générale"})
    f = px.bar(aces_long, x="Abuse_Type", y="Prevalence", color="Population", barmode="group",
               title="Maltraitance durant l'enfance : tueurs en série vs population générale (%)",
               color_discrete_map={"Tueurs en série": "#B00020", "Population générale": "#9aa0a8"})
    f.update_layout(yaxis_title="% des individus concernés", xaxis_title="")
    st.plotly_chart(style_fig(f, 21), use_container_width=True)

if bio_cov is not None:
    st.markdown("""
<div class="case-card">
Ce que <b>nos</b> notes mentionnent explicitement (≠ prévalence réelle) : la documentation se concentre sur les actes, rarement sur le passé du criminel — d'où la nécessité d'une source dédiée.
</div>
""", unsafe_allow_html=True)
    st.write("")
    f = px.bar(bio_cov.sort_values("Pct"), x="Pct", y="Factor", orientation="h",
               title="Facteurs biographiques mentionnés dans nos 757 résumés (%)")
    f.update_traces(marker_color="#8B0000")
    f.update_layout(xaxis_title="% des dossiers", yaxis_title="")
    st.plotly_chart(style_fig(f), use_container_width=True)

st.markdown("""
<div class="case-card">
<b>Comment lire ces écarts ?</b> Ils pointent vers le <b>cycle de la violence</b> (Joel Norris) :
des enfances marquées par la maltraitance ou la négligence augmentent le risque de comportements
violents à l'âge adulte. La criminologie a aussi repéré des marqueurs précoces (la « triade de
Macdonald » : énurésie tardive, fascination pour le feu, cruauté envers les animaux), souvent
associés à un foyer instable.
<br><br>
<b>Attention au piège.</b> Corrélation n'est pas causalité : l'immense majorité des enfants
maltraités ne deviennent <i>jamais</i> violents. La maltraitance est un <b>facteur de risque</b>
parmi d'autres (neurologiques, psychiatriques, sociaux), pas une fatalité ni une excuse. Le
passage à l'acte reste multifactoriel et rare.
<br><br>
<span class="src">Source : Mitchell, H. &amp; Aamodt, M. G. (2005). The incidence of child abuse
in serial killers. Journal of Police and Criminal Psychology, 20(1), 40-47.</span>
</div>
""", unsafe_allow_html=True)


# =======================================================
#  07 · EXPLORER
# =======================================================
section("07", "Pièces à conviction", "Explorer les dossiers")

fc1, fc2 = st.columns([1, 2])
with fc1:
    selected_country = st.selectbox(
        "Filtrer par pays",
        ["Tous"] + sorted(df["Country"].dropna().unique().tolist()))
with fc2:
    search = st.text_input("Rechercher un nom")

filtered = df
if selected_country != "Tous":
    filtered = filtered[filtered["Country"] == selected_country]
if search:
    filtered = filtered[filtered["Name"].str.contains(search, case=False, na=False)]

st.caption(f"{len(filtered)} dossier(s) correspondant(s)")
st.dataframe(
    filtered[["Name", "Country", "Start year", "End year",
              "Proven victims", "Possible victims", "Notes"]],
    use_container_width=True, height=420, hide_index=True,
    column_config={
        "Name": "Nom",
        "Country": "Pays",
        "Start year": st.column_config.NumberColumn("Début", format="%d"),
        "End year": st.column_config.NumberColumn("Fin", format="%d"),
        "Proven victims": st.column_config.NumberColumn("Confirmées"),
        "Possible victims": st.column_config.NumberColumn("Potentielles"),
        "Notes": st.column_config.TextColumn("Notes", width="large"),
    },
)

# --- Fiche dossier interactive ---
st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
names = sorted(filtered["Name"].dropna().unique().tolist())
choice = st.selectbox("Ouvrir un dossier", ["— Sélectionner un dossier —"] + names)

if choice != "— Sélectionner un dossier —" and names:
    row = filtered[filtered["Name"] == choice].iloc[0]

    def _year(v): return str(int(v)) if pd.notna(v) else "—"
    def _int(v):  return str(int(v)) if pd.notna(v) else "—"

    sy, ey = row["Start year"], row["End year"]
    period = f"{_year(sy)} – {_year(ey)}"
    dur = f"{int(ey - sy)} an(s)" if (pd.notna(sy) and pd.notna(ey) and ey >= sy) else "—"
    country = row["Country"] if pd.notna(row["Country"]) else "—"
    notes = row["Notes"] if pd.notna(row["Notes"]) else "Aucune note disponible."
    notes = str(notes).replace("<", "&lt;").replace(">", "&gt;")
    case_id = f"SK-{int(row.name):04d}"

    st.markdown(f"""
<div class="dossier">
<div class="dossier-head">
<div class="dossier-name">{choice}</div>
<div class="dossier-id">Dossier N° {case_id} · Classé</div>
</div>
<div class="dossier-grid">
<div class="fld"><span class="k">Pays</span><span class="v">{country}</span></div>
<div class="fld"><span class="k">Période active</span><span class="v">{period}</span></div>
<div class="fld"><span class="k">Durée</span><span class="v">{dur}</span></div>
<div class="fld"><span class="k">Victimes confirmées</span><span class="v vred">{_int(row['Proven victims'])}</span></div>
<div class="fld"><span class="k">Victimes potentielles</span><span class="v">{_int(row['Possible victims'])}</span></div>
</div>
<div class="dossier-notes"><span class="k">Notes d'enquête</span>{notes}</div>
</div>
""", unsafe_allow_html=True)


# =======================================================
#  VERDICT
# =======================================================
st.markdown('<div class="section-head"><div class="eyebrow">'
            '<span class="snum">★</span>Clôture du dossier</div></div>',
            unsafe_allow_html=True)
st.markdown("""
<div class="verdict">
<span class="stamp">⎯ Verdict de l'enquête ⎯</span>
Le phénomène se concentre fortement sur certaines périodes — surtout la seconde moitié du
XX<sup>e</sup> siècle — et sur quelques pays sur-représentés dans les sources. Le text-mining
révèle des schémas récurrents dans les méthodes et les catégories de victimes. Enfin, là où nos
données s'arrêtent au « comment », une source externe éclaire le « pourquoi » : une enfance
marquée par la maltraitance est nettement sur-représentée — un facteur de risque, jamais une
fatalité.
<br><br>
Ce site complète le notebook Colab et le dashboard Power BI en offrant une lecture continue,
interactive et documentée de l'ensemble de l'analyse.
</div>
""", unsafe_allow_html=True)