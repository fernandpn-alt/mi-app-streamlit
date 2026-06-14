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
SHEET_URL = "https://docs.google.com/spreadsheets/d/1A0BJg_Xr6BvhELp3vM6zeB4XSipcdeQTGGBgXENebq0/export?format=csv"

# Function to load data
def load_data():
    # If local database file doesn't exist, download from Google Sheets
    if not os.path.exists(CSV_FILE):
        try:
            # Skip the first empty row from Google Sheets CSV export
            df = pd.read_csv(SHEET_URL, skiprows=1)
            # Remove entirely empty rows/columns
            df = df.dropna(how='all')
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df.columns = df.columns.str.strip()
            # Clean numeric values
            df['PRECIO COMPRA'] = pd.to_numeric(df['PRECIO COMPRA'], errors='coerce').fillna(0.0)
            # Save locally
            df.to_csv(CSV_FILE, index=False)
        except Exception as e:
            st.error(f"Error cargando desde Google Sheets: {e}")
            return pd.DataFrame(columns=['CÓDIGO', 'PRODUCTO', 'DESCRIPCIÓN', 'MARCA', 'PRECIO COMPRA'])
    
    # Load from local CSV
    df = pd.read_csv(CSV_FILE)
    df['CÓDIGO'] = df['CÓDIGO'].astype(str).str.strip()
    df['PRODUCTO'] = df['PRODUCTO'].astype(str).str.strip()
    df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].astype(str).str.strip()
    df['MARCA'] = df['MARCA'].astype(str).str.strip()
    df['PRECIO COMPRA'] = pd.to_numeric(df['PRECIO COMPRA'], errors='coerce').fillna(0.0)
    return df

# Function to save data
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Load data into session state
df = load_data()

# Header
st.markdown("<h1 class='main-title'>📊 Gestor de Inventario</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Interfaz de administración y control para Maicitos.</p>", unsafe_allow_html=True)

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
            "CÓDIGO": st.column_config.TextColumn("Código", help="Código único de producto"),
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
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
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
                save_data(df)
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
            save_data(df)
            st.success(f"🗑️ Producto '{delete_name}' eliminado.")
            st.rerun()

# TAB 5: SYNC & DOWNLOAD
with tab_sync:
    st.subheader("Guardar y Sincronizar Cambios")
    st.markdown("""
    Como la aplicación corre de forma aislada en la nube o en tu dispositivo local:
    
    1. **Descarga tu inventario actualizado:** Puedes bajar la tabla actual en formato CSV e importarla en tu Google Sheets si deseas actualizar tu nube.
    2. **Resetear al original:** Si deseas borrar todos tus cambios locales y volver a cargar los datos originales de tu enlace de Google Sheets, usa el botón de restauración.
    """)
    
    # Download Button
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Inventario Actualizado (CSV)",
        data=csv_data,
        file_name="inventario_maicitos.csv",
        mime="text/csv"
    )
    
    st.divider()
    
    # Reset button
    st.markdown("### Restablecer Base de Datos")
    st.warning("Esto eliminará cualquier producto que hayas añadido, editado o borrado localmente, y volverá a descargar el Excel de Google Drive.")
    if st.button("🔄 Restablecer al original de Google Sheets"):
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        st.success("Base de datos local eliminada. Recargando datos originales...")
        st.rerun()
