import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import json
import ssl
import urllib.request
import urllib.parse

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
.dossier-top { display:flex; gap:22px; align-items:flex-start; flex-wrap:wrap; }
.dossier-main { flex:1; min-width:260px; }
.mug { width:150px; flex-shrink:0; border-radius:10px; overflow:hidden;
  border:1px solid rgba(255,59,59,.30); background:#100d0c;
  box-shadow:0 10px 26px rgba(0,0,0,.5); position:relative; }
.mug::after { content:"PIÈCE N°1"; position:absolute; bottom:0; left:0; right:0;
  text-align:center; font-family:'Special Elite',monospace; font-size:9px; letter-spacing:.12em;
  color:#cfcac2; background:rgba(0,0,0,.6); padding:3px 0; }
.mug img, .mug svg { display:block; width:150px; height:180px; object-fit:cover;
  filter:grayscale(100%) contrast(1.06) brightness(.96); }
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

def norm_country(c):
    if pd.isna(c):
        return None
    first = str(c).split(",")[0].strip()
    return _HIST.get(first, first)

@st.cache_data(show_spinner=False)
def geo_counts(country_series):
    s = country_series.map(norm_country).dropna().value_counts()
    return s.rename_axis("Country").reset_index(name="Killers")

@st.cache_data(show_spinner=False)
def decade_race(country_series, start_series, proven_series, top_n=10):
    d = pd.DataFrame({
        "Country": country_series.map(norm_country),
        "Decade": (start_series // 10 * 10),
        "Proven": proven_series,
    }).dropna(subset=["Country", "Decade"])
    d["Decade"] = d["Decade"].astype(int)
    d = d[(d["Decade"] >= 1850) & (d["Decade"] <= 2020)]
    top = d["Country"].value_counts().head(top_n).index.tolist()
    d = d[d["Country"].isin(top)]
    decades = sorted(d["Decade"].unique())
    grp = (d.groupby(["Decade", "Country"])
             .agg(Killers=("Country", "size"), Victims=("Proven", "sum"))
             .reset_index())
    full = pd.MultiIndex.from_product([decades, top], names=["Decade", "Country"])
    grp = grp.set_index(["Decade", "Country"]).reindex(full, fill_value=0).reset_index()
    grp = grp.sort_values("Decade")
    grp["CumKillers"] = grp.groupby("Country")["Killers"].cumsum()
    grp["CumVictims"] = grp.groupby("Country")["Victims"].cumsum()
    return grp

@st.cache_data(show_spinner=False)
def decade_metrics(start_series, end_series, proven_series):
    d = pd.DataFrame({"Start": start_series, "End": end_series,
                      "Proven": proven_series}).dropna(subset=["Start"])
    d["Decade"] = (d["Start"] // 10 * 10).astype(int)
    d["Career"] = d["End"] - d["Start"]
    d = d[(d["Decade"] >= 1960) & (d["Decade"] <= 2020)]
    return (d.groupby("Decade")
              .agg(Killers=("Start", "size"), AvgCareer=("Career", "mean"))
              .reset_index())

_WIKI_UA = "SerialKillersDataViz/1.0 (projet etudiant; contact: student@example.com)"

# Contexte SSL fiable (corrige CERTIFICATE_VERIFY_FAILED sur macOS / certains environnements)
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _SSL_CTX = ssl.create_default_context()

def _wiki_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": _WIKI_UA})
    try:
        with urllib.request.urlopen(req, timeout=6, context=_SSL_CTX) as r:
            return json.loads(r.read().decode("utf-8"))
    except ssl.SSLError:
        # Repli : certificats locaux non configurés (fréquent sur macOS).
        # Données publiques (images Wikipédia) -> repli acceptable.
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=6, context=ctx) as r:
            return json.loads(r.read().decode("utf-8"))

@st.cache_data(show_spinner=False, ttl=86400)
def get_mugshot(name):
    """1) recherche le bon article  2) récupère sa vignette. None si rien."""
    q = name.split(",")[0].split(" and ")[0].split(" et ")[0].strip()
    try:
        # 1) recherche (gère orthographes / homonymes / redirections)
        search = _wiki_get("https://en.wikipedia.org/w/rest.php/v1/search/page?limit=1&q="
                           + urllib.parse.quote(q))
        pages = search.get("pages", [])
        if not pages:
            return None
        title = pages[0]["key"]
        # 2) résumé de l'article -> vignette
        summary = _wiki_get("https://en.wikipedia.org/api/rest_v1/page/summary/"
                            + urllib.parse.quote(title))
        return (summary.get("thumbnail") or {}).get("source")
    except Exception:
        return None

# Silhouette de secours quand aucune photo n'est trouvée
MUG_PLACEHOLDER = (
    '<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="120" fill="#100d0c"/>'
    '<circle cx="50" cy="44" r="20" fill="none" stroke="#5a4a48" stroke-width="3"/>'
    '<path d="M20 108 C20 82 80 82 80 108" fill="none" stroke="#5a4a48" stroke-width="3"/>'
    '<text x="50" y="118" text-anchor="middle" fill="#5a4a48" '
    'font-family="monospace" font-size="7">SANS PHOTO</text></svg>'
)


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

# ----- KPI (compteurs animés) -----
total_killers   = int(df["Name"].nunique())
proven_victims  = int(df["Proven victims"].sum())
possible_victims= int(df["Possible victims"].sum())
peak = int(data["timeline"]["active_killers"].max()) if data["timeline"] is not None else 0

kpi_items = [
    ("N°01", total_killers,    "dossiers recensés"),
    ("N°02", proven_victims,   "victimes confirmées"),
    ("N°03", possible_victims, "victimes potentielles"),
    ("N°04", peak,             "pic de tueurs actifs"),
]
_cards = "".join(
    f'<div class="kpi"><div class="kpi-idx">{idx}</div>'
    f'<div class="kpi-value" data-target="{val}">0</div>'
    f'<div class="kpi-label">{lbl}</div></div>'
    for idx, val, lbl in kpi_items
)

KPI_HTML = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Special+Elite&family=Inter:wght@500&display=swap');
* { box-sizing: border-box; margin: 0; }
body { background: transparent; font-family: 'Inter', sans-serif; overflow: hidden; }
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi { position: relative; overflow: hidden; padding: 22px 18px 18px;
  background: linear-gradient(180deg,#161313,#0c0a0a);
  border: 1px solid rgba(236,231,223,0.10); border-radius: 14px;
  transition: transform .25s, box-shadow .25s, border-color .25s; }
.kpi::before { content:""; position:absolute; top:0; left:18px; right:18px; height:2px;
  background: linear-gradient(90deg,#ff3b3b,transparent); }
.kpi::after { content:"▮▯▮▮▯▮▯▯▮▮▯▮"; position:absolute; bottom:8px; right:12px;
  font-size:9px; letter-spacing:-1px; color:rgba(236,231,223,.16); font-family:monospace; }
.kpi:hover { transform: translateY(-5px); border-color: rgba(255,59,59,.35);
  box-shadow: 0 22px 44px rgba(139,0,0,.28); }
.kpi-idx { font-family:'Special Elite',monospace; font-size:11px; color:#8a8079; letter-spacing:.15em; }
.kpi-value { font-family:'JetBrains Mono',monospace; font-weight:700; font-size:40px;
  color:#fff; line-height:1; margin:8px 0 6px; }
.kpi-label { font-size:12px; color:#8a8079; text-transform:uppercase; letter-spacing:.10em; }
@media (max-width:640px){ .kpi-row{ grid-template-columns: repeat(2,1fr); } }
</style>
<div class="kpi-row">__CARDS__</div>
<script>
(function(){
  function fmt(n){ return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,' '); }
  function run(el){
    var target = +el.dataset.target, dur = 1300, t0 = performance.now();
    function tick(now){
      var p = Math.min((now - t0)/dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * e);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  document.querySelectorAll('.kpi-value').forEach(run);
})();
</script>
"""
components.html(KPI_HTML.replace("__CARDS__", _cards), height=160)


# =======================================================
#  01 · PROBLEMATIQUE
# =======================================================
section("01", "L'enquête", "La problématique")
st.markdown("""
<div class="case-card">
Peut-on retracer l'<b>essor</b> et le <b>déclin</b> des tueurs en série grâce aux données — et ces données reflètent-elles la <b>réalité</b> du phénomène, ou seulement ce qu'on en a <b>documenté</b> ?
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

# --- Frise animée : accumulation par pays, décennie par décennie ---
grp = decade_race(df["Country"], df["Start year"], df["Proven victims"])
if not grp.empty:
    xmax, ymax = grp["CumKillers"].max(), grp["CumVictims"].max()
    fig_race = px.scatter(
        grp, x="CumKillers", y="CumVictims", size="CumKillers", color="Country",
        animation_frame="Decade", hover_name="Country", size_max=50,
        range_x=[-xmax * 0.03, xmax * 1.12], range_y=[-ymax * 0.04, ymax * 1.12],
        title="Montée du phénomène, décennie par décennie (cumul par pays)",
        labels={"CumKillers": "Tueurs cumulés", "CumVictims": "Victimes cumulées"},
        color_discrete_sequence=px.colors.qualitative.Set3)
    fig_race.update_traces(marker=dict(line=dict(width=0.6, color="rgba(0,0,0,0.45)"),
                                       opacity=0.88))
    st.plotly_chart(style_fig(fig_race, 20), use_container_width=True)
    st.caption("▶ Appuie sur « lecture » pour voir les 10 pays les plus touchés s'accumuler décennie après décennie.")

st.markdown("""
<div class="case-card">
<b>Pourquoi ce pic — puis ce déclin ?</b> Plutôt que de l'affirmer, regardons les données.
</div>
""", unsafe_allow_html=True)
st.write("")

dm = decade_metrics(df["Start year"], df["End year"], df["Proven victims"])
cc1, cc2 = st.columns(2)

with cc1:
    fdur = px.line(dm, x="Decade", y="AvgCareer", markers=True,
                   title="Durée d'activité moyenne par décennie")
    fdur.update_traces(line_color="#B00020", line_width=3,
                       marker=dict(size=8, color="#ff3b3b"))
    fdur.update_layout(yaxis_title="années avant arrêt", xaxis_title="")
    st.plotly_chart(style_fig(fdur, 18), use_container_width=True)

with cc2:
    mobile = pd.DataFrame({"Decade": [1960, 1970, 1980, 1990, 2000, 2010, 2020],
                           "Mobile": [0, 0, 0, 2, 39, 91, 107]})
    mm = dm.merge(mobile, on="Decade", how="left")
    fov = make_subplots(specs=[[{"secondary_y": True}]])
    fov.add_bar(x=mm["Decade"], y=mm["Killers"], name="Tueurs (échelle gauche)",
                marker_color="#8B0000", opacity=0.9)
    fov.add_scatter(x=mm["Decade"], y=mm["Mobile"], name="Mobiles /100 hab. (échelle droite)",
                    mode="lines+markers", line=dict(color="#C0C0C0", width=3),
                    marker=dict(size=7), secondary_y=True)
    fov = style_fig(fov, 18)
    fov.update_layout(
        title="Tueurs par décennie vs adoption du mobile",
        legend=dict(orientation="h", yanchor="top", y=-0.16, x=0.5, xanchor="center"),
        margin=dict(t=52, b=60, l=8, r=8))
    fov.update_yaxes(title_text="tueurs", secondary_y=False,
                     title_font_color="#d9534f", tickfont_color="#d9534f")
    fov.update_yaxes(title_text="mobiles / 100 hab.", secondary_y=True, showgrid=False,
                     title_font_color="#C0C0C0", tickfont_color="#C0C0C0")
    st.plotly_chart(fov, use_container_width=True)

st.markdown("""
<div class="case-card" style="border-left:4px solid #B00020;">
<div style="font-family:'Special Elite',monospace; color:#ff3b3b; letter-spacing:.14em; text-transform:uppercase; font-size:13px; margin-bottom:10px;">Conclusion — ce que les données disent du pic</div>

<b>1. La montée et le sommet (données).</b> Le nombre de tueurs grimpe de <b>56</b> (années 1960) à <b>116</b> (1970) puis culmine à <b>155</b> dans les années 1980. Pendant cet « âge d'or », les tueurs restaient actifs <b>longtemps</b> — jusqu'à <b>~9-10 ans</b> en moyenne avant d'être arrêtés. Cette <b>fenêtre d'impunité</b> est le moteur du pic.
<br><br>
<b>2. Le déclin (directement mesurable).</b> La durée d'activité moyenne s'effondre à <b>3,6 ans</b> dans les années 2010 : les tueurs sont neutralisés bien plus vite. C'est la <b>signature, dans nos propres données</b>, des progrès de l'enquête (ADN, vidéosurveillance, téléphone) — que l'overlay avec l'adoption du mobile illustre.
<br><br>
<b>3. Ce qu'on ne sur-interprète pas.</b> Corrélation n'est pas causalité ; les causes <i>profondes</i> de la montée (mobilité, anonymat des victimes, contagion médiatique) ne sont <b>pas</b> dans notre dataset — on les tire de la littérature. Et une part du creux récent est un <b>artefact</b> : nos données ne contiennent que des affaires <b>résolues</b> (Golden State Killer identifié en 2018, Gilgo Beach en 2023), donc les dernières décennies sont <b>sous-comptées</b>.
<br><br>
Le « pic » n'est donc pas qu'un nombre : c'est l'empreinte d'une <b>époque où l'on tuait longtemps avant d'être pris</b> — une fenêtre que la technologie a refermée.
<br><br>
<span class="src">Sources : J. A. Fox (Northeastern University) ; M. Aamodt (Radford/FGCU) ; adoption du mobile : ITU / Banque mondiale (États-Unis).</span>
</div>
""", unsafe_allow_html=True)


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
#  05 · PROFILS (intensité)
# =======================================================
section("05", "Qui", "Profils extrêmes : l'intensité meurtrière")
prof = df.copy()
prof["Career"] = prof["End year"] - prof["Start year"]
prof = prof[prof["Career"].notna() & (prof["Career"] >= 0) & prof["Proven victims"].notna()]
prof["PerYear"] = (prof["Proven victims"] / prof["Career"].replace(0, 1)).round(1)
if not prof.empty:
    fig_sc = px.scatter(
        prof, x="Career", y="Proven victims",
        size="Proven victims", color="PerYear", hover_name="Name", size_max=34,
        color_continuous_scale=["#6b6b6b", "#8B0000", "#ff3b3b"],
        title="Durée d'activité vs victimes confirmées",
        labels={"Career": "Années d'activité", "Proven victims": "Victimes confirmées",
                "PerYear": "Victimes/an"})
    fig_sc.update_traces(marker=dict(line=dict(width=0.5, color="rgba(0,0,0,0.4)"), opacity=0.85))
    fig_sc.update_layout(coloraxis_colorbar=dict(title="Vict./an", thickness=10, len=0.6))
    st.plotly_chart(style_fig(fig_sc, 20), use_container_width=True)
    st.markdown("""
<div class="case-card src">
Chaque point est un tueur. À <b>droite</b>, des « carrières » étalées sur des décennies ; en <b>haut à gauche</b>, les profils les plus intenses — beaucoup de victimes en très peu de temps. La couleur (rouge vif) signale ce rythme meurtrier élevé. La taille est proportionnelle au nombre de victimes confirmées.
</div>
""", unsafe_allow_html=True)


# =======================================================
#  06 · METHODES (NLP)
# =======================================================
section("06", "Comment", "Les modes opératoires")
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
#  07 · LE POURQUOI
# =======================================================
section("07", "Pourquoi", "L'enfance derrière le crime")
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
#  08 · EXPLORER
# =======================================================
section("08", "Pièces à conviction", "Explorer les dossiers")

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

    photo = get_mugshot(choice)
    mug = f'<img src="{photo}" alt="">' if photo else MUG_PLACEHOLDER

    st.markdown(f"""
<div class="dossier">
<div class="dossier-top">
<div class="mug">{mug}</div>
<div class="dossier-main">
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
</div>
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
<b>Oui, les données permettent de retracer l'essor et le déclin des tueurs en série.</b> Le phénomène monte fortement jusqu'aux années 1980-90, puis recule. Et nos données expliquent ce recul : les tueurs restent actifs de moins en moins longtemps (de ≈ 9 ans à 3,6 ans), preuve qu'on les arrête plus vite — grâce à l'ADN, aux caméras et au téléphone.
<br><br>
Mais nos données montrent surtout ce qui a été <b>documenté</b>, pas toute la réalité. La carte reflète les pays les mieux couverts par les sources. Le déclin récent est en partie trompeur, car les affaires non encore résolues n'y figurent pas. Et nos dossiers ne disent pas le « pourquoi » : il a fallu une autre source pour voir le poids de l'enfance maltraitée.
<br><br>
La leçon : on peut retracer le phénomène par les données, à condition de ne pas confondre <b>la réalité avec ce qu'on en a gardé comme trace</b>. Dossier classé.
</div>
""", unsafe_allow_html=True)


# =======================================================
#  OUVERTURE
# =======================================================
st.markdown('<div class="section-head"><div class="eyebrow">'
            '<span class="snum">→</span>Ouverture</div>'
            '<h2>Une affaire en ouvre une autre</h2></div>',
            unsafe_allow_html=True)

ms = pd.DataFrame({"Decade": [1980, 1990, 2000, 2010],
                   "MassShootings": [2.6, 3.5, 4.1, 5.7]})
relay = dm[dm["Decade"].isin([1980, 1990, 2000, 2010])][["Decade", "Killers"]].merge(ms, on="Decade")

fig_o = make_subplots(specs=[[{"secondary_y": True}]])
fig_o.add_bar(x=relay["Decade"], y=relay["Killers"],
              name="Tueurs en série (échelle gauche)", marker_color="#8B0000", opacity=0.9)
fig_o.add_scatter(x=relay["Decade"], y=relay["MassShootings"],
                  name="Tueries de masse / an, É.-U. (échelle droite)",
                  mode="lines+markers", line=dict(color="#ff8c42", width=3),
                  marker=dict(size=9), secondary_y=True)
fig_o = style_fig(fig_o, 20)
fig_o.update_layout(
    title="Passage de relais ? Déclin des tueurs en série vs montée des tueries de masse",
    legend=dict(orientation="h", yanchor="top", y=-0.16, x=0.5, xanchor="center"),
    margin=dict(t=52, b=60, l=8, r=8))
fig_o.update_yaxes(title_text="tueurs en série (par décennie)", secondary_y=False,
                   title_font_color="#d9534f", tickfont_color="#d9534f")
fig_o.update_yaxes(title_text="tueries de masse / an (É.-U.)", secondary_y=True, showgrid=False,
                   title_font_color="#ff8c42", tickfont_color="#ff8c42")
st.plotly_chart(fig_o, use_container_width=True)

st.markdown("""
<div class="case-card" style="border-left:4px solid #ff8c42;">
<b>Et après ?</b> Notre enquête se referme sur un déclin — mais ce déclin coïncide avec la <b>montée d'une autre violence</b>. Là où les tueurs en série s'effacent après les années 1990, les <b>tueries de masse</b> progressent : aux États-Unis, leur fréquence passe d'environ <b>2,6 par an</b> (années 1980) à <b>5,7</b> (années 2010). Comme si une forme de violence en relayait une autre — l'acte caché et répété cédant la place à l'acte unique, public et spectaculaire.
<br><br>
<b>Prudence.</b> Les deux ne se mesurent pas sur la même échelle (tueurs recensés dans le monde vs tueries de masse annuelles aux États-Unis), et cette coïncidence dans le temps n'est <b>pas une preuve de causalité</b> : c'est une <b>hypothèse</b> discutée par les criminologues, et une piste pour une prochaine enquête.
<br><br>
<span class="src">Source : J. A. Fox, <i>Trends in U.S. Mass Shootings: Facts, Fears and Fatalities</i> (2024).</span>
</div>
""", unsafe_allow_html=True)