#!/usr/bin/env python3
"""
AI Job Displacement Tracker - Dashboard Generator
Google Sheets JSON -> WIRED-inspired interactive HTML dashboard

Input:  /tmp/agent-wip/displacement-data.json (Sheets API response)
Output: /Users/ryo/Documents/09_HTML/AGI-hub/displacement-map.html
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────
INPUT_PATH  = Path("/tmp/agent-wip/displacement-data.json")
OUTPUT_PATH = Path("/Users/ryo/Documents/09_HTML/AGI-hub/displacement-map.html")

# ── Country coordinates (ISO name -> lat/lng) ────────────────
COUNTRY_COORDS = {
    "United States": (39.8, -98.5),
    "United Kingdom": (54.0, -2.0),
    "India": (20.6, 78.9),
    "China": (35.9, 104.2),
    "Japan": (36.2, 138.3),
    "Germany": (51.2, 10.4),
    "France": (46.6, 2.2),
    "Canada": (56.1, -106.3),
    "Australia": (-25.3, 133.8),
    "Brazil": (-14.2, -51.9),
    "South Korea": (35.9, 127.8),
    "Singapore": (1.35, 103.8),
    "Spain": (40.5, -3.7),
    "South Africa": (-30.6, 22.9),
    "Sweden": (60.1, 18.6),
    "Netherlands": (52.1, 5.3),
    "Israel": (31.0, 34.9),
    "Mexico": (23.6, -102.6),
    "Italy": (41.9, 12.5),
    "Russia": (61.5, 105.3),
    "Switzerland": (46.8, 8.2),
    "Ireland": (53.1, -7.7),
    "Poland": (51.9, 19.1),
    "Turkey": (38.9, 35.2),
    "Indonesia": (-0.8, 113.9),
    "Thailand": (15.9, 100.9),
    "Vietnam": (14.1, 108.3),
    "Philippines": (12.9, 121.8),
    "Malaysia": (4.2, 101.9),
    "Taiwan": (23.7, 121.0),
    "Nigeria": (9.1, 8.7),
    "Kenya": (-0.02, 37.9),
    "Egypt": (26.8, 30.8),
    "Saudi Arabia": (23.9, 45.1),
    "UAE": (23.4, 53.8),
    "Argentina": (-38.4, -63.6),
    "Chile": (-35.7, -71.5),
    "Colombia": (4.6, -74.1),
    "New Zealand": (-40.9, 174.9),
    "Norway": (60.5, 8.5),
    "Denmark": (56.3, 9.5),
    "Finland": (61.9, 25.7),
    "Belgium": (50.5, 4.5),
    "Austria": (47.5, 14.6),
    "Portugal": (39.4, -8.2),
    "Czech Republic": (49.8, 15.5),
    "Romania": (45.9, 24.9),
    "Greece": (39.1, 21.8),
    "Hungary": (47.2, 19.5),
    "Pakistan": (30.4, 69.3),
    "Bangladesh": (23.7, 90.4),
    "Sri Lanka": (7.9, 80.8),
    "Global": (20.0, 0.0),
}

# ── Industry display names ────────────────────────────────────
INDUSTRY_LABELS = {
    "tech": "Tech",
    "finance": "Finance",
    "manufacturing": "Manufacturing",
    "media": "Media",
    "retail": "Retail",
    "healthcare": "Healthcare",
    "government": "Government",
    "transport": "Transport",
    "education": "Education",
    "professional_services": "Professional Services",
    "other": "Other",
}

# ── WIRED monotone palette for donut chart ────────────────────
INDUSTRY_COLORS = [
    "#1a1a1a",  # black
    "#b23a2f",  # red accent
    "#4a4a4a",  # dark gray
    "#6b6b6b",  # mid gray
    "#8c8c8c",  # gray
    "#a8a8a8",  # light gray
    "#c4c4c4",  # lighter gray
    "#d9d9d9",  # very light
    "#3d3d3d",  # near-black
    "#585858",  # medium
    "#e0e0e0",  # pale
]


def fmt_k(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def parse_data(path: Path) -> list[dict]:
    """Parse Sheets API JSON into list of article dicts."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = raw["values"]
    headers = rows[0]
    articles = []
    for row in rows[1:]:
        # Pad row to header length
        padded = row + [""] * (len(headers) - len(row))
        d = dict(zip(headers, padded))
        # Parse jobs_affected
        jobs_str = d.get("jobs_affected", "").strip().replace(",", "")
        d["_jobs"] = int(jobs_str) if jobs_str.isdigit() else 0
        articles.append(d)
    return articles


def aggregate_by_country(articles: list[dict]) -> dict:
    """Group articles by country, compute totals."""
    countries = defaultdict(lambda: {
        "jobs": 0, "count": 0, "industries": [],
    })
    for a in articles:
        c = a.get("country", "").strip()
        if not c:
            continue
        countries[c]["jobs"] += a["_jobs"]
        countries[c]["count"] += 1
        ind = a.get("industry", "other")
        countries[c]["industries"].append(ind)
    return dict(countries)


def aggregate_by_industry(articles: list[dict]) -> list[tuple[str, int]]:
    """Count articles per industry, sorted descending."""
    counter = Counter(a.get("industry", "other") for a in articles)
    return counter.most_common()


def aggregate_monthly(articles: list[dict]) -> list[dict]:
    """Group by YYYY-MM, compute count and jobs."""
    monthly = defaultdict(lambda: {"count": 0, "jobs": 0})
    for a in articles:
        date_str = a.get("news_date", "")
        if len(date_str) >= 7:
            month = date_str[:7]
            monthly[month]["count"] += 1
            monthly[month]["jobs"] += a["_jobs"]
    return [
        {"month": m, "count": v["count"], "jobs": v["jobs"]}
        for m, v in sorted(monthly.items())
    ]


def aggregate_top_companies(articles: list[dict], top_n: int = 10) -> list[dict]:
    """Top companies by affected jobs."""
    companies = defaultdict(lambda: {"jobs": 0, "count": 0})
    for a in articles:
        comp = a.get("company", "").strip()
        if not comp:
            continue
        companies[comp]["jobs"] += a["_jobs"]
        companies[comp]["count"] += 1
    sorted_c = sorted(companies.items(), key=lambda x: x[1]["jobs"], reverse=True)[:top_n]
    return [{"company": c, "jobs": d["jobs"], "count": d["count"]} for c, d in sorted_c]


def build_map_data(country_data: dict) -> list[dict]:
    """Build data for Leaflet map bubbles."""
    rows = []
    for country, d in country_data.items():
        coords = COUNTRY_COORDS.get(country)
        if not coords:
            continue
        top_industry = Counter(d["industries"]).most_common(1)
        top_ind = top_industry[0][0] if top_industry else "other"
        rows.append({
            "country": country,
            "lat": coords[0],
            "lng": coords[1],
            "jobs": d["jobs"],
            "count": d["count"],
            "top_industry": INDUSTRY_LABELS.get(top_ind, top_ind),
        })
    return rows


def build_country_bars(country_data: dict, top_n: int = 10) -> list[dict]:
    """Top N countries by jobs affected for horizontal bar chart."""
    sorted_c = sorted(
        country_data.items(),
        key=lambda x: x[1]["jobs"] if x[1]["jobs"] else x[1]["count"] * 500,
        reverse=True,
    )[:top_n]
    return [
        {"country": c, "jobs": d["jobs"] if d["jobs"] else d["count"] * 500, "count": d["count"]}
        for c, d in sorted_c
    ]


def generate_html(articles: list[dict]) -> str:
    """Generate complete WIRED-style HTML dashboard."""
    country_data = aggregate_by_country(articles)
    industry_data = aggregate_by_industry(articles)
    monthly_data = aggregate_monthly(articles)

    total_jobs = sum(a["_jobs"] for a in articles)
    n_articles = len(articles)
    n_countries = len(country_data)
    n_industries = len(set(a.get("industry", "other") for a in articles))

    # Latest date
    dates = [a.get("news_date", "") for a in articles if a.get("news_date")]
    latest_date = max(dates) if dates else "N/A"

    # JSON data for JS
    map_data = build_map_data(country_data)
    country_bars = build_country_bars(country_data)

    # Industry donut data with colors
    donut_data = []
    for i, (ind, count) in enumerate(industry_data):
        donut_data.append({
            "label": INDUSTRY_LABELS.get(ind, ind),
            "count": count,
            "color": INDUSTRY_COLORS[i % len(INDUSTRY_COLORS)],
        })

    js_map = json.dumps(map_data, ensure_ascii=False)
    js_bars = json.dumps(country_bars, ensure_ascii=False)
    js_donut = json.dumps(donut_data, ensure_ascii=False)
    js_trend = json.dumps(monthly_data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AI Job Displacement Tracker — AGI HUB</title>
<meta name="description" content="AIによる世界の雇用代替をリアルタイムで追跡するダッシュボード">

<link rel="stylesheet" href="design-system/palette.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: HelveticaNeue, "Helvetica Neue", Helvetica, Arial,
      "Hiragino Kaku Gothic ProN", sans-serif;
    font-feature-settings: "palt";
    background: #fff;
    color: #1a1a1a;
    -webkit-font-smoothing: antialiased;
  }}

  /* ── Dashboard wrapper ── */
  .dashboard {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 48px 48px 64px;
  }}

  /* ── Title block ── */
  .dash-title {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 42px;
    font-weight: 700;
    line-height: 1.1;
    color: #1a1a1a;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
  }}
  .dash-subtitle {{
    font-size: 16px;
    color: #757575;
    margin-bottom: 4px;
  }}
  .dash-date {{
    font-family: "SF Mono", "Fira Code", Menlo, Consolas, monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 40px;
  }}

  /* ── KPI cards ── */
  .kpi-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #e5e5e5;
    border: 1px solid #e5e5e5;
    margin-bottom: 40px;
  }}
  .kpi-card {{
    background: #fff;
    padding: 24px 28px;
  }}
  .kpi-value {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 40px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 6px;
    color: #1a1a1a;
  }}
  .kpi-value.accent {{ color: #b23a2f; }}
  .kpi-label {{
    font-family: "SF Mono", "Fira Code", Menlo, Consolas, monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #999;
  }}

  /* ── Section titles ── */
  .section-label {{
    font-family: "SF Mono", "Fira Code", Menlo, Consolas, monospace;
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #757575;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e5e5e5;
  }}

  /* ── Panel ── */
  .panel {{
    border: 1px solid #e5e5e5;
    padding: 24px;
    margin-bottom: 40px;
  }}

  /* ── Map ── */
  #map {{
    height: 420px;
    width: 100%;
    border: 1px solid #e5e5e5;
    margin-bottom: 40px;
  }}
  .leaflet-popup-content-wrapper {{
    border-radius: 0 !important;
    box-shadow: none !important;
    border: 1px solid #e5e5e5 !important;
  }}
  .leaflet-popup-tip {{ display: none !important; }}
  .popup-title {{
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 700;
    font-size: 15px;
    margin-bottom: 6px;
  }}
  .popup-stat {{
    font-size: 13px;
    color: #585858;
    line-height: 1.6;
  }}
  .popup-stat strong {{ color: #b23a2f; }}

  /* ── 2-col grid ── */
  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-bottom: 40px;
  }}

  /* ── Donut ── */
  .donut-wrap {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}
  #donutChart {{ max-width: 160px; max-height: 160px; flex-shrink: 0; }}
  .donut-legend {{ flex: 1; }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #585858;
  }}
  .legend-dot {{
    width: 8px; height: 8px;
    flex-shrink: 0;
  }}
  .legend-count {{
    margin-left: auto;
    font-family: "SF Mono", "Fira Code", Menlo, Consolas, monospace;
    font-size: 11px;
    color: #999;
  }}

  /* ── Trend chart ── */
  #trendChart {{ max-height: 260px; }}

  /* ── Footer ── */
  .dash-footer {{
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid #e5e5e5;
    font-size: 12px;
    color: #999;
    line-height: 1.6;
  }}

  /* ── Responsive ── */
  @media (max-width: 768px) {{
    .dashboard {{ padding: 24px 16px 48px; }}
    .dash-title {{ font-size: 28px; }}
    .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
    .two-col {{ grid-template-columns: 1fr; }}
    #map {{ height: 300px; }}
  }}
</style>
</head>
<body class="has-site-header">

<!-- ── Site header (AGI HUB shared) ── -->
<header class="site-header">
  <a href="index.html" class="site-logo">AGI HUB</a>
  <div class="site-nav-right">
    <div id="google_translate_element"></div>
    <a href="index.html" class="site-back">Archive</a>
  </div>
</header>

<div class="dashboard">

  <!-- ── Title ── -->
  <h1 class="dash-title">AI Job Displacement Tracker</h1>
  <p class="dash-subtitle">AIによる世界の雇用代替をリアルタイムで追跡する</p>
  <div class="dash-date">Latest data: {latest_date}</div>

  <!-- ── KPI ── -->
  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-value accent">{fmt_k(total_jobs)}</div>
      <div class="kpi-label">Jobs Affected</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">{n_articles}</div>
      <div class="kpi-label">News Stories</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">{n_countries}</div>
      <div class="kpi-label">Countries</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">{n_industries}</div>
      <div class="kpi-label">Industries</div>
    </div>
  </div>

  <!-- ── World Map ── -->
  <div class="section-label">Geographic Distribution</div>
  <div id="map"></div>

  <!-- ── 2-column: Country bars + Industry donut ── -->
  <div class="two-col">
    <div>
      <div class="section-label">Top Countries by Impact</div>
      <div class="panel">
        <canvas id="countryBarsChart"></canvas>
      </div>
    </div>
    <div>
      <div class="section-label">Industry Breakdown</div>
      <div class="panel">
        <div class="donut-wrap">
          <canvas id="donutChart"></canvas>
          <div class="donut-legend" id="donutLegend"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Monthly trend ── -->
  <div class="section-label">Monthly Trend</div>
  <div class="panel">
    <canvas id="trendChart"></canvas>
  </div>

  <!-- ── Footer ── -->
  <div class="dash-footer">
    Data collected from Google News, Bing News, Reddit, and direct RSS feeds. Classified by GPT-4o-mini.<br>
    Source: ai-job-displacement-map pipeline
  </div>

</div>

<!-- ── Google Translate ── -->
<script>
function googleTranslateElementInit() {{
  new google.translate.TranslateElement({{
    pageLanguage: 'ja',
    includedLanguages: 'en,ja,zh-CN,ko,es,fr,de',
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
    autoDisplay: false
  }}, 'google_translate_element');
}}
</script>
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>

<script>
// ── Data ────────────────────────────────────────────────────
const MAP_DATA      = {js_map};
const COUNTRY_BARS  = {js_bars};
const CATEGORIES    = {js_donut};
const TREND         = {js_trend};

// ── Colors ──────────────────────────────────────────────────
const C_BLACK   = "#1a1a1a";
const C_RED     = "#b23a2f";
const C_BORDER  = "#e5e5e5";
const C_META    = "#757575";
const C_GRAY    = "#999";

// ── Chart.js defaults ───────────────────────────────────────
Chart.defaults.color = C_META;
Chart.defaults.font.family = 'HelveticaNeue, "Helvetica Neue", Helvetica, Arial, sans-serif';
Chart.defaults.font.size = 11;

// ── 1. Leaflet Map ──────────────────────────────────────────
const map = L.map('map', {{
  scrollWheelZoom: false,
  zoomControl: true,
}}).setView([25, 10], 2);

L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}@2x.png', {{
  attribution: '&copy; OpenStreetMap &copy; CARTO',
  subdomains: 'abcd',
  maxZoom: 18,
}}).addTo(map);

const maxJobs = Math.max(...MAP_DATA.map(d => d.jobs || d.count * 500), 1);
MAP_DATA.forEach(d => {{
  const val = d.jobs || d.count * 500;
  const r = 6 + Math.sqrt(val / maxJobs) * 30;
  const circle = L.circleMarker([d.lat, d.lng], {{
    radius: r,
    fillColor: d.jobs > 0 ? C_RED : C_BLACK,
    color: '#fff',
    weight: 1,
    opacity: 0.9,
    fillOpacity: 0.65,
  }}).addTo(map);

  const jobsLabel = d.jobs > 0 ? fmtK(d.jobs) : `~${{fmtK(d.count * 500)}}`;
  circle.bindPopup(`
    <div class="popup-title">${{d.country}}</div>
    <div class="popup-stat">
      Jobs affected: <strong>${{jobsLabel}}</strong><br>
      News stories: ${{d.count}}<br>
      Top industry: ${{d.top_industry}}
    </div>
  `, {{ closeButton: false }});

  circle.on('mouseover', function() {{ this.openPopup(); }});
  circle.on('mouseout', function() {{ this.closePopup(); }});
}});

// ── 2. Country horizontal bar ───────────────────────────────
new Chart(document.getElementById('countryBarsChart'), {{
  type: 'bar',
  data: {{
    labels: COUNTRY_BARS.map(d => d.country),
    datasets: [{{
      label: 'Jobs affected',
      data: COUNTRY_BARS.map(d => d.jobs),
      backgroundColor: COUNTRY_BARS.map((d, i) => i === 0 ? C_RED : C_BLACK),
      borderWidth: 0,
      borderRadius: 0,
    }}],
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ' ' + fmtK(ctx.raw) + ' jobs',
        }},
      }},
    }},
    scales: {{
      x: {{
        grid: {{ color: C_BORDER }},
        ticks: {{ callback: v => fmtK(v) }},
        border: {{ display: false }},
      }},
      y: {{
        grid: {{ display: false }},
        border: {{ display: false }},
      }},
    }},
  }},
}});

// ── 3. Industry donut ───────────────────────────────────────
const donutCtx = document.getElementById('donutChart');
const total = CATEGORIES.reduce((s, d) => s + d.count, 0);

new Chart(donutCtx, {{
  type: 'doughnut',
  data: {{
    labels: CATEGORIES.map(d => d.label),
    datasets: [{{
      data: CATEGORIES.map(d => d.count),
      backgroundColor: CATEGORIES.map(d => d.color),
      borderColor: '#fff',
      borderWidth: 2,
      hoverOffset: 4,
    }}],
  }},
  options: {{
    cutout: '68%',
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.label}}: ${{ctx.raw}}`,
        }},
      }},
    }},
  }},
  plugins: [{{
    id: 'center-text',
    afterDraw(chart) {{
      const {{ ctx, chartArea: {{ left, right, top, bottom }} }} = chart;
      const cx = (left + right) / 2;
      const cy = (top + bottom) / 2;
      ctx.save();
      ctx.font = 'bold 22px Georgia, serif';
      ctx.fillStyle = C_BLACK;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(total, cx, cy - 6);
      ctx.font = '10px "SF Mono", monospace';
      ctx.fillStyle = C_GRAY;
      ctx.fillText('STORIES', cx, cy + 12);
      ctx.restore();
    }},
  }}],
}});

// Build legend
const legendEl = document.getElementById('donutLegend');
CATEGORIES.forEach(d => {{
  legendEl.innerHTML += `
    <div class="legend-item">
      <span class="legend-dot" style="background:${{d.color}}"></span>
      <span>${{d.label}}</span>
      <span class="legend-count">${{d.count}}</span>
    </div>`;
}});

// ── 4. Monthly trend (bar: count, line: jobs) ───────────────
if (TREND.length >= 2) {{
  new Chart(document.getElementById('trendChart'), {{
    data: {{
      labels: TREND.map(d => d.month),
      datasets: [
        {{
          type: 'bar',
          label: 'News count',
          data: TREND.map(d => d.count),
          backgroundColor: 'rgba(26,26,26,0.15)',
          borderColor: 'transparent',
          yAxisID: 'y2',
          borderRadius: 0,
          order: 2,
        }},
        {{
          type: 'line',
          label: 'Jobs affected',
          data: TREND.map(d => d.jobs),
          borderColor: C_RED,
          backgroundColor: 'rgba(178,58,47,0.06)',
          fill: true,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: C_RED,
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          borderWidth: 2,
          yAxisID: 'y',
          order: 1,
        }},
      ],
    }},
    options: {{
      responsive: true,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{
          position: 'top',
          labels: {{ boxWidth: 10, padding: 16, usePointStyle: false }},
        }},
        tooltip: {{
          callbacks: {{
            label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.datasetIndex === 0 ? ctx.raw : fmtK(ctx.raw)}}`,
          }},
        }},
      }},
      scales: {{
        x: {{
          grid: {{ color: C_BORDER }},
          border: {{ display: false }},
        }},
        y: {{
          position: 'left',
          grid: {{ color: C_BORDER }},
          border: {{ display: false }},
          ticks: {{ callback: v => fmtK(v), color: C_RED }},
          title: {{ display: true, text: 'Jobs', color: C_RED, font: {{ size: 10 }} }},
        }},
        y2: {{
          position: 'right',
          grid: {{ display: false }},
          border: {{ display: false }},
          ticks: {{ color: C_META }},
          title: {{ display: true, text: 'Count', color: C_META, font: {{ size: 10 }} }},
        }},
      }},
    }},
  }});
}} else {{
  document.getElementById('trendChart').parentElement.innerHTML +=
    '<p style="color:#999;font-size:13px;margin-top:12px">Accumulating data...</p>';
}}

// ── Utilities ───────────────────────────────────────────────
function fmtK(n) {{
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000)     return Math.round(n / 1_000) + 'K';
  return String(Math.round(n));
}}
</script>
</body>
</html>"""

    return html


def main():
    if not INPUT_PATH.exists():
        print(f"Input file not found: {INPUT_PATH}")
        raise SystemExit(1)

    articles = parse_data(INPUT_PATH)
    print(f"Loaded {len(articles)} articles from {INPUT_PATH.name}")

    html = generate_html(articles)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Dashboard saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
