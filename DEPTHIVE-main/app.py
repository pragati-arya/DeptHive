import streamlit as st
from datetime import datetime

import pandas as pd



from auth import init_db, create_user, verify_user

from data_processor import (

    load_dataset,

    generate_data_quality_report,

    clean_dataset

)

from intelligence_engine import analyze_department_performance



st.set_page_config(

    page_title="DEPTHIVE | Organizational Intelligence",

    page_icon="◈",

    layout="wide",

    initial_sidebar_state="collapsed",

)



init_db()



st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap');
:root{--bg:#f7f5f1;--ink:#17213d;--muted:#65718a;--blue:#2864df;--line:#e5e5ed}
.stApp{background:radial-gradient(ellipse at 85% 4%,#e3eaff 0%,transparent 30%),radial-gradient(ellipse at 8% 55%,#f2e9ff 0%,transparent 25%),linear-gradient(135deg,#f9f7f3,#f3f4fa 65%,#fbf1e9);color:var(--ink);font-family:'DM Sans',sans-serif}
.block-container{max-width:1450px;padding:2rem 2.4rem 3rem}
h1,h2,h3{color:var(--ink)!important;letter-spacing:-.035em}
h1,h2,h3,.hero-title,.card-value{font-family:'Playfair Display',serif!important}
h1{font-size:clamp(2.3rem,4vw,3.6rem)!important;line-height:1.1!important}
p,label,.stMarkdown,.stCaption{color:var(--ink)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#fffdf9,#f0f2fb);border-right:1px solid #e4e5ee}
[data-testid="stSidebar"]>div:first-child{padding-top:1.5rem}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border-radius:12px;padding:.35rem .55rem}
div[data-testid="stForm"],div[data-testid="stExpander"]{background:rgba(255,255,255,.82);border:1px solid var(--line);padding:1.4rem;border-radius:20px;box-shadow:0 10px 35px rgba(48,57,100,.05)}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:#fff!important;color:var(--ink)!important;border:1px solid #dfe2ee!important;border-radius:12px!important}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:var(--blue)!important;box-shadow:0 0 0 3px rgba(40,100,223,.12)!important}
.stButton>button,.stFormSubmitButton>button{background:linear-gradient(110deg,#2864df,#6758d9);color:white!important;border:1px solid transparent;border-radius:12px;min-height:2.8rem;font-weight:600;box-shadow:0 7px 18px rgba(53,91,204,.17);transition:transform .2s ease,box-shadow .2s ease}
.stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-2px);box-shadow:0 11px 25px rgba(53,91,204,.23);border-color:#aebfff}
.stSelectbox [data-baseweb="select"]>div{background:white;color:var(--ink);border-color:#dfe2ee;border-radius:12px}
[data-testid="stMetric"]{background:rgba(255,255,255,.88);border:1px solid rgba(219,222,237,.95);border-radius:20px;padding:1.2rem 1.3rem;box-shadow:0 10px 35px rgba(48,57,100,.055)}
[data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:.88rem}
[data-testid="stMetricValue"]{color:var(--ink)!important;font-weight:700}
[data-testid="stDataFrame"],[data-testid="stTable"]{border:1px solid var(--line);border-radius:14px;overflow:hidden}
[data-testid="stAlert"]{border-radius:14px}
a{color:#315dcc!important}
.brand{font-family:'DM Sans',sans-serif;font-size:1.12rem;font-weight:700;letter-spacing:.12em;color:var(--ink)}
.brand-mark{display:inline-flex;width:38px;height:38px;align-items:center;justify-content:center;margin-right:10px;border-radius:13px;color:white;background:linear-gradient(135deg,#2864df,#8c80ef);font-size:1.25rem;box-shadow:0 6px 16px #526ad52c}
.eyebrow{color:#4267ba;font-size:.72rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase}
.hero-title{font-size:clamp(3rem,5.5vw,5.2rem);line-height:1.04;font-weight:600;letter-spacing:-.055em;margin:.7rem 0 1.2rem;color:#17213d}
.gradient-text{background:linear-gradient(100deg,#2864df,#8574dd);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.subtle{color:#65718a;font-size:1rem;line-height:1.8;max-width:650px}
.glass-card{background:linear-gradient(145deg,rgba(255,255,255,.94),rgba(247,247,255,.82));border:1px solid rgba(218,221,239,.95);border-radius:22px;padding:24px;min-height:130px;box-shadow:0 14px 42px rgba(41,54,105,.065);backdrop-filter:blur(16px);transition:transform .2s ease,box-shadow .2s ease}
.glass-card:hover{transform:translateY(-3px);box-shadow:0 20px 45px rgba(41,54,105,.10)}
.card-label{color:var(--muted);font-size:.84rem}
.card-value{color:var(--ink);font-size:1.9rem;font-weight:600;margin-top:8px}
.pill{display:inline-block;border:1px solid #d8ddf4;background:linear-gradient(100deg,#edf2ff,#f1edff);color:#3859a7;border-radius:99px;padding:6px 11px;font-size:.76rem;font-weight:600}
hr{border-color:#e1e3ec!important}
#MainMenu,footer{visibility:hidden}
@media(max-width:768px){.block-container{padding:1.2rem 1rem 2rem}.hero-title{font-size:2.8rem}.glass-card{padding:18px}}

.page-hero{position:relative;overflow:hidden;margin:.4rem 0 2.2rem;padding:2.2rem 2.35rem 1.9rem;border:1px solid #dfe4f4;border-radius:28px;background:linear-gradient(112deg,rgba(255,255,255,.96) 0%,rgba(242,245,255,.93) 57%,rgba(237,231,255,.9) 100%);box-shadow:0 18px 50px rgba(38,56,112,.075)}
.page-hero:after{content:"◈";position:absolute;right:3.2rem;top:-2.4rem;font-size:12rem;line-height:1;color:rgba(68,99,202,.065);transform:rotate(-12deg);pointer-events:none}
.page-hero h1{font-size:clamp(2.1rem,3.8vw,3.25rem)!important;margin:.55rem 0 .65rem!important;max-width:850px}
.hero-description{font-size:1.03rem;line-height:1.75;color:#68738d;max-width:760px;margin:0}
.hero-meta{display:flex;align-items:center;gap:9px;margin-top:1.25rem;font-size:.68rem;font-weight:700;letter-spacing:.12em;color:#697592}
.status-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#3dbb91;box-shadow:0 0 0 4px #dff7ee}
.meta-divider{color:#c2c7d8;margin:0 3px}
.section-kicker{font-size:.7rem;font-weight:800;letter-spacing:.16em;color:#68779e;margin:1.5rem 0 .9rem}
.metric-tile{min-height:174px;padding:1.2rem 1.25rem;border:1px solid #e0e4f1;border-radius:20px;background:linear-gradient(145deg,#fff 0%,#f8f9ff 100%);box-shadow:0 12px 32px rgba(45,58,111,.055);transition:transform .18s ease,box-shadow .18s ease}
.metric-tile:hover,.module-card:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(45,58,111,.10)}
.tile-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem}
.tile-index{font-size:.68rem;letter-spacing:.1em;font-weight:800;color:#8190b3}
.tile-orb{width:30px;height:30px;border-radius:10px;background:linear-gradient(135deg,#e5edff,#eee8ff);border:1px solid #dce3fa}
.tile-label{font-size:.85rem;font-weight:600;color:#66718b}
.tile-value{font-family:'DM Sans',sans-serif!important;font-size:1.65rem;font-weight:750;letter-spacing:-.04em;color:#17213d;margin:.38rem 0}
.tile-note{font-size:.73rem;color:#8b94aa;line-height:1.45}
.setup-banner{display:flex;align-items:center;gap:1.1rem;padding:1.35rem 1.5rem;border-radius:22px;background:linear-gradient(105deg,#243c81,#4268c9 62%,#7c75d8);box-shadow:0 16px 36px rgba(53,77,164,.19);color:white;margin-bottom:1.8rem}
.setup-number{flex:0 0 48px;height:48px;display:flex;align-items:center;justify-content:center;border-radius:15px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.23);font-size:1.1rem;font-weight:800}
.setup-copy{flex:1}
.setup-title{font-size:1.1rem;font-weight:750;color:#fff;margin-bottom:.28rem}
.setup-text{font-size:.84rem;line-height:1.65;color:#e2e8ff;max-width:700px}
.setup-tag{font-size:.63rem;font-weight:800;letter-spacing:.1em;padding:.55rem .7rem;border:1px solid #a7b7f1;border-radius:9px;color:#f3f5ff;white-space:nowrap}
.module-card{padding:1.35rem 1.45rem;margin-bottom:1rem;border:1px solid #e1e5f2;border-radius:21px;background:rgba(255,255,255,.88);box-shadow:0 12px 30px rgba(45,58,111,.05);min-height:174px;transition:transform .18s ease,box-shadow .18s ease}
.module-heading{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem}
.module-letter{display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:12px;background:#edf1ff;color:#3659bb;font-weight:800}
.module-tag{font-size:.62rem;font-weight:800;letter-spacing:.1em;color:#8b91aa}
.module-title{font-size:1.08rem;font-weight:750;color:#202b4a;margin-bottom:.45rem}
.module-body{font-size:.84rem;color:#717b94;line-height:1.65}
[data-testid="stSidebar"] [data-testid="stRadio"] label{font-weight:600;color:#44516f}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#e9edfb}
div[data-testid="stFileUploader"]{border:1.5px dashed #b9c5eb;border-radius:18px;background:#f8f9ff;padding:.7rem}
div[data-testid="stFileUploader"] section{background:transparent}
div[data-testid="stSubheader"]{margin-top:1.5rem}
@media(max-width:800px){.page-hero{padding:1.5rem;border-radius:22px}.page-hero:after{right:-1rem;font-size:8rem}.setup-banner{align-items:flex-start;flex-wrap:wrap}.setup-tag{margin-left:59px}.metric-tile{min-height:150px}}


/* Refined dashboard presentation */
.page-hero{position:relative;overflow:hidden;margin:.2rem 0 1.35rem;padding:1.65rem 1.8rem 1.45rem;border:1px solid rgba(213,222,245,.9);border-radius:24px;background:linear-gradient(105deg,rgba(255,255,255,.97) 0%,rgba(246,247,255,.94) 55%,rgba(234,237,255,.91) 100%);box-shadow:0 12px 38px rgba(37,55,111,.07)}
.page-hero:after{content:"◈";position:absolute;right:2.8rem;top:-2.6rem;font-size:10rem;color:rgba(60,99,209,.055);transform:rotate(-12deg);pointer-events:none}
.page-hero h1{font-size:clamp(2.05rem,3.2vw,3.15rem)!important;line-height:1.05!important;margin:.45rem 0 .55rem!important;color:#111d3c!important}
.hero-description{font-size:.98rem;line-height:1.65;color:#586783;max-width:760px;margin:0}
.hero-meta{display:flex;align-items:center;gap:9px;margin-top:1rem;font-size:.64rem;font-weight:800;letter-spacing:.12em;color:#647392}
.status-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#37b991;box-shadow:0 0 0 4px #e1f7ef}
.meta-divider{color:#b9c3da;margin:0 3px}
.section-kicker{font-size:.66rem;font-weight:850;letter-spacing:.16em;color:#7180a4;margin:1.15rem 0 .72rem}
.metric-tile{min-height:158px;padding:1.05rem 1.05rem;border:1px solid #e1e5f2;border-radius:18px;background:linear-gradient(145deg,#fff 0%,#f8f9ff 100%);box-shadow:0 9px 24px rgba(45,58,111,.045)}
.tile-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:.65rem}
.tile-symbol{display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:12px;background:#eaf0ff;color:#345dc0;font-size:1.35rem;font-weight:700}
.tile-orb{width:25px;height:25px;border-radius:9px;background:linear-gradient(135deg,#e6edff,#f0e9ff);border:1px solid #dce3fa}
.tile-label{font-size:.78rem;font-weight:650;color:#687590}
.tile-value{font-family:'DM Sans',sans-serif!important;font-size:1.35rem;font-weight:800;letter-spacing:-.035em;color:#192543;margin:.34rem 0}
.tile-note{font-size:.67rem;color:#8a94aa;line-height:1.4}
.setup-banner{display:flex;align-items:center;gap:1rem;padding:1.15rem 1.3rem;border-radius:19px;background:linear-gradient(105deg,#243d82,#4569c6 63%,#8078d7);box-shadow:0 12px 28px rgba(53,77,164,.16);color:white;margin:.4rem 0 1.2rem}
.setup-number{flex:0 0 42px;height:42px;display:flex;align-items:center;justify-content:center;border-radius:13px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.23);font-weight:800}
.setup-copy{flex:1}.setup-title{font-size:1rem;font-weight:800;color:#fff;margin-bottom:.2rem}
.setup-text{font-size:.78rem;line-height:1.55;color:#e2e8ff;max-width:720px}
.setup-tag{font-size:.58rem;font-weight:850;letter-spacing:.08em;padding:.5rem .6rem;border:1px solid #a7b7f1;border-radius:9px;color:#f3f5ff;white-space:nowrap}
.chart-placeholder{min-height:280px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:2rem;border:1px dashed #cbd5ee;border-radius:20px;background:linear-gradient(145deg,#fff,#f8f9ff)}
.placeholder-mark{font-size:2rem;color:#7991dc;margin-bottom:.5rem}.placeholder-title{font-weight:800;color:#263454;margin-bottom:.4rem}.placeholder-copy{font-size:.82rem;line-height:1.6;color:#78839c;max-width:340px}
.insight-card{display:flex;align-items:flex-start;gap:.75rem;padding:.9rem .85rem;margin-bottom:.65rem;border:1px solid #e5e8f3;border-radius:16px;background:rgba(255,255,255,.88);box-shadow:0 5px 15px rgba(45,58,111,.035)}
.insight-icon{flex:0 0 35px;height:35px;display:flex;align-items:center;justify-content:center;border-radius:11px;background:#e7f7f0;color:#188d69;font-size:1.1rem;font-weight:800}
.insight-icon.amber{background:#fff2df;color:#c47b1b}.insight-icon.violet{background:#f0eaff;color:#7954cb}
.insight-title{font-size:.8rem;font-weight:800;color:#202c4b;margin:.08rem 0 .25rem}.insight-copy{font-size:.72rem;line-height:1.5;color:#74809a}
.feature-tile{min-height:180px;padding:1rem;border:1px solid #e4e7f2;border-radius:18px;background:linear-gradient(145deg,#fff,#f4f6ff);box-shadow:0 9px 23px rgba(45,58,111,.045)}
.feature-tile.lavender{background:linear-gradient(145deg,#fff,#f3edff)}.feature-tile.peach{background:linear-gradient(145deg,#fff,#fff0e7)}.feature-tile.gold{background:linear-gradient(145deg,#fff,#fff6e5)}
.feature-icon{display:flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:12px;background:#e4edff;color:#3267cb;font-size:1.25rem;font-weight:800;margin-bottom:.75rem}
.lavender .feature-icon{background:#e8dcff;color:#8156d8}.peach .feature-icon{background:#ffe0cf;color:#b76c38}.gold .feature-icon{background:#ffebc1;color:#a97817}
.feature-tag{font-size:.55rem;letter-spacing:.12em;font-weight:850;color:#8a94ad;margin-bottom:.35rem}.feature-title{font-size:.88rem;font-weight:800;color:#202b49;margin-bottom:.35rem}.feature-copy{font-size:.72rem;line-height:1.5;color:#75809a}
div[data-testid="stFileUploader"]{border:1.5px dashed #b9c5eb;border-radius:18px;background:#f8f9ff;padding:.7rem}
div[data-testid="stMetric"]{background:#fff;padding:16px;border:1px solid #e1e5f2;border-radius:14px}
div[data-testid="stMetricLabel"]{color:#73809b}div[data-testid="stMetricValue"]{color:#192543}
@media(max-width:900px){.page-hero{padding:1.3rem}.page-hero:after{right:-1rem;font-size:7rem}.setup-banner{align-items:flex-start;flex-wrap:wrap}.setup-tag{margin-left:55px}.metric-tile{min-height:145px}}


/* Dashboard styling aligned to the supplied visual reference */
.block-container{max-width:1560px!important;padding-top:.55rem!important;padding-bottom:1.2rem!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#fffdf9 0%,#f1f4ff 100%)!important;border-right:1px solid #e3e8f4}
.stApp{background:radial-gradient(ellipse at 76% 0%,#e5edff 0%,#f8f7f5 42%,#fff8f0 100%)!important;color:#152343!important}
h1,h2,h3{color:#111c3b!important}
.reference-hero{position:relative;overflow:hidden;margin:.2rem 0 1.15rem;padding:1.35rem 1.2rem 1.2rem;border-radius:20px;border:1px solid rgba(255,255,255,.8);background:linear-gradient(95deg,rgba(255,255,255,.92),rgba(247,249,255,.79) 60%,rgba(236,240,255,.67));box-shadow:0 8px 28px rgba(40,61,125,.035);min-height:205px}
.reference-hero:after{content:"◈";position:absolute;right:8%;top:-3.4rem;font-size:13rem;color:rgba(62,103,198,.045);pointer-events:none}
.reference-eyebrow{font-size:.62rem;font-weight:800;letter-spacing:.22em;color:#3261b5;margin-bottom:.85rem}
.reference-headline{font-family:'Playfair Display',Georgia,serif;font-size:clamp(2.15rem,4vw,3.55rem);line-height:.99;letter-spacing:-.045em;color:#101a37;max-width:980px}
.reference-headline span{font-style:italic;color:#2377df}
.reference-description{font-size:.91rem;line-height:1.65;color:#34486e;margin-top:.7rem;max-width:760px}
.hero-note{position:absolute;right:2.4rem;bottom:1.4rem;display:flex;flex-direction:column;gap:.25rem;font-size:.56rem;font-weight:800;letter-spacing:.12em;color:#6c7ca0;opacity:.8}
.utility-pill{margin-top:.05rem;padding:.6rem .8rem;text-align:center;border:1px solid #dfe5f2;border-radius:13px;background:rgba(255,255,255,.8);color:#445678;font-size:.75rem}
.section-kicker{font-size:.62rem;font-weight:850;letter-spacing:.16em;color:#7785a5;margin:.95rem 0 .65rem}
.reference-metric{position:relative;display:flex;align-items:flex-start;gap:.65rem;min-height:118px;padding:.95rem .8rem;border:1px solid #e5e7f0;border-radius:17px;background:rgba(255,255,255,.86);box-shadow:0 8px 22px rgba(34,53,108,.045);overflow:hidden}
.metric-icon{flex:0 0 40px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:13px;font-size:1.4rem;font-weight:800}
.metric-icon.green{background:#e2f6ec;color:#16845d}.green .metric-icon{background:#e2f6ec;color:#16845d}
.metric-icon.blue{background:#e1ecff;color:#2866c9}.blue .metric-icon{background:#e1ecff;color:#2866c9}
.metric-icon.coral{background:#ffe5e1;color:#e84b4b}.coral .metric-icon{background:#ffe5e1;color:#e84b4b}
.metric-icon.purple{background:#efe5ff;color:#7650d8}.purple .metric-icon{background:#efe5ff;color:#7650d8}
.metric-content{min-width:0;flex:1}.metric-label{font-size:.7rem;font-weight:650;color:#586785;line-height:1.35}.metric-value{font-family:'Playfair Display',Georgia,serif;font-size:1.25rem;font-weight:700;color:#101a37;margin:.35rem 0 .25rem;line-height:1.2}.metric-note{font-size:.61rem;line-height:1.35;color:#8490a8}.metric-spark{position:absolute;right:.6rem;bottom:.4rem;color:#8b9fd1;font-size:1.1rem;opacity:.6}
.panel-heading{display:flex;align-items:center;gap:.7rem;padding:.8rem .85rem .65rem;border:1px solid #e5e8f2;border-bottom:0;border-radius:17px 17px 0 0;background:rgba(255,255,255,.86)}
.panel-icon{display:flex;align-items:center;justify-content:center;width:35px;height:35px;border-radius:11px;font-size:1.1rem;font-weight:800}.panel-icon.blue{background:#e1ecff;color:#2866c9}.panel-icon.amber{background:#fff0d9;color:#c78122}
.panel-title{font-family:'Playfair Display',Georgia,serif;font-size:1.08rem;font-weight:700;color:#17213d}
.chart-empty{min-height:260px;padding:2rem 1.2rem;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:rgba(255,255,255,.85);border:1px solid #e5e8f2;border-top:0;border-radius:0 0 17px 17px}
.empty-chart-symbol{font-size:2.1rem;color:#7c9be1;margin-bottom:.5rem}.empty-chart-title{font-size:.9rem;font-weight:800;color:#273655;margin-bottom:.35rem}.empty-chart-copy{font-size:.75rem;line-height:1.55;color:#7886a2;max-width:320px}
.reference-insight{display:flex;align-items:center;gap:.6rem;padding:.62rem .65rem;margin-bottom:.45rem;border:1px solid #e6e8f1;border-radius:14px;background:rgba(255,255,255,.86)}
.insight-icon{flex:0 0 33px;height:33px;display:flex;align-items:center;justify-content:center;border-radius:10px;font-size:1rem;font-weight:800}
.insight-icon.green{background:#e2f6ed;color:#16845d}.insight-icon.coral{background:#ffe5e1;color:#e84b4b}.insight-icon.blue{background:#e1ecff;color:#2866c9}.insight-icon.purple{background:#efe5ff;color:#7650d8}
.insight-text{min-width:0;flex:1}.insight-title{font-size:.72rem;font-weight:800;color:#1b2745;margin-bottom:.2rem}.insight-desc{font-size:.63rem;line-height:1.4;color:#75819a}.insight-arrow{color:#3e83df;font-size:.95rem}
.reference-feature{position:relative;overflow:hidden;min-height:145px;padding:1rem;border:1px solid #e3e6f0;border-radius:17px;background:linear-gradient(140deg,rgba(255,255,255,.96),rgba(228,237,255,.88));box-shadow:0 8px 20px rgba(34,53,108,.04)}
.reference-feature.lavender{background:linear-gradient(140deg,#fff,#f0e8ff)}.reference-feature.sky{background:linear-gradient(140deg,#fff,#e4f4ff)}.reference-feature.peach{background:linear-gradient(140deg,#fff,#fff0e2)}
.feature-art{font-size:1.55rem;color:#4b85d8;margin-bottom:.65rem}.lavender .feature-art{color:#9062dc}.peach .feature-art{color:#ba773a}
.feature-title{font-family:'Playfair Display',Georgia,serif;font-size:.95rem;font-weight:700;color:#17213d;margin-bottom:.35rem}.feature-desc{font-size:.68rem;line-height:1.45;color:#687794;max-width:190px}.feature-arrow{position:absolute;right:.8rem;bottom:.7rem;width:27px;height:27px;display:flex;align-items:center;justify-content:center;border-radius:50%;border:1px solid #dce3f5;background:#fff;color:#2b67ca}
div[data-testid="stFileUploader"]{border:1.5px dashed #b9c5eb;border-radius:18px;background:#f8f9ff;padding:.7rem}
div[data-testid="stMetric"]{background:#fff;padding:15px;border:1px solid #e1e5f2;border-radius:14px}
@media(max-width:1000px){.reference-hero{padding:1.1rem}.hero-note{display:none}.reference-metric{min-height:125px;padding:.75rem .6rem;gap:.45rem}.metric-icon{flex-basis:32px;height:32px;font-size:1.1rem}.metric-value{font-size:1.05rem}.panel-title{font-size:.95rem}.reference-feature{min-height:155px}}


/* Shared visual system for all DEPTHIVE workspace pages */
.workspace-section{padding:1.05rem 1.15rem;border:1px solid #e3e7f2;border-radius:17px;background:rgba(255,255,255,.84);box-shadow:0 8px 20px rgba(34,53,108,.035);margin:.55rem 0 1rem}
.workspace-section-title{font-family:'Playfair Display',Georgia,serif;font-size:1.08rem;font-weight:700;color:#17213d;margin-bottom:.35rem}
.workspace-section-copy{font-size:.78rem;line-height:1.6;color:#71809c}
.workspace-step{display:flex;align-items:flex-start;gap:.7rem;padding:.8rem .85rem;border:1px solid #e4e8f2;border-radius:14px;background:rgba(255,255,255,.82);margin:.45rem 0}
.workspace-step-number{display:flex;align-items:center;justify-content:center;flex:0 0 30px;height:30px;border-radius:10px;background:#e6edff;color:#2f60bd;font-weight:800}
.workspace-step-title{font-size:.8rem;font-weight:800;color:#1c2949;margin-bottom:.2rem}
.workspace-step-copy{font-size:.72rem;line-height:1.5;color:#74809a}
div[data-testid="stDataFrame"]{border:1px solid #e2e7f2;border-radius:14px;overflow:hidden}
div[data-testid="stPlotlyChart"],div[data-testid="stVegaLiteChart"]{border:1px solid #e2e7f2;border-radius:16px;background:rgba(255,255,255,.75);padding:.45rem}
div[data-testid="stAlert"]{border-radius:13px}
div[data-testid="stForm"]{background:rgba(255,255,255,.88)!important;border:1px solid #e2e7f2!important;border-radius:17px!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:#fff!important;color:#17213d!important;border:1px solid #dbe2f0!important;border-radius:10px!important}
.stSelectbox div[data-baseweb="select"],.stMultiSelect div[data-baseweb="select"]{background:#fff!important;border-radius:10px!important}
.stButton>button,.stFormSubmitButton>button{border-radius:11px!important;min-height:2.55rem!important;box-shadow:0 4px 12px rgba(55,89,181,.09)}


/* Attractive, consistent layouts for every secondary module */
.module-banner{display:flex;align-items:center;gap:1rem;padding:1.05rem 1.2rem;margin:.6rem 0 1.15rem;border:1px solid #e2e7f4;border-radius:18px;background:linear-gradient(110deg,rgba(255,255,255,.96),rgba(240,244,255,.9));box-shadow:0 8px 24px rgba(43,61,120,.04)}
.module-banner-icon{flex:0 0 44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:14px;background:linear-gradient(135deg,#e3edff,#eee6ff);color:#3869c8;font-size:1.35rem;font-weight:800}
.module-banner-title{font-family:'Playfair Display',Georgia,serif;font-size:1.12rem;font-weight:700;color:#17213d;margin-bottom:.2rem}
.module-banner-copy{font-size:.76rem;line-height:1.55;color:#71809b}
.module-chip{display:inline-block;margin:.1rem .25rem .2rem 0;padding:.34rem .58rem;border-radius:99px;background:#edf2ff;color:#4664a5;font-size:.62rem;font-weight:800;letter-spacing:.04em;border:1px solid #dce5fb}
.module-card-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin:.7rem 0 1rem}
.module-mini-card{padding:1rem 1.05rem;border:1px solid #e2e7f2;border-radius:16px;background:rgba(255,255,255,.88);box-shadow:0 7px 20px rgba(43,61,120,.035)}
.module-mini-title{font-size:.8rem;font-weight:800;color:#1c2948;margin-bottom:.35rem}
.module-mini-copy{font-size:.72rem;line-height:1.55;color:#75819a}
.module-section-heading{display:flex;align-items:center;gap:.6rem;font-family:'Playfair Display',Georgia,serif;font-size:1.18rem;font-weight:700;color:#17213d;margin:1rem 0 .55rem}
.module-section-heading:before{content:"";display:inline-block;width:5px;height:22px;border-radius:8px;background:linear-gradient(180deg,#377be1,#9b7be9)}
.module-note{padding:.8rem 1rem;border-radius:13px;background:#f0f4ff;border:1px solid #e0e8fb;color:#5d6e92;font-size:.75rem;line-height:1.6;margin:.5rem 0 .9rem}
div[data-testid="stTabs"] button{border-radius:10px 10px 0 0!important;font-weight:700!important}
div[data-testid="stDataFrame"]{box-shadow:0 6px 18px rgba(43,61,120,.04)}
div[data-testid="stFileUploader"] section{border-radius:13px}
@media(max-width:760px){.module-banner{align-items:flex-start}.module-card-grid{grid-template-columns:1fr}}


/* Light chrome and accessible controls */
header[data-testid="stHeader"]{background:rgba(248,249,253,.88)!important;border-bottom:1px solid #e5e9f4!important}
header[data-testid="stHeader"] [data-testid="stToolbar"]{background:transparent!important}
[data-testid="stAppViewContainer"]{background:transparent!important}
[data-testid="stMain"]{background:transparent!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#fffdf9 0%,#f1f4ff 100%)!important}
[data-testid="stSidebar"] button{color:#17213d!important}
.stDownloadButton>button{background:linear-gradient(110deg,#2864df,#6758d9)!important;color:#fff!important;border:0!important}
div[data-testid="stTable"]{border:1px solid #e1e6f2!important;border-radius:14px!important;overflow:hidden!important;background:#fff!important}
div[data-testid="stTable"] table{background:#fff!important;border-collapse:collapse!important}
div[data-testid="stTable"] thead tr th{background:#edf2ff!important;color:#25365e!important;border-bottom:1px solid #dce4f5!important}
div[data-testid="stTable"] tbody tr td{background:#fff!important;color:#24314f!important;border-bottom:1px solid #edf0f7!important}
div[data-testid="stTable"] tbody tr:nth-child(even) td{background:#f8f9fe!important}


/* Soft cloud-watermark atmosphere across every DEPTHIVE page */
.stApp{
  background:
    radial-gradient(ellipse at 8% 8%, rgba(184,211,255,.30) 0, rgba(184,211,255,0) 28%),
    radial-gradient(ellipse at 92% 15%, rgba(207,192,255,.26) 0, rgba(207,192,255,0) 25%),
    radial-gradient(ellipse at 78% 76%, rgba(255,220,205,.23) 0, rgba(255,220,205,0) 28%),
    radial-gradient(ellipse at 12% 90%, rgba(187,224,255,.24) 0, rgba(187,224,255,0) 25%),
    linear-gradient(135deg,#fbfcff 0%,#f5f7ff 47%,#fff9f3 100%) !important;
  background-attachment:fixed!important;
}
[data-testid="stAppViewContainer"]{position:relative;isolation:isolate}
[data-testid="stMain"]{position:relative;z-index:1}
[data-testid="stAppViewContainer"]::before{
  content:"";position:fixed;inset:72px 0 0 250px;z-index:-1;pointer-events:none;opacity:.58;
  background:
    radial-gradient(ellipse 115px 45px at 8% 16%,rgba(177,207,255,.23) 0 60%,transparent 72%),
    radial-gradient(ellipse 155px 58px at 12% 14%,rgba(177,207,255,.18) 0 58%,transparent 72%),
    radial-gradient(ellipse 110px 40px at 90% 20%,rgba(195,183,255,.22) 0 58%,transparent 74%),
    radial-gradient(ellipse 170px 58px at 94% 18%,rgba(195,183,255,.17) 0 60%,transparent 74%),
    radial-gradient(ellipse 150px 50px at 83% 83%,rgba(255,213,196,.20) 0 58%,transparent 74%),
    radial-gradient(ellipse 100px 36px at 78% 86%,rgba(255,213,196,.16) 0 58%,transparent 74%),
    radial-gradient(ellipse 145px 48px at 5% 77%,rgba(170,215,255,.19) 0 58%,transparent 74%);
}
[data-testid="stSidebar"]{
  background:
    radial-gradient(ellipse at 8% 8%,rgba(184,211,255,.24),transparent 38%),
    radial-gradient(ellipse at 90% 84%,rgba(207,192,255,.20),transparent 35%),
    linear-gradient(180deg,#fffefa 0%,#f4f6ff 100%) !important;
  position:relative;overflow:hidden;
}
[data-testid="stSidebar"]::after{
  content:"";position:absolute;left:-48px;bottom:-28px;width:280px;height:180px;pointer-events:none;opacity:.6;
  background:
    radial-gradient(ellipse 100px 40px at 24% 55%,rgba(164,207,255,.28) 0 58%,transparent 73%),
    radial-gradient(ellipse 130px 48px at 52% 72%,rgba(164,207,255,.22) 0 58%,transparent 73%),
    radial-gradient(ellipse 105px 38px at 76% 48%,rgba(199,185,255,.22) 0 58%,transparent 73%);
}
.reference-hero,.page-hero{
  background:
    radial-gradient(ellipse at 92% 22%,rgba(188,208,255,.40),transparent 32%),
    radial-gradient(ellipse at 78% 100%,rgba(222,207,255,.30),transparent 30%),
    linear-gradient(105deg,rgba(255,255,255,.92),rgba(246,248,255,.82) 55%,rgba(239,242,255,.79)) !important;
}
.workspace-section,.module-banner,.module-mini-card,.reference-metric,.reference-insight,.reference-feature,.metric-tile,.module-card{
  backdrop-filter:blur(8px);
}
.reference-hero::before,.page-hero::before{
  content:"✦  ･  ✧";position:absolute;right:24%;top:18%;font-size:1.25rem;letter-spacing:1.2rem;color:rgba(100,139,235,.28);pointer-events:none;
}
@media(max-width:700px){
  [data-testid="stAppViewContainer"]::before{inset:60px 0 0 0}
}


/* Illustrated pastel cloud watermark system */
.stApp{
 background:
  radial-gradient(ellipse 220px 95px at 5% 12%,rgba(174,211,255,.48) 0 55%,transparent 72%),
  radial-gradient(ellipse 180px 80px at 13% 9%,rgba(194,219,255,.42) 0 54%,transparent 72%),
  radial-gradient(ellipse 260px 110px at 96% 18%,rgba(183,207,255,.45) 0 52%,transparent 72%),
  radial-gradient(ellipse 180px 75px at 88% 13%,rgba(210,198,255,.38) 0 55%,transparent 73%),
  radial-gradient(ellipse 230px 90px at 3% 88%,rgba(172,213,255,.42) 0 53%,transparent 73%),
  radial-gradient(ellipse 250px 100px at 96% 93%,rgba(255,217,198,.34) 0 52%,transparent 72%),
  radial-gradient(ellipse 300px 120px at 68% 54%,rgba(221,215,255,.25) 0 48%,transparent 72%),
  linear-gradient(135deg,#fbfcff 0%,#f1f5ff 45%,#fff8f2 100%) !important;
 background-attachment:fixed!important;
}
[data-testid="stAppViewContainer"]{position:relative;isolation:isolate}
[data-testid="stAppViewContainer"]::before{
 content:"";position:fixed;inset:76px 0 0 250px;z-index:0;pointer-events:none;opacity:.72;
 background:
  radial-gradient(ellipse 95px 55px at 10% 12%,rgba(255,255,255,.92) 0 50%,transparent 72%),
  radial-gradient(ellipse 130px 65px at 15% 12%,rgba(255,255,255,.76) 0 48%,transparent 72%),
  radial-gradient(ellipse 100px 52px at 88% 25%,rgba(255,255,255,.84) 0 50%,transparent 72%),
  radial-gradient(ellipse 150px 72px at 93% 24%,rgba(255,255,255,.7) 0 48%,transparent 72%),
  radial-gradient(ellipse 115px 55px at 6% 76%,rgba(255,255,255,.78) 0 50%,transparent 72%),
  radial-gradient(ellipse 160px 72px at 10% 78%,rgba(255,255,255,.62) 0 48%,transparent 72%),
  radial-gradient(ellipse 125px 62px at 96% 86%,rgba(255,255,255,.76) 0 48%,transparent 72%);
}
[data-testid="stAppViewContainer"]::after{
 content:"✦        ✧                       ✦";white-space:pre;position:fixed;top:112px;right:5%;z-index:-1;pointer-events:none;
 color:rgba(106,145,235,.32);font-size:30px;letter-spacing:22px;line-height:2.2;
}
[data-testid="stSidebar"]{
 background:
  radial-gradient(ellipse 180px 75px at 10% 8%,rgba(180,213,255,.44),transparent 75%),
  radial-gradient(ellipse 190px 85px at 85% 88%,rgba(201,190,255,.32),transparent 75%),
  linear-gradient(180deg,#fffefa 0%,#f2f5ff 100%) !important;
 position:relative;overflow:hidden;
}
[data-testid="stSidebar"]::after{
 content:"";position:absolute;left:-55px;bottom:-24px;width:330px;height:220px;pointer-events:none;opacity:.95;
 background:
  radial-gradient(ellipse 100px 65px at 22% 56%,rgba(151,202,255,.48) 0 52%,transparent 72%),
  radial-gradient(ellipse 130px 75px at 48% 66%,rgba(171,210,255,.42) 0 52%,transparent 72%),
  radial-gradient(ellipse 115px 68px at 76% 53%,rgba(200,190,255,.32) 0 52%,transparent 72%);
}
.reference-hero,.page-hero{
 background:
  radial-gradient(ellipse 240px 110px at 95% 12%,rgba(176,207,255,.48),transparent 72%),
  radial-gradient(ellipse 210px 95px at 83% 100%,rgba(211,197,255,.40),transparent 72%),
  linear-gradient(105deg,rgba(255,255,255,.95),rgba(246,248,255,.88) 55%,rgba(235,241,255,.84)) !important;
}
.reference-hero::before,.page-hero::before{
 content:"✦      〰      ✧";position:absolute;right:8%;top:18%;white-space:pre;
 font-size:1.4rem;letter-spacing:.65rem;color:rgba(89,135,231,.43);pointer-events:none;
}
.workspace-section,.module-banner,.module-mini-card,.reference-metric,.reference-insight,.reference-feature,.metric-tile,.module-card{
 backdrop-filter:blur(10px);background-color:rgba(255,255,255,.80);
}
@media(max-width:700px){[data-testid="stAppViewContainer"]::before{inset:60px 0 0 0}}


div[data-testid="stVerticalBlockBorderWrapper"]{border-color:rgba(220,228,247,.9)!important}
div[data-testid="stExpander"]{border:1px solid #e1e8f8!important;border-radius:16px!important;background:rgba(255,255,255,.74)!important}
.stButton>button{transition:all .18s ease!important}
.stButton>button:hover{transform:translateY(-1px);box-shadow:0 8px 20px rgba(75,112,210,.17)!important}

</style>

""", unsafe_allow_html=True)



def brand():

    st.markdown('<div class="brand"><span class="brand-mark">◈</span>DEPTHIVE</div>', unsafe_allow_html=True)



def set_page(page):
    st.session_state.page = page


def infer_kpi_direction(column_name):
    """Heuristic only; confirm KPI direction with the data owner."""
    name = str(column_name).strip().lower().replace("_", " ").replace("-", " ")
    lower_is_better = (
        "fail", "failure", "absence", "absent", "dropout", "drop out",
        "error", "incident", "complaint", "risk", "cost", "delay",
        "debt", "defect", "missing", "late", "attrition", "turnover",
        "unresolved", "penalty", "loss", "shortage"
    )
    return "Lower is better" if any(term in name for term in lower_is_better) else "Higher is better"


def department_scorecard(data, directions):
    """Rank departments using per-KPI percentile scores (0-100).

    Department means are compared across departments. Direction is explicit per KPI;
    missing KPI values are excluded from that department's score and coverage is shown.
    This is a transparent relative ranking, not a validated predictive model.
    """
    if data is None or data.empty or "Department" not in data.columns:
        return pd.DataFrame(), []
    numeric_cols = data.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if data[c].notna().any()]
    if not numeric_cols:
        return pd.DataFrame(), []

    working = data.copy()
    working["Department"] = working["Department"].astype("string").str.strip()
    working = working[working["Department"].notna() & (working["Department"] != "")]
    if working.empty:
        return pd.DataFrame(), numeric_cols

    means = working.groupby("Department", dropna=True)[numeric_cols].mean(numeric_only=True)
    score_parts = {}
    for col in numeric_cols:
        vals = means[col]
        valid = vals.dropna()
        if valid.empty:
            continue
        # Percentile rank is robust to units and outliers; ties receive average rank.
        percentile = valid.rank(method="average", pct=True) * 100
        if directions.get(col, infer_kpi_direction(col)) == "Lower is better":
            percentile = 100 - percentile
        score_parts[col] = percentile.reindex(means.index)

    if not score_parts:
        return pd.DataFrame(), numeric_cols

    component_scores = pd.DataFrame(score_parts, index=means.index)
    result = pd.DataFrame(index=means.index)
    result["Performance Score"] = component_scores.mean(axis=1, skipna=True).round(1)
    result["Risk Score"] = (100 - result["Performance Score"]).round(1)
    result["KPIs Available"] = component_scores.notna().sum(axis=1)
    result["KPI Coverage (%)"] = (component_scores.notna().mean(axis=1) * 100).round(0).astype("Int64")
    result["Risk Level"] = result["Risk Score"].apply(
        lambda x: "High" if x >= 66.7 else ("Moderate" if x >= 33.3 else "Low")
    )
    result = result.sort_values(["Risk Score", "Performance Score"], ascending=[False, True])
    result.insert(0, "Department", result.index.astype(str))
    result = result.reset_index(drop=True)
    return result, numeric_cols


def choose_kpi_directions(numeric_cols, key_prefix="kpi_direction"):
    """Let users explicitly set the meaning of every numeric KPI."""
    directions = {}
    if not numeric_cols:
        return directions
    with st.expander("⚙️ Configure KPI meaning (important for accurate ranking)", expanded=False):
        st.caption("Choose whether higher or lower values are better. Suggested defaults are inferred from column names and may be wrong.")
        cols = st.columns(2)
        for i, name in enumerate(numeric_cols):
            default = infer_kpi_direction(name)
            with cols[i % 2]:
                directions[name] = st.selectbox(
                    name,
                    ["Higher is better", "Lower is better"],
                    index=0 if default == "Higher is better" else 1,
                    key=f"{key_prefix}_{name}",
                )
    return directions



if "page" not in st.session_state:

    st.session_state.page = "Home"

if "user" not in st.session_state:

    st.session_state.user = None



# Authenticated navigation
if st.session_state.user:

    with st.sidebar:

        brand()

        st.caption("ORGANIZATIONAL INTELLIGENCE")

        st.markdown("---")

        pages = ["Overview", "Data Hub", "Department Intelligence", "KPI Explorer",

                 "Predictive Analytics", "WHY Engine", "Risk Center",

                 "Recommendations & Actions", "What-If Lab", "AI Copilot",

                 "Reports", "Settings & Audit Logs"]

        choice = st.radio("WORKSPACE", pages, label_visibility="visible")

        st.markdown("---")

        st.caption(f"Signed in as **{st.session_state.user['name']}**")

        if st.button("Log out", use_container_width=True):

            st.session_state.user = None

            st.session_state.page = "Home"

            st.rerun()

    # Consistent top utility bar across every authenticated workspace page.
    if st.session_state.user:
        st.markdown("""
        <style>
        .top-date-card{padding:.58rem .72rem;border:1px solid #e2e7f4;border-radius:13px;
          background:rgba(255,255,255,.82);color:#344568;font-size:.72rem;line-height:1.45;white-space:nowrap}
        .top-avatar{width:36px;height:36px;display:flex;align-items:center;justify-content:center;border-radius:50%;
          background:linear-gradient(135deg,#9da7ff,#4d83eb);color:white;font-weight:800;font-size:1rem;margin:auto}
        .top-utility [data-testid="stTextInput"] input{border-radius:13px!important;background:rgba(255,255,255,.86)!important}
        .top-utility .stButton>button{min-height:2.5rem!important;height:2.5rem!important;width:2.5rem!important;
          padding:0!important;border-radius:50%!important;background:rgba(255,255,255,.9)!important;
          color:#36517f!important;border:1px solid #dce4f4!important;box-shadow:none!important}
        .top-utility .stButton>button:hover{background:#edf2ff!important;transform:translateY(-1px)}
        /* Streamlit renders the utility controls outside the empty wrapper; style the real controls too. */
        [data-testid="stHorizontalBlock"] button[kind="secondary"]{
          background:rgba(255,255,255,.94)!important;color:#36517f!important;
          border:1px solid #dce4f4!important;border-radius:13px!important;
          box-shadow:0 4px 14px rgba(56,83,150,.08)!important;
        }
        [data-testid="stHorizontalBlock"] button[kind="secondary"]:hover{
          background:#edf2ff!important;border-color:#bfcdf4!important;
        }
        .stTextInput input{
          background:rgba(255,255,255,.96)!important;color:#17213d!important;
          border:1px solid #dce4f4!important;
        }
        .stDownloadButton>button,.stFormSubmitButton>button{
          background:linear-gradient(110deg,#2864df,#6758d9)!important;color:#fff!important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="top-utility"></div>', unsafe_allow_html=True)
        search_col, notif_col, theme_col, avatar_col, date_col = st.columns([5.2, .48, .48, .5, 1.7], vertical_alignment="center")
        with search_col:
            st.text_input(
                "Search departments, KPIs, insights",
                key="global_workspace_search",
                placeholder="⌕  Search departments, KPIs, insights…",
                label_visibility="collapsed"
            )
        with notif_col:
            if st.button("♧", key="top_notifications", help="Notifications"):
                st.info("You're all caught up. New alerts will appear here when analysis produces them.")
        with theme_col:
            if "depthive_theme" not in st.session_state:
                st.session_state.depthive_theme = "light"
            if st.button("☼" if st.session_state.depthive_theme == "light" else "☾",
                         key="top_theme_toggle", help="Toggle light / dark appearance"):
                st.session_state.depthive_theme = "dark" if st.session_state.depthive_theme == "light" else "light"
                st.rerun()
        with avatar_col:
            initial = str(st.session_state.user.get("name", "P") or "P")[:1].upper()
            st.markdown(f'<div class="top-avatar">{initial}</div>', unsafe_allow_html=True)
        with date_col:
            now_label = datetime.now().strftime("%a, %d %b %Y<br>%H:%M")
            st.markdown(f'<div class="top-date-card">▦ &nbsp; {now_label}</div>', unsafe_allow_html=True)

        if st.session_state.get("depthive_theme") == "dark":
            st.markdown("""<style>
            .stApp{background:linear-gradient(135deg,#151c30,#202944 60%,#29243b)!important;color:#eef2ff!important}
            [data-testid="stAppViewContainer"],[data-testid="stMain"]{background:transparent!important}
            [data-testid="stSidebar"]{background:linear-gradient(180deg,#202943,#191f35)!important}
            [data-testid="stSidebar"] *{color:#eef2ff!important}
            .reference-hero,.page-hero,.workspace-section,.module-banner,.module-mini-card,.reference-metric,
            .reference-insight,.reference-feature,.metric-tile,.module-card,.top-date-card{
              background:rgba(35,44,70,.91)!important;border-color:#394565!important}
            .reference-headline,.page-hero h1,.hero-description,.module-title,.module-section-heading,
            .workspace-section-title,.metric-value,.metric-label,.insight-title,.insight-desc,.feature-title,.feature-desc,
            h1,h2,h3,p,label{color:#edf1ff!important}
            .stTextInput input,.stTextArea textarea,.stSelectbox [data-baseweb="select"]>div{
              background:#222c46!important;color:#f1f4ff!important;border-color:#414e70!important}
            div[data-testid="stTable"] table,div[data-testid="stTable"] tbody tr td{background:#222c46!important;color:#f1f4ff!important}
            </style>""", unsafe_allow_html=True)

    # Keep the workspace canvas clean; each module provides its own visual heading.
    if choice != "Overview":
        page_descriptions = {
            "Data Hub": ("DATA FOUNDATION", "Your data, ready for intelligence", "Import, inspect and prepare organizational data."),
            "Department Intelligence": ("PERFORMANCE INTELLIGENCE", "Understand department performance", "Compare departments and identify performance gaps."),
            "KPI Explorer": ("METRICS STUDIO", "Explore the metrics behind decisions", "Review numeric KPIs, distributions and department comparisons."),
            "Predictive Analytics": ("FORWARD LOOK", "Explore what may come next", "Inspect historical trends and prototype estimates."),
            "WHY Engine": ("ROOT-CAUSE ANALYSIS", "Look beyond the surface metric", "Compare department results with overall performance."),
            "Risk Center": ("RISK MONITOR", "Review organizational risk signals", "Inspect KPI-based risk indicators using available data."),
            "Recommendations & Actions": ("ACTION WORKSPACE", "Turn findings into next steps", "Review evidence-led recommendations and action plans."),
            "What-If Lab": ("SCENARIO PLANNING", "Explore decisions before acting", "Compare supported assumptions and scenario outcomes."),
            "AI Copilot": ("ANALYTICS ASSISTANT", "Ask questions about your data", "Explore supported metrics and dataset patterns."),
            "Reports": ("REPORT CENTER", "Create a shareable data snapshot", "Generate summaries from the data in your workspace."),
            "Settings & Audit Logs": ("WORKSPACE CONTROL", "Settings & activity", "Review session details, dataset status and recorded activity.")
        }
        eyebrow, headline, description = page_descriptions.get(
            choice, ("DEPTHIVE WORKSPACE", choice, "Organizational intelligence workspace.")
        )
        st.markdown(
            f'<div class="reference-hero"><div class="reference-eyebrow">DEPTHIVE / {eyebrow}</div>'
            f'<div class="reference-headline">{headline}</div>'
            f'<div class="reference-description">{description}</div>'
            f'<div class="hero-note"><span>ANALYZE</span><span>UNDERSTAND</span><span>DECIDE</span></div></div>',
            unsafe_allow_html=True
        )

    if choice == "Overview":
        df = st.session_state.get("uploaded_preview")
        if df is None:
            df = st.session_state.get("dataset")

        st.markdown(
            '<div class="reference-hero"><div class="reference-eyebrow">WELCOME TO DEPTHIVE</div>'
            '<div class="reference-headline">Organizational<br>Intelligence for <span>Smarter Decisions</span></div>'
            '<div class="reference-description">A decision-focused snapshot of data quality, department performance and risk signals.</div>'
            '<div class="hero-note"><span>MEASURE</span><span>COMPARE</span><span>PRIORITIZE</span></div></div>',
            unsafe_allow_html=True,
        )

        if df is None or df.empty:
            st.info("Upload a CSV or Excel file in Data Hub to populate your live overview.")
            st.markdown("#### What you will see here")
            a, b, c = st.columns(3)
            a.markdown("**01 · Performance**\n\nDepartment comparisons and KPI trends.")
            b.markdown("**02 · Risk signals**\n\nRanked areas that may need review.")
            c.markdown("**03 · Data quality**\n\nMissing values, duplicates and coverage.")
        else:
            row_count, col_count = df.shape
            missing_count = int(df.isna().sum().sum())
            duplicate_count = int(df.duplicated().sum())
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            has_dept = "Department" in df.columns
            dept_count = int(df["Department"].nunique(dropna=True)) if has_dept else 0
            completeness = (1 - missing_count / max(1, row_count * col_count)) * 100

            st.markdown('<div class="section-kicker">LIVE DATA SNAPSHOT</div>', unsafe_allow_html=True)
            metrics = st.columns(5)
            metrics[0].metric("Rows", f"{row_count:,}")
            metrics[1].metric("Attributes", f"{col_count:,}")
            metrics[2].metric("Departments", f"{dept_count:,}" if has_dept else "Not detected")
            metrics[3].metric("Data completeness", f"{completeness:.1f}%")
            metrics[4].metric("Duplicate rows", f"{duplicate_count:,}")

            if not has_dept:
                st.warning("Department-level ranking needs a column named exactly `Department`. Rename the matching column in your dataset to enable it.")
            elif not numeric_cols:
                st.warning("Department column found, but no numeric KPI columns are available for comparison.")
            else:
                inferred_directions = {c: infer_kpi_direction(c) for c in numeric_cols}
                scorecard, used_cols = department_scorecard(df, inferred_directions)
                left, right = st.columns([1.5, 1])
                with left:
                    st.markdown("### Department performance ranking")
                    if not scorecard.empty:
                        ranking_metric = st.selectbox("Rank departments by", ["Performance Score", "Risk Score"], key="overview_rank_metric")
                        chart_data = scorecard.set_index("Department")[ranking_metric].sort_values(ascending=(ranking_metric == "Risk Score"))
                        st.bar_chart(chart_data, use_container_width=True)
                        st.caption("Scores are relative percentile-based comparisons across the departments in this dataset.")
                with right:
                    st.markdown("### Priority signals")
                    if not scorecard.empty:
                        high_risk = int((scorecard["Risk Level"] == "High").sum())
                        moderate_risk = int((scorecard["Risk Level"] == "Moderate").sum())
                        best = scorecard.sort_values("Performance Score", ascending=False).iloc[0]
                        highest_risk = scorecard.sort_values("Risk Score", ascending=False).iloc[0]
                        st.metric("High-risk departments", high_risk)
                        st.metric("Moderate-risk departments", moderate_risk)
                        st.success(f"Strongest relative performer: **{best['Department']}** ({best['Performance Score']:.1f}/100)")
                        st.warning(f"First department to review: **{highest_risk['Department']}** (risk score {highest_risk['Risk Score']:.1f}/100)")

                st.markdown("### Department scorecard")
                display_cols = ["Department", "Performance Score", "Risk Score", "Risk Level", "KPIs Available", "KPI Coverage (%)"]
                st.dataframe(scorecard[display_cols], use_container_width=True, hide_index=True)
                with st.expander("See KPI averages by department"):
                    st.dataframe(df.groupby("Department", dropna=True)[numeric_cols].mean(numeric_only=True).round(2).reset_index(), use_container_width=True, hide_index=True)
                st.caption("Direction defaults are inferred from column names. Review them in Department Intelligence or Risk Center before relying on rankings. These are decision-support indicators, not guaranteed-accurate predictions.")

            st.markdown("### Data quality at a glance")
            q1, q2 = st.columns([1, 1.5])
            with q1:
                quality = pd.DataFrame({"Check": ["Present cells", "Missing cells", "Duplicate rows"], "Count": [int(df.notna().sum().sum()), missing_count, duplicate_count]})
                st.bar_chart(quality.set_index("Check"))
            with q2:
                missing_by_col = df.isna().sum().sort_values(ascending=False)
                missing_by_col = missing_by_col[missing_by_col > 0].head(10)
                if missing_by_col.empty:
                    st.success("No missing values detected in this dataset.")
                else:
                    st.markdown("**Columns with the most missing values**")
                    st.bar_chart(missing_by_col)
                    st.dataframe(missing_by_col.rename("Missing cells").reset_index(names="Attribute"), use_container_width=True, hide_index=True)

        st.markdown('<div class="section-kicker">EXPLORE YOUR WORKSPACE</div>', unsafe_allow_html=True)
        feature_data = [
            ("▤", "Data Hub", "Upload, validate and clean your data.", "blue"),
            ("♙", "Department Intelligence", "Compare performance and rank departments.", "lavender"),
            ("△", "Risk Center", "Review configurable risk factors.", "peach"),
            ("⚗", "What-If Lab", "Explore scenario assumptions.", "sky"),
        ]
        feature_cols = st.columns(4)
        for col, (icon, title, desc, theme) in zip(feature_cols, feature_data):
            with col:
                st.markdown(f'<div class="reference-feature {theme}"><div class="feature-art">{icon}</div><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>', unsafe_allow_html=True)
        st.caption("DEPTHIVE · Metrics are calculated from the currently uploaded dataset.")

    elif choice == "Data Hub":
        st.markdown('<div class="module-banner"><div class="module-banner-icon">▤</div><div><div class="module-banner-title">Your data, ready for intelligence</div><div class="module-banner-copy">Import a dataset, inspect its quality, and prepare it for analysis in one workspace.</div></div></div>', unsafe_allow_html=True)
        st.subheader("Data intake")

        st.write(

            "Upload a CSV or Excel dataset to inspect data quality "

            "and remove exact duplicate rows."

        )



        upload = st.file_uploader(

            "Upload organization dataset",

            type=["csv", "xlsx"],

            key="data_hub_upload"

        )



        if upload is not None:

            try:

                # Load uploaded dataset
                df = load_dataset(upload)



                st.success(

                    f"Loaded {len(df):,} rows and "

                    f"{len(df.columns)} columns."

                )



                # Dataset preview
                st.markdown('<div class="module-section-heading">Dataset preview</div>', unsafe_allow_html=True)

                st.dataframe(df.head(100), use_container_width=True)



                # Data quality analysis
                report = generate_data_quality_report(df)



                st.markdown('<div class="module-section-heading">Data quality overview</div>', unsafe_allow_html=True)



                col1, col2, col3, col4 = st.columns(4)



                col1.metric("Total Rows", report["total_rows"])

                col2.metric("Total Columns", report["total_columns"])

                col3.metric("Duplicate Rows", report["duplicate_rows"])

                col4.metric("Missing Cells", report["missing_cells"])



                # Column-level details
                with st.expander("View Column Details"):

                    column_details = pd.DataFrame({

                        "Column": report["column_names"],

                        "Data Type": [

                            report["data_types"][column]

                            for column in report["column_names"]

                        ],

                        "Missing Values": [

                            report["missing_values_by_column"][column]

                            for column in report["column_names"]

                        ]

                    })



                    st.dataframe(

                        column_details,

                        use_container_width=True

                    )



                # Remove duplicate rows
                st.subheader("Data Cleaning")



                cleaned_df, summary = clean_dataset(df)



                st.write(

                    f"**Original rows:** {summary['original_rows']}"

                )

                st.write(

                    f"**Cleaned rows:** {summary['cleaned_rows']}"

                )

                st.write(

                    f"**Duplicate rows removed:** "

                    f"{summary['duplicates_removed']}"

                )

                st.info(

                    "Missing values are retained for now; "

                    "they are reported rather than automatically deleted."

                )



                st.dataframe(

                    cleaned_df.head(100),

                    use_container_width=True

                )



                # Download cleaned dataset
                csv_data = cleaned_df.to_csv(index=False).encode("utf-8")



                st.download_button(

                    label="Download Cleaned CSV",

                    data=csv_data,

                    file_name="depthive_cleaned_dataset.csv",

                    mime="text/csv"

                )



                # Keep original and cleaned datasets available during the session
                st.session_state["uploaded_preview"] = df

                st.session_state["cleaned_dataset"] = cleaned_df



            except Exception as e:

                st.error(f"Could not process this file: {e}")

    elif choice == "Department Intelligence":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Department performance intelligence</div><div class="workspace-section-copy">A relative, configurable ranking that accounts for whether each KPI should increase or decrease.</div></div>', unsafe_allow_html=True)
        df = st.session_state.get("uploaded_preview")
        if df is None or df.empty:
            st.info("Please upload a dataset in Data Hub first.")
        elif "Department" not in df.columns:
            st.warning("Dataset must contain a column named exactly `Department`.")
        else:
            numeric_cols = [c for c in df.select_dtypes(include="number").columns if df[c].notna().any()]
            if not numeric_cols:
                st.warning("No numeric KPI columns found. Convert the metrics you want to analyze to numeric values.")
            else:
                directions = choose_kpi_directions(numeric_cols, "department_direction")
                # Expander returns only values interacted with in this run; fill all other values with inferred defaults.
                full_directions = {c: directions.get(c, infer_kpi_direction(c)) for c in numeric_cols}
                scorecard, _ = department_scorecard(df, full_directions)
                if scorecard.empty:
                    st.warning("Not enough valid department data to calculate a ranking.")
                else:
                    best = scorecard.sort_values("Performance Score", ascending=False).iloc[0]
                    review = scorecard.sort_values("Risk Score", ascending=False).iloc[0]
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Departments", len(scorecard))
                    m2.metric("Top performer", str(best["Department"]))
                    m3.metric("Lowest relative score", str(review["Department"]))
                    m4.metric("Mean performance score", f"{scorecard['Performance Score'].mean():.1f}/100")
                    left, right = st.columns(2)
                    with left:
                        st.markdown("### Performance score")
                        st.bar_chart(scorecard.set_index("Department")["Performance Score"].sort_values(ascending=False), use_container_width=True)
                    with right:
                        st.markdown("### Risk priority")
                        st.bar_chart(scorecard.set_index("Department")["Risk Score"].sort_values(ascending=False), use_container_width=True)
                    st.markdown("### Ranked department scorecard")
                    st.dataframe(scorecard, use_container_width=True, hide_index=True)
                    st.download_button("Download department ranking (CSV)", scorecard.to_csv(index=False).encode("utf-8"), file_name="depthive_department_ranking.csv", mime="text/csv")
                    st.caption("Method: each department's mean for each KPI is converted to a percentile rank; direction is applied per KPI; KPI scores are averaged. This creates a relative ranking, not absolute performance truth. Check KPI direction and data quality before using it for decisions.")

    elif choice == "KPI Explorer":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">KPI analysis workspace</div><div class="workspace-section-copy">Select a numeric KPI and explore its average, minimum, maximum, distribution and department-level comparison.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="module-section-heading">KPI explorer</div>', unsafe_allow_html=True)

        st.markdown('<div class="module-note">Choose a numeric measure to review its central tendency, range, distribution, and department-level pattern.</div>', unsafe_allow_html=True)



        df = st.session_state.get("uploaded_preview")



        if df is None:

            st.info("Please upload a dataset in Data Hub first.")



        else:

            numeric_columns = df.select_dtypes(

                include=["number"]

            ).columns.tolist()



            if not numeric_columns:

                st.warning("No numeric KPI columns found in the dataset.")



            else:

                selected_kpi = st.selectbox(

                    "Select a KPI",

                    numeric_columns

                )



                col1, col2, col3 = st.columns(3)



                col1.metric(

                    "Average",

                    round(df[selected_kpi].mean(), 2)

                )



                col2.metric(

                    "Maximum",

                    round(df[selected_kpi].max(), 2)

                )



                col3.metric(

                    "Minimum",

                    round(df[selected_kpi].min(), 2)

                )



                st.subheader(f"{selected_kpi} — Data Distribution")

                st.bar_chart(df[selected_kpi])



                if "Department" in df.columns:

                    st.subheader(f"{selected_kpi} by Department")



                    department_kpi = (

                        df.groupby("Department")[selected_kpi]

                        .mean()

                        .sort_values(ascending=False)

                    )



                    st.bar_chart(department_kpi)



                    st.dataframe(

                        department_kpi.reset_index(),

                        use_container_width=True

                    )



    elif choice == "Predictive Analytics":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Forecasting workspace</div><div class="workspace-section-copy">Use historical numeric values to inspect patterns and explore estimates. Predictions depend on the quality and quantity of uploaded data.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="module-section-heading">Predictive analytics</div>', unsafe_allow_html=True)

        st.markdown('<div class="module-note">Forecasts are exploratory estimates from available historical values, not guarantees. Connect enough clean data before interpreting a trend.</div>', unsafe_allow_html=True)



        df = st.session_state.get("uploaded_preview")



        if df is None:

            st.info("Please upload a dataset in Data Hub first.")

        else:

            numeric_columns = df.select_dtypes(

                include=["number"]

            ).columns.tolist()



            if not numeric_columns:

                st.warning("No numeric KPI columns found.")

            else:

                selected_kpi = st.selectbox(

                    "Select KPI for prediction",

                    numeric_columns,

                    key="prediction_kpi"

                )



                values = (

                    pd.to_numeric(df[selected_kpi], errors="coerce")

                    .dropna()

                    .reset_index(drop=True)

                )



                if len(values) < 3:

                    st.warning("At least 3 numeric observations are required.")

                else:

                    prediction = round(values.tail(5).mean(), 2)



                    col1, col2 = st.columns(2)



                    col1.metric(

                        "Latest Observed Value",

                        round(values.iloc[-1], 2)

                    )



                    col2.metric(

                        "Estimated Next Value",

                        prediction

                    )



                    st.subheader("Historical KPI Trend")

                    st.line_chart(values)



                    st.subheader("Latest vs Estimated Value")

                    st.bar_chart(

                        pd.DataFrame({

                            "Value": [

                                round(values.iloc[-1], 2),

                                prediction

                            ]

                        }, index=["Latest Observed", "Estimated Next"])

                    )



                    st.caption(

                        "Prototype estimate based on the last five observations; "

                        "this is not a validated forecasting model."

                    )

    elif choice == "WHY Engine":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Evidence-led root-cause exploration</div><div class="workspace-section-copy">Investigate possible explanations for observed changes. Treat results as hypotheses unless supported by sufficient evidence.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="module-section-heading">Root-cause exploration</div>', unsafe_allow_html=True)

        st.write("Understand why a department's performance may be changing.")



        df = st.session_state.get("uploaded_preview")



        if df is None:

            st.info("Please upload a dataset in Data Hub first.")

        else:

            numeric_columns = df.select_dtypes(

                include=["number"]

            ).columns.tolist()



            if "Department" not in df.columns:

                st.warning(

                    "Dataset must contain a 'Department' column."

                )

            elif not numeric_columns:

                st.warning("No numeric KPI columns found.")

            else:

                departments = df["Department"].dropna().unique().tolist()



                selected_department = st.selectbox(

                    "Select Department",

                    departments,

                    key="why_department"

                )



                department_df = df[

                    df["Department"] == selected_department

                ]



                st.markdown("### Department KPI Analysis")



                findings = []



                for col in numeric_columns:

                    department_avg = pd.to_numeric(

                        department_df[col], errors="coerce"

                    ).mean()



                    overall_avg = pd.to_numeric(

                        df[col], errors="coerce"

                    ).mean()



                    if pd.isna(department_avg) or pd.isna(overall_avg):

                        continue



                    difference = department_avg - overall_avg



                    if difference < 0:

                        status = "Below overall average"

                    elif difference > 0:

                        status = "Above overall average"

                    else:

                        status = "At overall average"



                    findings.append({

                        "KPI": col,

                        "Department Average": round(department_avg, 2),

                        "Overall Average": round(overall_avg, 2),

                        "Difference": round(difference, 2),

                        "Finding": status

                    })



                if findings:

                    findings_df = pd.DataFrame(findings)



                    st.dataframe(

                        findings_df,

                        use_container_width=True,

                        hide_index=True

                    )



                    st.markdown("### Possible Reasons")



                    below_average = findings_df[

                        findings_df["Difference"] < 0

                    ]



                    if not below_average.empty:

                        for _, row in below_average.iterrows():

                            st.warning(

                                f"**{row['KPI']}** is below the overall "

                                f"average by {abs(row['Difference'])}. "

                                "This KPI may need investigation."

                            )

                    else:

                        st.success(

                            "No numeric KPI is below the overall average."

                        )



                    st.caption(

                        "These are comparisons, not proven causes. "

                        "Business context is needed to confirm the reasons."

                    )

                else:



                    st.warning("No usable numeric KPI values were found.")

    elif choice == "Risk Center":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Risk factor analysis</div><div class="workspace-section-copy">Prioritize departments using KPI direction, relative performance and data coverage instead of treating every low number as a risk.</div></div>', unsafe_allow_html=True)
        st.subheader("Risk Center")
        df = st.session_state.get("uploaded_preview")
        if df is None or df.empty:
            st.info("Please upload a dataset in Data Hub first.")
        elif "Department" not in df.columns:
            st.warning("Dataset must contain a column named exactly `Department`.")
        else:
            numeric_cols = [c for c in df.select_dtypes(include="number").columns if df[c].notna().any()]
            if not numeric_cols:
                st.warning("No numeric KPI columns found.")
            else:
                directions = choose_kpi_directions(numeric_cols, "risk_direction")
                full_directions = {c: directions.get(c, infer_kpi_direction(c)) for c in numeric_cols}
                scorecard, _ = department_scorecard(df, full_directions)
                if scorecard.empty:
                    st.warning("Not enough valid data to calculate risk scores.")
                else:
                    high = int((scorecard["Risk Level"] == "High").sum())
                    moderate = int((scorecard["Risk Level"] == "Moderate").sum())
                    low = int((scorecard["Risk Level"] == "Low").sum())
                    a, b, c, d = st.columns(4)
                    a.metric("High priority", high)
                    b.metric("Moderate priority", moderate)
                    c.metric("Low priority", low)
                    d.metric("KPIs analyzed", len(numeric_cols))

                    left, right = st.columns([1.25, 1])
                    with left:
                        st.markdown("### Risk priority by department")
                        risk_chart = scorecard.set_index("Department")["Risk Score"].sort_values(ascending=False)
                        st.bar_chart(risk_chart, use_container_width=True)
                    with right:
                        st.markdown("### Risk factor contribution")
                        dept_options = scorecard["Department"].astype(str).tolist()
                        selected_dept = st.selectbox("Inspect department", dept_options, key="risk_factor_department")
                        subset = df[df["Department"].astype("string").str.strip() == selected_dept]
                        dept_means = subset[numeric_cols].mean(numeric_only=True)
                        overall_means = df[numeric_cols].mean(numeric_only=True)
                        factor_rows = []
                        for col in numeric_cols:
                            dv, ov = dept_means.get(col), overall_means.get(col)
                            if pd.isna(dv) or pd.isna(ov):
                                continue
                            # Display relative difference, while risk score itself is percentile based.
                            delta = ((float(dv) - float(ov)) / abs(float(ov)) * 100) if float(ov) != 0 else None
                            direction = full_directions[col]
                            is_unfavorable = (float(dv) < float(ov)) if direction == "Higher is better" else (float(dv) > float(ov))
                            factor_rows.append({"Risk factor": col, "Department average": round(float(dv), 2), "Overall average": round(float(ov), 2), "Difference (%)": round(delta, 1) if delta is not None else "N/A", "Direction": direction, "Signal": "Review" if is_unfavorable else "Favourable"})
                        factor_df = pd.DataFrame(factor_rows)
                        if not factor_df.empty:
                            st.dataframe(factor_df.sort_values("Signal", ascending=False), use_container_width=True, hide_index=True)
                        else:
                            st.info("Not enough non-missing values to compare this department.")

                    st.markdown("### Department risk ranking")
                    st.dataframe(scorecard.sort_values("Risk Score", ascending=False), use_container_width=True, hide_index=True)
                    st.download_button("Download risk assessment (CSV)", scorecard.to_csv(index=False).encode("utf-8"), file_name="depthive_risk_assessment.csv", mime="text/csv")
                    with st.expander("How the risk score works"):
                        st.markdown("""
                        1. Calculate each department's mean for every numeric KPI.
                        2. Convert each KPI's department averages into percentile ranks, so different units can be compared.
                        3. Reverse the percentile for KPIs marked **Lower is better**.
                        4. Average the available KPI scores into a performance score; risk score = 100 − performance score.
                        5. Label risk as High (66.7–100), Moderate (33.3–66.6) or Low (0–33.2).

                        **Important:** this is a transparent relative screening algorithm, not a clinically/financially/operationally validated model. Column-name defaults are only suggestions. Configure directions using domain knowledge and add explicit targets/weights if some KPIs matter more than others.
                        """)

    elif choice == "Recommendations & Actions":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">From findings to action</div><div class="workspace-section-copy">Review available recommendations and define follow-up actions based on organizational evidence.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="module-section-heading">Recommendations & actions</div>', unsafe_allow_html=True)

        st.write(

            "Turn department performance findings into actionable next steps."

        )



        df = st.session_state.get("uploaded_preview")



        if df is None:

            st.info("Please upload a dataset in Data Hub first.")



        elif "Department" not in df.columns:

            st.warning(

                "Dataset must contain a 'Department' column."

            )



        else:

            numeric_columns = df.select_dtypes(

                include=["number"]

            ).columns.tolist()



            if not numeric_columns:

                st.warning("No numeric KPI columns found.")



            else:

                departments = df["Department"].dropna().unique().tolist()



                selected_department = st.selectbox(

                    "Select Department",

                    departments,

                    key="recommendation_department"

                )



                dept_df = df[

                    df["Department"] == selected_department

                ]



                st.markdown("### Department Findings")



                recommendations = []



                for col in numeric_columns:

                    dept_avg = pd.to_numeric(

                        dept_df[col], errors="coerce"

                    ).mean()



                    overall_avg = pd.to_numeric(

                        df[col], errors="coerce"

                    ).mean()



                    if pd.isna(dept_avg) or pd.isna(overall_avg):

                        continue



                    if overall_avg != 0 and dept_avg < overall_avg * 0.8:

                        recommendations.append({

                            "KPI": col,

                            "Department Average": round(dept_avg, 2),

                            "Overall Average": round(overall_avg, 2),

                            "Priority": "High",

                            "Recommended Action": (

                                f"Investigate why {col} is below the "

                                "overall average. Review the underlying "

                                "records and identify improvement steps."

                            )

                        })



                    elif dept_avg < overall_avg:

                        recommendations.append({

                            "KPI": col,

                            "Department Average": round(dept_avg, 2),

                            "Overall Average": round(overall_avg, 2),

                            "Priority": "Medium",

                            "Recommended Action": (

                                f"Monitor {col}, compare recent results, "

                                "and review whether corrective action is needed."

                            )

                        })



                if recommendations:

                    recommendations_df = pd.DataFrame(recommendations)



                    st.dataframe(

                        recommendations_df,

                        use_container_width=True,

                        hide_index=True

                    )



                    st.markdown("### Action Plan")



                    for i, item in enumerate(recommendations, start=1):

                        with st.expander(

                            f"{i}. {item['KPI']} — {item['Priority']} Priority"

                        ):

                            st.write(item["Recommended Action"])



                            owner = st.text_input(

                                "Action Owner",

                                key=f"action_owner_{i}"

                            )



                            due_date = st.date_input(

                                "Target Date",

                                key=f"action_date_{i}"

                            )



                            st.text_area(

                                "Progress Notes",

                                key=f"action_notes_{i}"

                            )



                    st.caption(

                        "Recommendations are generated from KPI comparisons. "

                        "Validate whether higher or lower values are desirable "

                        "before acting on them."

                    )



                else:

                    st.success(

                        "No below-average numeric KPIs were identified "

                        "for this department."

                    )

    elif choice == "What-If Lab":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Scenario comparison lab</div><div class="workspace-section-copy">Adjust supported inputs and compare scenario outcomes. Simulations are only as reliable as their assumptions.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="module-section-heading">Scenario lab</div>', unsafe_allow_html=True)

        st.write(

            "Simulate KPI changes and explore their potential impact."

        )



        df = st.session_state.get("uploaded_preview")



        if df is None:

            st.info("Please upload a dataset in Data Hub first.")



        elif "Department" not in df.columns:

            st.warning("Dataset must contain a 'Department' column.")



        else:

            numeric_columns = df.select_dtypes(

                include=["number"]

            ).columns.tolist()



            if not numeric_columns:

                st.warning("No numeric KPI columns found.")



            else:

                departments = df["Department"].dropna().unique().tolist()



                selected_department = st.selectbox(

                    "Select Department",

                    departments,

                    key="whatif_department"

                )



                selected_kpi = st.selectbox(

                    "Select KPI",

                    numeric_columns,

                    key="whatif_kpi"

                )



                dept_df = df[

                    df["Department"] == selected_department

                ]



                current_value = pd.to_numeric(

                    dept_df[selected_kpi], errors="coerce"

                ).mean()



                overall_value = pd.to_numeric(

                    df[selected_kpi], errors="coerce"

                ).mean()



                if pd.isna(current_value):

                    st.warning("No valid numeric values for this KPI.")

                else:

                    st.metric(

                        "Current Department Average",

                        round(current_value, 2)

                    )



                    st.metric(

                        "Overall Dataset Average",

                        round(overall_value, 2)

                        if pd.notna(overall_value) else "N/A"

                    )



                    st.markdown("### Simulate a KPI Change")



                    change_pct = st.slider(

                        "Adjust KPI value (%)",

                        min_value=-50,

                        max_value=100,

                        value=10,

                        step=5,

                        key="whatif_change"

                    )



                    simulated_value = current_value * (

                        1 + change_pct / 100

                    )



                    col1, col2 = st.columns(2)



                    col1.metric(

                        "Current Value",

                        round(current_value, 2)

                    )



                    col2.metric(

                        "Simulated Value",

                        round(simulated_value, 2),

                        delta=f"{change_pct}%"

                    )



                    if pd.notna(overall_value):

                        if simulated_value > overall_value:

                            st.success(

                                "In this simulation, the KPI is above "

                                "the overall dataset average."

                            )

                        elif simulated_value < overall_value:

                            st.warning(

                                "In this simulation, the KPI remains below "

                                "the overall dataset average."

                            )

                        else:

                            st.info(

                                "In this simulation, the KPI matches "

                                "the overall dataset average."

                            )



                    comparison_df = pd.DataFrame({

                        "Value": [

                            current_value,

                            simulated_value

                        ]

                    }, index=["Current", "Simulated"])



                    st.bar_chart(comparison_df)



                    st.caption(

                        "This is a mathematical what-if simulation, not a "

                        "causal prediction. It assumes the selected KPI "

                        "changes while other factors remain constant."

                    )

    elif choice == "AI Copilot":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Ask your dataset</div><div class="workspace-section-copy">Use supported natural-language prompts to inspect metrics, compare departments and check data quality.</div></div>', unsafe_allow_html=True)

        st.subheader("🤖 DEPTHIVE AI Copilot")

        st.write(

            "Ask questions about your uploaded department dataset."

        )



        df = st.session_state.get("uploaded_preview")



        if df is None:

            st.info("Please upload a dataset in Data Hub first.")



        else:

            st.markdown("### Dataset Overview")



            col1, col2, col3 = st.columns(3)



            col1.metric("Total Records", len(df))

            col2.metric("Total Columns", len(df.columns))

            col3.metric(

                "Departments",

                df["Department"].nunique()

                if "Department" in df.columns else "N/A"

            )



            st.markdown("### Ask a Question")



            question = st.text_input(

                "Your question",

                placeholder="e.g. Which department has the highest average KPI?"

            )



            if st.button("Analyze", key="copilot_analyze"):

                if not question.strip():

                    st.warning("Please enter a question.")



                else:

                    q = question.lower()

                    numeric_columns = df.select_dtypes(

                        include=["number"]

                    ).columns.tolist()



                    if "department" in q and (

                        "list" in q or "how many" in q

                    ):

                        if "Department" in df.columns:

                            departments = (

                                df["Department"]

                                .dropna()

                                .unique()

                                .tolist()

                            )



                            st.write(

                                f"**Number of departments:** {len(departments)}"

                            )

                            st.write("**Departments:**", ", ".join(

                                map(str, departments)

                            ))

                        else:

                            st.warning(

                                "The dataset has no Department column."

                            )



                    elif any(word in q for word in [

                        "average", "mean", "highest", "maximum",

                        "lowest", "minimum"

                    ]):

                        if not numeric_columns:

                            st.warning(

                                "No numeric columns found in the dataset."

                            )



                        else:

                            selected_kpi = st.selectbox(

                                "Choose KPI to analyze",

                                numeric_columns,

                                key="copilot_kpi"

                            )



                            values = pd.to_numeric(

                                df[selected_kpi], errors="coerce"

                            )



                            if "highest" in q or "maximum" in q:

                                st.success(

                                    f"Highest {selected_kpi}: "

                                    f"{values.max():.2f}"

                                )



                            elif "lowest" in q or "minimum" in q:

                                st.info(

                                    f"Lowest {selected_kpi}: "

                                    f"{values.min():.2f}"

                                )



                            else:

                                st.success(

                                    f"Average {selected_kpi}: "

                                    f"{values.mean():.2f}"

                                )



                    elif "department" in q and any(

                        word in q for word in [

                            "performance", "compare", "ranking"

                        ]

                    ):

                        if "Department" not in df.columns:

                            st.warning(

                                "The dataset has no Department column."

                            )



                        elif not numeric_columns:

                            st.warning("No numeric KPI columns found.")



                        else:

                            selected_kpi = st.selectbox(

                                "Choose KPI for department comparison",

                                numeric_columns,

                                key="copilot_compare_kpi"

                            )



                            summary = df.groupby("Department")[

                                selected_kpi

                            ].mean().sort_values(ascending=False)



                            st.write("Department averages:")

                            st.dataframe(

                                summary.reset_index(),

                                use_container_width=True,

                                hide_index=True

                            )



                            st.bar_chart(summary)



                    elif "missing" in q or "null" in q:

                        missing = df.isna().sum()

                        st.write("Missing values by column:")

                        st.dataframe(

                            missing[missing > 0].rename(

                                "Missing Values"

                            ).reset_index().rename(

                                columns={"index": "Column"}

                            ),

                            use_container_width=True,

                            hide_index=True

                        )



                    else:

                        st.info(

                            "I can currently answer questions about "

                            "department counts, KPI averages, maximum/minimum "

                            "values, department comparisons, and missing data. "

                            "Try rephrasing your question using one of these topics."

                        )



            st.caption(

                "Prototype dataset assistant using predefined analytical rules. "

                "It is not connected to an external LLM."

            )

    elif choice == "Reports":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Report builder</div><div class="workspace-section-copy">Create a downloadable summary from the dataset currently available in your workspace.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="module-section-heading">Report studio</div>', unsafe_allow_html=True)

        st.markdown('<div class="module-note">Build a concise, downloadable snapshot of the data currently connected to your workspace.</div>', unsafe_allow_html=True)



        df = st.session_state.get("uploaded_preview")



        if df is None:

            st.info("Please upload a dataset in Data Hub first.")



        else:

            st.markdown("### Dataset Summary")



            col1, col2, col3 = st.columns(3)



            col1.metric("Total Records", len(df))

            col2.metric("Total Columns", len(df.columns))

            col3.metric(

                "Missing Values",

                int(df.isna().sum().sum())

            )



            st.markdown("### Data Preview")

            st.dataframe(df.head(10), use_container_width=True)



            st.markdown("### Download Reports")



            csv_data = df.to_csv(index=False).encode("utf-8")



            st.download_button(

                label="📥 Download Dataset Report (CSV)",

                data=csv_data,

                file_name="depthive_dataset_report.csv",

                mime="text/csv"

            )



            summary_lines = [

                "DEPTHIVE - DATASET SUMMARY REPORT",

                "=" * 40,

                f"Total Records: {len(df)}",

                f"Total Columns: {len(df.columns)}",

                f"Total Missing Values: {int(df.isna().sum().sum())}",

                "",

                "COLUMN DETAILS"

            ]



            for col in df.columns:

                summary_lines.append(

                    f"{col}: {df[col].nunique(dropna=True)} unique values, "

                    f"{int(df[col].isna().sum())} missing values"

                )



            numeric_columns = df.select_dtypes(

                include=["number"]

            ).columns.tolist()



            if numeric_columns:

                summary_lines.extend([

                    "",

                    "NUMERIC KPI STATISTICS"

                ])



                summary_lines.append(

                    df[numeric_columns].describe().round(2).to_string()

                )



            if "Department" in df.columns:

                summary_lines.extend([

                    "",

                    "DEPARTMENT RECORD COUNTS",

                    df["Department"].value_counts().to_string()

                ])



            report_text = "\n".join(summary_lines)



            st.download_button(

                label="📄 Download Executive Summary (TXT)",

                data=report_text,

                file_name="depthive_executive_summary.txt",

                mime="text/plain"

            )



            if numeric_columns:

                st.markdown("### KPI Statistics")

                st.dataframe(

                    df[numeric_columns].describe().round(2),

                    use_container_width=True

                )



            st.caption(

                "Reports summarize the uploaded dataset. "

                "They do not represent an independently validated audit."

            )

    elif choice == "Settings & Audit Logs":
        st.markdown('<div class="workspace-section"><div class="workspace-section-title">Settings & activity</div><div class="workspace-section-copy">Review the workspace controls and audit details supported by the current prototype.</div></div>', unsafe_allow_html=True)

        st.subheader("⚙️ Settings & Audit Logs")

        st.write("Review the current session and track app activities.")



        df = st.session_state.get("uploaded_preview")



        if "activity_logs" not in st.session_state:

            st.session_state["activity_logs"] = []



        if not st.session_state.get("audit_initialized"):

            st.session_state["activity_logs"].append({

                "Timestamp": pd.Timestamp.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),

                "Activity": "Settings & Audit Logs opened",

                "Details": "Session activity tracking initialized"

            })

            st.session_state["audit_initialized"] = True



        col1, col2, col3 = st.columns(3)



        current_user = st.session_state.get("user")
        if isinstance(current_user, dict):
            session_user_label = current_user.get("name", "Logged in")
        else:
            session_user_label = str(current_user or "Logged in")

        col1.metric("Session User", session_user_label)



        col2.metric(

            "Dataset Status",

            "Uploaded" if df is not None else "Not uploaded"

        )



        col3.metric(

            "Tracked Activities",

            len(st.session_state["activity_logs"])

        )



        st.markdown("### Dataset Settings")



        if df is not None:

            st.write(f"**Rows:** {df.shape[0]}")

            st.write(f"**Columns:** {df.shape[1]}")

            st.write("**Column names:**", ", ".join(map(str, df.columns)))



            if st.button("Log Dataset Review"):

                st.session_state["activity_logs"].append({

                    "Timestamp": pd.Timestamp.now().strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),

                    "Activity": "Dataset review",

                    "Details": f"Reviewed dataset with {len(df)} rows"

                })

                st.success("Dataset review activity logged.")



        else:

            st.info("Upload a dataset in Data Hub to view dataset settings.")



        st.markdown("### Activity Log")



        logs_df = pd.DataFrame(

            st.session_state["activity_logs"]

        )



        if not logs_df.empty:

            st.table(logs_df)



            st.download_button(

                "📥 Download Audit Log (CSV)",

                data=logs_df.to_csv(index=False).encode("utf-8"),

                file_name="depthive_audit_log.csv",

                mime="text/csv"

            )



        else:

            st.info("No activities have been recorded yet.")



        st.caption(

            "Prototype session log only. It is not a permanent, "

            "tamper-proof security audit trail."

        )

    else:

        st.markdown(

            '<div class="glass-card">'

            '<span class="pill">MODULE SCAFFOLD</span>'

            '<h3>Ready for implementation</h3>'

            '<p class="subtle">This page is in the product navigation. '

            'We will connect its real calculations, database records, '

            'and interactions in the next build step.</p></div>',

            unsafe_allow_html=True

        )



        st.caption(

            "Only implemented features should be presented as live capabilities."

        )

else:

    brand()

    st.markdown("<br>", unsafe_allow_html=True)

    page = st.session_state.page

    if page == "Home":

        left, right = st.columns([1.12, .88], gap="large")

        with left:

            st.markdown('<div class="eyebrow">ORGANIZATIONAL INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)

            st.markdown('<div class="hero-title">See Beyond Data.<br><span class="gradient-text">Decide with Intelligence.</span></div>', unsafe_allow_html=True)

            st.markdown('<p class="subtle">Bring organizational data together, uncover performance signals, investigate risks, and turn analysis into measurable action.</p>', unsafe_allow_html=True)

            st.markdown('<span class="pill">DATA • ANALYTICS • DECISIONS</span>', unsafe_allow_html=True)

            st.write("")

            c1,c2 = st.columns([1,1])

            with c1:

                if st.button("Get Started  →", use_container_width=True):

                    set_page("Sign Up"); st.rerun()

            with c2:

                if st.button("Sign In", use_container_width=True):

                    set_page("Login"); st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            st.caption("Built for evidence-led decisions—not just another dashboard.")

        with right:

            st.markdown("""

            <div class="glass-card" style="min-height:430px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:radial-gradient(circle at 50% 35%,#173c72 0%,#0a1932 45%,#081126 100%);">

              <div style="font-size:7rem;line-height:1.1;background:linear-gradient(135deg,#42d9ff,#6c75ff,#a16aff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">◉</div>

              <div class="eyebrow">INTELLIGENCE CORE</div>

              <h2 style="margin-top:12px;">One workspace.<br>Clearer decisions.</h2>

              <p class="subtle" style="font-size:.9rem;">Connect data · Understand performance · Take action</p>

              <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;"><span class="pill">Analytics</span><span class="pill">Risk signals</span><span class="pill">Action tracking</span></div>

            </div>

            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        f1,f2,f3 = st.columns(3)

        for col, title, desc in [

            (f1,"01 / Connect","Import and validate organizational data."),

            (f2,"02 / Understand","Explore KPIs, trends, and possible risk signals."),

            (f3,"03 / Improve","Review recommendations and measure outcomes.")]:

            with col:

                st.markdown(f'<div class="glass-card"><div class="eyebrow">{title}</div><p class="subtle" style="font-size:.92rem">{desc}</p></div>', unsafe_allow_html=True)



    elif page == "Login":

        left, right = st.columns([.9,1.1], gap="large")

        with left:

            st.markdown('<div class="eyebrow">WELCOME BACK</div><h1>Sign in to your<br>intelligence workspace.</h1><p class="subtle">Your data. Your teams. A clearer view of what comes next.</p>', unsafe_allow_html=True)

        with right:

            st.markdown("### Sign in")

            with st.form("login_form"):

                email = st.text_input("Work email", placeholder="you@organization.com")

                password = st.text_input("Password", type="password", placeholder="Enter your password")

                submitted = st.form_submit_button("Sign In →", use_container_width=True)

            if submitted:

                user = verify_user(email.strip().lower(), password)

                if user:

                    st.session_state.user = user

                    st.session_state.page = "Overview"

                    st.rerun()

                else:

                    st.error("Sign-in failed. Check your email and password, or create an account.")

            c1,c2 = st.columns(2)

            with c1:

                if st.button("Create account", use_container_width=True):

                    set_page("Sign Up"); st.rerun()

            with c2:

                if st.button("Forgot password?", use_container_width=True):

                    set_page("Forgot Password"); st.rerun()

    elif page == "Sign Up":

        left, right = st.columns([.85,1.15], gap="large")

        with left:

            st.markdown('<div class="eyebrow">CREATE YOUR WORKSPACE</div><h1>Build a smarter<br><span class="gradient-text">organization.</span></h1><p class="subtle">Create your account to begin setting up Depthive. Access to organization data should be granted by an authorized administrator.</p>', unsafe_allow_html=True)

        with right:

            st.markdown("### Create account")

            with st.form("signup_form"):

                name = st.text_input("Full name", placeholder="Your full name")

                email = st.text_input("Work email", placeholder="you@organization.com")

                org = st.text_input("Organization name", placeholder="Organization or college")

                role = st.selectbox("Requested role", ["Analyst / Viewer", "Department Lead", "HOD / Manager", "Admin"])

                password = st.text_input("Password", type="password", help="Use at least 10 characters.")

                confirm = st.text_input("Confirm password", type="password")

                accepted = st.checkbox("I agree to the workspace terms and privacy notice.")

                submitted = st.form_submit_button("Create account →", use_container_width=True)

            if submitted:

                if not all([name.strip(), email.strip(), org.strip(), password, confirm]):

                    st.error("Please complete every field.")

                elif "@" not in email or "." not in email.split("@")[-1]:

                    st.error("Enter a valid email address.")

                elif len(password) < 10:

                    st.error("Use a password with at least 10 characters.")

                elif password != confirm:

                    st.error("Passwords do not match.")

                elif not accepted:

                    st.error("Please accept the terms to continue.")

                else:

                    ok, message = create_user(name.strip(), email.strip().lower(), org.strip(), role, password)

                    if ok:

                        st.success(message)

                        st.info("For this local prototype, email verification and admin approval workflows are not yet configured.")

                    else:

                        st.error(message)

            if st.button("← Back to sign in"):

                set_page("Login"); st.rerun()

    elif page == "Forgot Password":

        st.markdown('<div class="eyebrow">ACCOUNT RECOVERY</div><h1>Reset your password.</h1><p class="subtle">Password recovery needs a verified email delivery service. This starter keeps account security explicit rather than pretending to send an email.</p>', unsafe_allow_html=True)

        with st.form("forgot_form"):

            email = st.text_input("Account email", placeholder="you@organization.com")

            submitted = st.form_submit_button("Request reset instructions")

        if submitted:

            st.info("Password-reset email is not configured in this prototype. We will add a secure, expiring reset-token flow with email delivery before deployment.")

        if st.button("← Back to login"):

            set_page("Login"); st.rerun()



st.markdown("<br><hr>", unsafe_allow_html=True)

st.caption("DEPTHIVE • Prototype foundation • Use synthetic or authorized data for testing.")
