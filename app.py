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
)

# Custom Premium Styling
st.markdown("""
<style>
    .main-title {
        color: #f8fafc;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    div[data-testid="stForm"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 25px;
        border-radius: 15px;
    }
    .badge-green {
        background-color: #065f46;
        color: #34d399;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
    .badge-orange {
        background-color: #78350f;
        color: #fbbf24;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
    .badge-red {
        background-color: #7f1d1d;
        color: #f87171;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
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

# Attempt connection to Google Sheets
try:
    has_secrets = False
    has_raw_secrets = False
    try:
        has_secrets = "gserviceaccount" in st.secrets
        has_raw_secrets = "gserviceaccount_raw" in st.secrets
    except Exception:
        pass

    if has_secrets or has_raw_secrets:
        import gspread
        if has_raw_secrets:
            creds_dict = json.loads(st.secrets["gserviceaccount_raw"])
            gc = gspread.service_account_from_dict(creds_dict)
        else:
            gc = gspread.service_account_from_dict(dict(st.secrets["gserviceaccount"]))
        
        target_url = st.secrets.get("spreadsheet_url", SHEET_URL)
        sh = gc.open_by_url(target_url)
        worksheet = sh.get_worksheet(0)
        use_gsheets = True
except Exception as e:
    st.sidebar.error(f"Error conectando a Google Sheets: {e}")

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

# Helper to load sheet/csv
def load_table(sheet_name, columns, csv_filename):
    global use_gsheets
    if use_gsheets and sh is not None:
        try:
            ws = get_or_create_worksheet(sheet_name, columns)
            all_values = ws.get_all_values()
            if len(all_values) < 2:
                return pd.DataFrame(columns=columns)
            
            headers = [h.strip() for h in all_values[0]]
            rows = all_values[1:]
            df = pd.DataFrame(rows, columns=headers)
            
            df = df[[c for c in columns if c in df.columns]]
            for c in columns:
                if c not in df.columns:
                    df[c] = ""
            return df
        except Exception as e:
            st.sidebar.warning(f"⚠️ Sincronización de tabla '{sheet_name}' falló. Usando copia local. Detalle: {e}")
            use_gsheets = False
            
    if not os.path.exists(csv_filename):
        pd.DataFrame(columns=columns).to_csv(csv_filename, index=False)
    df = pd.read_csv(csv_filename)
    # Ensure all columns exist
    for c in columns:
        if c not in df.columns:
            df[c] = ""
    return df

def save_table(df, sheet_name, csv_filename, columns):
    global use_gsheets
    # Ensure correct columns and format
    df = df[columns].copy()
    if use_gsheets and sh is not None:
        try:
            ws = get_or_create_worksheet(sheet_name, columns)
            ws.clear()
            data_to_write = [columns] + df.values.tolist()
            ws.update('A1', data_to_write)
            return
        except Exception as e:
            st.sidebar.error(f"❌ Error guardando '{sheet_name}' en Drive: {e}. Guardando copia local.")
            use_gsheets = False
            
    df.to_csv(csv_filename, index=False)

# Load Productos (Special because of original structure and stock)
def load_productos():
    global use_gsheets
    if use_gsheets and worksheet is not None:
        try:
            all_values = worksheet.get_all_values()
            if len(all_values) < 2:
                return pd.DataFrame(columns=['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA', 'STOCK'])
            
            headers = [h.strip() for h in all_values[1]]
            rows = all_values[2:]
            df = pd.DataFrame(rows, columns=headers)
            
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
    cols = ['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA', 'STOCK']
    df = df[cols].copy()
    if use_gsheets and worksheet is not None:
        try:
            worksheet.clear()
            headers = cols
            data_to_write = [headers] + df.values.tolist()
            worksheet.update('A2', data_to_write)
            return
        except Exception as e:
            st.sidebar.error(f"❌ Error al guardar Productos en Sheets: {e}. Guardando copia local.")
            use_gsheets = False
            
    df.to_csv(PROD_FILE, index=False)

# Load Databases
df_productos = load_productos()
df_recibos = load_table("Recibos", ["FOLIO", "FECHA", "CLIENTE", "PRODUCTOS", "TOTAL", "COSTO", "GANANCIA", "TIPO_PAGO", "ESTADO_PAGO", "ABONADO", "PENDIENTE"], REC_FILE)
df_clientes = load_table("Clientes", ["CLIENTE", "TOTAL_COMPRADO", "METODO_COMUN", "FRECUENCIA", "DEUDA", "ESTADO"], CLI_FILE)
df_gastos = load_table("Gastos", ["FECHA", "CATEGORIA", "DESCRIPCION", "MONTO"], GAS_FILE)

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
    st.header("⚙️ Configuración General")
    api_key = st.text_input("Gemini API Key:", type="password", value=st.secrets.get("gemini_api_key", ""))
    
    if use_gsheets:
        st.success("🟢 Conectado a Google Sheets")
    else:
        st.warning("⚠️ Ejecutando en Modo Local")

    st.divider()
    st.markdown("### Resumen Rápido")
    st.write(f"Productos únicos: {len(df_productos)}")
    st.write(f"Ventas registradas: {len(df_recibos)}")
    st.write(f"Clientes registrados: {len(df_clientes)}")
    st.write(f"Gastos operativos: {len(df_gastos)}")

# Main Tabs
tab_dash, tab_fact, tab_rec, tab_gastos, tab_ia = st.tabs([
    "📊 Vista Rápida",
    "🧾 Facturación",
    "📋 Recibos e Historial",
    "💸 Gastos Operativos",
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
    st.markdown("### Estado del Inventario")
    
    # Showcase stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Productos", len(df_productos))
    with c2:
        insuficiente = len(df_productos[df_productos['STOCK'] < 100])
        st.metric("Productos con Bajo Stock (<100 pz)", insuficiente)
    with c3:
        total_piezas = df_productos['STOCK'].sum()
        st.metric("Total de Piezas en Almacén", f"{total_piezas:,} pz")
    with c4:
        val_compra = (df_productos['STOCK'] * df_productos['PRECIO COMPRA']).sum()
        st.metric("Valor del Inventario (Costo)", f"${val_compra:,.2f}")
        
    st.divider()
    
    st.markdown("#### Niveles de Stock Detallados")
    
    # Present a clean list with HTML colored stocks
    df_show = df_productos.copy()
    df_show['Estado Stock'] = df_show['STOCK'].apply(
        lambda x: "🟢 Suficiente (>300)" if x > 300 else ("🟡 Medio (100-300)" if x >= 100 else "🔴 Bajo (<100)")
    )
    
    st.dataframe(
        df_show[['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'STOCK', 'Estado Stock']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "STOCK": st.column_config.NumberColumn("Piezas en Almacén", format="%d pz"),
            "Estado Stock": st.column_config.TextColumn("Estado de Abastecimiento")
        }
    )

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
            
        with st.form("billing_form"):
            # Date Selector
            ticket_date = st.date_input("Fecha de emisión del ticket:", value=datetime.today().date())
            
            # Client Selector
            client_list = ["➕ Nuevo Cliente"] + sorted(df_clientes["CLIENTE"].unique().tolist())
            selected_client = st.selectbox("Cliente:", client_list)
            
            new_client_name = ""
            if selected_client == "➕ Nuevo Cliente":
                new_client_name = st.text_input("Escribe el nombre del nuevo cliente:").strip().upper()
                
            # Check if cart contains 30gr product (forces Contado)
            has_30gr_in_cart = any("30 GR" in item["DESCRIPCIÓN"].upper() for item in st.session_state.cart)
            
            # Payment Type Selector
            if has_30gr_in_cart:
                st.warning("⚠️ Se incluye un producto de 30gr (Fueguito), por lo que toda la venta debe realizarse de CONTADO.")
                payment_term = st.selectbox("Tipo de Pago:", ["Contado"], disabled=True)
            else:
                payment_term = st.selectbox("Tipo de Pago:", ["Contado", "Consigna"])
                
            # Submit to review
            preview_submitted = st.form_submit_button("Generar Vista Previa del Ticket")
            
            if preview_submitted:
                client_to_use = new_client_name if selected_client == "➕ Nuevo Cliente" else selected_client
                if not client_to_use:
                    st.error("⚠️ Debes proporcionar un nombre de cliente.")
                else:
                    st.session_state.client_name = client_to_use
                    st.session_state.ticket_date = ticket_date.strftime("%Y-%m-%d")
                    st.session_state.payment_term = payment_term
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
            
            # Calculate payment status
            # Contado starts as fully paid (ABONADO = TOTAL, PENDIENTE = 0)
            # Consigna starts as unpaid (ABONADO = 0, PENDIENTE = TOTAL)
            abonado = total_sale if st.session_state.payment_term == "Contado" else 0.0
            pendiente = 0.0 if st.session_state.payment_term == "Contado" else total_sale
            estado_pago = "Pagado" if pendiente == 0.0 else "Por Pagar"
            
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
            
            df_recibos = pd.concat([df_recibos, pd.DataFrame([new_receipt])], ignore_index=True)
            save_table(df_recibos, "Recibos", REC_FILE, ["FOLIO", "FECHA", "CLIENTE", "PRODUCTOS", "TOTAL", "COSTO", "GANANCIA", "TIPO_PAGO", "ESTADO_PAGO", "ABONADO", "PENDIENTE"])
            
            # 4. Update Clientes Database
            client_name = st.session_state.client_name
            # Calculate Frequency based on this client's purchase history
            client_receipts = df_recibos[df_recibos['CLIENTE'] == client_name]
            if len(client_receipts) >= 2:
                dates = pd.to_datetime(client_receipts['FECHA'], errors='coerce').dropna().sort_values()
                diffs = dates.diff().dt.days.dropna()
                if len(diffs) > 0:
                    avg_days = int(diffs.mean())
                    frecuencia = f"Cada {avg_days} días"
                else:
                    frecuencia = "Cada 15 días (Estimado)"
            else:
                frecuencia = "Primeras compras"
            
            # Recalculate total debt
            client_debt = df_recibos[df_recibos['CLIENTE'] == client_name]['PENDIENTE'].sum()
            client_estado = "Debe" if client_debt > 0 else "Al corriente"
            
            if client_name in df_clientes['CLIENTE'].values:
                idx = df_clientes[df_clientes['CLIENTE'] == client_name].index[0]
                df_clientes.at[idx, 'TOTAL_COMPRADO'] = float(df_clientes.at[idx, 'TOTAL_COMPRADO']) + total_sale
                df_clientes.at[idx, 'METODO_COMUN'] = st.session_state.payment_term
                df_clientes.at[idx, 'FRECUENCIA'] = frecuencia
                df_clientes.at[idx, 'DEUDA'] = client_debt
                df_clientes.at[idx, 'ESTADO'] = client_estado
            else:
                new_client = {
                    "CLIENTE": client_name,
                    "TOTAL_COMPRADO": total_sale,
                    "METODO_COMUN": st.session_state.payment_term,
                    "FRECUENCIA": frecuencia,
                    "DEUDA": client_debt,
                    "ESTADO": client_estado
                }
                df_clientes = pd.concat([df_clientes, pd.DataFrame([new_client])], ignore_index=True)
                
            save_table(df_clientes, "Clientes", CLI_FILE, ["CLIENTE", "TOTAL_COMPRADO", "METODO_COMUN", "FRECUENCIA", "DEUDA", "ESTADO"])
            
            # 5. Generate Receipt Text for WhatsApp
            receipt_txt = f"""==================================
        TICKET DE COMPRA
==================================
Folio: {new_folio}
Fecha: {st.session_state.ticket_date}
Cliente: {client_name}
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
        
        # WhatsApp Share Link
        st.download_button(
            label="📥 Descargar Recibo (.txt)",
            data=st.session_state.generated_text,
            file_name=f"recibo_{st.session_state.generated_folio}.txt",
            mime="text/plain"
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
    rec_filter = st.selectbox("Filtrar recibos:", ["Todos", "Solo Pagados", "Solo Por Pagar (Pendientes)"])
    
    df_rec_filtered = df_recibos.copy()
    if rec_filter == "Solo Pagados":
        df_rec_filtered = df_rec_filtered[df_rec_filtered['ESTADO_PAGO'] == "Pagado"]
    elif rec_filter == "Solo Por Pagar (Pendientes)":
        df_rec_filtered = df_rec_filtered[df_rec_filtered['ESTADO_PAGO'] == "Por Pagar"]
        
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
    pending_tickets = df_recibos[df_recibos['ESTADO_PAGO'] == "Por Pagar"]
    
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
                
                # Update receipt
                df_recibos.at[ticket_idx, 'ABONADO'] = new_abonado
                df_recibos.at[ticket_idx, 'PENDIENTE'] = new_pendiente
                df_recibos.at[ticket_idx, 'ESTADO_PAGO'] = "Pagado" if new_pendiente == 0.0 else "Por Pagar"
                
                # Save receipts
                save_table(df_recibos, "Recibos", REC_FILE, ["FOLIO", "FECHA", "CLIENTE", "PRODUCTOS", "TOTAL", "COSTO", "GANANCIA", "TIPO_PAGO", "ESTADO_PAGO", "ABONADO", "PENDIENTE"])
                
                # Recalculate debts for all clients in df_clientes
                for c_idx, c_row in df_clientes.iterrows():
                    c_name = c_row['CLIENTE']
                    debt = df_recibos[df_recibos['CLIENTE'] == c_name]['PENDIENTE'].sum()
                    df_clientes.at[c_idx, 'DEUDA'] = debt
                    df_clientes.at[c_idx, 'ESTADO'] = "Debe" if debt > 0 else "Al corriente"
                    
                save_table(df_clientes, "Clientes", CLI_FILE, ["CLIENTE", "TOTAL_COMPRADO", "METODO_COMUN", "FRECUENCIA", "DEUDA", "ESTADO"])
                
                st.success(f"Abono de ${abono_val:.2f} registrado para el folio {selected_folio}.")
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
    st.subheader("Gestión de Gastos y Balance General")
    
    col_gasto_form, col_balance = st.columns([1, 1.5])
    
    with col_gasto_form:
        st.markdown("#### Registrar Gasto Operativo")
        with st.form("expense_form", clear_on_submit=True):
            exp_date = st.date_input("Fecha del Gasto:", value=datetime.today().date())
            exp_cat = st.selectbox("Categoría:", ["GASOLINA", "RENTA", "SERVICIOS", "EXTRA"])
            exp_desc = st.text_input("Descripción del gasto:", placeholder="Ej. Combustible camión de reparto").strip().upper()
            exp_amount = st.number_input("Monto ($):", min_value=0.0, step=10.0, value=0.0)
            
            submit_gasto = st.form_submit_button("Guardar Gasto")
            
            if submit_gasto:
                if not exp_desc or exp_amount <= 0.0:
                    st.error("Por favor completa la descripción y el monto del gasto.")
                else:
                    new_expense = {
                        "FECHA": exp_date.strftime("%Y-%m-%d"),
                        "CATEGORIA": exp_cat,
                        "DESCRIPCION": exp_desc,
                        "MONTO": exp_amount
                    }
                    df_gastos = pd.concat([df_gastos, pd.DataFrame([new_expense])], ignore_index=True)
                    save_table(df_gastos, "Gastos", GAS_FILE, ["FECHA", "CATEGORIA", "DESCRIPCION", "MONTO"])
                    st.success(f"Gasto registrado: {exp_cat} por ${exp_amount:.2f}")
                    st.rerun()
                    
        # List Expenses
        st.markdown("#### Historial de Gastos")
        st.dataframe(df_gastos, use_container_width=True, hide_index=True)
        
    with col_balance:
        st.markdown("#### Balance General del Negocio")
        
        # Financial aggregates
        total_ingresos = df_recibos['TOTAL'].sum()
        total_costos_compra = df_recibos['COSTO'].sum()
        utilidad_bruta = total_ingresos - total_costos_compra
        total_gastos_op = df_gastos['MONTO'].sum()
        utilidad_neta = utilidad_bruta - total_gastos_op
        
        # Metrics Display
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric("Ventas Totales (Ingresos)", f"${total_ingresos:,.2f}")
            st.metric("Utilidad Bruta", f"${utilidad_bruta:,.2f}")
            st.metric("Gastos Operativos Totales", f"${total_gastos_op:,.2f}")
        with col_metric2:
            st.metric("Costo de Compra de Productos", f"${total_costos_compra:,.2f}")
            st.metric("Utilidad Neta (Ganancia Real)", f"${utilidad_neta:,.2f}")
            st.write("")
            st.info("📊 *Nota: La Utilidad Neta es la ganancia final del negocio restando el costo de los maicitos y los gastos operativos (gasolina, servicios, etc).*")

# TAB 5: ASISTENTE DE IA (ANTIGRAVITY)
with tab_ia:
    st.subheader("🤖 Asistente de IA de tu Negocio")
    
    if not api_key:
        st.warning("⚠️ **Falta la API Key:** Ingresa tu Gemini API Key en la barra lateral para poder chatear con tu asistente.")
    else:
        # Load google-generativeai dynamically
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
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
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(context_prompt)
                        st.markdown(response.text)
                st.session_state.ia_messages.append({"role": "assistant", "content": response.text})
                
        except Exception as e:
            st.error(f"Error al conectar con la IA de Gemini: {e}")
