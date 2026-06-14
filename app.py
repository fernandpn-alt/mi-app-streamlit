import streamlit as st
import pandas as pd
import os

# Set page config for a widescreen professional layout
st.set_page_config(
    page_title="Gestor de Inventario - Maicitos",
    page_icon="📊",
    layout="wide"
)

# Custom premium styling
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
</style>
""", unsafe_allow_html=True)

CSV_FILE = "productos.csv"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1A0BJg_Xr6BvhELp3vM6zeB4XSipcdeQTGGBgXENebq0/edit"
SHEET_EXPORT_URL = "https://docs.google.com/spreadsheets/d/1A0BJg_Xr6BvhELp3vM6zeB4XSipcdeQTGGBgXENebq0/export?format=csv"

# Global states
use_gsheets = False
worksheet = None

# Attempt to connect to Google Sheets using credentials in st.secrets
if "gserviceaccount" in st.secrets:
    try:
        import gspread
        # Authenticate using the service account credentials from Streamlit Secrets
        gc = gspread.service_account_from_dict(dict(st.secrets["gserviceaccount"]))
        
        # Get sheet URL from secrets or use default
        target_url = st.secrets.get("spreadsheet_url", SHEET_URL)
        sh = gc.open_by_url(target_url)
        worksheet = sh.get_worksheet(0)
        use_gsheets = True
    except Exception as e:
        st.sidebar.error(f"Error conectando a Google Sheets: {e}")

# Function to load data
def load_data():
    if use_gsheets and worksheet is not None:
        try:
            all_values = worksheet.get_all_values()
            if len(all_values) < 2:
                return pd.DataFrame(columns=['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA'])
            
            # Row 1 is empty in the user's spreadsheet, Row 2 is the header
            headers = [h.strip() for h in all_values[1]]
            rows = all_values[2:]
            
            df = pd.DataFrame(rows, columns=headers)
            # Filter to needed columns
            valid_cols = ['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA']
            cols_to_keep = [c for c in valid_cols if c in df.columns]
            df = df[cols_to_keep]
            
            # Ensure columns exist
            for col in valid_cols:
                if col not in df.columns:
                    df[col] = ""
            
            # Clean and parse types
            df['CÓDIGO'] = df['CÓDIGO'].astype(str).str.strip()
            df = df[df['CÓDIGO'] != ""]
            df['PRODUCTO'] = df['PRODUCTO'].astype(str).str.strip().str.upper()
            df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].astype(str).str.strip().str.upper()
            df['MARCA'] = df['MARCA'].astype(str).str.strip().str.upper()
            df['PRECIO COMPRA'] = pd.to_numeric(df['PRECIO COMPRA'], errors='coerce').fillna(0.0)
            return df
        except Exception as e:
            st.error(f"Error cargando datos desde Google Drive: {e}. Usando respaldo local.")
    
    # Fallback to local CSV
    if not os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(SHEET_EXPORT_URL, skiprows=1)
            df = df.dropna(how='all')
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df.columns = df.columns.str.strip()
            df['PRECIO COMPRA'] = pd.to_numeric(df['PRECIO COMPRA'], errors='coerce').fillna(0.0)
            df.to_csv(CSV_FILE, index=False)
        except Exception as e:
            return pd.DataFrame(columns=['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA'])
            
    df = pd.read_csv(CSV_FILE)
    df['CÓDIGO'] = df['CÓDIGO'].astype(str).str.strip()
    df['PRODUCTO'] = df['PRODUCTO'].astype(str).str.strip()
    df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].astype(str).str.strip()
    df['MARCA'] = df['MARCA'].astype(str).str.strip()
    df['PRECIO COMPRA'] = pd.to_numeric(df['PRECIO COMPRA'], errors='coerce').fillna(0.0)
    return df

# Function to save data
def save_data(df):
    if use_gsheets and worksheet is not None:
        try:
            # Clear and write starting at row 2 to preserve row 1 layout
            worksheet.clear()
            headers = ['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA']
            data_to_write = [headers] + df[headers].values.tolist()
            worksheet.update('A2', data_to_write)
            return True
        except Exception as e:
            st.error(f"Error guardando cambios en Google Drive: {e}")
            return False
            
    # Save local CSV
    df.to_csv(CSV_FILE, index=False)
    return True

# Load data into memory
df = load_data()

# Header
st.markdown("<h1 class='main-title'>📊 Gestor de Inventario</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Interfaz de administración y control para Maicitos.</p>", unsafe_allow_html=True)

# Connection Banner
if use_gsheets:
    st.success("🟢 **Conectado directamente a Google Drive.** Todos los cambios se guardarán automáticamente en tu hoja de cálculo en tiempo real.")
else:
    st.warning("⚠️ **Corriendo en Modo Local:** Los cambios se guardan temporalmente en la app. Para conectar la app directamente a tu Google Drive sin descargar archivos, ve a la pestaña **Sincronizar**.")

# Metrics / KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Productos", len(df))
with col2:
    avg_price = df['PRECIO COMPRA'].mean() if len(df) > 0 else 0.0
    st.metric("Precio Compra Promedio", f"${avg_price:.2f}")
with col3:
    max_price = df['PRECIO COMPRA'].max() if len(df) > 0 else 0.0
    st.metric("Precio Compra Máximo", f"${max_price:.2f}")

st.divider()

# Navigation Tabs
tab_list, tab_add, tab_edit, tab_delete, tab_sync = st.tabs([
    "📋 Ver Inventario", 
    "➕ Añadir Producto", 
    "✏️ Editar Producto", 
    "❌ Eliminar Producto",
    "💾 Sincronizar"
])

# TAB 1: VIEW INVENTORY
with tab_list:
    st.subheader("Lista de Productos")
    
    # Search and Filter Controls
    search_col, filter_col = st.columns([2, 1])
    with search_col:
        search_query = st.text_input("🔍 Buscar por Código, Producto o Descripción:", "").strip().lower()
    with filter_col:
        brands = ["Todos"] + sorted(df['MARCA'].unique().tolist())
        selected_brand = st.selectbox("Filtrar por Marca:", brands)
    
    # Filter dataframe
    filtered_df = df.copy()
    if selected_brand != "Todos":
        filtered_df = filtered_df[filtered_df['MARCA'] == selected_brand]
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['CÓDIGO'].str.lower().str.contains(search_query) |
            filtered_df['PRODUCTO'].str.lower().str.contains(search_query) |
            filtered_df['DESCRIPCIÓN'].str.lower().str.contains(search_query)
        ]
    
    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "CÓDIGO": st.column_config.TextColumn("Código"),
            "PRODUCTO": st.column_config.TextColumn("Producto"),
            "DESCRIPCIÓN": st.column_config.TextColumn("Descripción"),
            "MARCA": st.column_config.TextColumn("Marca"),
            "PRECIO COMPRA": st.column_config.NumberColumn("Precio Compra", format="$%.2f")
        }
    )

# TAB 2: ADD PRODUCT
with tab_add:
    st.subheader("Añadir un Nuevo Producto")
    with st.form("add_form", clear_on_submit=True):
        new_code = st.text_input("Código (único):", placeholder="Ej. PO09").strip().upper()
        new_product = st.text_input("Nombre del Producto:", placeholder="Ej. QUESITO").strip().upper()
        new_description = st.text_input("Descripción / Tamaño:", placeholder="Ej. BOLSA 50 GR").strip().upper()
        new_brand = st.text_input("Marca:", value="MAICITOS").strip().upper()
        new_price = st.number_input("Precio de Compra:", min_value=0.0, step=0.05, value=0.0)
        
        submitted = st.form_submit_button("Guardar Producto")
        
        if submitted:
            if not new_code or not new_product:
                st.error("⚠️ El Código y el Nombre del Producto son obligatorios.")
            elif new_code in df['CÓDIGO'].values:
                st.error(f"⚠️ El código '{new_code}' ya está asignado a otro producto.")
            else:
                new_row = {
                    "CÓDIGO": new_code,
                    "PRODUCTO": new_product,
                    "DESCRIPCIÓN": new_description,
                    "MARCA": new_brand,
                    "PRECIO COMPRA": new_price
                }
                # Append and save
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                if save_data(df):
                    st.success(f"🎉 Producto '{new_product}' añadido correctamente.")
                    st.rerun()

# TAB 3: EDIT PRODUCT
with tab_edit:
    st.subheader("Modificar un Producto Existente")
    if len(df) == 0:
        st.info("No hay productos disponibles para editar.")
    else:
        # Select product to edit
        product_options = [f"{row['CÓDIGO']} - {row['PRODUCTO']}" for _, row in df.iterrows()]
        selected_option = st.selectbox("Selecciona el producto a editar:", product_options)
        
        selected_code = selected_option.split(" - ")[0]
        product_idx = df[df['CÓDIGO'] == selected_code].index[0]
        current_data = df.loc[product_idx]
        
        with st.form("edit_form"):
            edit_code = st.text_input("Código (No editable):", value=current_data['CÓDIGO'], disabled=True)
            edit_product = st.text_input("Nombre del Producto:", value=current_data['PRODUCTO']).strip().upper()
            edit_description = st.text_input("Descripción / Tamaño:", value=current_data['DESCRIPCIÓN']).strip().upper()
            edit_brand = st.text_input("Marca:", value=current_data['MARCA']).strip().upper()
            edit_price = st.number_input("Precio de Compra:", min_value=0.0, step=0.05, value=float(current_data['PRECIO COMPRA']))
            
            save_changes = st.form_submit_button("Guardar Cambios")
            
            if save_changes:
                df.at[product_idx, 'PRODUCTO'] = edit_product
                df.at[product_idx, 'DESCRIPCIÓN'] = edit_description
                df.at[product_idx, 'MARCA'] = edit_brand
                df.at[product_idx, 'PRECIO COMPRA'] = edit_price
                if save_data(df):
                    st.success(f"✏️ Cambios guardados para el producto '{edit_product}'.")
                    st.rerun()

# TAB 4: DELETE PRODUCT
with tab_delete:
    st.subheader("Eliminar un Producto")
    if len(df) == 0:
        st.info("No hay productos para eliminar.")
    else:
        # Select product to delete
        delete_options = [f"{row['CÓDIGO']} - {row['PRODUCTO']}" for _, row in df.iterrows()]
        selected_delete = st.selectbox("Selecciona el producto a eliminar:", delete_options)
        
        delete_code = selected_delete.split(" - ")[0]
        delete_name = selected_delete.split(" - ")[1]
        
        st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar permanentemente a **{selected_delete}**?")
        confirm_delete = st.button("🗑️ Sí, eliminar producto", type="primary")
        
        if confirm_delete:
            df = df[df['CÓDIGO'] != delete_code]
            if save_data(df):
                st.success(f"🗑️ Producto '{delete_name}' eliminado.")
                st.rerun()

# TAB 5: SYNC & SECRET SETUP
with tab_sync:
    st.subheader("Configurar Conexión Directa a Google Drive")
    
    if use_gsheets:
        st.success("🟢 Tu aplicación ya está conectada directamente con Google Sheets. Los cambios se guardan automáticamente.")
    
    st.markdown(f"""
    Para sincronizar la app directamente con tu hoja en Drive sin descargas, sigue estos pasos:
    
    ### 1. Compartir tu hoja de cálculo
    Comparte tu hoja de cálculo con permisos de **Editor** al correo de la Cuenta de Servicio de Google que crees en el paso 2.
    * Tu hoja de cálculo actual es: [{SHEET_URL}]({SHEET_URL})
    
    ### 2. Obtener Credenciales de Cuenta de Servicio
    1. Ve a [Google Cloud Console](https://console.cloud.google.com/).
    2. Crea un proyecto y habilita la **Google Sheets API** y **Google Drive API**.
    3. Ve a **IAM & Admin > Service Accounts** (Cuentas de Servicio) y crea una.
    4. Genera una clave en formato **JSON** para esa cuenta y descárgala.
    5. Copia la dirección de correo de esa cuenta de servicio y **compártele tu Google Sheets en Drive como Editor**.
    
    ### 3. Agregar credenciales a los Secrets de Streamlit
    Abre tu panel de control en **Streamlit Community Cloud**, entra a la configuración de tu aplicación (*Settings > Secrets*) y pega lo siguiente adaptándolo con los datos de tu JSON descargado:
    
    ```toml
    spreadsheet_url = "{SHEET_URL}"
    
    [gserviceaccount]
    type = "service_account"
    project_id = "tu-proyecto-id"
    private_key_id = "tu-private-key-id"
    private_key = "-----BEGIN PRIVATE KEY-----\\nTuLlavePrivada...\\n-----END PRIVATE KEY-----\\n"
    client_email = "tu-cuenta-de-servicio@proyecto.iam.gserviceaccount.com"
    client_id = "tu-client-id"
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "https://www.googleapis.com/..."
    ```
    """)
    
    st.divider()
    
    st.markdown("### Respaldar Datos Locales")
    # Download Button
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Inventario Actual (CSV)",
        data=csv_data,
        file_name="inventario_maicitos.csv",
        mime="text/csv"
    )
