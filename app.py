import streamlit as st
import pandas as pd
from html import escape
from pathlib import Path

st.set_page_config(page_title="Fulfillment Hub", layout="wide")


# STYLES

st.markdown(r"""
<style>
:root{--navy:#172554;--blue:#2563EB;--border:#E2E8F0;--bg:#F5F7FB;--text:#172033;--muted:#64748B}
.stApp{background:var(--bg);color:var(--text);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
header[data-testid="stHeader"]{background:#172554!important}
header[data-testid="stHeader"] button{color:white!important}
.top-color-bar{position:fixed;top:0;left:0;right:0;height:4px;z-index:999999;background:linear-gradient(90deg,#172554,#2563EB,#0D9488)}
.block-container{padding-top:2rem;padding-bottom:3rem;max-width:1600px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#172554 0%,#1E3A8A 100%)}
.sidebar-title{color:white!important;font-size:27px;font-weight:800;letter-spacing:-.5px}
.workspace-label{color:#BFDBFE!important;font-size:11px;font-weight:750;letter-spacing:.08em}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{display:none!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{color:#DBEAFE!important;padding:11px 13px;border-radius:9px;font-size:14px;font-weight:600;margin-bottom:5px}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){background:#2563EB;color:white!important}
.page-header-title{color:var(--navy);font-size:28px;font-weight:800;letter-spacing:-.5px;margin:4px 0 7px}
.page-subtitle{color:var(--muted);font-size:13px;margin:0 0 24px}
.section-heading-title{color:var(--navy);font-size:18px;font-weight:750;margin:12px 0 14px}
.card-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.dashboard-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}
.packing-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.summary-card{background:white;border:1px solid var(--border);border-radius:12px;padding:16px 18px;min-height:90px;box-shadow:0 2px 5px rgba(15,23,42,.025);border-top:3px solid var(--blue)}
.summary-card.purple{border-top-color:#7C3AED}.summary-card.red{border-top-color:#DC2626}.summary-card.orange{border-top-color:#F59E0B}.summary-card.teal{border-top-color:#0D9488}.summary-card.green{border-top-color:#16A34A}
.card-label{color:var(--muted);font-size:12px;font-weight:650}.card-value{color:var(--navy);font-size:26px;font-weight:800;margin-top:8px}.card-note{color:#94A3B8;font-size:11px;margin-top:5px}
.table-card{background:white;border:1px solid var(--border);border-radius:10px;overflow-x:auto;width:100%}.fh-table{width:max-content;min-width:100%;border-collapse:collapse;background:white}.fh-table th{text-align:left;padding:11px 12px;background:#F1F5F9;color:#334155;font-size:12px;border-bottom:1px solid #CBD5E1;white-space:nowrap}.fh-table td{padding:9px 12px;font-size:12px;border-bottom:1px solid var(--border);white-space:nowrap}.fh-table tbody tr:nth-child(even) td{background:#FAFBFD}.fh-table tbody tr:hover td{background:#EFF6FF}
.empty-state{padding:22px;color:var(--muted);background:white;border:1px solid var(--border);border-radius:10px;text-align:center}.order-id{color:#1D4ED8;font-weight:750}
.badge{display:inline-block;padding:4px 8px;border-radius:6px;font-size:11px;font-weight:700}.priority-badge{background:#FEE2E2;color:#B91C1C}.normal-badge{background:#F1F5F9;color:#475569}.status-picking{background:#DBEAFE;color:#1D4ED8}.status-packed{background:#EDE9FE;color:#6D28D9}.status-staged{background:#FEF3C7;color:#B45309}.status-ready{background:#CCFBF1;color:#0F766E}.status-waiting{background:#FEE2E2;color:#B91C1C}.status-complete{background:#DCFCE7;color:#15803D}.status-default{background:#F1F5F9;color:#475569}.issue-danger{background:#FEF2F2;color:#B91C1C}.issue-warning{background:#FFFBEB;color:#B45309}.issue-neutral{background:#F1F5F9;color:#475569}.location-badge{background:#F1F5F9;color:#334155;padding:4px 8px;border-radius:6px}.location-stage{background:#F0FDFA;color:#0F766E;padding:4px 8px;border-radius:6px}.owner-badge{background:#F5F3FF;color:#6D28D9;padding:4px 8px;border-radius:6px}.issue-action{color:#1D4ED8;font-weight:700}
.verification-card{background:white;border:1px solid var(--border);border-radius:12px;padding:18px 20px}.verification-order{color:var(--navy);font-size:18px;font-weight:800}.verification-expected{background:#F8FAFC;border:1px solid var(--border);border-radius:9px;padding:13px 15px;margin:12px 0}.verification-result{border-radius:9px;padding:12px 14px;margin-top:12px;font-size:13px;font-weight:650}.verification-pass{background:#F0FDF4;border:1px solid #BBF7D0;color:#166534}.verification-fail{background:#FEF2F2;border:1px solid #FECACA;color:#B91C1C}
.workflow-flow{display:flex;gap:12px;overflow-x:auto;padding-bottom:10px}.workflow-stage{flex:1;min-width:145px;min-height:155px;padding:16px 12px;text-align:center;border:1px solid var(--border);border-radius:12px;background:white}.stage-name{font-size:13px;font-weight:800;color:var(--navy)}.stage-count{font-size:24px;font-weight:800;color:var(--navy);margin-top:10px}.stage-percent{font-size:12px;color:var(--blue);margin-top:4px}.stage-description{font-size:11px;color:var(--muted);margin-top:12px}


/* Colored Fulfillment Workflow stages */
.workflow-stage:nth-child(1) {
    background: #EFF6FF;
    border-color: #93C5FD;
}
.workflow-stage:nth-child(1) .stage-count {
    color: #2563EB;
}

.workflow-stage:nth-child(2) {
    background: #F5F3FF;
    border-color: #C4B5FD;
}
.workflow-stage:nth-child(2) .stage-count {
    color: #7C3AED;
}

.workflow-stage:nth-child(3) {
    background: #FFFBEB;
    border-color: #FCD34D;
}
.workflow-stage:nth-child(3) .stage-count {
    color: #B45309;
}

.workflow-stage:nth-child(4) {
    background: #F0FDFA;
    border-color: #5EEAD4;
}
.workflow-stage:nth-child(4) .stage-count {
    color: #0F766E;
}

.workflow-stage:nth-child(5) {
    background: #F0FDF4;
    border-color: #86EFAC;
}
.workflow-stage:nth-child(5) .stage-count {
    color: #15803D;
}

.workflow-stage:nth-child(6) {
    background: #ECFDF5;
    border-color: #6EE7B7;
}
.workflow-stage:nth-child(6) .stage-count {
    color: #047857;
}

.workflow-stage {
    transition: transform .15s ease, box-shadow .15s ease;
}
.workflow-stage:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 14px rgba(15, 23, 42, .08);
}

/* Deadline status colors */
.deadline-overdue {
    background: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FECACA;
}

.deadline-soon {
    background: #FFEDD5;
    color: #C2410C;
    border: 1px solid #FED7AA;
}

.deadline-track {
    background: #DCFCE7;
    color: #15803D;
    border: 1px solid #BBF7D0;
}

.deadline-completed {
    background: #DBEAFE;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
}

.deadline-none {
    background: #F1F5F9;
    color: #475569;
    border: 1px solid #E2E8F0;
}



/* Form labels and controls */
.stApp [data-testid="stWidgetLabel"] label,.stApp [data-testid="stWidgetLabel"] p{color:#334155!important;font-size:13px!important;font-weight:600!important;opacity:1!important}
.stApp [data-baseweb="select"]>div{background:#fff!important;border:1px solid #CBD5E1!important;border-radius:8px!important;min-height:42px;box-shadow:none!important}
.stApp [data-baseweb="select"] span,.stApp [data-baseweb="input"] input{color:#172033!important;font-size:14px!important}
.stApp [data-baseweb="input"]>div{background:#fff!important;border:1px solid #CBD5E1!important;border-radius:8px!important;min-height:42px}
.stApp [data-baseweb="select"]>div:focus-within,.stApp [data-baseweb="input"]>div:focus-within{border-color:#2563EB!important;box-shadow:0 0 0 2px rgba(37,99,235,.12)!important}
.stApp .stButton>button,.stApp .stDownloadButton>button{min-height:40px;padding:7px 15px;border-radius:8px;font-size:13px;font-weight:650;transition:background .15s ease}
.stApp .stButton>button[kind="primary"]{background:#2563EB!important;color:#fff!important;border:1px solid #2563EB!important}.stApp .stButton>button[kind="primary"]:hover{background:#1D4ED8!important;border-color:#1D4ED8!important}
.stApp .stButton>button[kind="secondary"],.stApp .stDownloadButton>button{background:#fff!important;color:#334155!important;border:1px solid #CBD5E1!important}.stApp .stButton>button[kind="secondary"]:hover,.stApp .stDownloadButton>button:hover{background:#F1F5F9!important;border-color:#94A3B8!important;color:#0F172A!important}
.stApp [data-testid="stVerticalBlockBorderWrapper"]{border-color:#E2E8F0!important;border-radius:12px!important}.stApp [data-testid="stCaptionContainer"]{color:#64748B!important}.stApp hr{border-color:#E2E8F0!important}
@media(max-width:1250px){.dashboard-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:850px){.dashboard-grid,.card-grid,.packing-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){.dashboard-grid,.card-grid,.packing-grid{grid-template-columns:1fr}.block-container{padding:1.25rem 1rem 2rem}.page-header-title{font-size:24px}}
</style><div class="top-color-bar"></div>
""", unsafe_allow_html=True)

# LOAD CSV FILES

@st.cache_data
def load_data():
    data_dir = Path("data")
    paths = {
        "orders": data_dir / "orders.csv",
        "inventory": data_dir / "inventory.csv",
        "products": data_dir / "products.csv",
        "couriers": data_dir / "couriers.csv",
    }
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        st.error("Required CSV files are missing: " + ", ".join(missing))
        st.info("Place orders.csv, inventory.csv, products.csv and couriers.csv inside the data folder.")
        st.stop()
    try:
        data = {name: pd.read_csv(path) for name, path in paths.items()}
    except (pd.errors.ParserError, UnicodeDecodeError, OSError) as exc:
        st.error(f"Could not read a CSV file: {exc}")
        st.stop()
    if data["orders"].empty:
        st.error("orders.csv contains no orders.")
        st.stop()
    return data["orders"], data["inventory"], data["products"], data["couriers"]

orders_source, inventory, products, couriers = load_data()

required_order_columns = [
    "Order ID", "Order Time", "Deadline", "Customer", "SKU", "Product",
    "Variant", "Quantity", "Priority", "Status", "Courier", "Stock Status", "Issue"
]
for column in required_order_columns:
    if column not in orders_source.columns:
        orders_source[column] = ""
for column in ["Warehouse Location", "Staging Location"]:
    if column not in orders_source.columns:
        orders_source[column] = ""

warehouse_locations = [
    "A-01-01", "A-01-02", "A-01-03", "A-02-01", "A-02-02", "A-02-03",
    "B-01-01", "B-01-02", "B-01-03", "B-02-01", "B-02-02", "B-02-03"
]
for position, idx in enumerate(orders_source.index):
    loc = str(orders_source.at[idx, "Warehouse Location"]).strip()
    if not loc or loc.lower() == "nan":
        orders_source.at[idx, "Warehouse Location"] = warehouse_locations[position % len(warehouse_locations)]
    stage = str(orders_source.at[idx, "Staging Location"]).strip()
    if not stage or stage.lower() == "nan":
        status = str(orders_source.at[idx, "Status"]).strip()
        if status == "Staged": stage = f"Staging Bay {(position % 3) + 1}"
        elif status == "Ready for Pickup": stage = f"Pickup Rack {(position % 2) + 1}"
        elif status == "Waiting for Stock": stage = "Stock Hold"
        elif status in ["Shipped", "Delivered"]: stage = "—"
        else: stage = "Packing Area"
        orders_source.at[idx, "Staging Location"] = stage


# CALCULATIONS AND OPERATIONAL RULES

COMPLETED_STATUSES = {"Shipped", "Delivered"}
EMPTY_ISSUES = {"", "none", "nan", "null", "n/a", "na", "no issue"}

def clean_text(series):
    return series.fillna("").astype(str).str.strip()

def active_order_mask(df):
    return ~clean_text(df["Status"]).isin(COMPLETED_STATUSES)

def priority_mask(df):
    return clean_text(df["Priority"]).str.casefold().eq("priority")

def normalize_issue_series(df):
    issue = clean_text(df["Issue"])
    return issue.mask(issue.str.casefold().isin(EMPTY_ISSUES), "")

def issue_description(row):
    issue = str(row.get("Issue", "")).strip()
    if issue.casefold() in EMPTY_ISSUES:
        issue = ""
    if issue:
        return issue
    if str(row.get("Status", "")).strip() == "Waiting for Stock":
        return "Waiting for stock"
    stock_status = str(row.get("Stock Status", "")).strip()
    if stock_status and stock_status.casefold() not in {"available", "unknown"}:
        return "Stock unavailable"
    return ""

def issue_type(row):
    issue = issue_description(row).casefold()
    status = str(row.get("Status", "")).strip()
    if status == "Waiting for Stock" or any(x in issue for x in ["stock", "inventory", "transfer", "unavailable", "low stock"]):
        return "Stock"
    if any(x in issue for x in ["courier", "pickup", "dispatch", "delivery delay"]):
        return "Pickup"
    if any(x in issue for x in ["packing", "variant", "wrong product", "quantity"]):
        return "Packing"
    return "Other" if issue else ""

def issue_action_owner(row):
    kind, issue = issue_type(row), issue_description(row).casefold()
    if "transfer" in issue: return "Track / Complete Transfer", "Warehouse"
    if kind == "Stock": return "Check Stock Availability", "Warehouse"
    if kind == "Pickup": return "Confirm Courier Pickup", "Dispatch"
    if kind == "Packing": return "Resolve Packing Issue", "Packing"
    if kind == "Other": return "Review and Resolve", "Fulfillment Lead"
    return "—", "—"

def stock_issue_mask(df):
    stock = clean_text(df["Stock Status"]).str.casefold()
    status = clean_text(df["Status"])
    types = df.apply(issue_type, axis=1)
    return active_order_mask(df) & (stock.ne("available") | status.eq("Waiting for Stock") | types.eq("Stock"))

def pickup_issue_mask(df):
    return active_order_mask(df) & df.apply(issue_type, axis=1).eq("Pickup")

def operational_issue_mask(df):
    return active_order_mask(df) & (df.apply(issue_type, axis=1).ne("") | stock_issue_mask(df))

def refresh_derived(df, now=None):
    result = df.copy()
    now = now if now is not None else pd.Timestamp.now().floor("min")
    result["Order Time"] = pd.to_datetime(result["Order Time"], errors="coerce")
    result["Deadline"] = pd.to_datetime(result["Deadline"], errors="coerce")
    result["Priority"] = clean_text(result["Priority"]).replace("", "Normal")
    result["Status"] = clean_text(result["Status"]).replace("", "Picking")
    result["Stock Status"] = clean_text(result["Stock Status"]).replace("", "Unknown")
    result["Issue"] = normalize_issue_series(result)
    result["Minutes to Deadline"] = (result["Deadline"] - now).dt.total_seconds() / 60
    active = active_order_mask(result)
    result["Overdue"] = active & result["Deadline"].notna() & result["Minutes to Deadline"].lt(0)
    active = ~result["Status"].isin(["Shipped", "Delivered"])
    result["At Risk"] = (
        active
        & result["Deadline"].notna()
        & result["Deadline"].le(pd.Timestamp.now())
    )
    result["Deadline Status"] = "On Track"
    result.loc[result["Deadline"].isna(), "Deadline Status"] = "No Deadline"
    result.loc[active & result["Minutes to Deadline"].between(0, 60, inclusive="both"), "Deadline Status"] = "Due Soon"
    result.loc[result["Overdue"], "Deadline Status"] = "Overdue"
    result.loc[~active, "Deadline Status"] = "Completed"
    result["Issue Type"] = result.apply(issue_type, axis=1)
    result["Operational Issue"] = result.apply(issue_description, axis=1)
    action_owner = result.apply(issue_action_owner, axis=1)
    result["Action"] = action_owner.map(lambda item: item[0])
    result["Owner"] = action_owner.map(lambda item: item[1])
    result["Needs Action"] = operational_issue_mask(result)
    return result

def calculate_inventory(df):
    result = df.copy()
    for column in ["Main Warehouse", "Secondary Warehouse", "Reorder Level"]:
        if column not in result.columns: result[column] = 0
        result[column] = pd.to_numeric(result[column], errors="coerce").fillna(0)
    result["Total Stock"] = result["Main Warehouse"] + result["Secondary Warehouse"]
    result["Inventory Status"] = "In Stock"
    result.loc[result["Total Stock"] <= 0, "Inventory Status"] = "Out of Stock"
    result.loc[(result["Total Stock"] > 0) & (result["Total Stock"] <= result["Reorder Level"]), "Inventory Status"] = "Reorder Needed"
    return result

if "orders_working" not in st.session_state:
    st.session_state["orders_working"] = orders_source.copy()
st.session_state.setdefault("transfer_requests", [])
st.session_state.setdefault("action_log", [])
st.session_state.setdefault("packing_verification", {})
st.session_state.setdefault("success_message", "")
orders = refresh_derived(st.session_state["orders_working"])
st.session_state["orders_working"] = orders.copy()


# DISPLAY HELPERS

def html_block(content):
    st.markdown(content, unsafe_allow_html=True)

def page_header(title, subtitle=""):
    html_block(f'<div class="page-header-title">{escape(str(title))}</div>' + (f'<div class="page-subtitle">{escape(str(subtitle))}</div>' if subtitle else ''))

def section(title):
    html_block(f'<div class="section-heading-title">{escape(str(title))}</div>')

def cards(items, grid_class="card-grid"):
    output = f'<div class="{grid_class}">'
    for label, value, note, color in items:
        output += f'<div class="summary-card {escape(str(color))}"><div class="card-label">{escape(str(label))}</div><div class="card-value">{escape(str(value))}</div><div class="card-note">{escape(str(note))}</div></div>'
    html_block(output + '</div>')

def status_badge(value):
    value = str(value) if pd.notna(value) else "—"
    classes = {"Picking":"status-picking","Packed":"status-packed","Staged":"status-staged","Ready for Pickup":"status-ready","Waiting for Stock":"status-waiting","Shipped":"status-complete","Delivered":"status-complete"}
    return f'<span class="badge {classes.get(value, "status-default")}">{escape(value)}</span>'

def priority_badge(value):
    return '<span class="badge priority-badge">PRIORITY</span>' if str(value).strip().casefold() == "priority" else '<span class="badge normal-badge">Normal</span>'

def issue_badge(value):
    value = str(value) if pd.notna(value) else ""
    low = value.casefold()
    css = "issue-danger" if any(x in low for x in ["unavailable", "missing"]) else "issue-warning" if any(x in low for x in ["stock", "inventory", "transfer", "courier", "pickup", "delay"]) else "issue-neutral"
    return f'<span class="badge {css}">{escape(value or "—")}</span>'

def cell(column, value):
    if pd.isna(value): value = ""
    if column == "Order ID": return f'<span class="order-id">{escape(str(value))}</span>'
    if column == "Priority": return priority_badge(value)
    if column == "Status": return status_badge(value)
    if column in ["Issue", "Operational Issue"]: return issue_badge(value)
    if column == "Action": return f'<span class="issue-action">{escape(str(value))}</span>'
    if column == "Owner": return f'<span class="owner-badge">{escape(str(value))}</span>'
    if column == "Warehouse Location": return f'<span class="location-badge">{escape(str(value))}</span>'
    if column == "Staging Location": return f'<span class="location-stage">{escape(str(value))}</span>'
    if column == "Packing Verified": return '<span class="badge status-complete">Verified</span>' if bool(value) else '<span class="badge normal-badge">Pending</span>'
    if column in ["At Risk", "Overdue"]:
        return f'<span class="badge {"issue-danger" if bool(value) else "normal-badge"}">{("OVERDUE" if column == "Overdue" else "YES") if bool(value) else "No"}</span>'
    if column == "Stock Status":
        text = str(value).strip() or "Unknown"
        key = text.casefold()
        css = "status-complete" if key == "available" else "issue-warning" if key in {"transfer required", "transfer pending", "low stock"} else "issue-danger"
        return f'<span class="badge {css}">{escape(text)}</span>'
    
    if column == "Deadline Status":
        deadline_classes = {
            "Overdue": "deadline-overdue",
            "Due Soon": "deadline-soon",
            "On Track": "deadline-track",
            "Completed": "deadline-completed",
            "No Deadline": "deadline-none",
        }
        status = str(value).strip()
        css_class = deadline_classes.get(status, "deadline-none")
        return (
            f'<span class="badge {css_class}">'
            f'{escape(status)}</span>'
        )

    return escape(str(value))

def table(df, table_key="table"):
    if df is None or df.empty:
        html_block('<div class="empty-state">No records to display.</div>')
        return
    data = df.copy().reset_index(drop=True)
    total = len(data)
    state_key = f"table_show_all_{table_key}"
    show_all = bool(st.session_state.get(state_key, False))
    display = data if total <= 5 or show_all else data.head(5)
    for column in display.columns:
        if pd.api.types.is_datetime64_any_dtype(display[column]):
            display[column] = display[column].dt.strftime("%Y-%m-%d %H:%M")
    headers = "".join(f"<th>{escape(str(c))}</th>" for c in display.columns)
    rows = []
    for _, row in display.iterrows():
        rows.append("<tr>" + "".join(f"<td>{cell(c, row[c])}</td>" for c in display.columns) + "</tr>")
    html_block(f'<div class="table-card"><table class="fh-table"><thead><tr>{headers}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    if total > 5:
        left, right = st.columns([9, 1])
        with left: st.caption(f"Showing 1–{total if show_all else 5} of {total}")
        with right:
            if st.button("Show first 5" if show_all else "Show all", key=f"{table_key}_toggle"):
                st.session_state[state_key] = not show_all
                st.rerun()

def issue_table(df, table_key="issues"):
    data = df.copy()
    data["Issue"] = data["Operational Issue"].replace("", "Needs attention")
    columns = ["Order ID", "Issue", "Priority", "Status", "Action", "Owner", "Warehouse Location", "Staging Location"]
    for col in columns:
        if col not in data: data[col] = ""
    table(data[columns], table_key)


# ACTION LOG AND SAVING

DERIVED_COLUMNS = ["Minutes to Deadline", "Overdue", "At Risk", "Deadline Status", "Issue Type", "Operational Issue", "Needs Action", "Action", "Owner"]

def add_action_log(order_id, action, detail=""):
    st.session_state["action_log"].append({"Time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), "Order ID": str(order_id), "Action": action, "Details": detail})

def save_orders_to_csv():
    output = st.session_state["orders_working"].drop(columns=DERIVED_COLUMNS, errors="ignore")
    output_path = Path("data/orders.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)
    load_data.clear()

def set_order_fields(order_id, **fields):
    working = st.session_state["orders_working"].copy()
    mask = working["Order ID"].astype(str).eq(str(order_id))
    for column, value in fields.items():
        if column not in working.columns: working[column] = ""
        working.loc[mask, column] = value
    st.session_state["orders_working"] = working

def packing_verified(order_id):
    return bool(st.session_state["packing_verification"].get(str(order_id), False))

# PACKING VERIFICATION

def normalized(value):
    return " ".join(str(value).strip().casefold().split())

def render_packing_verification(df):
    section("Packing Verification")
    active = df[active_order_mask(df)].copy()
    if active.empty:
        html_block('<div class="empty-state">There are no active orders available for packing verification.</div>')
        return
    selected = st.selectbox("Order to verify", active["Order ID"].astype(str).tolist(), key="packing_verify_order")
    row = active[active["Order ID"].astype(str).eq(str(selected))].iloc[0]
    html_block(f'<div class="verification-card"><div class="verification-order">Order {escape(str(row["Order ID"]))}</div><div class="verification-expected"><b>Expected order details</b><br>Product: {escape(str(row["Product"]))} &nbsp; | &nbsp; Variant: {escape(str(row["Variant"]))} &nbsp; | &nbsp; Quantity: {escape(str(row["Quantity"]))}</div></div>')
    product_options = products["Product"].dropna().astype(str).tolist() if "Product" in products.columns else []
    product_options = sorted(set(product_options + active["Product"].dropna().astype(str).tolist()))
    if not product_options:
        st.warning("No products are available for verification.")
        return
    c1, c2, c3 = st.columns([2.2, 2, 1])
    with c1:
        expected_product = str(row["Product"])
        product_index = product_options.index(expected_product) if expected_product in product_options else 0
        packed_product = st.selectbox("Packed Product", product_options, index=product_index, key="packed_product")
    variants = []
    if {"Product", "Variants"}.issubset(products.columns):
        matched = products[products["Product"].astype(str).eq(str(packed_product))]
        if not matched.empty:
            variants = [x.strip() for x in str(matched.iloc[0]["Variants"]).split("|") if x.strip()]
    if not variants:
        variants = sorted(set(active.loc[active["Product"].astype(str).eq(str(packed_product)), "Variant"].dropna().astype(str).tolist()))
    if not variants: variants = [str(row["Variant"])]
    with c2:
        expected_variant = str(row["Variant"])
        variant_index = variants.index(expected_variant) if packed_product == str(row["Product"]) and expected_variant in variants else 0
        packed_variant = st.selectbox("Packed Variant", variants, index=variant_index, key="packed_variant")
    try: expected_quantity = int(float(row["Quantity"]))
    except (ValueError, TypeError): expected_quantity = 1
    with c3:
        packed_quantity = st.number_input("Packed Quantity", min_value=0, value=expected_quantity, step=1, key="packed_quantity")
    if st.button("Verify Packing", key="verify_packing", type="primary"):
        checks = [normalized(packed_product) == normalized(row["Product"]), normalized(packed_variant) == normalized(row["Variant"]), int(packed_quantity) == expected_quantity]
        st.session_state["packing_verification"][str(selected)] = all(checks)
        if all(checks):
            st.success("Packing verified. Product, variant and quantity match.")
        else:
            problems = [label for passed, label in zip(checks, ["Product does not match", "Variant does not match", "Quantity does not match"]) if not passed]
            st.error(" | ".join(problems) + ". Correct the packed item.")
    if packing_verified(selected):
        html_block('<div class="verification-result verification-pass">This order is currently marked as verified in this session.</div>')


# WORKFLOW AND COURIER RECOMMENDATIONS

def workflow(df):
    total = len(df)
    stages = [("Picking", "Items being picked from inventory"), ("Packed", "Orders packed and ready for staging"), ("Staged", "Packed boxes waiting for handoff"), ("Ready for Pickup", "Ready for courier collection"), ("Shipped", "Courier handoff completed"), ("Delivered", "Successfully delivered")]
    section("Fulfillment Workflow")
    output = '<div class="workflow-flow">'
    for name, desc in stages:
        count = int(clean_text(df["Status"]).eq(name).sum())
        pct = round(count / total * 100) if total else 0
        output += f'<div class="workflow-stage"><div class="stage-name">{escape(name)}</div><div class="stage-count">{count}</div><div class="stage-percent">{pct}%</div><div class="stage-description">{escape(desc)}</div></div>'
    html_block(output + '</div>')

def recommend_courier(courier_df):
    if courier_df.empty: return pd.DataFrame()
    result = courier_df.copy().rename(columns={"Courier": "Courier Name"})
    required = ["Courier Name", "Cost per Order", "Delivery Days", "Pickup Time"]
    for col in required:
        if col not in result.columns: result[col] = "Not available"
    result["Cost per Order"] = pd.to_numeric(result["Cost per Order"], errors="coerce")
    result["Delivery Days"] = pd.to_numeric(result["Delivery Days"], errors="coerce")
    cheapest, fastest = result["Cost per Order"].min(), result["Delivery Days"].min()
    def recommendation(row):
        low = pd.notna(cheapest) and row["Cost per Order"] == cheapest
        fast = pd.notna(fastest) and row["Delivery Days"] == fastest
        if low and fast: return "Fastest and lowest cost"
        if fast: return "Fastest delivery"
        if low: return "Lowest cost"
        return "Alternative option"
    result["Recommendation"] = result.apply(recommendation, axis=1)
    return result.sort_values(["Delivery Days", "Cost per Order"], na_position="last")[["Courier Name", "Cost per Order", "Delivery Days", "Pickup Time", "Recommendation"]]


# NAVIGATION

pages = ["Dashboard", "Orders", "Inventory", "Packing & Pickup"]
if st.session_state.get("page") not in pages: st.session_state["page"] = "Dashboard"
with st.sidebar:
    st.markdown('<div class="sidebar-title">Fulfillment Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="workspace-label">OPERATIONS WORKSPACE</div>', unsafe_allow_html=True)
    st.divider()
    selected_page = st.radio("Navigation", pages, index=pages.index(st.session_state["page"]), key="page_radio", label_visibility="collapsed")
    st.session_state["page"] = selected_page
with st.expander("How to use Fulfillment Hub", expanded=False):
    st.markdown("1. Check **Dashboard** for orders needing attention.\n2. Open **Orders** to search and update an order.\n3. Use **Packing & Pickup** to verify product, variant and quantity.\n4. Click **Save Changes** after updating orders to save them to the CSV.")


# DASHBOARD PAGE

if st.session_state["page"] == "Dashboard":
    page_header("Dashboard")
    cards([
        ("Total Orders", len(orders), "All current orders", "blue"),
        ("Priority Orders", int(priority_mask(orders).sum()), "High-priority orders", "purple"),
        ("Orders At Risk", int(orders["At Risk"].sum()), "Priority orders overdue or due within 60 minutes", "red"),
        ("Stock Issues", int(stock_issue_mask(orders).sum()), "Active orders needing stock action", "orange"),
        ("Pickup Issues", int(pickup_issue_mask(orders).sum()), "Active courier or pickup issues", "teal"),
    ], "dashboard-grid")
    st.markdown("<br>", unsafe_allow_html=True)
    section("Needs Action")
    issues = orders[operational_issue_mask(orders)].copy()
    if issues.empty: html_block('<div class="empty-state">No orders currently need action.</div>')
    else:
        issues["_sort"] = 4
        text = issues["Operational Issue"].str.casefold()
        issues.loc[text.str.contains("unavailable|missing", na=False), "_sort"] = 1
        issues.loc[issues["Status"].eq("Waiting for Stock"), "_sort"] = 2
        issues.loc[text.str.contains("courier|pickup|delay", na=False), "_sort"] = 3
        issues = issues.sort_values(["_sort", "Deadline"], na_position="last")
        issue_table(issues, "dashboard_issues")
    st.markdown("<br>", unsafe_allow_html=True)
    section("Deadline Attention")
    order = {"Overdue": 0, "Due Soon": 1, "On Track": 2, "No Deadline": 3, "Completed": 4}
    attention = orders.copy()
    attention["_sort"] = attention["Deadline Status"].map(order)
    attention = attention.sort_values(["_sort", "Deadline"], na_position="last")
    table(attention[["Order ID", "Customer", "Product", "Priority", "Status", "Deadline", "Deadline Status"]], "dashboard_deadlines")
    st.markdown("<br>", unsafe_allow_html=True)
    section("Courier Overview")
    summary = orders.groupby("Courier", dropna=False).agg(Orders=("Order ID", "count"), Active=("Status", lambda values: int((~values.fillna("").isin(COMPLETED_STATUSES)).sum()))).reset_index()
    pickup_counts = orders.assign(_PickupIssue=pickup_issue_mask(orders)).groupby("Courier", dropna=False)["_PickupIssue"].sum()
    summary["Pickup Issues"] = summary["Courier"].map(pickup_counts).fillna(0).astype(int)
    summary["Courier"] = summary["Courier"].fillna("Unassigned")
    summary = summary.sort_values(["Pickup Issues", "Orders"], ascending=[False, False])
    table(summary[["Courier", "Orders", "Active", "Pickup Issues"]], "dashboard_couriers")
    st.markdown("<br>", unsafe_allow_html=True)
    section("Recent Orders")
    recent = orders.sort_values("Order Time", ascending=False).head(10).copy()
    recent["Packing Verified"] = recent["Order ID"].astype(str).map(packing_verified)
    table(recent[["Order ID", "Product", "Priority", "Status", "Courier", "Warehouse Location", "Staging Location", "Packing Verified", "At Risk"]], "dashboard_recent")


# ORDERS PAGE

elif st.session_state["page"] == "Orders":
    page_header("Orders")
    cards([
        ("Total Orders", len(orders), "All current orders", "blue"),
        ("Priority Orders", int(priority_mask(orders).sum()), "High-priority orders", "purple"),
        ("Orders At Risk", int(orders["At Risk"].sum()), "Priority orders overdue or due within 60 minutes", "red"),
        ("Overdue", int(orders["Overdue"].sum()), "Active orders past deadline", "orange"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    section("Find an Order")
    c1, c2, c3, c4 = st.columns([2.3, 1, 1, 1])
    with c1: search = st.text_input("Search", placeholder="Order ID or customer", label_visibility="collapsed", key="order_search")
    with c2: priority_filter = st.selectbox("Priority", ["All", "Priority", "Normal"], label_visibility="collapsed", key="order_priority")
    with c3:
        status_filter = st.selectbox("Status", ["All"] + sorted(orders["Status"].dropna().astype(str).unique().tolist()), label_visibility="collapsed", key="order_status")
    with c4:
        courier_filter = st.selectbox("Courier", ["All"] + sorted(orders["Courier"].dropna().astype(str).unique().tolist()), label_visibility="collapsed", key="order_courier")
    risk_filter = st.checkbox("Show only orders at risk", key="order_risk_filter")
    filtered = orders.copy()
    if search:
        term = search.casefold().strip()
        filtered = filtered[filtered["Order ID"].astype(str).str.casefold().str.contains(term, na=False, regex=False) | filtered["Customer"].astype(str).str.casefold().str.contains(term, na=False, regex=False)]
    if priority_filter != "All": filtered = filtered[clean_text(filtered["Priority"]).str.casefold().eq(priority_filter.casefold())]
    if status_filter != "All": filtered = filtered[filtered["Status"].eq(status_filter)]
    if courier_filter != "All": filtered = filtered[filtered["Courier"].eq(courier_filter)]
    if risk_filter: filtered = filtered[filtered["At Risk"]]
    if filtered.empty: html_block('<div class="empty-state">No orders match the selected filters.</div>')
    else:
        filtered = filtered.copy()
        filtered["Packing Verified"] = filtered["Order ID"].astype(str).map(packing_verified)
        table(filtered[["Order ID", "Customer", "Product", "Variant", "Quantity", "Priority", "Status", "Warehouse Location", "Staging Location", "Deadline", "Courier", "Stock Status", "Packing Verified", "At Risk"]], "orders_list")
    st.markdown("<br>", unsafe_allow_html=True)
    
    section("Update an Order")

    with st.container(border=True):
        order_ids = orders["Order ID"].astype(str).tolist()

        selected_order = st.selectbox(
            "Order to update", order_ids, key="manage_order_id"
        )

        manage_row = orders[
            orders["Order ID"].astype(str).eq(str(selected_order))
        ].iloc[0]

        status_options = [
            "Picking", "Packed", "Staged", "Ready for Pickup",
            "Waiting for Stock", "Shipped", "Delivered"
        ]

        current_status = str(manage_row["Status"])
        status_index = (
            status_options.index(current_status)
            if current_status in status_options else 0
        )

        new_status = st.selectbox(
            "New status",
            status_options,
            index=status_index,
            key="manage_new_status"
        )
        
    if st.button("Update Status", key="update_order_status", type="primary"):

        if current_status == new_status:
            st.info(f"{selected_order} is already {new_status}.")

        else:
            set_order_fields(selected_order, Status=new_status)

            add_action_log(
                selected_order,
                "Status updated",
                f"{current_status} → {new_status}"
            )

            st.session_state["status_update_notice"] = (
                f"{selected_order} status updated successfully. "
                "Click Save Changes to save the update."
            )

            st.rerun()

    if st.session_state.get("status_update_notice"):
        st.success(st.session_state["status_update_notice"])
        st.session_state["status_update_notice"] = None

    st.divider()        
        
    section("Fulfillment Actions")
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button("Mark Stock Moved", key="mark_stock_moved", type="secondary", use_container_width=True):
            set_order_fields(selected_order, **{"Stock Status": "Available", "Status": "Picking", "Issue": ""})
            add_action_log(selected_order, "Stock moved", "Stock marked available; issue cleared")
            st.session_state["success_message"] = "Stock action recorded. Save changes to persist it."
            st.rerun()
    with action_col2:
        if st.button("Confirm Courier Pickup", key="confirm_courier_pickup", type="secondary", use_container_width=True):
            set_order_fields(selected_order, **{"Status": "Shipped", "Issue": ""})
            add_action_log(selected_order, "Courier pickup confirmed", "Order marked shipped")
            st.session_state["success_message"] = "Pickup recorded. Save changes to persist it."
            st.rerun()
    if st.button("Request Stock Transfer", key="request_stock_transfer", type="secondary"):
        existing = [x for x in st.session_state["transfer_requests"] if x["Order ID"] == str(selected_order) and x["Status"] == "Requested"]
        if not existing:
            st.session_state["transfer_requests"].append({"Order ID": str(selected_order), "Product": str(manage_row.get("Product", "")), "SKU": str(manage_row.get("SKU", "")), "Quantity": manage_row.get("Quantity", ""), "Requested At": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), "Status": "Requested"})
            add_action_log(selected_order, "Stock transfer requested", str(manage_row.get("Product", "")))
        st.session_state["success_message"] = "Transfer request added."
        st.rerun()
    if st.session_state["transfer_requests"]:
        section("Stock Transfer Requests")
        transfer_df = pd.DataFrame(st.session_state["transfer_requests"])
        table(transfer_df, "stock_transfer_requests")
        st.download_button("Download Transfer List", transfer_df.to_csv(index=False).encode("utf-8"), file_name="stock_transfer_requests.csv", mime="text/csv")
    st.divider()
    save_col, history_col = st.columns([1, 2])
    with save_col:
        if st.button("Save Changes", key="save_order_changes", type="primary", use_container_width=True):
            try:
                save_orders_to_csv()
                if st.session_state["action_log"]:
                    pd.DataFrame(st.session_state["action_log"]).to_csv("data/action_log.csv", index=False)
                st.session_state["success_message"] = "Changes saved to data/orders.csv."
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save changes: {exc}")
    with history_col:
        if st.session_state["action_log"]:
            log_df = pd.DataFrame(st.session_state["action_log"])
            st.download_button("Download Action History", log_df.to_csv(index=False).encode("utf-8"), file_name="action_log.csv", mime="text/csv")


# INVENTORY PAGE

elif st.session_state["page"] == "Inventory":
    page_header("Inventory")
    available_orders = int((active_order_mask(orders) & clean_text(orders["Stock Status"]).str.casefold().eq("available")).sum())
    stock_count = int(stock_issue_mask(orders).sum())
    waiting_count = int(clean_text(orders["Status"]).eq("Waiting for Stock").sum())
    cards([("Inventory Records", len(inventory), "Current inventory records", "blue"), ("Orders with Stock", available_orders, "Active orders marked available", "green"), ("Stock Issues", stock_count, "Active orders needing stock action", "red"), ("Waiting for Stock", waiting_count, "Orders currently blocked", "orange")])
    st.markdown("<br>", unsafe_allow_html=True)
    section("Orders Blocked by Stock")
    blocked = orders[stock_issue_mask(orders)].copy()
    if blocked.empty: html_block('<div class="empty-state">No inventory blockers found.</div>')
    else:
        blocked["Issue"] = blocked["Operational Issue"]
        cols = ["Order ID", "SKU", "Product", "Quantity", "Status", "Warehouse Location", "Stock Status", "Issue", "Action", "Owner"]
        for col in cols:
            if col not in blocked: blocked[col] = ""
        table(blocked[cols], "inventory_blocked")
    st.markdown("<br>", unsafe_allow_html=True)
    section("Inventory Records")
    search_col, clear_col = st.columns([5, 1])
    with search_col: inventory_search = st.text_input("Search Inventory", placeholder="Search by SKU or product", label_visibility="collapsed", key="inventory_search")
    with clear_col:
        if inventory_search and st.button("Clear", key="clear_inventory_search"):
            st.session_state["inventory_search"] = ""
            st.rerun()
    inventory_calculated = calculate_inventory(inventory)
    inventory_filtered = inventory_calculated.copy()
    if inventory_search:
        term = inventory_search.casefold().strip()
        matches = inventory_filtered.astype(str).apply(lambda row: row.str.casefold().str.contains(term, na=False, regex=False).any(), axis=1)
        inventory_filtered = inventory_filtered[matches]
    st.caption(f"Showing {len(inventory_filtered)} of {len(inventory)} inventory records")
    display_cols = ["SKU", "Product", "Main Warehouse", "Secondary Warehouse", "Total Stock", "Reorder Level", "Inventory Status"]
    for col in display_cols:
        if col not in inventory_filtered: inventory_filtered[col] = ""
    table(inventory_filtered[display_cols], "inventory_records")


# PACKING & PICKUP PAGE

elif st.session_state["page"] == "Packing & Pickup":
    page_header("Packing & Pickup")
    waiting_count = int(clean_text(orders["Status"]).eq("Waiting for Stock").sum())
    pickup_count = int(pickup_issue_mask(orders).sum())
    cards([("Total Orders", len(orders), "All current orders", "blue"), ("Waiting for Stock", waiting_count, "Orders blocked by stock", "orange"), ("Pickup Issues", pickup_count, "Active courier or pickup issues", "red")], "packing-grid")
    st.markdown("<br>", unsafe_allow_html=True)
    workflow(orders)
    st.markdown("<br>", unsafe_allow_html=True)
    render_packing_verification(orders)
    st.markdown("<br>", unsafe_allow_html=True)
    section("Pickup Issues")
    pickup_orders = orders[pickup_issue_mask(orders)].copy()
    if pickup_orders.empty: html_block('<div class="empty-state">No courier or pickup issues reported.</div>')
    else:
        pickup_orders["Issue"] = pickup_orders["Operational Issue"]
        pickup_cols = ["Order ID", "Customer", "Product", "Status", "Staging Location", "Courier", "Deadline", "Issue", "Action", "Owner"]
        table(pickup_orders[pickup_cols], "pickup_issues")
    st.markdown("<br>", unsafe_allow_html=True)
    section("Courier Suggestions")
    recommendations = recommend_courier(couriers)
    if recommendations.empty: st.info("No courier details available.")
    else: table(recommendations, "courier_recommendations")
    st.markdown("<br>", unsafe_allow_html=True)
    section("Package Search")
    c1, c2, c3 = st.columns([2.3, 1, 1])
    with c1: tracking_search = st.text_input("Search", placeholder="Order ID or customer", label_visibility="collapsed", key="tracking_search")
    with c2: tracking_status = st.selectbox("Status", ["All", "Picking", "Packed", "Staged", "Ready for Pickup", "Waiting for Stock", "Shipped", "Delivered"], label_visibility="collapsed", key="tracking_status")
    with c3: tracking_courier = st.selectbox("Courier", ["All"] + sorted(orders["Courier"].dropna().astype(str).unique().tolist()), label_visibility="collapsed", key="tracking_courier")
    packages = orders.copy()
    if tracking_search:
        term = tracking_search.casefold().strip()
        packages = packages[packages["Order ID"].astype(str).str.casefold().str.contains(term, na=False, regex=False) | packages["Customer"].astype(str).str.casefold().str.contains(term, na=False, regex=False)]
    if tracking_status != "All": packages = packages[packages["Status"].eq(tracking_status)]
    if tracking_courier != "All": packages = packages[packages["Courier"].eq(tracking_courier)]
    if packages.empty: html_block('<div class="empty-state">No packages match the selected filters.</div>')
    else:
        packages = packages.copy()
        packages["Packing Verified"] = packages["Order ID"].astype(str).map(packing_verified)
        table(packages[["Order ID", "Customer", "Product", "Quantity", "Status", "Warehouse Location", "Staging Location", "Courier", "Deadline", "Stock Status", "Packing Verified"]], "package_list")
    if st.session_state["action_log"]:
        st.markdown("<br>", unsafe_allow_html=True)
        section("Recent Actions")
        table(pd.DataFrame(st.session_state["action_log"][-20:][::-1]), "recent_action_log")
