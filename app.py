import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Sistema de Administración - Maicitos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)# Custom Premium Styling (tienda.maicitos.com theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    /* Global Background and Fonts */
    html, body {
        font-family: 'Poppins', sans-serif !important;
        background-color: #faf8f0 !important;
        background-image: none !important;
        color: #2e1b12 !important;
        overflow-x: hidden;
    }
    
    body::before, body::after {
        content: none !important;
        display: none !important;
    }
    
    .stApp {
        font-family: 'Poppins', sans-serif !important;
        color: #2e1b12 !important;
        background-color: #faf8f0 !important;
    }
    
    /* Make layout containers transparent to reveal background */
    [data-testid="stAppViewContainer"], 
    [data-testid="stMain"], 
    [data-testid="stMainBlockContainer"], 
    .block-container, 
    [data-testid="stVerticalBlock"], 
    [data-testid="stVerticalBlockBorderWrapper"],
    div[role="tabpanel"],
    div[data-baseweb="tab-panel"] {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #ffd200 !important;
        border-bottom: 2px solid #2e1b12 !important;
    }
    
    /* Columns styled as product cards with border */
    div[data-testid="column"] {
        background: #ffffff !important;
        border: 1px solid #e5e0d8 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(46, 27, 18, 0.03) !important;
        margin-bottom: 20px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="column"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(46, 27, 18, 0.06) !important;
    }
    
    /* Sidebar styling as warm light beige panel (so black logo is visible) */
    section[data-testid="stSidebar"] {
        background-color: #f3ede2 !important;
        border-right: 2px solid #ffd200 !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #2e1b12 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span:not([data-testid="stIconMaterial"]) {
        color: #2e1b12 !important;
    }
    /* Collapse button arrow color and persistent visibility */
    section[data-testid="stSidebar"] button[data-testid="stSidebarCollapseButton"] span {
        color: #2e1b12 !important;
    }
    div[data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarCollapseButton"] {
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Text elements readability */
    .stApp p, .stApp label, .stApp li, .stApp div[data-testid="stMarkdownContainer"] p {
        color: #2e1b12 !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        color: #2e1b12 !important;
        font-weight: 700 !important;
    }
    
    .main-title {
        color: #2e1b12 !important;
        font-weight: 800;
        font-size: 2.6rem;
        margin-bottom: 0.1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .main-subtitle {
        color: #6d5b52;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Metrics cards */
    div[data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #e5e0d8 !important;
        padding: 20px;
        border-radius: 16px !important;
        box-shadow: 0 4px 15px rgba(46, 27, 18, 0.03) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(46, 27, 18, 0.06) !important;
    }
    div[data-testid="stMetricValue"] {
        color: #2e1b12 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #6d5b52 !important;
        font-weight: 600 !important;
    }
    
    /* Form containers */
    div[data-testid="stForm"] {
        background: #ffffff !important;
        border: 1px solid #e5e0d8 !important;
        padding: 30px;
        border-radius: 20px !important;
        box-shadow: 0 6px 20px rgba(46, 27, 18, 0.04) !important;
    }
    
    /* Buttons - Gold capsules with dark brown text */
    div.stButton > button {
        background-color: #ffd200 !important;
        color: #2e1b12 !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        padding: 10px 28px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px 12px rgba(255, 210, 0, 0.2) !important;
        letter-spacing: 0.5px !important;
    }
    div.stButton > button:hover {
        background-color: #f4c400 !important;
        transform: scale(1.03) !important;
        box-shadow: 0 6px 15px rgba(255, 210, 0, 0.3) !important;
        color: #2e1b12 !important;
        border: none !important;
    }
    div.stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* Primary buttons (Delete, Reset, Warning) */
    div.stButton > button[kind="primary"] {
        background-color: #ffebee !important;
        color: #c62828 !important;
        border: 1px solid #ffcdd2 !important;
        box-shadow: 0 4px 12px rgba(198, 40, 40, 0.1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #c62828 !important;
        color: #ffffff !important;
        box-shadow: 0 6px 15px rgba(198, 40, 40, 0.2) !important;
    }

    /* Input fields styling */
    .stApp input, .stApp select, .stApp textarea, .stApp div[role="textbox"], .stApp div[data-baseweb="select"] {
        color: #2e1b12 !important;
        background-color: #ffffff !important;
        border: 1px solid #e5e0d8 !important;
        border-radius: 12px !important;
        box-shadow: inset 0 2px 4px rgba(46, 27, 18, 0.02) !important;
        transition: all 0.3s ease !important;
    }
    .stApp input:focus, .stApp select:focus, .stApp textarea:focus {
        border-color: #ffd200 !important;
        box-shadow: 0 0 0 2px rgba(255, 210, 0, 0.2) !important;
    }
    
    /* Option lists inside selectors */
    div[data-baseweb="menu"] li, div[data-baseweb="popover"] div {
        color: #2e1b12 !important;
    }
    
    /* Badges */
    .badge-green {
        background-color: #e3ebd6 !important;
        color: #558b2f !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        display: inline-block !important;
        border: 1px solid rgba(85, 139, 47, 0.15) !important;
    }
    .badge-orange {
        background-color: #fff6cc !important;
        color: #f57f17 !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        display: inline-block !important;
        border: 1px solid rgba(245, 127, 23, 0.15) !important;
    }
    .badge-red {
        background-color: #ffebee !important;
        color: #c62828 !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        display: inline-block !important;
        border: 1px solid rgba(198, 40, 40, 0.15) !important;
    }
    
    /* Tabs styled matching brand identity and made sticky */
    div[data-baseweb="tab-list"],
    div[role="tablist"] {
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 56px !important;
        z-index: 999 !important;
        background-color: #faf8f0 !important;
        padding: 10px 0 !important;
        border-bottom: 2px solid #ffd200 !important;
        display: flex !important;
        width: 100% !important;
    }
    
    /* Secondary (nested) tab list container */
    div[data-baseweb="tab-panel"] div[data-baseweb="tab-list"],
    div[data-baseweb="tab-panel"] div[role="tablist"],
    div[role="tabpanel"] div[data-baseweb="tab-list"],
    div[role="tabpanel"] div[role="tablist"] {
        top: 114px !important; /* Stacked below main tabs */
        z-index: 998 !important;
        border-bottom: 1.5px solid #2e1b12 !important;
        padding: 6px 0 !important;
        background-color: #faf8f0 !important;
    }
    
    button[data-baseweb="tab-list"] {
        background-color: #e5e0d8 !important;
        border-radius: 12px !important;
        padding: 4px !important;
    }
    button[data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif !important;
        color: #2e1b12 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffd200 !important;
        color: #2e1b12 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# File names
PROD_FILE = "productos.csv"
REC_FILE = "recibos.csv"
CLI_FILE = "clientes.csv"
GAS_FILE = "gastos.csv"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1A0BJg_Xr6BvhELp3vM6zeB4XSipcdeQTGGBgXENebq0/edit"
SHEET_EXPORT_URL = "https://docs.google.com/spreadsheets/d/1A0BJg_Xr6BvhELp3vM6zeB4XSipcdeQTGGBgXENebq0/export?format=csv"

# Global states
use_gsheets = False
sh = None
worksheet = None

# Safe imports for custom service account client in case cryptography compilation is broken locally
try:
    import urllib.request
    import urllib.parse
    import base64
    from Crypto.PublicKey import RSA
    from Crypto.Signature import pkcs1_15
    from Crypto.Hash import SHA256
    has_custom_libs = True
except ImportError:
    has_custom_libs = False

def b64encode(data):
    return base64.urlsafe_b64encode(data).decode('utf-8').replace('=', '')

def get_access_token(creds_dict):
    header = {"alg": "RS256", "typ": "JWT"}
    now = int(time.time()) if 'time' in globals() else int(datetime.now().timestamp())
    payload = {
        "iss": creds_dict["client_email"],
        "scope": "https://www.googleapis.com/auth/spreadsheets",
        "aud": creds_dict["token_uri"],
        "exp": now + 3600,
        "iat": now
    }
    
    encoded_header = b64encode(json.dumps(header).encode('utf-8'))
    encoded_payload = b64encode(json.dumps(payload).encode('utf-8'))
    signing_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    
    key = RSA.import_key(creds_dict["private_key"])
    h = SHA256.new(signing_input)
    signature = pkcs1_15.new(key).sign(h)
    encoded_signature = b64encode(signature)
    
    jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    
    post_data = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token
    }).encode('utf-8')
    
    req = urllib.request.Request(creds_dict["token_uri"], data=post_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res["access_token"]

class CustomWorksheet:
    def __init__(self, spreadsheet_id, sheet_name, sheet_id, access_token):
        self.spreadsheet_id = spreadsheet_id
        self.title = sheet_name
        self.sheet_id = sheet_id
        self.access_token = access_token
        
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
    def get_all_values(self):
        safe_name = urllib.parse.quote(self.title)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{safe_name}?valueRenderOption=FORMATTED_VALUE"
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                return res.get("values", [])
        except Exception as e:
            raise Exception(f"Error reading values: {e}")
            
    def append_row(self, row, value_input_option="USER_ENTERED"):
        safe_name = urllib.parse.quote(self.title)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{safe_name}:append?valueInputOption={value_input_option}"
        body = json.dumps({
            "values": [row]
        }).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                return True
        except Exception as e:
            raise Exception(f"Error appending row: {e}")
            
    def update_cell(self, row, col, value):
        col_letter = self._col_to_letter(col)
        cell_range = f"{self.title}!{col_letter}{row}"
        safe_range = urllib.parse.quote(cell_range)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{safe_range}?valueInputOption=USER_ENTERED"
        body = json.dumps({
            "values": [[value]]
        }).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers=self._headers(), method="PUT")
        try:
            with urllib.request.urlopen(req) as response:
                return True
        except Exception as e:
            raise Exception(f"Error updating cell: {e}")
            
    def clear(self):
        safe_name = urllib.parse.quote(self.title)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{safe_name}:clear"
        req = urllib.request.Request(url, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                return True
        except Exception as e:
            raise Exception(f"Error clearing sheet: {e}")
            
    def update(self, range_name, values):
        full_range = f"{self.title}!{range_name}"
        safe_range = urllib.parse.quote(full_range)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{safe_range}?valueInputOption=USER_ENTERED"
        body = json.dumps({
            "values": values
        }).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers=self._headers(), method="PUT")
        try:
            with urllib.request.urlopen(req) as response:
                return True
        except Exception as e:
            raise Exception(f"Error updating range: {e}")
            
    def delete_rows(self, row_idx):
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}:batchUpdate"
        body = json.dumps({
            "requests": [{
                "deleteDimension": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "dimension": "ROWS",
                        "startIndex": row_idx - 1,
                        "endIndex": row_idx
                    }
                }
            }]
        }).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                return True
        except Exception as e:
            raise Exception(f"Error deleting row: {e}")
            
    def col_values(self, col, value_render_option="FORMATTED_VALUE"):
        col_letter = self._col_to_letter(col)
        cell_range = f"{self.title}!{col_letter}:{col_letter}"
        safe_range = urllib.parse.quote(cell_range)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{safe_range}?valueRenderOption={value_render_option}"
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                values_list = res.get("values", [])
                return [v[0] if v else "" for v in values_list]
        except Exception as e:
            raise Exception(f"Error reading column values: {e}")
            
    def _col_to_letter(self, col):
        letter = ""
        while col > 0:
            col, remainder = divmod(col - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter

class CustomSpreadsheet:
    def __init__(self, spreadsheet_url, access_token):
        parts = spreadsheet_url.split("/d/")
        if len(parts) > 1:
            self.id = parts[1].split("/")[0]
        else:
            self.id = spreadsheet_url
        self.access_token = access_token
        self._worksheets_cache = {}
        
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
    def worksheets(self):
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.id}"
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                sheets_list = []
                for s in res.get("sheets", []):
                    props = s.get("properties", {})
                    sheet_name = props.get("title")
                    sheet_id = props.get("sheetId")
                    ws = CustomWorksheet(self.id, sheet_name, sheet_id, self.access_token)
                    sheets_list.append(ws)
                    self._worksheets_cache[sheet_name.lower()] = ws
                return sheets_list
        except Exception as e:
            raise Exception(f"Error fetching worksheets list: {e}")
            
    def worksheet(self, title):
        title_lower = title.lower()
        if title_lower in self._worksheets_cache:
            return self._worksheets_cache[title_lower]
        self.worksheets()
        if title_lower in self._worksheets_cache:
            return self._worksheets_cache[title_lower]
        raise Exception(f"Worksheet not found: {title}")

# Cache Sheets connection and formulas repair to optimize API usage
@st.cache_resource(ttl=1800)
def get_sheets_connection(url):
    local_use_gsheets = False
    local_sh = None
    local_worksheet = None
    error_msg = None
    try:
        has_secrets = False
        has_raw_secrets = False
        try:
            has_secrets = "gserviceaccount" in st.secrets
            has_raw_secrets = "gserviceaccount_raw" in st.secrets
        except Exception:
            pass

        if has_secrets or has_raw_secrets:
            target_url = st.secrets.get("spreadsheet_url", url)
            
            # Try standard gspread library first
            try:
                import gspread
                if has_raw_secrets:
                    creds_dict = json.loads(st.secrets["gserviceaccount_raw"])
                else:
                    creds_dict = dict(st.secrets["gserviceaccount"])
                
                gc = gspread.service_account_from_dict(creds_dict)
                local_sh = gc.open_by_url(target_url)
                local_worksheet = local_sh.get_worksheet(0)
                local_use_gsheets = True
            except Exception as gspread_err:
                # Fall back to custom API client using pycryptodome
                if has_custom_libs:
                    try:
                        if has_raw_secrets:
                            creds_dict = json.loads(st.secrets["gserviceaccount_raw"])
                        else:
                            creds_dict = dict(st.secrets["gserviceaccount"])
                        
                        access_token = get_access_token(creds_dict)
                        local_sh = CustomSpreadsheet(target_url, access_token)
                        local_worksheet = local_sh.worksheet("PRODUCTOS")
                        local_use_gsheets = True
                    except Exception as custom_err:
                        raise Exception(f"gspread failed ({gspread_err}) and Custom fallback failed ({custom_err})")
                else:
                    raise gspread_err
            
            # Repair spreadsheet formulas in the STOCK sheet automatically
            if local_use_gsheets and local_sh is not None:
                try:
                    ws_stock = local_sh.worksheet("STOCK")
                    vals = ws_stock.col_values(6, value_render_option="FORMULA")
                    for i in range(2, len(vals)):
                        row_num = i + 1
                        val = vals[i]
                        if "CRITERIOSTOCK" in val:
                            ws_stock.update_cell(row_num, 6, f'=IF(B{row_num}<>"",SUMIFS(ENTRADASCANTIDAD,ENTRADASPRODUCTOS,B{row_num}),"")')
                    
                    # Map Row 3-10 to SALIDAS columns to fix missing calculations using batch update
                    formulas = [
                        ["=SUM(SALIDAS!F3:F1000)"],
                        ["=SUM(SALIDAS!G3:G1000)"],
                        ["=SUM(SALIDAS!H3:H1000)"],
                        ["=SUM(SALIDAS!I3:I1000)"],
                        ["=SUM(SALIDAS!J3:J1000)"],
                        ["=SUM(SALIDAS!K3:K1000)"],
                        ["=SUM(SALIDAS!L3:L1000)"],
                        ["=SUM(SALIDAS!M3:M1000)"]
                    ]
                    try:
                        ws_stock.update("G3:G10", formulas)
                    except Exception:
                        ws_stock.update_cell(3, 7, "=SUM(SALIDAS!F3:F1000)")
                        ws_stock.update_cell(4, 7, "=SUM(SALIDAS!G3:G1000)")
                        ws_stock.update_cell(5, 7, "=SUM(SALIDAS!H3:H1000)")
                        ws_stock.update_cell(6, 7, "=SUM(SALIDAS!I3:I1000)")
                        ws_stock.update_cell(7, 7, "=SUM(SALIDAS!J3:J1000)")
                        ws_stock.update_cell(8, 7, "=SUM(SALIDAS!K3:K1000)")
                        ws_stock.update_cell(9, 7, "=SUM(SALIDAS!L3:L1000)")
                        ws_stock.update_cell(10, 7, "=SUM(SALIDAS!M3:M1000)")
                except Exception:
                    pass
    except Exception as e:
        error_msg = str(e)
    return local_use_gsheets, local_sh, local_worksheet, error_msg

use_gsheets, sh, worksheet, conn_error = get_sheets_connection(SHEET_URL)
if conn_error:
    st.sidebar.error(f"Error conectando a Google Sheets: {conn_error}")

# Helper to safely look up or create worksheets (case-insensitive)
def get_or_create_worksheet(sheet_name, columns):
    worksheets = sh.worksheets()
    target_title = sheet_name.strip().lower()
    ws = None
    for w in worksheets:
        if w.title.strip().lower() == target_title:
            ws = w
            break
            
    if ws is None:
        ws = sh.add_worksheet(title=sheet_name, rows=1000, cols=len(columns))
        # Add headers
        ws.append_row(columns)
    return ws

# Helper to load sheet/csv (customized for sheet structures)

@st.cache_data(ttl=600)
def load_recibos_from_salidas():
    global use_gsheets
    recibos_cols = ["FOLIO", "FECHA", "CLIENTE", "PRODUCTOS", "TOTAL", "COSTO", "GANANCIA", "TIPO_PAGO", "ESTADO_PAGO", "ABONADO", "PENDIENTE"]
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("SALIDAS")
            all_values = ws.get_all_values()
            
            # Skip first 2 rows (row 0: sum totals, row 1: headers)
            if len(all_values) < 3:
                return pd.DataFrame(columns=recibos_cols)
                
            rows = all_values[2:]
            records = []
            
            # Match the order of flavor columns in the sheet (Cols E to L)
            product_names = ["FUEGO", "RANCHERO", "SALSAS NEGRAS", "JALAPEÑO", "QUESO", "NATURAL", "PIQUIN", "FUEGUITO"]
            
            for row in rows:
                row = row + [""] * (20 - len(row))
                
                col_b_val = row[1].strip()
                col_c_val = row[2].strip()
                col_d_val = row[3].strip()
                col_e_val = row[4].strip()
                col_s_val = row[18].strip()
                col_t_val = row[19].strip()
                
                # Check if the row is an old layout row (15 columns format)
                # In old format: row[1] (Col B) contains the Folio, and row[3] (Col D) contains the Date.
                is_old_row = False
                is_date_in_d = False
                if col_d_val:
                    if "/" in col_d_val or "-" in col_d_val:
                        is_date_in_d = True
                    else:
                        try:
                            if float(col_d_val) > 40000:
                                is_date_in_d = True
                        except ValueError:
                            pass
                            
                if col_b_val and is_date_in_d:
                    is_old_row = True
                    
                if is_old_row:
                    cliente = col_c_val.upper()
                    if not cliente or cliente == "CLIENTE":
                        continue
                        
                    folio = col_b_val
                    fecha = col_d_val
                    
                    # Parse flavor quantities from Columns E to L (index 4 to 11)
                    products_list = []
                    for p_idx, p_name in enumerate(product_names):
                        col_val = row[4 + p_idx].strip()
                        if col_val:
                            try:
                                qty = int(float(col_val))
                                if qty > 0:
                                    products_list.append(f"{qty}x {p_name}")
                            except ValueError:
                                pass
                    products_summary = "; ".join(products_list)
                    is_revoked = cliente.startswith("[REVOCADO]")
                    
                    # Financials (Columns M, N, O / indices 12, 13, 14)
                    try:
                        total = float(row[13].replace("$", "").replace(",", "").strip()) if row[13] else 0.0
                    except ValueError:
                        total = 0.0
                    try:
                        costo_total = float(row[12].replace("$", "").replace(",", "").strip()) if row[12] else 0.0
                    except ValueError:
                        costo_total = 0.0
                    try:
                        ganancia = float(row[14].replace("$", "").replace(",", "").strip()) if row[14] else 0.0
                    except ValueError:
                        ganancia = 0.0
                        
                    # Fallback payment values for old rows
                    abonado = total
                    pendiente = 0.0
                    estado_pago = "REVOCADO" if is_revoked else "Pagado"
                    tipo_pago = "Contado" if (total > 0) else "Consigna"
                    
                else:
                    cliente = col_d_val.upper()
                    if not cliente or cliente == "CLIENTE":
                        continue
                        
                    fecha = col_e_val
                    
                    # Parse flavor quantities from Columns F to M (index 5 to 12)
                    products_list = []
                    for p_idx, p_name in enumerate(product_names):
                        col_val = row[5 + p_idx].strip()
                        if col_val:
                            try:
                                qty = int(float(col_val))
                                if qty > 0:
                                    products_list.append(f"{qty}x {p_name}")
                            except ValueError:
                                pass
                    products_summary = "; ".join(products_list)
                    is_revoked = cliente.startswith("[REVOCADO]")
                    
                    # Financials (Columns N, O, P / indices 13, 14, 15)
                    try:
                        total = float(row[14].replace("$", "").replace(",", "").strip()) if row[14] else 0.0
                    except ValueError:
                        total = 0.0
                    try:
                        costo_total = float(row[13].replace("$", "").replace(",", "").strip()) if row[13] else 0.0
                    except ValueError:
                        costo_total = 0.0
                    try:
                        ganancia = float(row[15].replace("$", "").replace(",", "").strip()) if row[15] else 0.0
                    except ValueError:
                        ganancia = 0.0
                        
                    # Payment info
                    try:
                        abonado = float(row[16].replace("$", "").replace(",", "").strip()) if row[16] else 0.0
                    except ValueError:
                        abonado = 0.0
                    try:
                        pendiente = float(row[17].replace("$", "").replace(",", "").strip()) if row[17] else 0.0
                    except ValueError:
                        pendiente = 0.0
                        
                    # Detect if swapped
                    is_swapped = False
                    if col_c_val in ["Contado", "Consigna", "Por Pagar", "Pagado", "REVOCADO"] or col_s_val.startswith("F-") or col_s_val.isdigit():
                        is_swapped = True
                        
                    if is_swapped:
                        folio = col_s_val if col_s_val else f"F-{len(records)+1:03d}"
                        if col_t_val in ["Pagado", "Por Pagar", "REVOCADO"]:
                            estado_pago = col_t_val
                            tipo_pago = col_c_val if col_c_val in ["Contado", "Consigna"] else "Consigna"
                        elif col_c_val in ["Pagado", "Por Pagar", "REVOCADO"]:
                            estado_pago = col_c_val
                            tipo_pago = col_t_val if col_t_val in ["Contado", "Consigna"] else "Consigna"
                        else:
                            tipo_pago = col_c_val
                            estado_pago = col_t_val if col_t_val else ("Pagado" if (pendiente == 0) else "Por Pagar")
                    else:
                        folio = col_c_val if col_c_val else f"F-{len(records)+1:03d}"
                        estado_pago = col_s_val if col_s_val else ("Pagado" if (pendiente == 0) else "Por Pagar")
                        tipo_pago = col_t_val if col_t_val else ("Contado" if (pendiente == 0 or "FUEGUITO" in products_summary) else "Consigna")
                        
                records.append({
                    "FOLIO": folio,
                    "FECHA": fecha,
                    "CLIENTE": cliente,
                    "PRODUCTOS": products_summary,
                    "TOTAL": total,
                    "COSTO": costo_total,
                    "GANANCIA": ganancia,
                    "TIPO_PAGO": tipo_pago,
                    "ESTADO_PAGO": estado_pago,
                    "ABONADO": abonado,
                    "PENDIENTE": pendiente
                })
                
            return pd.DataFrame(records)
        except Exception as e:
            st.sidebar.warning(f"⚠️ Sincronización de Salidas falló. Usando copia local. Detalle: {e}")
            use_gsheets = False
            
    # Fallback to local CSV
    if not os.path.exists(REC_FILE):
        pd.DataFrame(columns=recibos_cols).to_csv(REC_FILE, index=False)
    df = pd.read_csv(REC_FILE)
    for c in recibos_cols:
        if c not in df.columns:
            df[c] = ""
    return df

def save_recibo_to_salidas(folio, fecha, cliente, cart, total_sale, total_cost, total_profit, payment_term, abonado, pendiente, estado_pago):
    global use_gsheets
    recibos_cols = ["FOLIO", "FECHA", "CLIENTE", "PRODUCTOS", "TOTAL", "COSTO", "GANANCIA", "TIPO_PAGO", "ESTADO_PAGO", "ABONADO", "PENDIENTE"]
    products_summary = "; ".join([f"{item['CANTIDAD']}x {item['PRODUCTO']}" for item in cart])
    
    # Save locally first
    if os.path.exists(REC_FILE):
        df_local = pd.read_csv(REC_FILE)
    else:
        df_local = pd.DataFrame(columns=recibos_cols)
        
    new_local_receipt = {
        "FOLIO": folio,
        "FECHA": fecha,
        "CLIENTE": cliente,
        "PRODUCTOS": products_summary,
        "TOTAL": total_sale,
        "COSTO": total_cost,
        "GANANCIA": total_profit,
        "TIPO_PAGO": payment_term,
        "ESTADO_PAGO": estado_pago,
        "ABONADO": abonado,
        "PENDIENTE": pendiente
    }
    df_local = pd.concat([df_local, pd.DataFrame([new_local_receipt])], ignore_index=True)
    df_local.to_csv(REC_FILE, index=False)
    st.cache_data.clear()
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("SALIDAS")
            current_rows = len(ws.get_all_values())
            new_row_idx = current_rows + 1
            
            product_names = ["FUEGO", "RANCHERO", "SALSAS NEGRAS", "JALAPEÑO", "QUESO", "NATURAL", "PIQUIN", "FUEGUITO"]
            qtys = [0] * len(product_names)
            for item in cart:
                item_name = item['PRODUCTO'].strip().upper()
                if item_name in product_names:
                    idx = product_names.index(item_name)
                    qtys[idx] += item['CANTIDAD']
                    
            # Map elements to the correct sheet columns (preserving formulas in columns N and P)
            new_row = [
                "", # Col A (1)
                "", # Col B (2)
                folio, # Col C (3) (FOLIO)
                cliente, # Col D (4) (CLIENTE)
                fecha, # Col E (5) (FECHA)
                qtys[0] if qtys[0] > 0 else "", # Col F (6) (FUEGO)
                qtys[1] if qtys[1] > 0 else "", # Col G (7) (RANCHERO)
                qtys[2] if qtys[2] > 0 else "", # Col H (8) (SALSAS NEGRAS)
                qtys[3] if qtys[3] > 0 else "", # Col I (9) (JALAPEÑO)
                qtys[4] if qtys[4] > 0 else "", # Col J (10) (QUESO)
                qtys[5] if qtys[5] > 0 else "", # Col K (11) (NATURAL)
                qtys[6] if qtys[6] > 0 else "", # Col L (12) (PIQUIN)
                qtys[7] if qtys[7] > 0 else "", # Col M (13) (FUEGUITO)
                f"=SUM(F{new_row_idx}*PRODUCTOS!$G$3,G{new_row_idx}*PRODUCTOS!$G$4,H{new_row_idx}*PRODUCTOS!$G$5,I{new_row_idx}*PRODUCTOS!$G$6,J{new_row_idx}*PRODUCTOS!$G$7,K{new_row_idx}*PRODUCTOS!$G$8,L{new_row_idx}*PRODUCTOS!$G$10,M{new_row_idx}*PRODUCTOS!$G$9)", # Col N (14) (COMPRA)
                total_sale, # Col O (15) (VENTA)
                f"=O{new_row_idx}-N{new_row_idx}", # Col P (16) (GANANCIA BRUTA)
                abonado, # Col Q (17) (ABONADO)
                pendiente, # Col R (18) (PENDIENTE)
                estado_pago, # Col S (19) (ESTADO_PAGO)
                payment_term # Col T (20) (TIPO_PAGO)
            ]
            ws.append_row(new_row, value_input_option="USER_ENTERED")
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al guardar en Drive (Salidas): {e}")
            use_gsheets = False
    return False

def update_abono_in_salidas(folio, new_abonado, new_pendiente, nuevo_estado):
    global use_gsheets
    if os.path.exists(REC_FILE):
        df_local = pd.read_csv(REC_FILE)
        df_local.loc[df_local['FOLIO'] == folio, 'ABONADO'] = new_abonado
        df_local.loc[df_local['FOLIO'] == folio, 'PENDIENTE'] = new_pendiente
        df_local.loc[df_local['FOLIO'] == folio, 'ESTADO_PAGO'] = nuevo_estado
        df_local.to_csv(REC_FILE, index=False)
        st.cache_data.clear()
        
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("SALIDAS")
            all_values = ws.get_all_values()
            for i, row in enumerate(all_values):
                if i < 2:
                    continue
                match_row = False
                is_old = False
                is_swapped = False
                
                # Check different folio positions
                if len(row) > 18 and row[18].strip() == folio.strip():
                    match_row = True
                    is_swapped = True
                elif len(row) > 2 and row[2].strip() == folio.strip():
                    match_row = True
                elif len(row) > 1 and row[1].strip() == folio.strip():
                    match_row = True
                    is_old = True
                    
                if match_row:
                    row_idx = i + 1
                    if is_old:
                        ws.update_cell(row_idx, 16, new_abonado)
                        ws.update_cell(row_idx, 17, new_pendiente)
                        ws.update_cell(row_idx, 18, nuevo_estado)
                    elif is_swapped:
                        ws.update_cell(row_idx, 17, new_abonado)  # Col Q (17)
                        ws.update_cell(row_idx, 18, new_pendiente) # Col R (18)
                        ws.update_cell(row_idx, 20, nuevo_estado)  # Col T (20)
                    else:
                        ws.update_cell(row_idx, 17, new_abonado)  # Col Q (17)
                        ws.update_cell(row_idx, 18, new_pendiente) # Col R (18)
                        ws.update_cell(row_idx, 19, nuevo_estado)  # Col S (19)
                    break
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al actualizar abono en Drive: {e}")
            use_gsheets = False
    return False

def revoke_recibo_in_salidas(folio):
    global use_gsheets
    if os.path.exists(REC_FILE):
        df_local = pd.read_csv(REC_FILE)
        idx_local = df_local[df_local['FOLIO'] == folio].index[0]
        original_summary = df_local.at[idx_local, 'PRODUCTOS']
        
        df_local.at[idx_local, 'PRODUCTOS'] = f"[REVOCADO] {original_summary}"
        df_local.at[idx_local, 'TOTAL'] = 0.0
        df_local.at[idx_local, 'COSTO'] = 0.0
        df_local.at[idx_local, 'GANANCIA'] = 0.0
        df_local.at[idx_local, 'ABONADO'] = 0.0
        df_local.at[idx_local, 'PENDIENTE'] = 0.0
        df_local.at[idx_local, 'ESTADO_PAGO'] = "REVOCADO"
        df_local.to_csv(REC_FILE, index=False)
        st.cache_data.clear()
        
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("SALIDAS")
            all_values = ws.get_all_values()
            for i, row in enumerate(all_values):
                if i < 2:
                    continue
                
                # Check different folio positions
                if len(row) > 18 and row[18].strip() == folio.strip():
                    row_idx = i + 1
                    original_name = row[3]
                    ws.update_cell(row_idx, 4, f"[REVOCADO] {original_name}") # Col D (4)
                    for c in range(6, 14):
                        ws.update_cell(row_idx, c, "") # Columns F to M (6 to 13)
                    ws.update_cell(row_idx, 15, 0.0) # Column O (15, VENTA)
                    ws.update_cell(row_idx, 17, 0.0) # Column Q (17, ABONADO)
                    ws.update_cell(row_idx, 18, 0.0) # Column R (18, PENDIENTE)
                    ws.update_cell(row_idx, 19, "REVOCADO") # Column S (19, ESTADO_PAGO)
                    break
                elif len(row) > 2 and row[2].strip() == folio.strip():
                    row_idx = i + 1
                    original_name = row[3]
                    ws.update_cell(row_idx, 4, f"[REVOCADO] {original_name}") # Col D (4)
                    for c in range(6, 14):
                        ws.update_cell(row_idx, c, "") # Columns F to M (6 to 13)
                    ws.update_cell(row_idx, 15, 0.0) # Column O (15, VENTA)
                    ws.update_cell(row_idx, 17, 0.0) # Column Q (17, ABONADO)
                    ws.update_cell(row_idx, 18, 0.0) # Column R (18, PENDIENTE)
                    ws.update_cell(row_idx, 19, "REVOCADO") # Column S (19, ESTADO_PAGO)
                    break
                elif len(row) > 1 and row[1].strip() == folio.strip():
                    row_idx = i + 1
                    original_name = row[2]
                    ws.update_cell(row_idx, 3, f"[REVOCADO] {original_name}") # Col C (3)
                    for c in range(5, 13):
                        ws.update_cell(row_idx, c, "") # Columns E to L (5 to 12)
                    ws.update_cell(row_idx, 14, 0.0) # Column N (14, VENTA)
                    break
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al revocar recibo en Drive: {e}")
            use_gsheets = False
    return False

# Date parser helper
def safe_parse_date(date_str):
    if not date_str:
        return datetime.today().date()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(str(date_str).strip(), fmt).date()
        except ValueError:
            pass
    try:
        return pd.to_datetime(date_str).date()
    except Exception:
        return datetime.today().date()

@st.cache_data(ttl=600)
def load_gastos_from_sheet():
    global use_gsheets
    gastos_cols = ["ROW_IDX", "COL_IDX", "FECHA", "CATEGORIA", "DESCRIPCION", "MONTO"]
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("GASTOS")
            all_values = ws.get_all_values()
            if len(all_values) < 3:
                return pd.DataFrame(columns=gastos_cols)
                
            rows = all_values[2:]
            records = []
            category_names = ["CASETA", "GASOLINA", "COCHE", "ESTACIONAMIENTO", "PUBLICIDAD", "OTROS"]
            
            for r_idx, row in enumerate(rows):
                row = row + [""] * (10 - len(row))
                fecha = row[1].strip()
                if not fecha:
                    continue
                    
                observaciones = row[8].strip()
                found_gasto = False
                
                # Check category columns C to H
                for c_offset, cat in enumerate(category_names):
                    val = row[2 + c_offset].strip()
                    if val:
                        try:
                            monto = float(val.replace("$", "").replace(",", "").strip())
                            if monto > 0:
                                records.append({
                                    "ROW_IDX": r_idx + 3, # 1-based row index in sheet
                                    "COL_IDX": 2 + c_offset + 1, # 1-based col index (Col C is 3)
                                    "FECHA": fecha,
                                    "CATEGORIA": cat,
                                    "DESCRIPCION": observaciones if observaciones else cat,
                                    "MONTO": monto
                                })
                                found_gasto = True
                        except ValueError:
                            pass
                            
                # Fallback to total if no category columns matched
                if not found_gasto:
                    total_val = row[9].strip()
                    if total_val:
                        try:
                            monto = float(total_val.replace("$", "").replace(",", "").strip())
                            if monto > 0:
                                records.append({
                                    "ROW_IDX": r_idx + 3,
                                    "COL_IDX": 10, # Column J (10)
                                    "FECHA": fecha,
                                    "CATEGORIA": "OTROS",
                                    "DESCRIPCION": observaciones if observaciones else "OTROS",
                                    "MONTO": monto
                                })
                        except ValueError:
                            pass
                            
            return pd.DataFrame(records)
        except Exception as e:
            st.sidebar.warning(f"⚠️ Sincronización de Gastos falló. Usando copia local. Detalle: {e}")
            use_gsheets = False
            
    # Local fallback
    if not os.path.exists(GAS_FILE):
        pd.DataFrame(columns=["FECHA", "CATEGORIA", "DESCRIPCION", "MONTO"]).to_csv(GAS_FILE, index=False)
    df = pd.read_csv(GAS_FILE)
    df['ROW_IDX'] = df.index
    df['COL_IDX'] = 0
    return df[["ROW_IDX", "COL_IDX", "FECHA", "CATEGORIA", "DESCRIPCION", "MONTO"]]

def save_gasto_to_sheet(fecha, categoria, descripcion, monto):
    global use_gsheets
    # Save locally first
    if os.path.exists(GAS_FILE):
        df_local = pd.read_csv(GAS_FILE)
    else:
        df_local = pd.DataFrame(columns=["FECHA", "CATEGORIA", "DESCRIPCION", "MONTO"])
        
    new_local_expense = {
        "FECHA": fecha,
        "CATEGORIA": categoria,
        "DESCRIPCION": descripcion,
        "MONTO": monto
    }
    df_local = pd.concat([df_local, pd.DataFrame([new_local_expense])], ignore_index=True)
    df_local.to_csv(GAS_FILE, index=False)
    st.cache_data.clear()
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("GASTOS")
            current_rows = len(ws.get_all_values())
            new_row_idx = current_rows + 1
            
            category_names = ["CASETA", "GASOLINA", "COCHE", "ESTACIONAMIENTO", "PUBLICIDAD", "OTROS"]
            cat_vals = [""] * len(category_names)
            
            if categoria in category_names:
                idx = category_names.index(categoria)
                cat_vals[idx] = monto
            else:
                cat_vals[5] = monto
                
            new_row = [
                "", # Col A (1)
                fecha, # Col B (2)
                cat_vals[0], # Col C (3, CASETA)
                cat_vals[1], # Col D (4, GASOLINA)
                cat_vals[2], # Col E (5, COCHE)
                cat_vals[3], # Col F (6, ESTACIONAMIENTO)
                cat_vals[4], # Col G (7, PUBLICIDAD)
                cat_vals[5], # Col H (8, VARIOS/OTROS)
                descripcion, # Col I (9, OBSERVACIONES)
                f"=SUM(C{new_row_idx}:H{new_row_idx})" # Col J (10, TOTAL)
            ]
            ws.append_row(new_row, value_input_option="USER_ENTERED")
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al guardar gasto en Drive: {e}")
            use_gsheets = False
    return False

def update_gasto_in_sheet(row_idx, old_col_idx, new_col_idx, new_fecha, new_monto, new_descripcion):
    global use_gsheets
    st.cache_data.clear()
    
    # Update locally
    if os.path.exists(GAS_FILE):
        df_local = pd.read_csv(GAS_FILE)
        if not use_gsheets:
            df_local.at[row_idx, 'FECHA'] = new_fecha
            category_names = ["CASETA", "GASOLINA", "COCHE", "ESTACIONAMIENTO", "PUBLICIDAD", "OTROS"]
            new_cat = category_names[new_col_idx - 3] if (3 <= new_col_idx <= 8) else "OTROS"
            df_local.at[row_idx, 'CATEGORIA'] = new_cat
            df_local.at[row_idx, 'DESCRIPCION'] = new_descripcion
            df_local.at[row_idx, 'MONTO'] = new_monto
            df_local.to_csv(GAS_FILE, index=False)
            
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("GASTOS")
            ws.update_cell(row_idx, 2, new_fecha)
            if old_col_idx != new_col_idx:
                ws.update_cell(row_idx, old_col_idx, "")
            ws.update_cell(row_idx, new_col_idx, new_monto)
            ws.update_cell(row_idx, 9, new_descripcion)
            ws.update_cell(row_idx, 10, f"=SUM(C{row_idx}:H{row_idx})")
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al editar gasto en Drive: {e}")
    else:
        return not use_gsheets
    return False

def delete_gasto_in_sheet(row_idx, col_idx):
    global use_gsheets
    st.cache_data.clear()
    
    # Delete locally
    if os.path.exists(GAS_FILE):
        df_local = pd.read_csv(GAS_FILE)
        if not use_gsheets:
            df_local = df_local.drop(row_idx)
            df_local.to_csv(GAS_FILE, index=False)
            
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("GASTOS")
            ws.update_cell(row_idx, col_idx, "")
            
            row_vals = ws.row_values(row_idx)
            row_vals = row_vals + [""] * (10 - len(row_vals))
            has_other_gastos = False
            for c in range(2, 8):
                if row_vals[c].strip():
                    has_other_gastos = True
                    break
                    
            if not has_other_gastos:
                ws.update_cell(row_idx, 2, "") # Fecha
                ws.update_cell(row_idx, 9, "") # Observaciones
                ws.update_cell(row_idx, 10, "") # Total
            else:
                ws.update_cell(row_idx, 10, f"=SUM(C{row_idx}:H{row_idx})")
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al eliminar gasto en Drive: {e}")
    else:
        return not use_gsheets
    return False

@st.cache_data(ttl=600)
def load_entradas_from_sheet():
    global use_gsheets
    entradas_cols = ["ROW_IDX", "CÓDIGO", "PRODUCTO", "DESCRIPCIÓN", "MARCA", "CANTIDAD", "FECHA", "OBSERVACIÓN"]
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("ENTRADAS")
            all_values = ws.get_all_values()
            if len(all_values) < 3: # Skip row 0 and 1
                return pd.DataFrame(columns=entradas_cols)
                
            rows = all_values[2:]
            records = []
            for idx, row in enumerate(rows, 3):
                row = row + [""] * (8 - len(row))
                codigo = row[1].strip()
                producto = row[2].strip()
                if not producto:
                    continue
                descripcion = row[3].strip()
                marca = row[4].strip()
                try:
                    cantidad = int(float(row[5].replace(",", "").strip()))
                except ValueError:
                    cantidad = 0
                fecha = row[6].strip()
                observacion = row[7].strip()
                
                records.append({
                    "ROW_IDX": idx,
                    "CÓDIGO": codigo,
                    "PRODUCTO": producto,
                    "DESCRIPCIÓN": descripcion,
                    "MARCA": marca,
                    "CANTIDAD": cantidad,
                    "FECHA": fecha,
                    "OBSERVACIÓN": observacion
                })
            return pd.DataFrame(records)
        except Exception as e:
            st.sidebar.warning(f"⚠️ Sincronización de Entradas falló. Usando copia local. Detalle: {e}")
            use_gsheets = False
            
    # Local fallback
    if not os.path.exists("entradas.csv"):
        pd.DataFrame(columns=["CÓDIGO", "PRODUCTO", "DESCRIPCIÓN", "MARCA", "CANTIDAD", "FECHA", "OBSERVACIÓN"]).to_csv("entradas.csv", index=False)
    df = pd.read_csv("entradas.csv")
    df['ROW_IDX'] = df.index
    return df[["ROW_IDX", "CÓDIGO", "PRODUCTO", "DESCRIPCIÓN", "MARCA", "CANTIDAD", "FECHA", "OBSERVACIÓN"]]

def save_entrada_to_sheet(codigo, producto, descripcion, marca, cantidad, fecha, observacion):
    global use_gsheets
    entradas_cols = ["CÓDIGO", "PRODUCTO", "DESCRIPCIÓN", "MARCA", "CANTIDAD", "FECHA", "OBSERVACIÓN"]
    
    if os.path.exists("entradas.csv"):
        df_local = pd.read_csv("entradas.csv")
    else:
        df_local = pd.DataFrame(columns=entradas_cols)
        
    new_entry = {
        "CÓDIGO": codigo,
        "PRODUCTO": producto,
        "DESCRIPCIÓN": descripcion,
        "MARCA": marca,
        "CANTIDAD": cantidad,
        "FECHA": fecha,
        "OBSERVACIÓN": observacion
    }
    df_local = pd.concat([df_local, pd.DataFrame([new_entry])], ignore_index=True)
    df_local.to_csv("entradas.csv", index=False)
    st.cache_data.clear()
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("ENTRADAS")
            new_row = ["", codigo, producto, descripcion, marca, cantidad, fecha, observacion]
            ws.append_row(new_row)
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al guardar entrada de stock en Drive: {e}")
    return False

def update_entrada_in_sheet(row_idx, codigo, producto, descripcion, marca, old_qty, new_qty, new_fecha, new_obs):
    global use_gsheets
    st.cache_data.clear()
    
    diff = new_qty - old_qty
    df_productos.loc[df_productos['CÓDIGO'] == codigo, 'STOCK'] += diff
    save_productos(df_productos)
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("ENTRADAS")
            ws.update_cell(row_idx, 2, codigo)
            ws.update_cell(row_idx, 3, producto)
            ws.update_cell(row_idx, 4, descripcion)
            ws.update_cell(row_idx, 5, marca)
            ws.update_cell(row_idx, 6, new_qty)
            ws.update_cell(row_idx, 7, new_fecha)
            ws.update_cell(row_idx, 8, new_obs)
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al actualizar entrada en Drive: {e}")
    else:
        # Local mode update
        if os.path.exists("entradas.csv"):
            df_local = pd.read_csv("entradas.csv")
            df_local.at[row_idx, 'CÓDIGO'] = codigo
            df_local.at[row_idx, 'PRODUCTO'] = producto
            df_local.at[row_idx, 'DESCRIPCIÓN'] = descripcion
            df_local.at[row_idx, 'MARCA'] = marca
            df_local.at[row_idx, 'CANTIDAD'] = new_qty
            df_local.at[row_idx, 'FECHA'] = new_fecha
            df_local.at[row_idx, 'OBSERVACIÓN'] = new_obs
            df_local.to_csv("entradas.csv", index=False)
            return True
    return False

def delete_entrada_in_sheet(row_idx, codigo, qty):
    global use_gsheets
    st.cache_data.clear()
    
    df_productos.loc[df_productos['CÓDIGO'] == codigo, 'STOCK'] -= qty
    save_productos(df_productos)
    
    if use_gsheets and sh is not None:
        try:
            ws = sh.worksheet("ENTRADAS")
            ws.delete_rows(row_idx)
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error al eliminar entrada en Drive: {e}")
    else:
        # Local mode deletion
        if os.path.exists("entradas.csv"):
            df_local = pd.read_csv("entradas.csv")
            df_local = df_local.drop(row_idx)
            df_local.to_csv("entradas.csv", index=False)
            return True
    return False

# Load Productos (Special because of original structure and stock)
@st.cache_data(ttl=600)
def load_productos():
    global use_gsheets
    if use_gsheets and worksheet is not None:
        try:
            all_values = worksheet.get_all_values()
            if len(all_values) < 2:
                return pd.DataFrame(columns=['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA', 'STOCK'])
            
            headers = [h.strip() for h in all_values[1]]
            seen = {}
            dedup_headers = []
            for h in headers:
                if h in seen:
                    seen[h] += 1
                    dedup_headers.append(f"{h}_{seen[h]}")
                else:
                    seen[h] = 0
                    dedup_headers.append(h)
                    
            rows = all_values[2:]
            df = pd.DataFrame(rows, columns=dedup_headers)
            
            valid_cols = ['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA', 'STOCK']
            df = df[[c for c in valid_cols if c in df.columns]]
            
            for col in valid_cols:
                if col not in df.columns:
                    if col == 'STOCK':
                        df['STOCK'] = 350
                    else:
                        df[col] = ""
            
            df['CÓDIGO'] = df['CÓDIGO'].astype(str).str.strip()
            df = df[df['CÓDIGO'] != ""]
            df['PRECIO COMPRA'] = pd.to_numeric(df['PRECIO COMPRA'], errors='coerce').fillna(0.0)
            df['STOCK'] = pd.to_numeric(df['STOCK'], errors='coerce').fillna(350).astype(int)
            return df
        except Exception as e:
            st.sidebar.warning(f"⚠️ Sincronización de Productos falló. Usando copia local. Detalle: {e}")
            use_gsheets = False
            
    if not os.path.exists(PROD_FILE):
        try:
            df = pd.read_csv(SHEET_EXPORT_URL, skiprows=1)
            df = df.dropna(how='all')
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df.columns = df.columns.str.strip()
            df['STOCK'] = 350
            df.to_csv(PROD_FILE, index=False)
        except Exception:
            return pd.DataFrame(columns=['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA', 'STOCK'])
            
    df = pd.read_csv(PROD_FILE)
    if 'STOCK' not in df.columns:
        df['STOCK'] = 350
    df['CÓDIGO'] = df['CÓDIGO'].astype(str).str.strip()
    df['STOCK'] = pd.to_numeric(df['STOCK'], errors='coerce').fillna(350).astype(int)
    return df

def save_productos(df):
    global use_gsheets
    st.cache_data.clear()
    
    cols = ['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA', 'STOCK']
    df = df[cols].copy()
    if use_gsheets and worksheet is not None:
        try:
            worksheet.clear()
            data_to_write = []
            data_to_write.append(['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA', 'STOCK', 'PRECIO COMPRA']) # Header row
            for _, row in df.iterrows():
                data_to_write.append([
                    row['CÓDIGO'],
                    row['PRODUCTO'],
                    row['DESCRIPCIÓN'],
                    row['MARCA'],
                    float(row['PRECIO COMPRA']),
                    int(row['STOCK']),
                    float(row['PRECIO COMPRA']) # Write price to Col G for GSheets formulas
                ])
            worksheet.update('A2', data_to_write)
            return
        except Exception as e:
            st.sidebar.error(f"❌ Error al guardar Productos en Sheets: {e}. Guardando copia local.")
            use_gsheets = False
            
    df.to_csv(PROD_FILE, index=False)

# Load Databases
df_productos = load_productos()
df_recibos = load_recibos_from_salidas()

# Helper to build Clientes dynamically from Recibos
def get_clientes_from_recibos(df_rec):
    if len(df_rec) == 0:
        return pd.DataFrame(columns=["CLIENTE", "TOTAL_COMPRADO", "METODO_COMUN", "FRECUENCIA", "DEUDA", "ESTADO"])
    active_rec = df_rec[df_rec['ESTADO_PAGO'] != "REVOCADO"]
    records = []
    for client in active_rec['CLIENTE'].unique():
        client_receipts = active_rec[active_rec['CLIENTE'] == client]
        total_comprado = client_receipts['TOTAL'].sum()
        deuda = client_receipts['PENDIENTE'].sum()
        estado = "Debe" if deuda > 0 else "Al corriente"
        
        metodo_comun = "Contado"
        if len(client_receipts) > 0:
            methods = client_receipts['TIPO_PAGO'].value_counts()
            if len(methods) > 0:
                metodo_comun = methods.index[0]
                
        frecuencia = "Primeras compras"
        if len(client_receipts) >= 2:
            dates = pd.to_datetime(client_receipts['FECHA'], format="%d/%m/%Y", errors='coerce').dropna().sort_values()
            if len(dates) == 0:
                dates = pd.to_datetime(client_receipts['FECHA'], errors='coerce').dropna().sort_values()
            diffs = dates.diff().dt.days.dropna()
            if len(diffs) > 0:
                avg_days = int(diffs.mean())
                frecuencia = f"Cada {avg_days} días"
            else:
                frecuencia = "Cada 15 días (Estimado)"
                
        records.append({
            "CLIENTE": client,
            "TOTAL_COMPRADO": total_comprado,
            "METODO_COMUN": metodo_comun,
            "FRECUENCIA": frecuencia,
            "DEUDA": deuda,
            "ESTADO": estado
        })
    return pd.DataFrame(records)

df_clientes = get_clientes_from_recibos(df_recibos)
df_gastos = load_gastos_from_sheet()

# Ensure correct numeric types
df_recibos['TOTAL'] = pd.to_numeric(df_recibos['TOTAL'], errors='coerce').fillna(0.0)
df_recibos['COSTO'] = pd.to_numeric(df_recibos['COSTO'], errors='coerce').fillna(0.0)
df_recibos['GANANCIA'] = pd.to_numeric(df_recibos['GANANCIA'], errors='coerce').fillna(0.0)
df_recibos['ABONADO'] = pd.to_numeric(df_recibos['ABONADO'], errors='coerce').fillna(0.0)
df_recibos['PENDIENTE'] = pd.to_numeric(df_recibos['PENDIENTE'], errors='coerce').fillna(0.0)

df_clientes['TOTAL_COMPRADO'] = pd.to_numeric(df_clientes['TOTAL_COMPRADO'], errors='coerce').fillna(0.0)
df_clientes['DEUDA'] = pd.to_numeric(df_clientes['DEUDA'], errors='coerce').fillna(0.0)

df_gastos['MONTO'] = pd.to_numeric(df_gastos['MONTO'], errors='coerce').fillna(0.0)

# Sidebar Info
with st.sidebar:
    st.image("https://tienda.maicitos.com/cdn/shop/files/LOGOO-MAICTI-TOS_4x-2048x744_1.png", width=180)
    st.header("⚙️ Configuración General")
    has_secrets_api_key = False
    api_key = ""
    try:
        if "gemini_api_key" in st.secrets and st.secrets["gemini_api_key"].strip():
            api_key = st.secrets["gemini_api_key"].strip()
            has_secrets_api_key = True
    except Exception:
        pass

    if has_secrets_api_key:
        st.success("🤖 Asistente de IA Activo")
    else:
        api_key = st.text_input("Gemini API Key:", type="password")
    
    if use_gsheets:
        st.success("🟢 Conectado a Google Sheets")
        if st.button("🔄 Sincronizar con Drive (Recargar)", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    else:
        st.warning("⚠️ Ejecutando en Modo Local")

    st.divider()
    st.markdown("### Resumen Rápido")
    st.write(f"Productos únicos: {len(df_productos)}")
    st.write(f"Ventas registradas: {len(df_recibos)}")
    st.write(f"Clientes registrados: {len(df_clientes)}")
    st.write(f"Gastos operativos: {len(df_gastos)}")

# Main Tabs
tab_dash, tab_fact, tab_rec, tab_gastos, tab_stock, tab_ia = st.tabs([
    "📊 Vista Rápida",
    "🧾 Facturación",
    "📋 Recibos e Historial",
    "💸 Gastos Operativos",
    "📦 Administrar Stock",
    "🤖 Asistente de IA"
])

# Helper to print colored stock badges in HTML
def get_stock_badge(stock):
    if stock > 300:
        return f'<span class="badge-green">{stock} pz</span>'
    elif stock >= 100:
        return f'<span class="badge-orange">{stock} pz</span>'
    else:
        return f'<span class="badge-red">{stock} pz</span>'

# TAB 1: DASHBOARD / VISTA RÁPIDA
with tab_dash:
    st.markdown("### Resumen General del Negocio")
    
    # Calculate stats
    total_productos = len(df_productos)
    insuficiente = len(df_productos[df_productos['STOCK'] < 100])
    total_piezas = df_productos['STOCK'].sum()
    val_compra = (df_productos['STOCK'] * df_productos['PRECIO COMPRA']).sum()
    
    # Today's stats (exclude revoked receipts)
    today_str = datetime.today().strftime("%Y-%m-%d")
    df_today_rec = df_recibos[(df_recibos['FECHA'] == today_str) & (df_recibos['ESTADO_PAGO'] != "REVOCADO")]
    today_sales_count = len(df_today_rec)
    today_revenue = df_today_rec['TOTAL'].sum()
    today_profit = df_today_rec['GANANCIA'].sum()
    
    # Debts stats
    total_debt = df_clientes['DEUDA'].sum()
    debtor_clients = df_clientes[df_clientes['DEUDA'] > 0]
    top_debtor = "Ninguno"
    top_debt_val = 0.0
    if len(debtor_clients) > 0:
        idx_max_debt = debtor_clients['DEUDA'].idxmax()
        top_debtor = debtor_clients.loc[idx_max_debt, 'CLIENTE']
        top_debt_val = debtor_clients.loc[idx_max_debt, 'DEUDA']
        
    # Top selling products
    from collections import Counter
    product_counter = Counter()
    for _, row in df_recibos[df_recibos['ESTADO_PAGO'] != "REVOCADO"].iterrows():
        products_str = row['PRODUCTOS']
        parts = products_str.split("; ")
        for part in parts:
            if "x " in part:
                try:
                    qty_str, prod_name = part.split("x ", 1)
                    qty = int(qty_str)
                    product_counter[prod_name.strip().upper()] += qty
                except Exception:
                    pass
    top_selling = product_counter.most_common(3)
    
    # HTML for KPI Cards (tienda.maicitos.com style)
    kpi_html = f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 25px;">
        <div style="background: #ffffff; border: 1px solid #e5e0d8; border-top: 4px solid #ffd200; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(46, 27, 18, 0.03); text-align: center; font-family: 'Poppins', sans-serif;">
            <span style="font-size: 0.8rem; color: #6d5b52; font-weight: 600; text-transform: uppercase;">Ventas de Hoy</span>
            <div style="font-size: 1.8rem; font-weight: 800; color: #2e1b12; margin-top: 5px;">${today_revenue:,.2f}</div>
            <span style="font-size: 0.75rem; color: #8a766c;">{today_sales_count} ventas registradas</span>
        </div>
        <div style="background: #ffffff; border: 1px solid #e5e0d8; border-top: 4px solid #ff7415; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(46, 27, 18, 0.03); text-align: center; font-family: 'Poppins', sans-serif;">
            <span style="font-size: 0.8rem; color: #6d5b52; font-weight: 600; text-transform: uppercase;">Por Cobrar (Clientes)</span>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ff7415; margin-top: 5px;">${total_debt:,.2f}</div>
            <span style="font-size: 0.75rem; color: #8a766c;">Saldo pendiente de pago</span>
        </div>
        <div style="background: #ffffff; border: 1px solid #e5e0d8; border-top: 4px solid #2e1b12; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(46, 27, 18, 0.03); text-align: center; font-family: 'Poppins', sans-serif;">
            <span style="font-size: 0.8rem; color: #6d5b52; font-weight: 600; text-transform: uppercase;">Valor en Almacén</span>
            <div style="font-size: 1.8rem; font-weight: 800; color: #2e1b12; margin-top: 5px;">${val_compra:,.2f}</div>
            <span style="font-size: 0.75rem; color: #8a766c;">Inventario total a precio costo</span>
        </div>
        <div style="background: #ffffff; border: 1px solid #e5e0d8; border-top: 4px solid #7cb342; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(46, 27, 18, 0.03); text-align: center; font-family: 'Poppins', sans-serif;">
            <span style="font-size: 0.8rem; color: #6d5b52; font-weight: 600; text-transform: uppercase;">Stock en Almacén</span>
            <div style="font-size: 1.8rem; font-weight: 800; color: #7cb342; margin-top: 5px;">{total_piezas:,} pz</div>
            <span style="font-size: 0.75rem; color: #8a766c;">{total_productos} sabores | {insuficiente} bajo stock</span>
        </div>
    </div>
    """
    st.markdown("\n".join([line.strip() for line in kpi_html.split("\n")]), unsafe_allow_html=True)
    
    st.divider()
    
    # Business Statistics Section
    st.markdown("#### Estadísticas de Ventas y Clientes")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("##### 🏆 Sabores Más Populares (Histórico)")
        if len(top_selling) == 0:
            st.info("Aún no hay ventas registradas para calcular sabores populares.")
        else:
            for rank, (flavor, qty) in enumerate(top_selling, 1):
                st.markdown(f"""
                <div style="background-color: #ffffff; border: 1px solid #e5e0d8; padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; border-left: 4px solid #ff7415; font-family: 'Poppins', sans-serif; box-shadow: 0 4px 12px rgba(46, 27, 18, 0.02);">
                    <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 0.9rem; color: #2e1b12;">
                        <span>#{rank} {flavor}</span>
                        <span style="color: #ff7415;">{qty:,} piezas</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    with col_right:
        st.markdown("##### 👥 Resumen de Cartera")
        total_clientes = len(df_clientes)
        debtors_count = len(debtor_clients)
        st.markdown(f"""
        <div style="background-color: #ffffff; border: 1px solid #e5e0d8; padding: 15px; border-radius: 12px; border-left: 4px solid #ffd200; font-family: 'Poppins', sans-serif; box-shadow: 0 4px 12px rgba(46, 27, 18, 0.02); height: 100%;">
            <p style="margin: 0 0 8px 0; font-size: 0.9rem; color: #2e1b12;">Clientes registrados: <b>{total_clientes}</b></p>
            <p style="margin: 0 0 8px 0; font-size: 0.9rem; color: #2e1b12;">Clientes con adeudo: <b style="color: #c62828;">{debtors_count}</b></p>
            <p style="margin: 0; font-size: 0.9rem; color: #2e1b12;">Cliente con mayor deuda: <b>{top_debtor}</b> (${top_debt_val:,.2f})</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    # Detailed Stock Level (Responsive Cards, never truncates)
    st.markdown("#### Niveles de Stock Detallados")
    
    stock_grid_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px;">'
    for _, row in df_productos.iterrows():
        stock = row['STOCK']
        flavor_name = row['PRODUCTO']
        code = row['CÓDIGO']
        description = row['DESCRIPCIÓN']
        brand = row['MARCA']
        precio_compra = row['PRECIO COMPRA']
        stock_value = stock * precio_compra
        
        # Color coding
        if stock > 300:
            color = "#10b981"  # Emerald green
            badge_bg = "#e6f4ea"
            badge_color = "#137333"
            status_text = "Suficiente"
        elif stock >= 100:
            color = "#f59e0b"  # Amber orange
            badge_bg = "#fef3c7"
            badge_color = "#b45309"
            status_text = "Medio"
        else:
            color = "#ef4444"  # Red
            badge_bg = "#fce8e6"
            badge_color = "#c5221f"
            status_text = "Bajo Stock"
            
        # Action button style depending on stock
        btn_bg = "#ffd200"
        btn_color = "#2e1b12"
        btn_text = "Ver Detalles"
        if stock < 100:
            btn_bg = "#7cb342"
            btn_color = "#ffffff"
            btn_text = "Explorar Recetas"

        stock_grid_html += f"""
        <div style="background-color: #ffffff; border: 1px solid #e5e0d8; border-left: 5px solid {color}; border-radius: 16px; padding: 20px; box-shadow: 0 4px 12px rgba(46, 27, 18, 0.03); font-family: 'Poppins', sans-serif; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease;">
            <!-- Product Text -->
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 5px;">
                    <h5 style="margin: 0; font-size: 1.1rem; color: #2e1b12; text-transform: uppercase; font-family: 'Poppins', sans-serif; font-weight: 700; line-height: 1.2;">{flavor_name}</h5>
                    <span style="background-color: {badge_bg}; color: {badge_color}; font-size: 0.8rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; white-space: nowrap;">{stock:,} pz</span>
                </div>
                <span style="font-size: 0.75rem; color: #6d5b52; display: block; margin-bottom: 12px;">Código: {code} | {description}</span>
            </div>
            <!-- Info & Button -->
            <div style="margin-top: auto; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #6d5b52; border-top: 1px solid #f0ede8; padding-top: 8px;">
                    <span>Valor: <b>${stock_value:,.2f}</b></span>
                    <span>Estado: <b style="color: {badge_color};">{status_text}</b></span>
                </div>
                <div style="background-color: {btn_bg}; color: {btn_color}; font-size: 0.8rem; font-weight: 700; text-align: center; padding: 8px 12px; border-radius: 20px; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.5px;">
                    {btn_text}
                </div>
            </div>
        </div>
        """
    stock_grid_html += '</div>'
    st.markdown("\n".join([line.strip() for line in stock_grid_html.split("\n")]), unsafe_allow_html=True)

# TAB 2: FACTURACIÓN / CREAR TICKET
with tab_fact:
    st.subheader("Generar Nuevo Ticket de Venta")
    
    # Initialize cart session state
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "step" not in st.session_state:
        st.session_state.step = 1
        
    # Helper to calculate price and profits
    def calculate_item_financials(desc, qty, term):
        is_30gr = "30 GR" in desc.upper()
        cost_per_piece = 0.0
        price_per_piece = 0.0
        
        if is_30gr:
            cost_per_piece = 570.0 / 120.0  # $4.75
            price_per_piece = 1000.0 / 120.0  # $8.33
        else:
            cost_per_piece = 640.0 / 100.0  # $6.40
            if qty >= 100:
                price_per_piece = 12.00 if term == "Contado" else 13.50
            elif qty == 30:
                price_per_piece = 30.00 if term == "Contado" else 14.50
            else:
                price_per_piece = 30.00 if term == "Contado" else 14.50 # Default retail
                
        total = price_per_piece * qty
        cost = cost_per_piece * qty
        profit = total - cost
        return price_per_piece, total, cost, profit

    # WIZARD STEP 1: Add items to Cart
    if st.session_state.step == 1:
        st.markdown("#### Paso 1: Agregar Productos al Carrito")
        
        # Grid of products to select
        col_sel, col_cart = st.columns([1, 1])
        
        with col_sel:
            st.markdown("##### Seleccionar Producto")
            # Create list of products for selector
            prod_options = [f"{row['CÓDIGO']} - {row['PRODUCTO']} ({row['DESCRIPCIÓN']})" for _, row in df_productos.iterrows()]
            selected_prod_str = st.selectbox("Producto:", prod_options)
            
            selected_code = selected_prod_str.split(" - ")[0]
            prod_row = df_productos[df_productos['CÓDIGO'] == selected_code].iloc[0]
            desc = prod_row['DESCRIPCIÓN']
            is_30gr = "30 GR" in desc.upper()
            
            # Stock alert
            stock_val = prod_row['STOCK']
            if stock_val > 300:
                st.markdown(f"Stock disponible: <b style='color:#10b981;'>{stock_val} pz (Suficiente)</b>", unsafe_allow_html=True)
            elif stock_val >= 100:
                st.markdown(f"Stock disponible: <b style='color:#f59e0b;'>{stock_val} pz (Moderado)</b>", unsafe_allow_html=True)
            else:
                st.markdown(f"Stock disponible: <b style='color:#ef4444;'>{stock_val} pz (CRÍTICO)</b>", unsafe_allow_html=True)
                
            # Formats selection
            if is_30gr:
                st.info("💡 Este producto (Fueguito 30gr) solo se vende en cajas de 120 pz, de Contado.")
                format_option = st.selectbox("Formato de venta:", ["Caja de 120 piezas"])
                num_boxes = st.number_input("Número de Cajas:", min_value=1, step=1, value=1)
                qty_to_add = num_boxes * 120
            else:
                format_option = st.selectbox("Formato de venta:", ["Caja de 100 piezas", "Paquete de 30 piezas", "Cantidad personalizada"])
                if format_option == "Caja de 100 piezas":
                    num_boxes = st.number_input("Número de Cajas:", min_value=1, step=1, value=1)
                    qty_to_add = num_boxes * 100
                elif format_option == "Paquete de 30 piezas":
                    num_packs = st.number_input("Número de Paquetes:", min_value=1, step=1, value=1)
                    qty_to_add = num_packs * 30
                else:
                    qty_to_add = st.number_input("Cantidad exacta (piezas):", min_value=1, step=1, value=1)
                    
            if st.button("🛒 Agregar al Carrito"):
                if qty_to_add > stock_val:
                    st.error("❌ No hay suficiente stock en almacén para esta cantidad.")
                else:
                    # Check if already in cart
                    existing_cart_idx = next((i for i, item in enumerate(st.session_state.cart) if item["CÓDIGO"] == selected_code), None)
                    if existing_cart_idx is not None:
                        st.session_state.cart[existing_cart_idx]["CANTIDAD"] += qty_to_add
                    else:
                        st.session_state.cart.append({
                            "CÓDIGO": selected_code,
                            "PRODUCTO": prod_row["PRODUCTO"],
                            "DESCRIPCIÓN": desc,
                            "CANTIDAD": qty_to_add,
                            "COSTO_COMPRA": prod_row["PRECIO COMPRA"]
                        })
                    st.success(f"Añadido: {qty_to_add} pz de {prod_row['PRODUCTO']}.")
                    st.rerun()
                    
        with col_cart:
            st.markdown("##### Carrito de Compras")
            if not st.session_state.cart:
                st.info("El carrito está vacío.")
            else:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'CANTIDAD']], use_container_width=True, hide_index=True)
                
                c_del, c_cont = st.columns(2)
                with c_del:
                    if st.button("🗑️ Vaciar Carrito"):
                        st.session_state.cart = []
                        st.rerun()
                with c_cont:
                    if st.button("Continuar a Datos de Venta ➡️"):
                        st.session_state.step = 2
                        st.rerun()

    # WIZARD STEP 2: Client & Payment selection & Financial preview
    elif st.session_state.step == 2:
        st.markdown("#### Paso 2: Información del Cliente y Condiciones")
        
        # Go back button
        if st.button("⬅️ Volver al Carrito"):
            st.session_state.step = 1
            st.rerun()
            
        # Date Selector
        ticket_date = st.date_input("Fecha de emisión del ticket:", value=datetime.today().date())
        
        # Client Selector
        client_list = ["➕ Nuevo Cliente"] + sorted(df_clientes["CLIENTE"].unique().tolist())
        selected_client = st.selectbox("Cliente:", client_list)
        
        new_client_name = ""
        if selected_client == "➕ Nuevo Cliente":
            new_client_name = st.text_input("Escribe el nombre del nuevo cliente:").strip().upper()
            
        # Check if cart contains 30gr product (forces Contado and Ya pagó)
        has_30gr_in_cart = any("30 GR" in item["DESCRIPCIÓN"].upper() for item in st.session_state.cart)
        
        # Payment Type Selector
        if has_30gr_in_cart:
            st.warning("⚠️ Se incluye un producto de 30gr (Fueguito), por lo que toda la venta debe realizarse de CONTADO y pagarse inmediatamente.")
            payment_term = st.selectbox("Tipo de Pago:", ["Contado"], disabled=True)
            payment_status = st.selectbox("Estado del Pago:", ["Ya pagó"], disabled=True)
        else:
            payment_term = st.selectbox("Tipo de Pago:", ["Contado", "Consigna"])
            payment_status = st.selectbox("Estado del Pago:", ["Ya pagó", "Va a pagar (A crédito/consigna)"])
            
        # Submit to review
        preview_submitted = st.button("Generar Vista Previa del Ticket", type="primary")
        
        if preview_submitted:
            client_to_use = new_client_name if selected_client == "➕ Nuevo Cliente" else selected_client
            if not client_to_use:
                st.error("⚠️ Debes proporcionar un nombre de cliente.")
            else:
                st.session_state.client_name = client_to_use
                st.session_state.ticket_date = ticket_date.strftime("%Y-%m-%d")
                st.session_state.payment_term = payment_term
                st.session_state.payment_status = payment_status
                st.session_state.step = 3
                st.rerun()

    # WIZARD STEP 3: Preview and Finalize
    elif st.session_state.step == 3:
        st.markdown("#### Paso 3: Vista Previa y Confirmación")
        
        # Back button
        if st.button("⬅️ Cambiar Cliente/Condiciones"):
            st.session_state.step = 2
            st.rerun()
            
        # Compile financial data
        detailed_items = []
        total_sale = 0.0
        total_cost = 0.0
        
        for item in st.session_state.cart:
            price, item_total, item_cost, item_profit = calculate_item_financials(
                item["DESCRIPCIÓN"], item["CANTIDAD"], st.session_state.payment_term
            )
            total_sale += item_total
            total_cost += item_cost
            detailed_items.append({
                "CÓDIGO": item["CÓDIGO"],
                "PRODUCTO": item["PRODUCTO"],
                "DESCRIPCIÓN": item["DESCRIPCIÓN"],
                "CANTIDAD": item["CANTIDAD"],
                "PRECIO UNITARIO": price,
                "TOTAL": item_total,
                "COSTO": item_cost,
                "GANANCIA": item_profit
            })
            
        total_profit = total_sale - total_cost
        
        # Display preview table
        df_preview = pd.DataFrame(detailed_items)
        st.dataframe(
            df_preview[['PRODUCTO', 'DESCRIPCIÓN', 'CANTIDAD', 'PRECIO UNITARIO', 'TOTAL']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "PRECIO UNITARIO": st.column_config.NumberColumn("Precio Unitario", format="$%.2f"),
                "TOTAL": st.column_config.NumberColumn("Subtotal", format="$%.2f")
            }
        )
        
        # Total metrics
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total a Cobrar", f"${total_sale:,.2f}")
        with c2:
            st.write(f"**Cliente:** {st.session_state.client_name}")
            st.write(f"**Fecha:** {st.session_state.ticket_date}")
        with c3:
            st.write(f"**Tipo de venta:** {st.session_state.payment_term}")
            st.write(f"**Estado del pago:** {st.session_state.payment_status}")
            
        st.divider()
        
        # Final confirmation
        if st.button("🔥 Finalizar Venta y Descontar Inventario", type="primary"):
            # 1. Generate Folio
            if len(df_recibos) == 0:
                new_folio = "F-001"
            else:
                try:
                    last_folio = df_recibos['FOLIO'].iloc[-1]
                    last_num = int(last_folio.split("-")[1])
                    new_folio = f"F-{last_num + 1:03d}"
                except Exception:
                    new_folio = f"F-{len(df_recibos) + 1:03d}"
            
            # 2. Subtract Stock from df_productos
            for item in st.session_state.cart:
                df_productos.loc[df_productos['CÓDIGO'] == item['CÓDIGO'], 'STOCK'] -= item['CANTIDAD']
            save_productos(df_productos)
            
            # 3. Add to Receipts
            products_summary = "; ".join([f"{item['CANTIDAD']}x {item['PRODUCTO']}" for item in st.session_state.cart])
            
            # Calculate payment status based on chosen payment status
            if st.session_state.payment_status == "Ya pagó":
                abonado = total_sale
                pendiente = 0.0
                estado_pago = "Pagado"
            else:
                abonado = 0.0
                pendiente = total_sale
                estado_pago = "Por Pagar"
            
            new_receipt = {
                "FOLIO": new_folio,
                "FECHA": st.session_state.ticket_date,
                "CLIENTE": st.session_state.client_name,
                "PRODUCTOS": products_summary,
                "TOTAL": total_sale,
                "COSTO": total_cost,
                "GANANCIA": total_profit,
                "TIPO_PAGO": st.session_state.payment_term,
                "ESTADO_PAGO": estado_pago,
                "ABONADO": abonado,
                "PENDIENTE": pendiente
            }
            
            # Save receipt to Salidas sheet and local CSV
            save_recibo_to_salidas(
                new_folio,
                st.session_state.ticket_date,
                st.session_state.client_name,
                st.session_state.cart,
                total_sale,
                total_cost,
                total_profit,
                st.session_state.payment_term,
                abonado,
                pendiente,
                estado_pago
            )
            
            # 5. Generate Receipt Text for WhatsApp
            receipt_txt = f"""==================================
        TICKET DE COMPRA
==================================
Folio: {new_folio}
Fecha: {st.session_state.ticket_date}
Cliente: {st.session_state.client_name}
Tipo de venta: {st.session_state.payment_term}
Estado: {estado_pago}

PRODUCTOS:
"""
            for i, item in enumerate(detailed_items):
                receipt_txt += f"- {item['CANTIDAD']}x {item['PRODUCTO']}\n  ({item['DESCRIPCIÓN']})\n  Subtotal: ${item['TOTAL']:.2f}\n"
                
            receipt_txt += f"""----------------------------------
TOTAL COMPRA: ${total_sale:.2f}
Monto Abonado: ${abonado:.2f}
Falta por pagar: ${pendiente:.2f}
==================================
¡Gracias por su preferencia!
=================================="""

            st.session_state.generated_folio = new_folio
            st.session_state.generated_text = receipt_txt
            st.session_state.step = 4
            st.rerun()

    # WIZARD STEP 4: Success, show receipt to copy
    elif st.session_state.step == 4:
        st.success(f"🎉 Venta registrada con éxito. Folio generado: {st.session_state.generated_folio}")
        
        st.markdown("#### Recibo de WhatsApp (Copia con un clic)")
        st.info("💡 Haz clic en el botón de copiar en la esquina superior derecha del siguiente cuadro de código para enviarlo fácilmente por WhatsApp.")
        st.code(st.session_state.generated_text, language="text")
        
        # Actions container using columns
        col_actions1, col_actions2 = st.columns(2)
        with col_actions1:
            st.download_button(
                label="📥 Descargar Recibo (.txt)",
                data=st.session_state.generated_text,
                file_name=f"recibo_{st.session_state.generated_folio}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_actions2:
            import urllib.parse
            whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(st.session_state.generated_text)}"
            st.link_button(
                label="📲 Compartir por WhatsApp",
                url=whatsapp_url,
                use_container_width=True
            )
        
        if st.button("🔄 Crear Nueva Venta"):
            # Clear session state and go back to step 1
            st.session_state.cart = []
            st.session_state.step = 1
            st.rerun()

# TAB 3: RECIBOS E HISTORIAL (TICKETS & CLIENTES)
with tab_rec:
    st.subheader("Control de Recibos y Clientes")
    
    # 1. Receipts Table
    st.markdown("### Historial de Recibos")
    # Search filters
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        rec_filter = st.selectbox("Filtrar Estado:", ["Todos", "Solo Pagados", "Solo Por Pagar (Pendientes)", "Solo Revocados"])
    with col_f2:
        search_folio = st.text_input("Buscar Folio:", "").strip()
    with col_f3:
        search_cliente = st.text_input("Buscar Cliente:", "").strip()
    with col_f4:
        search_producto = st.text_input("Buscar Producto/Sabor:", "").strip()
        
    df_rec_filtered = df_recibos.copy()
    
    # Sort: newest at the top (chronological reverse order)
    df_rec_filtered = df_rec_filtered.iloc[::-1].reset_index(drop=True)
    
    # Filter by payment status
    if rec_filter == "Solo Pagados":
        df_rec_filtered = df_rec_filtered[df_rec_filtered['ESTADO_PAGO'] == "Pagado"]
    elif rec_filter == "Solo Por Pagar (Pendientes)":
        df_rec_filtered = df_rec_filtered[df_rec_filtered['ESTADO_PAGO'] == "Por Pagar"]
    elif rec_filter == "Solo Revocados":
        df_rec_filtered = df_rec_filtered[df_rec_filtered['ESTADO_PAGO'] == "REVOCADO"]
        
    # Filter by text search
    if search_folio:
        df_rec_filtered = df_rec_filtered[df_rec_filtered['FOLIO'].astype(str).str.contains(search_folio, case=False, na=False)]
    if search_cliente:
        df_rec_filtered = df_rec_filtered[df_rec_filtered['CLIENTE'].astype(str).str.contains(search_cliente, case=False, na=False)]
    if search_producto:
        df_rec_filtered = df_rec_filtered[df_rec_filtered['PRODUCTOS'].astype(str).str.contains(search_producto, case=False, na=False)]
        
    st.dataframe(
        df_rec_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "TOTAL": st.column_config.NumberColumn("Total", format="$%.2f"),
            "ABONADO": st.column_config.NumberColumn("Abonado", format="$%.2f"),
            "PENDIENTE": st.column_config.NumberColumn("Pendiente", format="$%.2f"),
            "GANANCIA": st.column_config.NumberColumn("Utilidad", format="$%.2f"),
            "COSTO": st.column_config.NumberColumn("Costo Compra", format="$%.2f")
        }
    )
    
    # Register installment / abono section
    st.markdown("#### Registrar Abono / Pago a Recibo")
    pending_tickets = df_recibos[df_recibos['ESTADO_PAGO'] == "Por Pagar"].iloc[::-1].reset_index(drop=True)
    
    if len(pending_tickets) == 0:
        st.info("No hay recibos pendientes de pago.")
    else:
        with st.form("abono_form"):
            col_sel_ticket, col_amount = st.columns(2)
            with col_sel_ticket:
                ticket_options = [f"{row['FOLIO']} - {row['CLIENTE']} (Falta: ${row['PENDIENTE']:.2f})" for _, row in pending_tickets.iterrows()]
                selected_ticket_str = st.selectbox("Selecciona el Recibo:", ticket_options)
            with col_amount:
                abono_val = st.number_input("Monto a Abonar ($):", min_value=0.01, step=50.0)
                
            submit_abono = st.form_submit_button("Registrar Pago")
            
            if submit_abono:
                selected_folio = selected_ticket_str.split(" - ")[0]
                ticket_idx = df_recibos[df_recibos['FOLIO'] == selected_folio].index[0]
                
                # Get current data
                current_total = float(df_recibos.at[ticket_idx, 'TOTAL'])
                current_abonado = float(df_recibos.at[ticket_idx, 'ABONADO'])
                
                new_abonado = current_abonado + abono_val
                new_pendiente = max(0.0, current_total - new_abonado)
                
                # Update abono in Google Sheet and CSV
                update_abono_in_salidas(selected_folio, new_abonado, new_pendiente, "Pagado" if new_pendiente == 0.0 else "Por Pagar")
                
                st.success(f"Abono de ${abono_val:.2f} registrado para el folio {selected_folio}.")
                st.rerun()
    st.divider()
    
    # Section to Revoke Ticket
    st.markdown("### ⚠️ Revocar Factura / Ticket")
    # Only show active (non-revoked) tickets
    active_tickets = df_recibos[df_recibos['ESTADO_PAGO'] != "REVOCADO"]
    if len(active_tickets) == 0:
        st.info("No hay recibos activos para revocar.")
    else:
        # Search filters for revocation
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            search_rev_folio = st.text_input("Buscar Folio a Revocar:", "").strip()
        with col_r2:
            search_rev_cliente = st.text_input("Buscar Cliente a Revocar:", "").strip()
            
        active_tickets_filtered = active_tickets.copy()
        
        # Sort: newest at the top (reverse chronological order)
        active_tickets_filtered = active_tickets_filtered.iloc[::-1].reset_index(drop=True)
        
        # Apply filters
        if search_rev_folio:
            active_tickets_filtered = active_tickets_filtered[active_tickets_filtered['FOLIO'].astype(str).str.contains(search_rev_folio, case=False, na=False)]
        if search_rev_cliente:
            active_tickets_filtered = active_tickets_filtered[active_tickets_filtered['CLIENTE'].astype(str).str.contains(search_rev_cliente, case=False, na=False)]
            
        if len(active_tickets_filtered) == 0:
            st.info("No hay recibos activos que coincidan con la búsqueda.")
        else:
            with st.form("revoke_form"):
                revoke_options = [f"{row['FOLIO']} - {row['CLIENTE']} (Total: ${row['TOTAL']:.2f})" for _, row in active_tickets_filtered.iterrows()]
                selected_revoke_str = st.selectbox("Selecciona el Recibo a Revocar:", revoke_options)
                confirm_revoke = st.checkbox("Confirmo que deseo revocar esta factura permanentemente y devolver los productos al inventario.")
                
                submit_revoke = st.form_submit_button("🚨 Revocar Factura", type="primary")
                
                if submit_revoke:
                    if not confirm_revoke:
                        st.error("Por favor, marca la casilla de confirmación para revocar.")
                    else:
                        selected_folio = selected_revoke_str.split(" - ")[0]
                        ticket_idx = df_recibos[df_recibos['FOLIO'] == selected_folio].index[0]
                        
                        # 1. Parse products and restore stock
                        products_summary = df_recibos.at[ticket_idx, 'PRODUCTOS']
                        parts = products_summary.split("; ")
                        restored_details = []
                        for part in parts:
                            if "x " in part:
                                qty_str, prod_name = part.split("x ", 1)
                                qty = int(qty_str)
                                # Find product
                                prod_matches = df_productos[df_productos['PRODUCTO'].str.strip().str.upper() == prod_name.strip().upper()]
                                if len(prod_matches) > 0:
                                    p_idx = prod_matches.index[0]
                                    df_productos.at[p_idx, 'STOCK'] = int(df_productos.at[p_idx, 'STOCK']) + qty
                                    restored_details.append(f"{qty} pz de {prod_name}")
                        
                        # Save updated products
                        save_productos(df_productos)
                        
                        # Revoke receipt in Google Sheet and CSV
                        revoke_recibo_in_salidas(selected_folio)
                        
                        st.success(f"🎉 Factura {selected_folio} revocada exitosamente. Se devolvieron al inventario: {', '.join(restored_details)}.")
                        st.rerun()
                    
    st.divider()
    
    # 2. Clients Table
    st.markdown("### Directorio de Clientes")
    st.dataframe(
        df_clientes,
        use_container_width=True,
        hide_index=True,
        column_config={
            "TOTAL_COMPRADO": st.column_config.NumberColumn("Total Comprado", format="$%.2f"),
            "DEUDA": st.column_config.NumberColumn("Deuda Actual", format="$%.2f")
        }
    )

# TAB 4: GASTOS OPERATIVOS
with tab_gastos:
    st.subheader("💸 Gestión de Gastos y Balance General")
    
    subtab_balance, subtab_registrar_g, subtab_editar_g = st.tabs([
        "📋 Historial y Balance",
        "➕ Registrar Gasto",
        "✏️ Editar o Eliminar Gasto"
    ])
    
    with subtab_balance:
        col_list, col_balance = st.columns([1.5, 1])
        
        with col_list:
            st.markdown("#### Historial de Gastos")
            if len(df_gastos) == 0:
                st.info("No hay gastos registrados.")
            else:
                st.dataframe(
                    df_gastos[['FECHA', 'CATEGORIA', 'DESCRIPCION', 'MONTO']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "MONTO": st.column_config.NumberColumn("Monto", format="$%.2f")
                    }
                )
                
        with col_balance:
            st.markdown("#### Balance General")
            total_ingresos = df_recibos['TOTAL'].sum()
            total_costos_compra = df_recibos['COSTO'].sum()
            utilidad_bruta = total_ingresos - total_costos_compra
            total_gastos_op = df_gastos['MONTO'].sum()
            utilidad_neta = utilidad_bruta - total_gastos_op
            
            st.metric("Ventas Totales (Ingresos)", f"${total_ingresos:,.2f}")
            st.metric("Costo de Compra", f"${total_costos_compra:,.2f}")
            st.metric("Utilidad Bruta", f"${utilidad_bruta:,.2f}")
            st.metric("Gastos Operativos", f"${total_gastos_op:,.2f}")
            st.metric("Utilidad Neta (Ganancia Real)", f"${utilidad_neta:,.2f}")
            st.info("📊 *Nota: La Utilidad Neta es la ganancia final del negocio restando el costo de los maicitos y los gastos operativos.*")
            
    with subtab_registrar_g:
        st.markdown("#### Registrar Gasto Operativo")
        with st.form("expense_form", clear_on_submit=True):
            exp_date = st.date_input("Fecha del Gasto:", value=datetime.today().date(), key="add_exp_date")
            exp_cat = st.selectbox("Categoría:", ["GASOLINA", "CASETA", "COCHE", "ESTACIONAMIENTO", "PUBLICIDAD", "OTROS"], key="add_exp_cat")
            exp_desc = st.text_input("Descripción del gasto:", placeholder="Ej. Combustible camión de reparto", key="add_exp_desc").strip().upper()
            exp_amount = st.number_input("Monto ($):", min_value=0.0, step=10.0, value=0.0, key="add_exp_amount")
            
            submit_gasto = st.form_submit_button("Guardar Gasto")
            if submit_gasto:
                if not exp_desc or exp_amount <= 0.0:
                    st.error("Por favor completa la descripción y el monto del gasto.")
                else:
                    formatted_date = f"{exp_date.day}/{exp_date.month}/{exp_date.year}"
                    save_gasto_to_sheet(formatted_date, exp_cat, exp_desc, exp_amount)
                    st.success(f"🎉 Gasto registrado: {exp_cat} por ${exp_amount:.2f}")
                    st.rerun()
                    
    with subtab_editar_g:
        st.markdown("#### Modificar o Eliminar Gasto")
        if len(df_gastos) == 0:
            st.info("No hay gastos registrados.")
        else:
            gasto_options = []
            for _, row in df_gastos.iterrows():
                gasto_options.append(f"{row['ROW_IDX']} - {row['FECHA']} - {row['CATEGORIA']} - {row['DESCRIPCION']} (${row['MONTO']:.2f})")
                
            selected_gasto_str = st.selectbox("Selecciona el gasto a editar o eliminar:", gasto_options)
            sel_row_idx = int(selected_gasto_str.split(" - ")[0])
            selected_row = df_gastos[df_gastos['ROW_IDX'] == sel_row_idx].iloc[0]
            
            g_fecha_parsed = safe_parse_date(selected_row['FECHA'])
            g_cat = selected_row['CATEGORIA']
            g_desc = selected_row['DESCRIPCION']
            g_monto = float(selected_row['MONTO'])
            old_col_idx = int(selected_row['COL_IDX'])
            
            with st.form("edit_expense_form"):
                e_date = st.date_input("Fecha del Gasto:", value=g_fecha_parsed, key="edit_exp_date")
                category_options = ["CASETA", "GASOLINA", "COCHE", "ESTACIONAMIENTO", "PUBLICIDAD", "OTROS"]
                e_cat = st.selectbox("Categoría:", category_options, index=category_options.index(g_cat) if g_cat in category_options else 5, key="edit_exp_cat")
                e_desc = st.text_input("Descripción del gasto:", value=g_desc, key="edit_exp_desc").strip().upper()
                e_amount = st.number_input("Monto ($):", min_value=0.01, step=10.0, value=g_monto, key="edit_exp_amount")
                
                category_names = ["CASETA", "GASOLINA", "COCHE", "ESTACIONAMIENTO", "PUBLICIDAD", "OTROS"]
                new_col_idx = 2 + category_names.index(e_cat) + 1
                
                c_edit, c_del = st.columns(2)
                with c_edit:
                    save_edit = st.form_submit_button("Guardar Cambios")
                with c_del:
                    delete_gasto = st.form_submit_button("🗑️ Eliminar Gasto", type="primary")
                    
                if save_edit:
                    formatted_date = f"{e_date.day}/{e_date.month}/{e_date.year}"
                    update_gasto_in_sheet(sel_row_idx, old_col_idx, new_col_idx, formatted_date, e_amount, e_desc)
                    st.success("✏️ Gasto modificado exitosamente.")
                    st.rerun()
                    
                if delete_gasto:
                    delete_gasto_in_sheet(sel_row_idx, old_col_idx)
                    st.success("🗑️ Gasto eliminado exitosamente.")
                    st.rerun()

# TAB 5: ADMINISTRAR STOCK
with tab_stock:
    st.subheader("📦 Administrar Stock e Inventario")
    
    subtab_entrada, subtab_editar, subtab_historial_entradas = st.tabs([
        "📥 Registrar Entrada (Cajas / Nuevos Productos)",
        "✏️ Editar o Eliminar Producto",
        "📋 Historial de Entradas (Editar / Eliminar)"
    ])
    
    with subtab_entrada:
        st.markdown("#### Registrar Entrada de Cajas al Inventario")
        
        tipo_entrada = st.radio(
            "¿El producto/sabor ya existe o es nuevo?",
            ["Sabor Existente (Reabastecer)", "Nuevo Sabor / Producto (Dar de Alta)"],
            horizontal=True,
            key="stock_tipo_entrada"
        )
        
        if tipo_entrada == "Sabor Existente (Reabastecer)":
            if len(df_productos) == 0:
                st.info("No hay productos registrados en el sistema.")
            else:
                with st.form("add_stock_form", clear_on_submit=True):
                    stock_options = [f"{row['CÓDIGO']} - {row['PRODUCTO']} ({row['DESCRIPCIÓN']})" for _, row in df_productos.iterrows()]
                    selected_stock_prod = st.selectbox("Selecciona el sabor/producto:", stock_options)
                    
                    selected_code = selected_stock_prod.split(" - ")[0]
                    prod_row = df_productos[df_productos['CÓDIGO'] == selected_code].iloc[0]
                    desc = prod_row['DESCRIPCIÓN']
                    is_30gr = "30 GR" in desc.upper()
                    default_size = 120 if is_30gr else 100
                    default_cost = 570.0 if is_30gr else 640.0
                    
                    if not is_30gr and "50 GR" not in desc.upper():
                        default_cost = float(prod_row['PRECIO COMPRA'] * default_size)
                    
                    st.write(f"Stock actual: **{prod_row['STOCK']} pz** (Costo unitario actual: **${prod_row['PRECIO COMPRA']:.2f}**)")
                    
                    col_box1, col_box2 = st.columns(2)
                    with col_box1:
                        box_size = st.number_input("Piezas por caja para esta entrada:", min_value=1, step=1, value=default_size)
                    with col_box2:
                        box_cost = st.number_input("Costo de la caja ($) para esta entrada:", min_value=0.0, step=10.0, value=float(default_cost))
                    
                    num_boxes = st.number_input("Cantidad de cajas a ingresar:", min_value=1, step=1, value=1)
                    record_expense = st.checkbox("Registrar automáticamente el costo como gasto del negocio", value=True)
                    
                    qty_added = num_boxes * box_size
                    cost_total = num_boxes * box_cost
                    
                    st.info(f"📊 **Resumen:** Se ingresarán **{qty_added} piezas** ({num_boxes} cajas de {box_size} pz). Costo de compra: **${cost_total:,.2f}**.")
                    
                    submit_stock = st.form_submit_button("Registrar Entrada")
                    
                    if submit_stock:
                        new_unit_cost = box_cost / box_size if box_size > 0 else 0.0
                        df_productos.loc[df_productos['CÓDIGO'] == selected_code, 'STOCK'] += qty_added
                        df_productos.loc[df_productos['CÓDIGO'] == selected_code, 'PRECIO COMPRA'] = new_unit_cost
                        save_productos(df_productos)
                        
                        today_date = datetime.today()
                        formatted_date = f"{today_date.day}/{today_date.month}/{today_date.year}"
                        save_entrada_to_sheet(
                            selected_code,
                            prod_row['PRODUCTO'],
                            desc,
                            prod_row['MARCA'],
                            qty_added,
                            formatted_date,
                            f"REABASTECER {num_boxes} CAJAS"
                        )
                        
                        if record_expense:
                            save_gasto_to_sheet(
                                formatted_date,
                                "OTROS",
                                f"COMPRA {num_boxes} CAJAS - {prod_row['PRODUCTO']} ({desc})",
                                cost_total
                            )
                            
                        st.success(f"🎉 Se registraron {qty_added} piezas nuevas ({num_boxes} cajas) para '{prod_row['PRODUCTO']}'.")
                        st.rerun()
                        
        else:
            with st.form("new_product_stock_form", clear_on_submit=True):
                st.markdown("##### Detalles del Nuevo Producto / Sabor")
                col1, col2 = st.columns(2)
                with col1:
                    new_code = st.text_input("Código de Producto (Único):", placeholder="Ej. PO09").strip().upper()
                    new_name = st.text_input("Nombre de Sabor / Producto:", placeholder="Ej. CHIPOTLE").strip().upper()
                with col2:
                    new_desc = st.text_input("Descripción / Gramaje:", value="BOLSA 50 GR", placeholder="Ej. BOLSA 80 GR").strip().upper()
                    new_brand = st.text_input("Marca:", value="MAICITOS").strip().upper()
                
                # Configurable box sizes and costs
                st.markdown("##### Configuración de Caja y Costo")
                col_box1, col_box2 = st.columns(2)
                with col_box1:
                    default_size = 120 if "30 GR" in new_desc.upper() else 100
                    box_size = st.number_input("Piezas por caja nueva:", min_value=1, step=1, value=default_size)
                with col_box2:
                    default_cost = 570.0 if "30 GR" in new_desc.upper() else 640.0
                    box_cost = st.number_input("Costo de la caja ($):", min_value=0.0, step=10.0, value=float(default_cost))
                
                unit_cost = box_cost / box_size if box_size > 0 else 0.0
                
                st.markdown("##### Detalles de Stock Inicial")
                num_boxes = st.number_input(f"Cantidad de cajas a ingresar:", min_value=0, step=1, value=1)
                record_expense = st.checkbox("Registrar automáticamente el costo como gasto del negocio", value=True)
                
                qty_added = num_boxes * box_size
                cost_total = num_boxes * box_cost
                
                st.info(f"📊 Resumen: Se ingresarán {qty_added} piezas ({num_boxes} cajas de {box_size} pz). Costo de compra: ${cost_total:,.2f} (Precio unitario: ${unit_cost:.2f}).")
                
                submit_new = st.form_submit_button("Crear Producto e Ingresar Stock")
                
                if submit_new:
                    if not new_code or not new_name:
                        st.error("Por favor completa el código y el nombre del producto.")
                    elif new_code in df_productos['CÓDIGO'].values:
                        st.error(f"El código '{new_code}' ya existe.")
                    else:
                        new_item = {
                            "CÓDIGO": new_code,
                            "PRODUCTO": new_name,
                            "DESCRIPCIÓN": new_desc,
                            "MARCA": new_brand,
                            "PRECIO COMPRA": unit_cost,
                            "STOCK": qty_added
                        }
                        
                        df_productos = pd.concat([df_productos, pd.DataFrame([new_item])], ignore_index=True)
                        save_productos(df_productos)
                        
                        today_date = datetime.today()
                        formatted_date = f"{today_date.day}/{today_date.month}/{today_date.year}"
                        save_entrada_to_sheet(
                            new_code,
                            new_name,
                            new_desc,
                            new_brand,
                            qty_added,
                            formatted_date,
                            f"NUEVO PRODUCTO - {num_boxes} CAJAS INICIALES"
                        )
                        
                        if record_expense and num_boxes > 0:
                            save_gasto_to_sheet(
                                formatted_date,
                                "OTROS",
                                f"COMPRA {num_boxes} CAJAS - {new_name} ({new_desc})",
                                cost_total
                            )
                            
                        st.success(f"🎉 Producto '{new_name}' creado con {qty_added} piezas ({num_boxes} cajas) en stock.")
                        st.rerun()

    with subtab_editar:
        st.markdown("#### Modificar o Eliminar un Producto de la Base de Datos")
        col_mod, col_el = st.columns(2)
        
        with col_mod:
            st.markdown("**Editar Información**")
            if len(df_productos) == 0:
                st.info("No hay productos.")
            else:
                product_edit_options = [f"{row['CÓDIGO']} - {row['PRODUCTO']}" for _, row in df_productos.iterrows()]
                selected_edit_prod = st.selectbox("Producto a editar:", product_edit_options, key="select_edit_prod")
                
                edit_code = selected_edit_prod.split(" - ")[0]
                prod_idx = df_productos[df_productos['CÓDIGO'] == edit_code].index[0]
                current_prod = df_productos.loc[prod_idx]
                
                with st.form("edit_product_details_form"):
                    e_name = st.text_input("Nombre del Producto:", value=current_prod['PRODUCTO']).strip().upper()
                    e_desc = st.text_input("Descripción / Tamaño:", value=current_prod['DESCRIPCIÓN']).strip().upper()
                    e_brand = st.text_input("Marca:", value=current_prod['MARCA']).strip().upper()
                    e_cost = st.number_input("Precio de Compra ($):", min_value=0.0, step=0.05, value=float(current_prod['PRECIO COMPRA']))
                    e_stock = st.number_input("Ajustar Stock (piezas):", min_value=0, step=1, value=int(current_prod['STOCK']))
                    
                    save_edit = st.form_submit_button("Guardar Cambios")
                    if save_edit:
                        df_productos.at[prod_idx, 'PRODUCTO'] = e_name
                        df_productos.at[prod_idx, 'DESCRIPCIÓN'] = e_desc
                        df_productos.at[prod_idx, 'MARCA'] = e_brand
                        df_productos.at[prod_idx, 'PRECIO COMPRA'] = e_cost
                        df_productos.at[prod_idx, 'STOCK'] = e_stock
                        save_productos(df_productos)
                        st.success(f"✏️ Cambios guardados para '{e_name}'.")
                        st.rerun()
                        
        with col_el:
            st.markdown("**Eliminar Producto**")
            if len(df_productos) == 0:
                st.info("No hay productos.")
            else:
                product_del_options = [f"{row['CÓDIGO']} - {row['PRODUCTO']}" for _, row in df_productos.iterrows()]
                selected_del_prod = st.selectbox("Producto a eliminar:", product_del_options, key="select_del_prod")
                
                del_code = selected_del_prod.split(" - ")[0]
                del_name = selected_del_prod.split(" - ")[1]
                
                st.warning(f"⚠️ ¿Estás seguro de eliminar permanentemente a **{selected_del_prod}**?")
                confirm_del = st.button("🗑️ Confirmar Eliminación", type="primary", key="btn_confirm_del")
                if confirm_del:
                    df_productos = df_productos[df_productos['CÓDIGO'] != del_code]
                    save_productos(df_productos)
                    st.success(f"🗑️ Producto '{del_name}' eliminado.")
                    st.rerun()
                    
    with subtab_historial_entradas:
        st.markdown("#### Historial de Entradas al Almacén")
        df_entradas = load_entradas_from_sheet()
        
        if len(df_entradas) == 0:
            st.info("No hay registros de entradas de stock.")
        else:
            # Search filters for warehouse entries
            col_ef1, col_ef2 = st.columns(2)
            with col_ef1:
                search_ent_prod = st.text_input("Buscar Producto:", "", key="search_ent_prod").strip()
            with col_ef2:
                search_ent_fecha = st.text_input("Buscar Fecha:", "", key="search_ent_fecha").strip()
                
            df_entradas_filtered = df_entradas.copy()
            
            # Sort: newest at the top (reverse chronological order)
            df_entradas_filtered = df_entradas_filtered.iloc[::-1].reset_index(drop=True)
            
            if search_ent_prod:
                df_entradas_filtered = df_entradas_filtered[df_entradas_filtered['PRODUCTO'].astype(str).str.contains(search_ent_prod, case=False, na=False)]
            if search_ent_fecha:
                df_entradas_filtered = df_entradas_filtered[df_entradas_filtered['FECHA'].astype(str).str.contains(search_ent_fecha, case=False, na=False)]
                
            col_list_ent, col_edit_ent = st.columns([1.5, 1])
            
            with col_list_ent:
                st.dataframe(
                    df_entradas_filtered[['FECHA', 'CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'CANTIDAD', 'OBSERVACIÓN']],
                    use_container_width=True,
                    hide_index=True
                )
                
            with col_edit_ent:
                st.markdown("##### Editar o Eliminar Entrada")
                if len(df_entradas_filtered) == 0:
                    st.info("No hay entradas que coincidan con la búsqueda.")
                else:
                    entrada_options = []
                    for _, row in df_entradas_filtered.iterrows():
                        entrada_options.append(f"{row['ROW_IDX']} - {row['FECHA']} - {row['PRODUCTO']} ({row['CANTIDAD']} pz)")
                        
                    selected_ent_str = st.selectbox("Selecciona la entrada a modificar:", entrada_options)
                    sel_ent_row_idx = int(selected_ent_str.split(" - ")[0])
                    selected_ent_row = df_entradas[df_entradas['ROW_IDX'] == sel_ent_row_idx].iloc[0]
                    
                    ent_fecha_parsed = safe_parse_date(selected_ent_row['FECHA'])
                    ent_qty = int(selected_ent_row['CANTIDAD'])
                    ent_obs = selected_ent_row['OBSERVACIÓN']
                    ent_code = selected_ent_row['CÓDIGO']
                    ent_prod = selected_ent_row['PRODUCTO']
                    ent_desc = selected_ent_row['DESCRIPCIÓN']
                    ent_brand = selected_ent_row['MARCA']
                    
                    with st.form("edit_entrada_form"):
                        e_ent_date = st.date_input("Fecha:", value=ent_fecha_parsed, key="edit_ent_date")
                        e_ent_qty = st.number_input("Cantidad (piezas):", min_value=min(1, ent_qty), step=10, value=ent_qty, key="edit_ent_qty")
                        e_ent_obs = st.text_input("Observación:", value=ent_obs, key="edit_ent_obs").strip().upper()
                        
                        c_ent_edit, c_ent_del = st.columns(2)
                        with c_ent_edit:
                            save_ent_edit = st.form_submit_button("Guardar Cambios")
                        with c_ent_del:
                            delete_ent = st.form_submit_button("🗑️ Eliminar Entrada", type="primary")
                            
                        if save_ent_edit:
                            formatted_ent_date = f"{e_ent_date.day}/{e_ent_date.month}/{e_ent_date.year}"
                            update_entrada_in_sheet(sel_ent_row_idx, ent_code, ent_prod, ent_desc, ent_brand, ent_qty, e_ent_qty, formatted_ent_date, e_ent_obs)
                            st.success("✏️ Entrada modificada exitosamente.")
                            st.rerun()
                            
                        if delete_ent:
                            delete_entrada_in_sheet(sel_ent_row_idx, ent_code, ent_qty)
                            st.success("🗑️ Entrada eliminada exitosamente y stock ajustado.")
                            st.rerun()

# TAB 6: ASISTENTE DE IA (ANTIGRAVITY)
with tab_ia:
    st.subheader("🤖 Asistente de IA de tu Negocio")
    
    if not api_key:
        st.warning("⚠️ **Falta la API Key:** Ingresa tu Gemini API Key en la barra lateral para poder chatear con tu asistente.")
    else:
        try:
            # Setup session state for chatbot
            if "ia_messages" not in st.session_state:
                st.session_state.ia_messages = [
                    {"role": "assistant", "content": "¡Hola! Soy Antigravity, tu asistente de negocios. Tengo acceso en tiempo real a tus tablas de inventario, recibos, clientes y gastos operativos. ¿En qué te puedo ayudar hoy?"}
                ]
                
            # Display chat
            for msg in st.session_state.ia_messages:
                avatar = "🤖" if msg["role"] == "assistant" else "🧑‍💻"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])
                    
            # User input
            if user_msg := st.chat_input("Pregúntame sobre ventas, deudas, stock o utilidades..."):
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(user_msg)
                st.session_state.ia_messages.append({"role": "user", "content": user_msg})
                
                # Context compiler
                context_prompt = f"""Eres Antigravity, el asistente virtual inteligente de este negocio de venta de Maicitos.
Tienes acceso en tiempo real a las siguientes tablas de datos del negocio. Utilízalas para dar respuestas sumamente precisas a las preguntas del usuario.
Responde de forma ejecutiva, amigable y clara en español.

---
DATOS DEL INVENTARIO ACTUAL:
{df_productos.to_string(index=False)}

---
HISTORIAL DE RECIBOS Y VENTAS REALIZADAS:
{df_recibos.to_string(index=False)}

---
HISTORIAL DE CLIENTES (DEUDAS, COMPRAS Y FRECUENCIAS):
{df_clientes.to_string(index=False)}

---
GASTOS OPERATIVOS DEL NEGOCIO:
{df_gastos.to_string(index=False)}
---

Pregunta del usuario: "{user_msg}"
Asistente:"""

                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Analizando información del negocio..."):
                        import requests
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                        headers = {"Content-Type": "application/json"}
                        payload = {
                            "contents": [
                                {
                                    "parts": [
                                        {"text": context_prompt}
                                    ]
                                }
                            ]
                        }
                        response = requests.post(url, json=payload, headers=headers)
                        response.raise_for_status()
                        res_data = response.json()
                        ai_response_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                        st.markdown(ai_response_text)
                st.session_state.ia_messages.append({"role": "assistant", "content": ai_response_text})
                
        except Exception as e:
            st.error(f"Error al conectar con la IA de Gemini: {e}")
