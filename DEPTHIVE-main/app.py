import os, io, sqlite3, hashlib, secrets, html
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

# DEPTHIVE | Student & Department Intelligence prototype
# Run: streamlit run app.py

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "depthive_data.db"
UPLOAD_DIR = APP_DIR / "depthive_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="DEPTHIVE | College Intelligence", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&family=Caveat:wght@500;600;700&display=swap');
:root{--ink:#2c332b;--muted:#73796d;--line:#e5e2d7;--sage:#66816a;--sage-dark:#3f5b45;--terracotta:#c4775b;--gold:#c5a15a;--lavender:#9585b4;--paper:#fbf8ef;--card:#fffdf7;}
.stApp{background:radial-gradient(ellipse at 90% 0%,rgba(197,161,90,.17),transparent 30%),radial-gradient(ellipse at 5% 25%,rgba(102,129,106,.13),transparent 28%),linear-gradient(135deg,#f5f1e6 0%,#f8f5ec 48%,#f0eee3 100%);font-family:'DM Sans',sans-serif;color:var(--ink)}
.block-container{max-width:1520px;padding:1.65rem 2.2rem 3rem}
h1,h2,h3{font-family:'Caveat','Playfair Display',cursive!important;letter-spacing:0!important;color:var(--ink)!important}
h1{font-size:clamp(2.8rem,4.2vw,4rem)!important;line-height:1.02!important;font-weight:700!important}
h2{font-size:2.25rem!important;font-weight:700!important}h3{font-size:1.75rem!important;font-weight:700!important}
.hero h1{font-family:'Caveat','Playfair Display',cursive!important;font-weight:700!important;color:#3f5b45!important}
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3{ text-wrap:balance }
p,li{line-height:1.7}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#eee9dc 0%,#e4e7d9 55%,#e9e0d4 100%);border-right:1px solid #d8d9cb}
[data-testid="stSidebar"]>div:first-child{padding-top:1.35rem}
[data-testid="stSidebar"] [data-testid="stRadio"] label{color:#384639!important;font-weight:650!important;border-radius:10px;padding:.2rem .3rem}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"]{color:#365a40!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,#fffdf7,#f4f0e5);border:1px solid #e2ddce;border-radius:19px;padding:1rem 1.05rem;box-shadow:0 9px 24px rgba(68,76,54,.07);height:100%;min-width:0;transition:transform .18s ease,box-shadow .18s ease}
[data-testid="stMetric"]:hover{transform:translateY(-2px);box-shadow:0 13px 28px rgba(68,76,54,.11)}
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] p{color:#73796d!important;font-size:.82rem!important;font-weight:700!important;white-space:normal!important;overflow-wrap:anywhere!important}
[data-testid="stMetricValue"]{color:#3f5b45!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:800!important;font-size:clamp(1.2rem,2vw,1.85rem)!important;overflow-wrap:anywhere}
[data-testid="stMetricDelta"]{white-space:normal!important}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{border-radius:12px;border:1px solid #56745b;background:linear-gradient(115deg,#48694e,#77916d);color:#fffdf7!important;font-weight:750;min-height:2.8rem;box-shadow:0 7px 18px rgba(63,91,69,.18);transition:all .18s ease}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{border-color:#3f5b45;transform:translateY(-2px);box-shadow:0 11px 24px rgba(63,91,69,.25)}
.stTextInput label,.stTextArea label,.stNumberInput label,.stSelectbox label,.stMultiSelect label,.stFileUploader label,.stRadio label,.stCheckbox label,.stDateInput label,.stTimeInput label{color:#465344!important;font-weight:700!important;font-size:.9rem!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{border-radius:12px!important;background:#fffdf8!important;color:var(--ink)!important;border:1px solid #dcd8ca!important;min-height:2.75rem}
.stTextInput input:focus,.stTextArea textarea:focus,.stNumberInput input:focus{border-color:#7e9a7d!important;box-shadow:0 0 0 3px #66816a24!important}
[data-baseweb="select"]>div{border-radius:12px!important;background:#fffdf8!important;border-color:#dcd8ca!important;color:var(--ink)!important;min-height:2.75rem}
[data-testid="stFileUploader"]{background:linear-gradient(135deg,#fffdf7,#f0eee2);border:1.5px dashed #9eaa8f;border-radius:17px;padding:.8rem}
[data-testid="stFileUploaderDropzone"]{background:transparent!important}
[data-testid="stDataFrame"],[data-testid="stTable"]{border:1px solid #e2ddce;border-radius:15px;overflow:hidden;background:#fffdf7}
[data-testid="stExpander"]{background:rgba(255,253,247,.88);border:1px solid #e2ddce;border-radius:15px}
[data-testid="stTabs"] button{font-weight:750!important;color:#73796d!important}
[data-testid="stTabs"] button[aria-selected="true"]{color:#3f5b45!important;border-bottom-color:#66816a!important}
[data-testid="stAlert"]{border-radius:14px}
.hero{padding:1.8rem 2rem;border:1px solid #ded9c8;border-radius:25px;background:linear-gradient(115deg,#fffdf6 0%,#f1efe2 58%,#e7eadc 100%);box-shadow:0 16px 42px rgba(65,73,52,.09);margin:.3rem 0 1.45rem}
.eyebrow{font-size:.72rem;font-weight:850;letter-spacing:.18em;text-transform:uppercase;color:#66816a;margin-bottom:.6rem}
.hero p{color:#73796d;max-width:850px;line-height:1.75;margin-bottom:0}
.brand{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.05rem;font-weight:850;letter-spacing:.15em;color:#344b37;display:flex;align-items:center}.brand span{display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#496b50,#8b9b73);color:#fffdf7;width:40px;height:40px;border-radius:13px;margin-right:11px;box-shadow:0 7px 16px #3f5b452e}
.section-note{color:#73796d;font-size:.92rem;line-height:1.65;margin-top:-.35rem;margin-bottom:1.1rem}
.small-label{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;font-weight:850;color:#8a7857}
.insight{border:1px solid #e2ddce;background:linear-gradient(145deg,#fffdf7,#f4f0e5);padding:1.15rem 1.2rem;border-radius:18px;height:100%;box-shadow:0 8px 24px rgba(68,76,54,.05)}
.insight b{display:block;margin-bottom:.4rem;color:#3f5b45;font-family:'Plus Jakarta Sans',sans-serif}.insight p{color:#73796d;font-size:.9rem;line-height:1.6;margin:0}
.auth-panel{background:rgba(255,253,247,.94);border:1px solid #e0dac9;border-radius:27px;padding:1.65rem 1.7rem;box-shadow:0 24px 65px rgba(57,66,45,.13);margin-top:1rem;backdrop-filter:blur(12px)}
.auth-title{font-family:'Playfair Display',serif;font-size:2.15rem;font-weight:700;letter-spacing:-.035em;color:#344b37;margin:.2rem 0 .45rem;line-height:1.12}
.auth-subtitle{color:#73796d;font-size:.95rem;line-height:1.7;margin-bottom:1.25rem}
.auth-left{padding:2.6rem 1rem 1rem .3rem}
.auth-pill{display:inline-block;padding:.48rem .75rem;border:1px solid #dcdcc9;background:#f8f5eb;border-radius:999px;color:#4f6b50;font-size:.75rem;font-weight:800;letter-spacing:.04em}
.auth-visual{position:relative;overflow:hidden;padding:1.2rem 1.3rem;border-radius:20px;background:linear-gradient(130deg,#e3e8d8,#f5e8d9 72%,#eee5d8);border:1px solid #ddd8c8;margin:1.25rem 0}
.auth-visual .orb{display:inline-block;width:11px;height:11px;border-radius:50%;background:#c4775b;margin-right:7px;box-shadow:18px 0 0 #c5a15a,36px 0 0 #66816a}
.auth-visual .visual-title{font-family:'Playfair Display',serif;font-size:1.35rem;color:#3f5b45;font-weight:700;margin:1rem 0 .35rem}
.auth-visual .visual-copy{color:#6d7567;font-size:.9rem;line-height:1.6}
hr{border-color:#e1ddcf!important}
.stApp,.stApp p,.stApp li,.stApp span,.stApp label,.stApp small,[data-testid="stMarkdownContainer"],[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] span,[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{color:#354033}
.stApp [data-testid="stCaptionContainer"],.stApp [data-testid="stCaptionContainer"] p{color:#73796d!important}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,[data-testid="stSidebar"] label,[data-testid="stSidebar"] small,[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *{color:#384639!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label,[data-testid="stSidebar"] [data-testid="stRadio"] label p,[data-testid="stRadio"] label,[data-testid="stRadio"] label p,[data-testid="stRadio"] [data-testid="stMarkdownContainer"]{color:#384639!important;opacity:1!important}
[data-testid="stRadio"] [role="radio"] + div,[data-testid="stRadio"] [role="radio"] + div p,[data-testid="stWidgetLabel"] p,[data-testid="stWidgetLabel"] span{color:#465344!important}
.auth-panel{color:#354033!important}.auth-panel .auth-title{color:#344b37!important}.auth-panel .auth-subtitle,.auth-panel .eyebrow{color:#66816a!important}
.auth-panel [data-testid="stRadio"] label,.auth-panel [data-testid="stRadio"] label p,.auth-panel [data-testid="stTextInput"] label,.auth-panel [data-testid="stSelectbox"] label{color:#465344!important;opacity:1!important}
.stApp [data-testid="stAlert"] p,.stApp [data-testid="stAlert"] span{color:inherit!important}
/* colorful Streamlit chart surfaces and badges */
[data-testid="stVegaLiteChart"],[data-testid="stArrowVegaLiteChart"],[data-testid="stPlotlyChart"]{background:linear-gradient(145deg,#fffdf8,#f1eee2);border:1px solid #e4dfd1;border-radius:18px;padding:.45rem;box-shadow:0 8px 22px rgba(68,76,54,.05)}
[data-testid="stMarkdownContainer"] code{background:#e8ecdf;color:#3f5b45;border-radius:6px;padding:.12rem .35rem}
/* Friendly drag-and-drop upload zone */
[data-testid="stFileUploader"]{background:linear-gradient(135deg,#fffaf0 0%,#f0f2e6 52%,#f7e9df 100%)!important;border:1px solid #d9d8c7!important;border-radius:20px!important;padding:1rem!important;box-shadow:0 8px 22px rgba(68,76,54,.06)!important}
[data-testid="stFileUploaderDropzone"]{border:2px dashed #91a58a!important;border-radius:15px!important;background:rgba(255,253,247,.72)!important;min-height:120px!important;transition:all .2s ease}
[data-testid="stFileUploaderDropzone"]:hover{border-color:#bd8064!important;background:#fbf1e8!important}
[data-testid="stFileUploaderDropzone"] button{border-radius:10px!important;background:#e3eadc!important;color:#3f5b45!important;border:1px solid #cbd7c5!important;font-weight:750!important}
[data-testid="stFileUploaderDropzoneInstructions"]{font-weight:650!important;color:#52634d!important}
[data-testid="stSidebar"] [data-testid="stImage"] img{border-radius:50%!important;border:3px solid #fffaf0!important;box-shadow:0 5px 18px rgba(63,91,69,.18)!important;object-fit:cover!important}
.account-greeting{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.08rem;font-weight:800;color:#344b37;line-height:1.35;margin:.35rem 0 .25rem;overflow-wrap:anywhere}
.account-role{font-size:.78rem;color:#73796d;font-weight:650;line-height:1.5}
.account-chip{display:inline-block;background:#e4ebdc;border:1px solid #d2ddc9;color:#3f5b45;padding:.25rem .55rem;border-radius:999px;font-size:.72rem;font-weight:800;margin-top:.35rem}
.stFileUploader small{font-weight:600!important}
@media(max-width:900px){.block-container{padding:1rem}.hero{padding:1.2rem}.auth-left{padding:1rem .2rem}.auth-panel{padding:1.2rem;margin-top:.3rem}.auth-title{font-size:1.8rem}}

/* Auth form surface: style Streamlit's real widgets instead of an empty split HTML wrapper. */
[data-testid="stForm"]{background:rgba(255,253,247,.94);border:1px solid #e0dac9;border-radius:20px;padding:1rem 1.05rem;box-shadow:0 12px 35px rgba(57,66,45,.08)}
[data-testid="stFormSubmitButton"] button{width:100%}

</style>
""", unsafe_allow_html=True)

# ---------- persistence ----------
def conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL,
            department TEXT DEFAULT '', academic_year INTEGER DEFAULT 0, approved INTEGER DEFAULT 1,
            created_at TEXT NOT NULL, avatar_path TEXT DEFAULT '')""")
        c.execute("""CREATE TABLE IF NOT EXISTS student_profiles(
            user_id INTEGER PRIMARY KEY, student_id TEXT, department TEXT, academic_year INTEGER,
            semester TEXT, cgpa REAL, attendance REAL, skills TEXT, projects TEXT, career_goal TEXT,
            updated_at TEXT, FOREIGN KEY(user_id) REFERENCES users(id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS uploads(
            id INTEGER PRIMARY KEY AUTOINCREMENT, uploader_id INTEGER, category TEXT, department TEXT,
            academic_year INTEGER, file_name TEXT, stored_path TEXT, uploaded_at TEXT, notes TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS audit_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, action TEXT, detail TEXT, created_at TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS approval_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT, approved_user_id INTEGER NOT NULL,
            approved_by_user_id INTEGER NOT NULL, approved_user_name TEXT NOT NULL,
            approved_user_email TEXT NOT NULL, approved_role TEXT NOT NULL,
            department TEXT DEFAULT '', approved_at TEXT NOT NULL)""")
        # Safe migration for databases created before profile photos were supported.
        user_columns = {row[1] for row in c.execute("PRAGMA table_info(users)").fetchall()}
        if "avatar_path" not in user_columns:
            c.execute("ALTER TABLE users ADD COLUMN avatar_path TEXT DEFAULT ''")

def password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 180000).hex()

def log_action(user_id, action, detail=""):
    with conn() as c:
        c.execute("INSERT INTO audit_log(user_id,action,detail,created_at) VALUES(?,?,?,?)", (user_id, action, detail[:500], datetime.now().isoformat(timespec="seconds")))

def register_user(name, email, password, role, department="", academic_year=0):
    salt = secrets.token_hex(16)
    # Local prototype bootstrap: allow the first College Admin even if a student account was created first.
    # Once an admin exists, additional staff/admin accounts require approval.
    with conn() as c:
        admin_count = c.execute("SELECT COUNT(*) FROM users WHERE role='College Admin' AND approved=1").fetchone()[0]
    approved = 1 if role == "Student" or (role == "College Admin" and admin_count == 0) else 0
    try:
        with conn() as c:
            c.execute("INSERT INTO users(full_name,email,salt,password_hash,role,department,academic_year,approved,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
                      (name.strip(), email.strip().lower(), salt, password_hash(password, salt), role, department.strip(), int(academic_year or 0), approved, datetime.now().isoformat(timespec="seconds")))
        return True, "Account created. Staff accounts require approval by an administrator."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

def authenticate(email, password):
    with conn() as c:
        row = c.execute("SELECT * FROM users WHERE email=?", (email.strip().lower(),)).fetchone()
    if not row or password_hash(password, row["salt"]) != row["password_hash"]:
        return None
    return dict(row)

def save_profile(user_id, values):
    with conn() as c:
        c.execute("""INSERT INTO student_profiles(user_id,student_id,department,academic_year,semester,cgpa,attendance,skills,projects,career_goal,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET student_id=excluded.student_id,department=excluded.department,
        academic_year=excluded.academic_year,semester=excluded.semester,cgpa=excluded.cgpa,attendance=excluded.attendance,
        skills=excluded.skills,projects=excluded.projects,career_goal=excluded.career_goal,updated_at=excluded.updated_at""",
        (user_id, values["student_id"], values["department"], values["academic_year"], values["semester"], values["cgpa"], values["attendance"], values["skills"], values["projects"], values["career_goal"], datetime.now().isoformat(timespec="seconds")))

def get_profile(user_id):
    with conn() as c:
        row = c.execute("SELECT * FROM student_profiles WHERE user_id=?", (user_id,)).fetchone()
    return dict(row) if row else None

def save_upload(uploaded_file, category, user, department="", academic_year=0, notes=""):
    safe_name = Path(uploaded_file.name).name.replace("..", "_")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    stored = UPLOAD_DIR / f"{stamp}_{safe_name}"
    stored.write_bytes(uploaded_file.getvalue())
    with conn() as c:
        c.execute("INSERT INTO uploads(uploader_id,category,department,academic_year,file_name,stored_path,uploaded_at,notes) VALUES(?,?,?,?,?,?,?,?)",
                  (user["id"], category, department or user.get("department", ""), int(academic_year or user.get("academic_year", 0) or 0), safe_name, str(stored), datetime.now().isoformat(timespec="seconds"), notes[:500]))
    log_action(user["id"], "UPLOAD", f"{category}: {safe_name}")

def list_uploads(category=None, department=None):
    sql = "SELECT * FROM uploads WHERE 1=1"
    args = []
    if category:
        sql += " AND category=?"; args.append(category)
    if department:
        sql += " AND department=?"; args.append(department)
    sql += " ORDER BY uploaded_at DESC"
    with conn() as c:
        rows = c.execute(sql, args).fetchall()
    return [dict(r) for r in rows]

def read_tabular_upload(row):
    p = Path(row["stored_path"])
    if not p.exists():
        raise FileNotFoundError("Stored file not found")
    suffix = p.suffix.lower()
    if suffix == ".csv": return pd.read_csv(p)
    if suffix in (".xlsx", ".xls"): return pd.read_excel(p)
    raise ValueError("This file is not a CSV or Excel data file")

def save_avatar(uploaded_file, user):
    """Store a validated image as the signed-in user's profile photo."""
    from PIL import Image
    import io as _io
    raw = uploaded_file.getvalue()
    image = Image.open(_io.BytesIO(raw))
    image.verify()
    image = Image.open(_io.BytesIO(raw)).convert("RGB")
    # Re-encode to JPEG so the stored file is safe and consistently viewable.
    out = _io.BytesIO()
    image.thumbnail((700, 700))
    image.save(out, format="JPEG", quality=88, optimize=True)
    stored = UPLOAD_DIR / f"profile_{int(user['id'])}.jpg"
    stored.write_bytes(out.getvalue())
    with conn() as c:
        c.execute("UPDATE users SET avatar_path=? WHERE id=?", (str(stored), user["id"]))
    user["avatar_path"] = str(stored)
    st.session_state.user = user

init_db()

# ---------- analytics ----------
ALIASES = {
    "student_id": ["student_id", "student id", "enrollment_no", "enrollment number", "roll_no", "roll number", "id"],
    "student_name": ["student_name", "student name", "full_name", "full name", "name", "student"],
    "department": ["department", "dept", "branch"],
    "year": ["academic_year", "year", "study_year", "year_of_study"],
    "cgpa": ["cgpa", "c.g.p.a", "overall_cgpa"],
    "attendance": ["attendance", "attendance_percent", "attendance_percentage", "attendance %"],
    "backlogs": ["backlogs", "active_backlogs", "backlog_count"],
    "sgpa": ["sgpa", "semester_gpa"],
    "internship_status": ["internship_status", "internship", "internship status"],
    "placement_status": ["placement_status", "placement", "placement status"],
    "eligible": ["eligible_for_placement", "placement_eligible", "eligible"],
    "package": ["package_lpa", "package", "ctc_lpa", "salary_lpa"]
}

def norm(s): return "".join(ch.lower() if ch.isalnum() else "_" for ch in str(s)).strip("_")
def normalize_columns(df):
    out = df.copy()
    mapping = {}
    normalized = {norm(c): c for c in out.columns}
    for canonical, aliases in ALIASES.items():
        for alias in aliases:
            if norm(alias) in normalized:
                mapping[normalized[norm(alias)]] = canonical
                break
    return out.rename(columns=mapping)

def numeric(df, col):
    if col not in df.columns: return pd.Series(index=df.index, dtype="float64")
    return pd.to_numeric(df[col].astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False), errors="coerce")

def safe_pct(n, d): return round(float(n) / float(d) * 100, 1) if d and pd.notna(d) else None

def risk_analysis(df):
    """Transparent rule-based student risk. Placement/internship are used only for Year 4."""
    data = normalize_columns(df)
    if "student_id" not in data.columns:
        data["student_id"] = [f"ROW-{i+1}" for i in range(len(data))]
    if "department" not in data.columns: data["department"] = "Unspecified"
    if "year" not in data.columns: data["year"] = 0
    data["year"] = numeric(data, "year").fillna(0).astype(int)
    for col in ["cgpa", "attendance", "backlogs"]: data[col] = numeric(data, col)
    records = []
    for _, r in data.iterrows():
        score, factors = 0, []
        year = int(r.get("year", 0) or 0)
        cgpa = r.get("cgpa"); attendance = r.get("attendance"); backlogs = r.get("backlogs")
        if pd.notna(cgpa):
            if cgpa < 5.0: score += 35; factors.append("CGPA below 5.0")
            elif cgpa < 6.0: score += 22; factors.append("CGPA below 6.0")
            elif cgpa < 7.0: score += 10; factors.append("CGPA below 7.0")
        if pd.notna(attendance):
            if attendance < 60: score += 30; factors.append("Attendance below 60%")
            elif attendance < 75: score += 18; factors.append("Attendance below 75%")
        if pd.notna(backlogs):
            if backlogs >= 3: score += 30; factors.append("3 or more active backlogs")
            elif backlogs >= 1: score += 18; factors.append("Active backlog(s)")
        if year == 4:
            ist = str(r.get("internship_status", "")).strip().lower()
            if ist in {"not started", "not_started", "none", "no", "pending"}:
                score += 15; factors.append("Internship not started (Year 4 rule)")
            pst = str(r.get("placement_status", "")).strip().lower()
            elig = str(r.get("eligible", "")).strip().lower()
            is_eligible = elig in {"yes", "true", "1", "eligible", "y"}
            is_unplaced = pst in {"unplaced", "seeking", "not placed", "not_placed", "no offer", "no_offer"}
            if is_eligible and is_unplaced:
                score += 20; factors.append("Eligible but not placed yet")
        score = min(score, 100)
        level = "High" if score >= 55 else "Moderate" if score >= 25 else "Low"
        records.append({"Student ID": str(r.get("student_id", "")), "Department": r.get("department", "Unspecified"), "Year": year if year else "Not set", "CGPA": round(cgpa, 2) if pd.notna(cgpa) else None, "Attendance %": round(attendance, 1) if pd.notna(attendance) else None, "Active Backlogs": int(backlogs) if pd.notna(backlogs) else None, "Risk Score": score, "Risk Level": level, "Risk Factors": "; ".join(factors) if factors else "No configured risk trigger detected"})
    return pd.DataFrame(records)

def placement_summary(df):
    data = normalize_columns(df)
    if "department" not in data.columns: return pd.DataFrame(), "Dataset needs a Department column."
    if "year" in data.columns:
        data["year"] = numeric(data, "year")
        data = data[data["year"] == 4]
    if "student_id" not in data.columns: return pd.DataFrame(), "Dataset needs a Student_ID column to avoid counting duplicate offers as multiple students."
    if "eligible" in data.columns:
        data["eligible_flag"] = data["eligible"].astype(str).str.lower().isin(["yes", "true", "1", "eligible", "y"])
    else:
        data["eligible_flag"] = True
    if "placement_status" in data.columns:
        data["placed_flag"] = data["placement_status"].astype(str).str.lower().isin(["placed", "offer received", "offer_received", "accepted", "yes"])
    else:
        data["placed_flag"] = False
    # One student counted once; a verified placement flag is enough to count as placed.
    # Compute unique student counts per department so multiple offers do not inflate placement rates.
    rows = []
    for dept, g in data.groupby("department", dropna=False):
        eligible_ids = g.loc[g["eligible_flag"], "student_id"].astype(str).nunique()
        placed_ids = g.loc[g["placed_flag"], "student_id"].astype(str).nunique()
        row = {"Department": str(dept), "Eligible Students": eligible_ids, "Placed Students": placed_ids, "Placement Rate %": safe_pct(placed_ids, eligible_ids)}
        if "internship_status" in g.columns:
            complete = g["internship_status"].astype(str).str.lower().isin(["completed", "complete", "yes", "verified"])
            row["Internship Completed"] = g.loc[complete, "student_id"].astype(str).nunique()
            row["Internship Rate %"] = safe_pct(row["Internship Completed"], g["student_id"].astype(str).nunique())
        if "package" in g.columns:
            g["package_num"] = numeric(g, "package")
            vals = g.loc[g["placed_flag"], ["student_id", "package_num"]].dropna().drop_duplicates("student_id")["package_num"]
            row["Median Package (LPA)"] = round(float(vals.median()), 2) if not vals.empty else None
            row["Highest Package (LPA)"] = round(float(vals.max()), 2) if not vals.empty else None
        rows.append(row)
    return pd.DataFrame(rows).sort_values("Placement Rate %", ascending=False, na_position="last"), None

def data_quality(df):
    return {"rows": len(df), "columns": len(df.columns), "missing": int(df.isna().sum().sum()), "duplicates": int(df.duplicated().sum()), "duplicate_ids": int(df["Student_ID"].duplicated().sum()) if "Student_ID" in df.columns else None}

def hero(kicker, title, desc):
    st.markdown(f'<div class="hero"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p>{desc}</p></div>', unsafe_allow_html=True)

def narrative_health(avg_cgpa=None, avg_attendance=None, high_risk_pct=None, placement_rate=None):
    """Generate a cautious plain-language summary from available, measured indicators."""
    parts=[]
    if avg_cgpa is not None and pd.notna(avg_cgpa):
        parts.append(f"average CGPA is {avg_cgpa:.2f}/10")
    if avg_attendance is not None and pd.notna(avg_attendance):
        parts.append(f"average attendance is {avg_attendance:.1f}%")
    if high_risk_pct is not None and pd.notna(high_risk_pct):
        parts.append(f"{high_risk_pct:.1f}% of reviewed students fall in the configured high-risk band")
    if placement_rate is not None and pd.notna(placement_rate):
        parts.append(f"verified placement rate is {placement_rate:.1f}% among eligible students")
    if not parts:
        return "Not enough validated data is available to summarize performance yet. Upload and verify the relevant records first."
    summary="Current indicators: " + "; ".join(parts) + "."
    if high_risk_pct is not None and pd.notna(high_risk_pct) and high_risk_pct >= 25:
        summary += " A relatively large share of students needs review; inspect the listed factors before deciding on interventions."
    elif avg_cgpa is not None and pd.notna(avg_cgpa) and avg_cgpa >= 7.5 and (high_risk_pct is None or pd.isna(high_risk_pct) or high_risk_pct < 10):
        summary += " Academic indicators look comparatively positive on the available measures. Keep monitoring cohort trends."
    else:
        summary += " Review the individual indicators and compare similar cohorts before labelling overall performance as good or risky."
    return summary

def copilot_reply(question, user, academic_df=None, placement_df=None):
    """Safe prototype assistant: answers common DEPTHIVE questions from available workspace data.
    Replace this retrieval/rule layer with a validated ML/LLM service for broader natural-language coverage.
    """
    q=question.strip().lower()
    role=user.get("role", "User")
    if not q:
        return "Ask about your dashboard, academic risk, department health, placement metrics, uploads or account permissions."
    if any(k in q for k in ["approve", "approval", "approved", "pending staff"]):
        if role != "College Admin": return "Staff approvals are managed by College Admin. Your account can only access the approval actions permitted for your role."
        with conn() as c:
            pending=c.execute("SELECT COUNT(*) FROM users WHERE approved=0").fetchone()[0]
            history=c.execute("SELECT COUNT(*) FROM approval_history").fetchone()[0]
        return f"There are {pending} account(s) awaiting approval and {history} recorded staff approval event(s). Open Access Approvals to review pending requests and approval history."
    if any(k in q for k in ["placement", "internship", "placed", "offer"]):
        if role not in ["College Admin", "Placement Cell", "Department / HOD"]:
            return "Placement and internship outcomes are department-managed and are not used as placement-risk indicators for Years 1–3. You can view your own profile and career-readiness guidance."
        if placement_df is None: return "No official placement file is available in this workspace yet. Ask the Placement Cell to upload the verified outcomes template."
        summary,err=placement_summary(placement_df)
        if err: return f"I found placement data, but it cannot be summarized yet: {err}"
        if summary.empty: return "No eligible Year 4 placement records were found in the current file. Check the graduating cohort and Year values."
        valid=summary.dropna(subset=["Placement Rate %"])
        if valid.empty: return "Placement data is present, but eligibility or placed-status values are not sufficient to calculate a rate."
        best=valid.sort_values("Placement Rate %",ascending=False).iloc[0]
        return f"Across the available Year 4 records, {best['Department']} has the highest calculated placement rate at {best['Placement Rate %']:.1f}%. This is based on uploaded data; verify cohort coverage and eligibility before comparing departments."
    if any(k in q for k in ["risk", "risky", "backlog", "attendance", "cgpa", "academic"]):
        if role == "Student":
            profile=get_profile(user["id"])
            if not profile: return "Complete My Profile & Progress first. Your personal indicators will then be calculated from the CGPA and attendance values you provide."
            bits=[]
            if profile.get("cgpa") is not None: bits.append(f"CGPA {profile['cgpa']:.2f}/10")
            if profile.get("attendance") is not None: bits.append(f"attendance {profile['attendance']:.1f}%")
            return "Your saved profile currently shows " + (", ".join(bits) if bits else "no numeric academic indicators") + ". Open My Risk & Recommendations for configured signals and next steps. These are guidance indicators, not guaranteed predictions."
        if academic_df is None: return "No academic roster is available. Upload a validated Academic roster before asking for department or student risk summaries."
        ra=risk_analysis(combined_analysis_roster())
        if role in ["Faculty", "Department / HOD"] and user.get("department"):
            ra=ra[ra["Department"].astype(str).str.strip().str.casefold()==user["department"].strip().casefold()]
        if ra.empty: return "No student records are available within your authorized workspace scope."
        high=int((ra["Risk Level"]=="High").sum()); mod=int((ra["Risk Level"]=="Moderate").sum()); low=int((ra["Risk Level"]=="Low").sum())
        return f"In your accessible roster, {len(ra)} student record(s) were reviewed: {high} high, {mod} moderate and {low} low under the current rule thresholds. Review the contributing factors in Student Risk Review; these thresholds need validation and are not a trained predictive model."
    if any(k in q for k in ["department", "which is doing good", "best department", "department health"]):
        if role == "Student": return "Department-level comparisons are restricted to authorized staff. You can review your own progress and recommendations."
        if academic_df is None: return "Upload an academic roster with Department, Year and academic measures to generate department comparisons."
        d=normalize_columns(academic_df)
        if "department" not in d.columns or "cgpa" not in d.columns: return "The current roster needs Department and CGPA columns before academic department comparison is possible."
        d["cgpa"]=numeric(d,"cgpa")
        sums=d.groupby("department")["cgpa"].mean().dropna().sort_values(ascending=False)
        if sums.empty: return "CGPA values are missing or not numeric, so I cannot rank departments yet."
        return f"By average CGPA only, {sums.index[0]} is currently highest at {sums.iloc[0]:.2f}/10 in the uploaded roster. This is not an overall department ranking; review attendance, backlogs and cohort comparability too."
    if any(k in q for k in ["upload", "file", "csv", "excel", "drag", "template"]):
        return "Use Academic Data Hub for the academic roster and Placement & Internship Data for official placement outcomes. Both support drag-and-drop CSV/Excel uploads, previews and templates. Student documents are uploaded separately in My Documents."
    if any(k in q for k in ["scorecard", "score card", "chart", "report"]):
        return "Open Overview for role-specific metrics, and the relevant analysis workspace for charts and detailed scorecards. The summary uses available uploaded records only; missing data is not treated as poor performance."
    return "I can currently answer common questions about DEPTHIVE navigation, approvals, academic risk, department comparisons, uploads and placement summaries. This prototype does not yet have a trained ML model or unrestricted natural-language reasoning. A trained model should be added only after curating and evaluating a safe, role-aware question/answer dataset."

def can_access(user, roles): return user.get("role") in roles and bool(user.get("approved", 0))

# ---------- authentication ----------
if "user" not in st.session_state: st.session_state.user = None
user = st.session_state.user

if not user:
    left, right = st.columns([1.08, .92], gap="large", vertical_alignment="center")
    with left:
        st.markdown('''<div class="auth-left">
          <div class="brand"><span>◈</span>DEPTHIVE</div>
          <div class="eyebrow" style="margin-top:2.3rem">COLLEGE INTELLIGENCE PLATFORM</div>
          <h1 style="margin:.55rem 0 1rem">From student data<br>to smarter decisions.</h1>
          <p style="color:#69758d;line-height:1.85;max-width:600px;font-size:1.03rem">A connected workspace for student progress, department health, academic risk and verified placement outcomes.</p>
          <div style="display:flex;flex-wrap:wrap;gap:.55rem;margin:1.35rem 0 1.25rem">
            <span class="auth-pill">Student success</span><span class="auth-pill">Department insights</span><span class="auth-pill">Evidence-led decisions</span>
          </div>
          <div class="auth-visual">
            <span class="orb"></span>
            <div class="visual-title">Clarity behind every decision.</div>
            <div class="visual-copy">One considered workspace for academic progress, student support and institutional insight — built around evidence, not assumptions.</div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:1rem">
              <span style="background:#fffdf6;border:1px solid #dedbcb;border-radius:10px;padding:.48rem .65rem;color:#49664b;font-size:.78rem;font-weight:750">01 · Progress</span>
              <span style="background:#fffdf6;border:1px solid #dedbcb;border-radius:10px;padding:.48rem .65rem;color:#a4664e;font-size:.78rem;font-weight:750">02 · Insight</span>
              <span style="background:#fffdf6;border:1px solid #dedbcb;border-radius:10px;padding:.48rem .65rem;color:#8a7446;font-size:.78rem;font-weight:750">03 · Action</span>
            </div>
          </div>
        </div>''', unsafe_allow_html=True)
        a,b,c = st.columns(3, gap="small")
        with a: st.markdown('<div class="insight"><b>Student view</b><p>Personal progress and guidance.</p></div>', unsafe_allow_html=True)
        with b: st.markdown('<div class="insight"><b>Department view</b><p>Compare academic health.</p></div>', unsafe_allow_html=True)
        with c: st.markdown('<div class="insight"><b>Year-aware risks</b><p>Relevant signals only.</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="eyebrow">YOUR CAMPUS, IN FOCUS</div><div class="auth-title">Welcome back.</div><div class="auth-subtitle">Sign in to your DEPTHIVE workspace, or create an account to get started.</div>', unsafe_allow_html=True)
        mode = st.radio("Choose an option", ["Sign in", "Create account"], horizontal=True, label_visibility="visible", key="auth_mode")
        st.caption("Students, Department / HOD, Faculty, Placement Cell and College Admin all use this same sign-in form. Your account role determines which workspace opens.")
        if mode == "Sign in":
            with st.form("login", clear_on_submit=False):
                email = st.text_input("Email address", placeholder="you@college.edu", autocomplete="email")
                password = st.text_input("Password", type="password", placeholder="Enter your password", autocomplete="current-password")
                submit = st.form_submit_button("Sign in →", width="stretch")
            if submit:
                found = authenticate(email, password)
                if not found: st.error("Email or password is incorrect.")
                elif not found["approved"]: st.warning("This staff account is awaiting admin approval. Ask your college administrator to approve it.")
                else:
                    st.session_state.user = found; st.rerun()
        else:
            with st.form("signup", clear_on_submit=False):
                name = st.text_input("Full name", placeholder="Your full name")
                email = st.text_input("Email address", placeholder="you@college.edu", autocomplete="email")
                role = st.selectbox("Account type", ["Student", "Faculty", "Department / HOD", "Placement Cell", "College Admin"])
                dept = st.text_input("Department / Branch", placeholder="e.g. CSE-DS", help="Required for department staff so records can be scoped to the right department.")
                year = st.selectbox("Current year (students only)", [1,2,3,4], index=2) if role == "Student" else 0
                if role == "Student":
                    st.info("Student accounts are activated immediately. Sign in with the email and password you create.")
                elif role == "College Admin":
                    st.warning("The first account created in a fresh database becomes the initial admin. Later admin accounts require approval.")
                else:
                    st.info("Department / HOD, Faculty and Placement Cell accounts require approval by the College Admin before sign-in is enabled.")
                password = st.text_input("Password (minimum 10 characters)", type="password", placeholder="Create a strong password", autocomplete="new-password")
                confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter password", autocomplete="new-password")
                submit = st.form_submit_button("Create account →", width="stretch")
            if submit:
                needs_department = role in ["Faculty", "Department / HOD", "Placement Cell"]
                if (not name.strip() or "@" not in email or len(password) < 10 or password != confirm
                        or (needs_department and not dept.strip())):
                    st.error("Enter your name and a valid email, use at least 10 characters for the password, ensure both passwords match, and provide a department for staff roles.")
                else:
                    ok, msg = register_user(name, email, password, role, dept, year)
                    if ok:
                        st.success(msg)
                        if role != "Student": st.info("Staff roles stay locked until an approved administrator grants access.")
                    else: st.error(msg)
    st.stop()

# ---------- app shell ----------
with st.sidebar:
    st.markdown('<div class="brand"><span>◈</span>DEPTHIVE</div>', unsafe_allow_html=True)
    st.caption("College intelligence workspace")
    st.markdown("---")
    # Refresh the profile photo path from the database in case it was added earlier.
    with conn() as _c:
        _urow = _c.execute("SELECT avatar_path FROM users WHERE id=?", (user["id"],)).fetchone()
    _avatar_path = (_urow["avatar_path"] if _urow else "") or user.get("avatar_path", "")
    user["avatar_path"] = _avatar_path
    if _avatar_path and Path(_avatar_path).exists():
        st.image(_avatar_path, width=92)
    else:
        _initials = "".join(part[0] for part in user["full_name"].split()[:2]).upper() or "U"
        st.markdown(f'<div style="width:76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#dce8d4,#f2d9c8);border:3px solid #fffaf0;color:#3f5b45;font-size:1.45rem;font-weight:850;box-shadow:0 5px 18px #3f5b4522">{html.escape(_initials)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="account-greeting">Hi, {html.escape(user["full_name"])}</div><div class="account-role">{html.escape(user["role"])} · {html.escape(user.get("department") or "Department not set")}</div><span class="account-chip">SIGNED IN</span>', unsafe_allow_html=True)
    with st.expander("Update profile photo", expanded=False):
        photo = st.file_uploader("Choose a profile picture", type=["png", "jpg", "jpeg", "webp"], key="profile_photo_upload", help="Use a clear square photo for the best result.")
        if photo is not None:
            if st.button("Save profile picture", key="save_profile_photo", width="stretch"):
                try:
                    save_avatar(photo, user)
                    st.success("Profile picture updated.")
                    st.rerun()
                except Exception:
                    st.error("Could not use this image. Please choose a valid PNG, JPG or WEBP image.")
    if not user.get("approved"):
        st.error("Account awaiting approval")
        if st.button("Sign out"): st.session_state.user = None; st.rerun()
        st.stop()
    common = ["Overview"]
    if user["role"] == "Student":
        pages = common + ["My Profile & Progress", "My Documents", "My Risk & Recommendations", "Department Leaderboard", "DEPTHIVE Copilot"]
    elif user["role"] == "Faculty":
        pages = common + ["Academic Data Hub", "Student Risk Review", "DEPTHIVE Copilot"]
    elif user["role"] == "Department / HOD":
        pages = common + ["Academic Data Hub", "Student Submissions", "Student Risk Review", "Department Intelligence", "DEPTHIVE Copilot"]
    elif user["role"] == "Placement Cell":
        pages = common + ["Placement & Internship Data", "Placement Intelligence", "DEPTHIVE Copilot"]
    else:
        pages = common + ["Academic Data Hub", "Student Submissions", "Student Risk Review", "Department Intelligence", "Placement & Internship Data", "Placement Intelligence", "Data Quality & Audit", "Access Approvals", "DEPTHIVE Copilot"]
    page = st.radio("WORKSPACE", pages, label_visibility="collapsed")
    st.markdown("---")
    st.caption("Prototype · Use authorized data only")
    if st.button("Sign out", width="stretch"):
        st.session_state.user = None; st.rerun()

# upload records for analysis
academic_uploads = list_uploads("Academic roster")
placement_uploads = list_uploads("Placement outcomes")

def latest_df(records):
    for record in records:
        try: return read_tabular_upload(record), record
        except Exception: continue
    return None, None

academic_df, academic_meta = latest_df(academic_uploads)
placement_df, placement_meta = latest_df(placement_uploads)

# Enforce department scoping in the UI data layer as well as navigation.
# College Admin can see institution-wide data; HOD/Faculty/Placement Cell see their assigned department.
if user.get("role") in ["Department / HOD", "Faculty", "Placement Cell"] and user.get("department"):
    scoped_department = str(user["department"]).strip().casefold()
    if academic_df is not None:
        _academic_norm = normalize_columns(academic_df)
        if "department" in _academic_norm.columns:
            academic_df = _academic_norm[_academic_norm["department"].astype(str).str.strip().str.casefold() == scoped_department].copy()
        else:
            academic_df = _academic_norm.iloc[0:0].copy()
    if placement_df is not None:
        _placement_norm = normalize_columns(placement_df)
        if "department" in _placement_norm.columns:
            placement_df = _placement_norm[_placement_norm["department"].astype(str).str.strip().str.casefold() == scoped_department].copy()
        else:
            placement_df = _placement_norm.iloc[0:0].copy()

def combined_analysis_roster():
    """Join official placement outcomes onto academic records by student ID.
    Only Year 4 rows use these fields in risk_analysis; earlier years ignore them.
    """
    if academic_df is None:
        return None
    base = normalize_columns(academic_df)
    if placement_df is None or "student_id" not in base.columns:
        return base
    career = normalize_columns(placement_df)
    if "student_id" not in career.columns:
        return base
    keep = [c for c in ["student_id", "internship_status", "placement_status", "eligible", "package"] if c in career.columns]
    if len(keep) <= 1:
        return base
    career = career[keep].copy()
    # One row per student for risk analysis; prevent duplicate offers from multiplying student records.
    career["student_id"] = career["student_id"].astype(str).str.strip()
    career = career.drop_duplicates("student_id", keep="last")
    base["student_id"] = base["student_id"].astype(str).str.strip()
    return base.merge(career, on="student_id", how="left", suffixes=("", "_placement"))

if page == "Overview":
    hero("WORKSPACE OVERVIEW", "A clearer picture of student success.", "A focused overview of academic health, student support signals and verified placement outcomes. Each area has its own workspace—no overloaded all-in-one page.")
    if user["role"] == "Student":
        profile = get_profile(user["id"])
        if profile:
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Current CGPA", f"{profile['cgpa']:.2f}" if profile["cgpa"] is not None else "Not added")
            c2.metric("Attendance", f"{profile['attendance']:.1f}%" if profile["attendance"] is not None else "Not added")
            c3.metric("Year", profile["academic_year"] or user.get("academic_year") or "Not set")
            c4.metric("Department", profile["department"] or user.get("department") or "Not set")
            st.markdown("### Your next steps")
            st.info("Keep your profile current. Official marks, attendance, internship and placement records should be verified by the college before they are used in institutional analysis.")
        else:
            st.info("Start by completing **My Profile & Progress**. You can add academic information and drag-and-drop supporting documents separately.")
        st.markdown("### Your workspace")
        x,y,z = st.columns(3)
        with x: st.markdown('<div class="insight"><b>My Profile & Progress</b><p>Enter your academic details and career goals.</p></div>', unsafe_allow_html=True)
        with y: st.markdown('<div class="insight"><b>My Documents</b><p>Upload marksheets, certificates and project evidence.</p></div>', unsafe_allow_html=True)
        with z: st.markdown('<div class="insight"><b>My Risk & Recommendations</b><p>See configured academic indicators and improvement steps.</p></div>', unsafe_allow_html=True)
    else:
        if academic_df is not None:
            q = data_quality(academic_df)
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Student records", f"{q['rows']:,}")
            c2.metric("Departments", int(normalize_columns(academic_df)["department"].nunique()) if "department" in normalize_columns(academic_df).columns else "—")
            c3.metric("Missing cells", f"{q['missing']:,}")
            c4.metric("Duplicate rows", f"{q['duplicates']:,}")
            st.markdown("### Academic health at a glance")
            ra = risk_analysis(combined_analysis_roster())
            l,r = st.columns([1.2,1])
            with l:
                st.markdown("**Student risk distribution**")
                st.bar_chart(ra["Risk Level"].value_counts().reindex(["Low","Moderate","High"], fill_value=0), color=["#66816a"])
            with r:
                st.markdown("**Department record coverage**")
                d = normalize_columns(academic_df)
                if "department" in d.columns: st.bar_chart(d["department"].value_counts(), color=["#c4775b"])
                else: st.info("Upload a dataset with a Department column to compare departments.")
        else:
            st.info("No academic roster uploaded yet. Open **Academic Data Hub** to drag and drop a CSV or Excel roster.")
        if placement_df is not None:
            st.markdown("### Latest verified placement snapshot")
            ps, err = placement_summary(placement_df)
            if err: st.warning(err)
            elif not ps.empty: st.dataframe(ps, width="stretch", hide_index=True)
        else:
            st.markdown('<div class="insight"><b>Placement data is separate</b><p>Placement and internship outcomes are uploaded by the Placement Cell / authorized department. They are not inferred from student self-reported data.</p></div>', unsafe_allow_html=True)

elif page == "My Profile & Progress":
    hero("STUDENT PORTAL", "Your progress, in one place.", "Add text-based details in the form. Use the separate document uploader for files such as marksheets and certificates.")
    profile = get_profile(user["id"]) or {}
    with st.form("student_profile_form"):
        c1,c2 = st.columns(2)
        with c1:
            student_id = st.text_input("Student ID / Enrollment number", value=profile.get("student_id") or "")
            dept = st.text_input("Department / Branch", value=profile.get("department") or user.get("department") or "")
            year = st.selectbox("Academic year", [1,2,3,4], index=max(0, min(3, int(profile.get("academic_year") or user.get("academic_year") or 1)-1)))
            semester = st.selectbox("Current semester", ["1","2","3","4","5","6","7","8"], index=0 if not profile.get("semester") else int(profile["semester"])-1)
        with c2:
            cgpa = st.number_input("Current CGPA (0–10)", min_value=0.0, max_value=10.0, value=float(profile.get("cgpa") or 0.0), step=.01)
            attendance = st.number_input("Attendance % (0–100)", min_value=0.0, max_value=100.0, value=float(profile.get("attendance") or 0.0), step=.5)
            skills = st.text_area("Skills (text)", value=profile.get("skills") or "", placeholder="Python, SQL, communication…")
            projects = st.text_area("Projects / certifications (text)", value=profile.get("projects") or "", placeholder="Project title, your contribution, certification…")
        career_goal = st.text_area("Career goals / areas to improve", value=profile.get("career_goal") or "")
        save = st.form_submit_button("Save profile", width="stretch")
    if save:
        if not student_id.strip() or not dept.strip(): st.error("Student ID and department are required.")
        else:
            save_profile(user["id"], {"student_id":student_id.strip(),"department":dept.strip(),"academic_year":year,"semester":semester,"cgpa":cgpa if cgpa else None,"attendance":attendance if attendance else None,"skills":skills,"projects":projects,"career_goal":career_goal})
            log_action(user["id"], "PROFILE_UPDATE", f"Student profile updated: {student_id}")
            st.success("Profile saved.")
    st.caption("Profile values are student-submitted. Official college records should be verified separately before institutional reporting.")

elif page == "My Documents":
    hero("STUDENT PORTAL", "Documents & evidence", "Drag and drop supporting documents here. Text fields stay in forms; files stay in the document library.")
    st.markdown("### Upload supporting files")
    files = st.file_uploader("Drag and drop your files here, or browse to upload", type=["pdf","png","jpg","jpeg","csv","xlsx","docx"], accept_multiple_files=True, help="Marksheets, certificates, project reports or other relevant evidence. Do not upload passwords, Aadhaar or unrelated sensitive documents.")
    category = st.selectbox("Document category", ["Marksheets / results", "Certificates", "Project evidence", "Resume", "Other supporting document"])
    notes = st.text_input("Short note (optional)")
    if st.button("Save uploaded documents", disabled=not files):
        profile_for_upload = get_profile(user["id"]) or {}
        student_department = str(profile_for_upload.get("department") or user.get("department") or "").strip()
        student_year = profile_for_upload.get("academic_year") or user.get("academic_year") or 0
        for f in files:
            save_upload(f, f"Student document: {category}", user, department=student_department, academic_year=student_year, notes=notes)
        st.success(f"Saved {len(files)} file(s). Your department can now see the submission if your profile has the correct department set.")
    mine = [u for u in list_uploads() if u["uploader_id"] == user["id"] and u["category"].startswith("Student document:")]
    st.markdown("### Your uploaded documents")
    if mine:
        st.dataframe(pd.DataFrame([{ "File":x["file_name"], "Category":x["category"].replace("Student document: ",""), "Uploaded":x["uploaded_at"], "Notes":x["notes"]} for x in mine]), width="stretch", hide_index=True)
    else: st.info("No documents uploaded yet.")

elif page == "My Risk & Recommendations":
    hero("STUDENT PORTAL", "My risk & improvement plan",
         "A transparent academic indicator based on the CGPA and attendance saved in your profile. This score is a guidance rule, not a prediction.")
    profile = get_profile(user["id"])
    if not profile:
        st.info("Complete your profile first to see your personal indicators.")
        if st.button("Open My Profile & Progress"):
            st.session_state["page"] = "My Profile & Progress"
            st.rerun()
    else:
        year = int(profile.get("academic_year") or user.get("academic_year") or 0)
        cgpa = pd.to_numeric(profile.get("cgpa"), errors="coerce")
        att = pd.to_numeric(profile.get("attendance"), errors="coerce")
        risk = 0
        factors = []

        if pd.notna(cgpa):
            if cgpa < 5:
                risk += 35
                factors.append("CGPA is below 5.0")
            elif cgpa < 6:
                risk += 22
                factors.append("CGPA is below 6.0")
            elif cgpa < 7:
                risk += 10
                factors.append("CGPA is below 7.0")
        if pd.notna(att):
            if att < 60:
                risk += 30
                factors.append("Attendance is below 60%")
            elif att < 75:
                risk += 18
                factors.append("Attendance is below 75%")

        risk = min(risk, 100)
        level = "High" if risk >= 55 else "Moderate" if risk >= 25 else "Low"

        st.markdown("### Your saved academic indicators")
        a, b, c = st.columns(3)
        a.metric("CGPA", f"{cgpa:.2f}" if pd.notna(cgpa) else "Not entered")
        b.metric("Attendance", f"{att:.1f}%" if pd.notna(att) else "Not entered")
        c.metric("Academic year", year if year else "Not set")

        st.markdown("### Current indicator")
        a, b = st.columns(2)
        a.metric("Configured risk score", f"{risk}/100")
        b.metric("Indicator level", level)

        if pd.isna(cgpa) and pd.isna(att):
            st.warning("Your profile does not contain a CGPA or attendance value yet, so this score cannot assess those indicators. Update your profile to get a meaningful result.")
        elif factors:
            st.markdown("### Signals to review")
            for factor in factors:
                st.warning(factor)
        else:
            st.success("Your saved CGPA and attendance do not cross this prototype's configured risk thresholds.")
            st.caption("A score of 0 means no configured trigger was detected in these two fields. It does not guarantee that there are no academic concerns.")

        st.markdown("### Suggested next steps")
        if pd.isna(cgpa):
            st.write("- Add your latest CGPA in My Profile & Progress.")
        elif cgpa < 7:
            st.write("- Meet your faculty mentor and make a subject-wise revision plan.")
        else:
            st.write("- Maintain your current CGPA and review subject-wise performance after each assessment.")
        if pd.isna(att):
            st.write("- Add your latest attendance percentage in My Profile & Progress.")
        elif att < 75:
            st.write("- Review attendance regularly and confirm the official record with your department.")
        else:
            st.write("- Keep checking attendance so it remains above your college's required minimum.")
        if year == 3:
            st.write("- Build projects, document your skills and practise aptitude if placement preparation is relevant to your goals. These are recommendations, not placement-risk signals.")
        elif year == 4:
            st.info("Official internship and placement status is managed by the department or Placement Cell, not taken from this student form.")

        st.caption("Scope: this personal indicator currently uses CGPA and attendance only. Backlogs are not assessed here unless added to the student profile. This is a guidance prototype, not a validated prediction; verify values against official college records.")

elif page == "Department Leaderboard":
    hero(
        "STUDENT PORTAL",
        "Department performance leaderboard",
        "View the department leaderboard using a weighted KPI score calculated from CGPA, attendance and available academic factors. The leaderboard displays only rank, student name and overall score."
    )
    profile = get_profile(user["id"]) or {}
    department = str(profile.get("department") or user.get("department") or "").strip()
    student_id = str(profile.get("student_id") or "").strip()
    if not department:
        st.warning("Complete My Profile & Progress and add your department before viewing a department comparison.")
    else:
        # Prefer the latest official roster. If one is not available, use saved student profiles
        # and clearly label the leaderboard as provisional/self-reported.
        roster = normalize_columns(academic_df) if academic_df is not None else None
        use_official = bool(roster is not None and "student_id" in roster.columns and "cgpa" in roster.columns and "department" in roster.columns)
        source_label = "Official department roster" if use_official else "Saved student profiles (self-reported; provisional)"
        records = []
        if use_official:
            roster["student_id"] = roster["student_id"].astype(str).str.strip()
            roster["department"] = roster["department"].astype(str).str.strip()
            roster = roster[roster["department"].str.casefold() == department.casefold()].copy()
            if "year" not in roster.columns:
                roster["year"] = pd.NA
            roster["year"] = numeric(roster, "year")
            roster["cgpa"] = numeric(roster, "cgpa")
            roster["attendance"] = numeric(roster, "attendance")
            roster["backlogs"] = numeric(roster, "backlogs")
            if "student_name" not in roster.columns:
                roster["student_name"] = ""
            # If the roster omits names, use names linked to student IDs in saved profiles.
            with conn() as _c:
                _name_rows = _c.execute("""SELECT u.full_name, sp.student_id FROM student_profiles sp
                                            JOIN users u ON u.id=sp.user_id
                                            WHERE sp.department=? AND COALESCE(sp.student_id,'')<>''""", (department,)).fetchall()
            _name_map = {str(r["student_id"]).strip(): r["full_name"] for r in _name_rows}
            roster["Student"] = roster.apply(lambda r: str(r.get("student_name") or "").strip() or _name_map.get(str(r["student_id"]).strip()) or ("Student " + str(r["student_id"])[-4:]), axis=1)
            roster = roster[roster["student_id"].ne("") & roster["cgpa"].notna()].copy()
            roster = roster.drop_duplicates(subset=["student_id"], keep="last")
            for _, r in roster.iterrows():
                records.append({"student_id": str(r["student_id"]).strip(), "Student": r["Student"], "Year": r.get("year"), "CGPA": r.get("cgpa"), "Attendance %": r.get("attendance"), "Backlogs": r.get("backlogs")})
        else:
            with conn() as _c:
                _profile_rows = _c.execute("""SELECT u.full_name, u.academic_year AS user_year, sp.*
                                               FROM student_profiles sp JOIN users u ON u.id=sp.user_id
                                               WHERE lower(trim(COALESCE(sp.department,'')))=lower(trim(?))
                                               AND u.role='Student'""", (department,)).fetchall()
            for r in _profile_rows:
                if r["cgpa"] is None or not str(r["student_id"] or "").strip():
                    continue
                records.append({"student_id": str(r["student_id"]).strip(), "Student": r["full_name"],
                                "Year": r["academic_year"] or r["user_year"], "CGPA": pd.to_numeric(r["cgpa"], errors="coerce"),
                                "Attendance %": pd.to_numeric(r["attendance"], errors="coerce"), "Backlogs": pd.NA})

        board = pd.DataFrame(records)
        if board.empty:
            st.info("No comparable records found for this department yet. Ask the HOD to upload an academic roster containing Student ID, Department and CGPA, or have students complete their profiles.")
        else:
            board["Year"] = pd.to_numeric(board["Year"], errors="coerce")
            current_year = int(profile.get("academic_year") or user.get("academic_year") or 0)
            if board["Year"].notna().any():
                year_options = ["Same academic year", "All years in department"]
                year_mode = st.radio("Compare with", year_options, horizontal=True, index=0, key="leaderboard_year_mode")
                if year_mode == "Same academic year" and current_year:
                    board = board[board["Year"].eq(current_year)]
            if board.empty:
                st.info("No records match your selected year. Ask the HOD to check the roster or choose all years in the department.")
            else:
                board["CGPA"] = pd.to_numeric(board["CGPA"], errors="coerce")
                board["Attendance %"] = pd.to_numeric(board["Attendance %"], errors="coerce")
                board["Backlogs"] = pd.to_numeric(board["Backlogs"], errors="coerce")
                # Weighted score: CGPA 75%, attendance 20%, backlogs 5% (when available).
                # If an indicator is absent for a row, its weight is redistributed proportionally
                # across the available indicators; no missing value is silently treated as zero.
                def weighted_score(row):
                    parts = []
                    if pd.notna(row["CGPA"]): parts.append((75.0, max(0.0, min(10.0, float(row["CGPA"]))) * 10.0))
                    if pd.notna(row["Attendance %"]): parts.append((20.0, max(0.0, min(100.0, float(row["Attendance %"])))) )
                    if pd.notna(row["Backlogs"]): parts.append((5.0, max(0.0, 100.0 - min(5.0, max(0.0, float(row["Backlogs"]))) * 20.0)))
                    total_weight = sum(w for w, _ in parts)
                    return round(sum(w * value for w, value in parts) / total_weight, 2) if total_weight else pd.NA
                board["Performance Score"] = board.apply(weighted_score, axis=1)
                board = board[board["Performance Score"].notna()].copy()
                board = board.sort_values(["Performance Score", "CGPA", "Attendance %"], ascending=[False, False, False], na_position="last").reset_index(drop=True)
                board["Rank"] = board["Performance Score"].rank(method="min", ascending=False).astype(int)
                # A single student should appear only once even if the roster had duplicate rows.
                board = board.drop_duplicates(subset=["student_id"], keep="first")
                board["Rank"] = board["Performance Score"].rank(method="min", ascending=False).astype(int)
                me = board[board["student_id"].astype(str).str.strip().eq(student_id)] if student_id else pd.DataFrame()
                st.caption(f"Data source: {source_label}. Department: {department}. Ranking is based on the records available to DEPTHIVE and is not an official university rank.")
                if not me.empty:
                    mine = me.iloc[0]
                    m1, m2 = st.columns(2)
                    m1.metric("Your department rank", f"#{int(mine['Rank'])} of {len(board)}")
                    m2.metric("Your performance score", f"{float(mine['Performance Score']):.2f}/100")
                else:
                    st.warning("Your Student ID was not found in the comparison records. Check that your profile Student ID exactly matches the ID in the official roster, then ask your HOD to update the roster if needed.")
                top = board.head(10).copy()
                if not top.empty:
                    st.markdown("#### 🏆 Top 10 students in your department")
                    st.caption("Students are ordered by weighted performance score. Ties are broken by CGPA, then attendance.")
                    chart = top.set_index("Student")["Performance Score"]
                    st.bar_chart(chart, color="#66816a")

                    top_view = top[["Rank", "Student", "Performance Score"]].copy()
                    rank_badges = {1: "🥇 1", 2: "🥈 2", 3: "🥉 3"}
                    top_view["Rank"] = top_view["Rank"].map(lambda r: rank_badges.get(int(r), f"#{int(r)}"))
                    top_view["Performance Score"] = top_view["Performance Score"].map(lambda x: f"{float(x):.2f}/100")
                    top_view = top_view.rename(columns={"Student": "Student Name", "Performance Score": "Score"})
                    st.dataframe(top_view, width="stretch", hide_index=True)

                with st.expander("View all ranked students", expanded=False):
                    view = board[["Rank", "Student", "Performance Score"]].copy()
                    view["Performance Score"] = view["Performance Score"].map(lambda x: f"{float(x):.2f}/100")
                    view = view.rename(columns={"Student": "Student Name", "Performance Score": "Score"})
                    st.dataframe(view, width="stretch", hide_index=True)
                st.caption("Scores are a transparent comparison metric for this prototype, not a validated predictive model. Official academic records should be verified before decisions are made.")

elif page == "Academic Data Hub":
    hero("COLLEGE DATA WORKSPACE", "Academic data hub", "Faculty / authorized department staff can drag and drop a roster. Use one row per student and clear column names so analysis can validate the data before scoring.")
    st.markdown("### 1 · Upload academic roster")
    with st.expander("Expected columns and file rules", expanded=True):
        st.write("Required for department comparisons: **Student_ID, Department, Year**. Recommended: **CGPA, Attendance, Backlogs**. Optional: Semester, SGPA, marks and skills assessment fields. Year must be 1–4. Use CSV or Excel (.xlsx).")
        template = pd.DataFrame(columns=["Student_ID","Department","Year","Semester","CGPA","Attendance","Backlogs","SGPA"])
        st.download_button("Download roster template (CSV)", template.to_csv(index=False).encode("utf-8"), "depthive_academic_roster_template.csv", "text/csv")
    uploaded = st.file_uploader("Drag and drop your academic roster here, or browse files", type=["csv","xlsx","xls"], key="academic_roster_upload")
    dept_override = st.text_input("Department label", value=(user.get("department", "") if user["role"] in ["Faculty", "Department / HOD"] else ""), disabled=user["role"] in ["Faculty", "Department / HOD"], help="Staff uploads are scoped to their assigned department.")
    notes = st.text_input("Upload note (optional)", key="academic_note")
    if uploaded:
        try:
            preview = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
            st.markdown("**Preview**")
            st.dataframe(preview.head(12), width="stretch", hide_index=True)
            q=data_quality(preview); a,b,c,d=st.columns(4); a.metric("Rows",q["rows"]); b.metric("Columns",q["columns"]); c.metric("Missing cells",q["missing"]); d.metric("Duplicate rows",q["duplicates"])
            normalized=normalize_columns(preview)
            if user["role"] in ["Faculty", "Department / HOD"] and user.get("department"):
                if "department" in normalized.columns:
                    supplied = set(normalized["department"].dropna().astype(str).str.strip().str.casefold())
                    if supplied and supplied != {user["department"].strip().casefold()}:
                        st.error("This file contains records outside your assigned department. Upload only your department's records.")
                        st.stop()
                elif "Department" not in preview.columns:
                    preview["Department"] = user["department"]
                    normalized = normalize_columns(preview)
            missing=[x for x in ["student_id","department","year"] if x not in normalized.columns and not (x=="department" and dept_override.strip())]
            if missing: st.error("Missing required fields: " + ", ".join(missing) + ". Fix column names or provide a department label.")
            elif st.button("Validate and save academic roster", width="stretch"):
                if dept_override.strip() and "department" not in normalized.columns: preview["Department"] = dept_override.strip()
                save_upload(uploaded, "Academic roster", user, department=dept_override.strip(), notes=notes)
                st.success("Academic roster saved. It is now available to authorized department/admin analysis.")
                st.rerun()
        except Exception as e: st.error(f"Could not read this file: {e}")
    st.markdown("### 2 · Latest saved academic uploads")
    rows=list_uploads("Academic roster", user.get("department") if user["role"]=="Department / HOD" else None)
    if rows: st.dataframe(pd.DataFrame([{ "File":x["file_name"],"Department":x["department"],"Uploaded":x["uploaded_at"],"Notes":x["notes"]} for x in rows]), width="stretch", hide_index=True)
    else: st.info("No academic roster has been saved yet.")

elif page == "Student Submissions":
    hero(
        "DEPARTMENT WORKSPACE",
        "Student submissions",
        "A student-first view of uploaded documents. Find a student once, then open their document list only when needed."
    )
    dept = str(user.get("department") or "").strip()
    if user["role"] == "Department / HOD" and not dept:
        st.warning("Your HOD account does not have a department assigned. Ask College Admin to update your account before viewing submissions.")
    else:
        # Resolve department/year from the upload first, then fall back to the student's profile.
        with conn() as c:
            sql = """SELECT up.*, u.full_name AS student_name, u.email AS student_email,
                     COALESCE(NULLIF(TRIM(up.department), ''), NULLIF(TRIM(sp.department), ''), '') AS resolved_department,
                     sp.student_id AS student_id,
                     COALESCE(up.academic_year, sp.academic_year, u.academic_year, 0) AS resolved_year
                     FROM uploads up
                     JOIN users u ON u.id = up.uploader_id
                     LEFT JOIN student_profiles sp ON sp.user_id = u.id
                     WHERE u.role = 'Student' AND up.category LIKE 'Student document:%'
                     ORDER BY up.uploaded_at DESC"""
            submission_rows = [dict(r) for r in c.execute(sql).fetchall()]

        if user["role"] == "Department / HOD":
            submission_rows = [
                r for r in submission_rows
                if str(r.get("resolved_department") or "").strip().casefold() == dept.casefold()
            ]

        if not submission_rows:
            st.info("No student documents found for this department yet. Ask students to complete My Profile & Progress (especially Student ID and Department) and upload their documents.")
        else:
            # Build a student-level index so multiple uploads don't overwhelm the HOD.
            grouped = {}
            for r in submission_rows:
                sid = str(r.get("student_id") or "").strip()
                email = str(r.get("student_email") or "").strip().casefold()
                group_key = sid or email or str(r.get("uploader_id"))
                if group_key not in grouped:
                    grouped[group_key] = {
                        "student_id": sid or "Not added",
                        "student_name": r.get("student_name") or "Unnamed student",
                        "email": r.get("student_email") or "",
                        "department": r.get("resolved_department") or "Not assigned",
                        "year": r.get("resolved_year") or "Not set",
                        "uploads": []
                    }
                grouped[group_key]["uploads"].append(r)

            student_cards = list(grouped.values())
            for student in student_cards:
                student["uploads"].sort(key=lambda x: str(x.get("uploaded_at") or ""), reverse=True)
                student["file_count"] = len(student["uploads"])
                student["latest_upload"] = str(student["uploads"][0].get("uploaded_at") or "Unknown")

            # Search and filters apply to the student index, not to a giant file table.
            f1, f2, f3 = st.columns([2, 1, 1])
            with f1:
                search_term = st.text_input("Search students", placeholder="Student ID or name...")
            with f2:
                years = sorted({str(s["year"]) for s in student_cards}, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x))
                selected_years = st.multiselect("Academic year", years, default=years)
            with f3:
                doc_types = sorted({
                    str(r.get("category") or "").replace("Student document: ", "")
                    for r in submission_rows
                })
                selected_types = st.multiselect("Document types", doc_types, default=doc_types)

            search_norm = search_term.strip().casefold()
            filtered_students = []
            for student in student_cards:
                searchable = f'{student["student_id"]} {student["student_name"]} {student["email"]}'.casefold()
                if search_norm and search_norm not in searchable:
                    continue
                if str(student["year"]) not in selected_years:
                    continue
                matching_uploads = [
                    r for r in student["uploads"]
                    if str(r.get("category") or "").replace("Student document: ", "") in selected_types
                ]
                if not matching_uploads:
                    continue
                item = dict(student)
                item["visible_uploads"] = matching_uploads
                item["visible_count"] = len(matching_uploads)
                filtered_students.append(item)

            total_files = sum(s["visible_count"] for s in filtered_students)
            recent_cut = sorted(
                [r for s in filtered_students for r in s["visible_uploads"]],
                key=lambda x: str(x.get("uploaded_at") or ""), reverse=True
            )
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Students with documents", f"{len(filtered_students):,}")
            m2.metric("Documents in view", f"{total_files:,}")
            m3.metric("Document types", len({str(r.get("category") or "").replace("Student document: ", "") for r in recent_cut}))
            m4.metric("Latest upload", str(recent_cut[0].get("uploaded_at") or "—")[:16].replace("T", " ") if recent_cut else "—")

            st.caption("Each student appears once. Expand a student row to review their files; this keeps the page readable as submissions grow.")
            if not filtered_students:
                st.warning("No students match these search and filter settings. Try clearing the search or selecting more filters.")
            else:
                for student in sorted(filtered_students, key=lambda x: (str(x["student_name"]).casefold(), str(x["student_id"]))):
                    heading = f'{student["student_name"]}  ·  ID: {student["student_id"]}  ·  {student["visible_count"]} document(s)'
                    with st.expander(heading, expanded=False):
                        a, b, c = st.columns(3)
                        a.markdown(f'**Department**\n\n{student["department"]}')
                        b.markdown(f'**Academic year**\n\n{student["year"]}')
                        c.markdown(f'**Latest upload**\n\n{student["latest_upload"]}')
                        file_labels = {}
                        for r in student["visible_uploads"]:
                            doc_type = str(r.get("category") or "").replace("Student document: ", "")
                            uploaded = str(r.get("uploaded_at") or "Unknown")
                            label = f'{doc_type} · {r.get("file_name") or "Unnamed file"} · {uploaded}'
                            file_labels[label] = r
                        st.dataframe(
                            pd.DataFrame([{
                                "Document type": str(r.get("category") or "").replace("Student document: ", ""),
                                "File name": r.get("file_name") or "Unnamed file",
                                "Uploaded": r.get("uploaded_at") or "Unknown",
                                "Notes": r.get("notes") or ""
                            } for r in student["visible_uploads"]]),
                            width="stretch",
                            hide_index=True
                        )
                        selected_label = st.selectbox(
                            "Select a document to download",
                            list(file_labels.keys()),
                            key=f"submission_select_{student['student_id']}_{student['email']}"
                        )
                        selected = file_labels[selected_label]
                        try:
                            file_path = Path(selected["stored_path"])
                            if file_path.exists():
                                st.download_button(
                                    "Download selected document",
                                    data=file_path.read_bytes(),
                                    file_name=selected["file_name"],
                                    key=f"download_student_submission_{selected['id']}"
                                )
                            else:
                                st.error("The file record exists, but the stored file could not be found on this installation.")
                        except Exception as e:
                            st.error(f"Could not open this file: {e}")

elif page == "Student Risk Review":
    hero("ACADEMIC SUPPORT", "Student risk review", "Risk signals are based on named academic attributes. Placement and internship signals are included only for fourth-year records and only when supplied in the official dataset.")
    if academic_df is None: st.info("Upload an academic roster in Academic Data Hub first.")
    else:
        ra=risk_analysis(combined_analysis_roster())
        if user["role"] in ["Department / HOD", "Faculty"] and user.get("department"):
            ra=ra[ra["Department"].astype(str).str.strip().str.casefold()==user["department"].strip().casefold()]
        c1,c2,c3,c4=st.columns(4); c1.metric("Students reviewed",len(ra)); c2.metric("High risk",int((ra["Risk Level"]=="High").sum())); c3.metric("Moderate",int((ra["Risk Level"]=="Moderate").sum())); c4.metric("Low",int((ra["Risk Level"]=="Low").sum()))
        l,r=st.columns([1,1.25])
        with l:
            st.markdown("**Risk distribution**")
            st.bar_chart(ra["Risk Level"].value_counts().reindex(["Low","Moderate","High"],fill_value=0), color=["#66816a"])
        with r:
            st.markdown("**Most important risk signals**")
            counts={}
            for text in ra["Risk Factors"].fillna(""):
                for factor in text.split("; "):
                    if factor and factor!="No configured risk trigger detected": counts[factor]=counts.get(factor,0)+1
            if counts: st.bar_chart(pd.Series(counts).sort_values(ascending=False).head(8), color=["#9585b4"])
            else: st.info("No configured risk triggers detected.")
        st.markdown("### Risk scorecard")
        high_pct=safe_pct(int((ra["Risk Level"]=="High").sum()),len(ra))
        moderate_pct=safe_pct(int((ra["Risk Level"]=="Moderate").sum()),len(ra))
        st.info(narrative_health(high_risk_pct=high_pct))
        st.markdown("### Students needing review")
        filt=st.multiselect("Filter risk level", ["High","Moderate","Low"], default=["High","Moderate"])
        view=ra[ra["Risk Level"].isin(filt)].sort_values("Risk Score",ascending=False)
        st.dataframe(view, width="stretch", hide_index=True)
        st.download_button("Download risk review CSV", view.to_csv(index=False).encode("utf-8"), "depthive_student_risk_review.csv", "text/csv")
        st.caption("Rules are transparent starter thresholds, not a clinically or statistically validated prediction model. Confirm records before taking action.")

elif page == "Department Intelligence":
    hero("DEPARTMENT ANALYTICS", "Department health & comparison", "Compare academic health separately from placement outcomes. The system does not blend unrelated years or treat missing data as poor performance.")
    if academic_df is None: st.info("Upload an academic roster first.")
    else:
        d=normalize_columns(academic_df)
        if "department" not in d.columns: st.error("Department column is required.")
        else:
            d["cgpa"]=numeric(d,"cgpa"); d["attendance"]=numeric(d,"attendance"); d["backlogs"]=numeric(d,"backlogs")
            summary=d.groupby("department",dropna=False).agg(Students=("student_id","nunique") if "student_id" in d.columns else ("department","size"), Average_CGPA=("cgpa","mean"), Average_Attendance=("attendance","mean"), Students_With_Backlogs=("backlogs",lambda x:int((x.fillna(0)>0).sum()))).reset_index()
            summary["Average_CGPA"]=summary["Average_CGPA"].round(2); summary["Average_Attendance"]=summary["Average_Attendance"].round(1)
            summary=summary.rename(columns={"department":"Department","Average_CGPA":"Average CGPA","Average_Attendance":"Average Attendance %","Students_With_Backlogs":"Students with backlogs"})
            st.markdown("### Academic comparison")
            a,b=st.columns(2)
            with a: st.markdown("**Average CGPA by department**"); st.bar_chart(summary.set_index("Department")["Average CGPA"], color=["#66816a"])
            with b: st.markdown("**Average attendance by department**"); st.bar_chart(summary.set_index("Department")["Average Attendance %"], color=["#c5a15a"])
            ranked_summary=summary.sort_values("Average CGPA",ascending=False,na_position="last")
            st.dataframe(ranked_summary,width="stretch",hide_index=True)
            if not ranked_summary.empty:
                best_row=ranked_summary.dropna(subset=["Average CGPA"]).head(1)
                if not best_row.empty:
                    br=best_row.iloc[0]
                    st.markdown("### Department scorecard")
                    m1,m2,m3=st.columns(3)
                    m1.metric("Highest average CGPA", f"{br['Average CGPA']:.2f}/10", str(br["Department"]))
                    m2.metric("Departments compared", int(summary["Department"].nunique()))
                    m3.metric("Student records", int(summary["Students"].sum()))
                    st.info(narrative_health(avg_cgpa=float(br["Average CGPA"]), avg_attendance=float(br["Average Attendance %"]) if pd.notna(br["Average Attendance %"]) else None))
            st.markdown("### Academic risk by department")
            ra=risk_analysis(combined_analysis_roster())
            risk_sum=ra.groupby("Department").agg(Students=("Student ID","count"),High_Risk=("Risk Level",lambda x:int((x=="High").sum())),Moderate_Risk=("Risk Level",lambda x:int((x=="Moderate").sum()))).reset_index()
            risk_sum["High Risk %"]=(risk_sum["High_Risk"]/risk_sum["Students"].replace(0,pd.NA)*100).round(1)
            st.bar_chart(risk_sum.set_index("Department")[["High_Risk","Moderate_Risk"]], color=["#c4775b", "#c5a15a"])
            st.dataframe(risk_sum.sort_values("High Risk %",ascending=False,na_position="last"),width="stretch",hide_index=True)
            st.caption("Department health is presented as separate measures, not a single opaque score. Compare similar cohorts and ensure the roster is current.")

elif page == "Placement & Internship Data":
    hero("PLACEMENT CELL WORKSPACE", "Official career outcomes", "Placement and internship data is uploaded by the Placement Cell / authorized department—not self-reported by students. Use one row per student; multiple offers should not create duplicate placed students.")
    with st.expander("Expected placement file columns",expanded=True):
        st.write("Required: **Student_ID, Department**. Recommended: **Year, Eligible_For_Placement, Placement_Status, Internship_Status**. Optional: **Package_LPA, Company, Role, Batch**. For placement-rate calculations, Year 4 records and eligibility are used when available.")
        tpl=pd.DataFrame(columns=["Student_ID","Department","Year","Eligible_For_Placement","Placement_Status","Internship_Status","Company","Role","Package_LPA","Batch"])
        st.download_button("Download placement template (CSV)",tpl.to_csv(index=False).encode("utf-8"),"depthive_placement_template.csv","text/csv")
    uploaded=st.file_uploader("Drag and drop placement / internship data here, or browse files",type=["csv","xlsx","xls"],key="placement_upload")
    dept=st.text_input("Department label", value=(user.get("department", "") if user["role"] == "Placement Cell" else ""), disabled=user["role"] == "Placement Cell", key="placement_dept")
    notes=st.text_input("Batch / upload notes (optional)",key="placement_notes")
    if uploaded:
        try:
            preview=pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
            st.dataframe(preview.head(12),width="stretch",hide_index=True)
            nd=normalize_columns(preview)
            if user["role"] == "Placement Cell" and user.get("department"):
                if "department" in nd.columns:
                    supplied = set(nd["department"].dropna().astype(str).str.strip().str.casefold())
                    if supplied and supplied != {user["department"].strip().casefold()}:
                        st.error("This file contains records outside your assigned department. Upload only your department's records.")
                        st.stop()
                elif "Department" not in preview.columns:
                    preview["Department"] = user["department"]
                    nd = normalize_columns(preview)
            if "student_id" not in nd.columns: st.error("Student_ID / Enrollment number column is required to prevent duplicate counting.")
            elif "department" not in nd.columns and not dept.strip(): st.error("Add a Department column or enter a department label.")
            elif st.button("Validate and save official outcomes",width="stretch"):
                if dept.strip() and "department" not in nd.columns: preview["Department"]=dept.strip()
                save_upload(uploaded,"Placement outcomes",user,department=dept.strip(),notes=notes)
                st.success("Official outcome file saved."); st.rerun()
        except Exception as e: st.error(f"Could not read this file: {e}")
    st.markdown("### Recent official uploads")
    rows=list_uploads("Placement outcomes",user.get("department") if user["role"]=="Department / HOD" else None)
    if rows: st.dataframe(pd.DataFrame([{ "File":x["file_name"],"Department":x["department"],"Uploaded":x["uploaded_at"],"Notes":x["notes"]} for x in rows]),width="stretch",hide_index=True)
    else: st.info("No official placement file has been uploaded.")

elif page == "Placement Intelligence":
    hero("CAREER OUTCOMES", "Placement & internship intelligence", "Compare graduating cohorts using verified department data. Year 1–3 students are excluded from placement-risk logic.")
    if placement_df is None: st.info("Placement data is not available yet. The Placement Cell should upload the official outcomes file.")
    else:
        ps,err=placement_summary(placement_df)
        if err: st.warning(err)
        elif ps.empty: st.info("No Year 4 records were found. Check the Year column and values in the uploaded dataset.")
        else:
            if "Placement Rate %" in ps.columns and not ps["Placement Rate %"].isna().all():
                best=ps.dropna(subset=["Placement Rate %"]).iloc[0]
                c1,c2,c3=st.columns(3); c1.metric("Departments",len(ps)); c2.metric("Top placement rate",f"{best['Placement Rate %']:.1f}%",str(best["Department"])); c3.metric("Eligible students",int(ps["Eligible Students"].sum()))
            st.markdown("### Department placement comparison")
            st.bar_chart(ps.set_index("Department")["Placement Rate %"], color=["#9585b4"])
            valid_rates=ps.dropna(subset=["Placement Rate %"]) if "Placement Rate %" in ps.columns else pd.DataFrame()
            if not valid_rates.empty:
                top=valid_rates.sort_values("Placement Rate %",ascending=False).iloc[0]
                st.markdown("### Placement scorecard")
                p1,p2,p3=st.columns(3)
                p1.metric("Highest placement rate",f"{top['Placement Rate %']:.1f}%",str(top["Department"]))
                p2.metric("Eligible students",int(ps["Eligible Students"].sum()))
                p3.metric("Placed students",int(ps["Placed Students"].sum()))
                st.info(narrative_health(placement_rate=float(top["Placement Rate %"])))
            st.dataframe(ps,width="stretch",hide_index=True)
            st.download_button("Download placement summary CSV",ps.to_csv(index=False).encode("utf-8"),"depthive_placement_summary.csv","text/csv")
            st.caption("Placement rates are meaningful only if eligibility, placement status and graduating-batch coverage are consistently recorded.")

elif page == "Data Quality & Audit":
    hero("GOVERNANCE", "Data quality & audit", "Review uploaded data sources and important workspace actions. Use the quality checks before interpreting any risk score or department ranking.")
    uploads=list_uploads()
    if uploads: st.dataframe(pd.DataFrame([{ "File":u["file_name"],"Type":u["category"],"Department":u["department"],"Year":u["academic_year"],"Uploaded":u["uploaded_at"],"Notes":u["notes"]} for u in uploads]),width="stretch",hide_index=True)
    else: st.info("No uploads recorded.")
    with conn() as c:
        logs=c.execute("SELECT a.id,a.created_at,u.full_name AS actor_name,u.email AS actor_email,a.action,a.detail FROM audit_log a LEFT JOIN users u ON u.id=a.user_id ORDER BY a.id DESC LIMIT 200").fetchall()
        all_users={int(r["id"]): dict(r) for r in c.execute("SELECT id,full_name,email,role,department FROM users").fetchall()}
        approval_by_audit={}
        # Link older APPROVE_USER audit events (which stored only a user ID) to the actual account.
        approval_rows=c.execute("SELECT approved_user_id,approved_user_name,approved_user_email,approved_role,department,approved_at FROM approval_history").fetchall()
        for r in approval_rows:
            approval_by_audit[int(r["approved_user_id"])]=dict(r)
    st.markdown("### Recent audit events")
    if logs:
        audit_view=[]
        for log in logs:
            item=dict(log)
            item["Admin / Actor"] = item.pop("actor_name") or item.pop("actor_email")
            item.pop("actor_email", None)
            target_id=None
            detail=str(item.get("detail") or "")
            if item.get("action")=="APPROVE_USER":
                # Support both the old format "Approved user id 4" and the newer descriptive format.
                import re
                match=re.search(r"user id\s*(\d+)", detail, flags=re.IGNORECASE)
                if match:
                    target_id=int(match.group(1))
                if target_id is not None:
                    target=all_users.get(target_id,{})
                    hist=approval_by_audit.get(target_id,{})
                    item["Approved user"] = hist.get("approved_user_name") or target.get("full_name") or f"User ID {target_id}"
                    item["Approved email"] = hist.get("approved_user_email") or target.get("email", "")
                    item["Role"] = hist.get("approved_role") or target.get("role", "")
                    item["Department"] = hist.get("department") or target.get("department", "")
                    item["detail"] = f"Approved {item['Approved user']} ({item['Approved email']}) as {item['Role']} · {item['Department']}"
                else:
                    # Newer audit entries already include name, email, role and department in detail.
                    item["Approved user"] = detail
            audit_view.append(item)
        audit_df=pd.DataFrame(audit_view)
        audit_df=audit_df.rename(columns={"created_at":"Date & time","actor_email":"Actor email","action":"Action","detail":"Details"})
        st.dataframe(audit_df.drop(columns=["id"],errors="ignore"),width="stretch",hide_index=True)
    else:
        st.info("No audit events yet.")

elif page == "Access Approvals":
    hero("ADMINISTRATION", "Access approvals", "Approve staff accounts only after verifying the person and their role. Students can create their own student accounts.")
    with conn() as c: pending=c.execute("SELECT id,full_name,email,role,department,created_at FROM users WHERE approved=0 ORDER BY created_at").fetchall()
    if not pending: st.success("No staff accounts are waiting for approval.")
    else:
        st.markdown("### Pending staff requests")
        st.dataframe(pd.DataFrame([dict(x) for x in pending]),width="stretch",hide_index=True)
        selected=st.selectbox("Select account to approve",[f"{x['id']} · {x['full_name']} · {x['role']} · {x['email']}" for x in pending])
        uid=int(selected.split(" · ")[0])
        if st.button("Approve selected staff account",width="stretch"):
            target=next((dict(x) for x in pending if int(x["id"])==uid),None)
            with conn() as c:
                c.execute("UPDATE users SET approved=1 WHERE id=?",(uid,))
                if target:
                    c.execute("INSERT INTO approval_history(approved_user_id,approved_by_user_id,approved_user_name,approved_user_email,approved_role,department,approved_at) VALUES(?,?,?,?,?,?,?)",
                              (uid,user["id"],target["full_name"],target["email"],target["role"],target["department"],datetime.now().isoformat(timespec="seconds")))
            log_action(user["id"],"APPROVE_USER",f"Approved {target['full_name']} ({target['email']}) as {target['role']} for {target['department']}")
            st.success("Account approved and approval history recorded."); st.rerun()
    st.markdown("### Approval history")
    with conn() as c:
        history=c.execute("SELECT approved_at,approved_user_name,approved_user_email,approved_role,department,approved_by_user_id FROM approval_history ORDER BY id DESC LIMIT 200").fetchall()
        approver_rows={r["id"]:r["full_name"] for r in c.execute("SELECT id,full_name FROM users").fetchall()}
    if history:
        hist=[]
        for row in history:
            item=dict(row); item["Approved by"]=approver_rows.get(item.pop("approved_by_user_id"),"Admin account")
            hist.append(item)
        st.dataframe(pd.DataFrame(hist).rename(columns={"approved_at":"Approved at","approved_user_name":"Approved user","approved_user_email":"Email","approved_role":"Role","department":"Department"}),width="stretch",hide_index=True)
    else: st.info("No approvals have been recorded yet. Future approvals will appear here.")

elif page == "DEPTHIVE Copilot":
    hero("ROLE-AWARE ASSISTANT", "DEPTHIVE Copilot", "Ask about the data and tools available in your current workspace. Responses respect the current role and clearly distinguish measured data from recommendations.")
    st.info("Copilot is currently a safe prototype assistant using configured rules and current workspace data. It is not yet a trained ML model and cannot reliably answer every possible question.")
    prompt=st.text_area("Ask DEPTHIVE Copilot", placeholder="Examples: How many students are high risk? Which department has the highest CGPA? How do I upload placement data?", height=110, key="copilot_question")
    if st.button("Ask Copilot", width="stretch"):
        answer=copilot_reply(prompt,user,academic_df,placement_df)
        st.session_state["copilot_last_question"]=prompt
        st.session_state["copilot_last_answer"]=answer
        log_action(user["id"],"COPILOT_QUERY",prompt[:300])
    if st.session_state.get("copilot_last_answer"):
        st.markdown("### Copilot response")
        st.info(st.session_state["copilot_last_answer"])
        st.caption("Check important conclusions against the source records. The assistant only has access to the current prototype workspace context.")
    st.markdown("### Planned ML upgrade")
    st.write("A future ML version should use a curated, reviewed question/answer dataset and retrieval from approved college records. It needs role-based access checks, evaluation for correctness, and a fallback when evidence is missing. It should not be trained on private student records without authorization.")

st.markdown("---")
st.caption("DEPTHIVE · Prototype. Rule-based risk scores are indicators for review, not guaranteed predictions. Restrict access to personal data and validate uploaded records before institutional decisions.")
