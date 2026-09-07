import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import io
import openpyxl
from PIL import Image

# Intentar cargar el logo corporativo
try:
    logo = Image.open("logo_PYS.jpeg")
except Exception:
    logo = None

# =========================================================================
# 1. CONFIGURACIÓN DE PÁGINA
# =========================================================================
st.set_page_config(
    page_title="Logística de Distribución - PYS",
    page_icon="logo_PYS.jpg" if logo else "📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# 2. ESTILO CSS AVANZADO UI/UX
# =========================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Contenedor Global */
    .block-container { 
        padding-top: 1.5rem; 
        padding-bottom: 2rem; 
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
    }
    
    h1, h2, h3, h4 { color: #0F172A; font-weight: 700; letter-spacing: -0.02em; }
    
    /* 📈 TARJETAS KPI */
    .kpi-card-premium {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
    }
    .kpi-blue { border-top: 4px solid #1E40AF; }
    .kpi-indigo { border-top: 4px solid #4F46E5; }
    .kpi-emerald { border-top: 4px solid #059669; }
    .kpi-orange { border-top: 4px solid #EA580C; }
    .kpi-val-p { font-size: 30px; font-weight: 700; color: #1E293B; line-height: 1; }
    .kpi-lbl-p { font-size: 11px; color: #64748B; text-transform: uppercase; margin-top: 8px; letter-spacing: 0.05em; font-weight: 600; }
    
    /* 📋 FILAS DE TRAZABILIDAD */
    .timeline-container-p {
        background-color: #FFFFFF; 
        border: 1px solid #E2E8F0; 
        border-radius: 12px;
        padding: 14px 18px; 
        margin-bottom: 12px; 
        display: flex; 
        flex-direction: column;
        gap: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .timeline-container-p:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px -3px rgba(0, 0, 0, 0.04);
        border-color: #CBD5E1;
    }
    .timeline-header-block {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .op-badge-p {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        color: white;
        padding: 6px 12px;
        font-weight: 700;
        border-radius: 8px;
        font-size: 13px;
        text-align: center;
    }
    /* Badge de operación clicable (botón real disfrazado del mismo estilo del badge) */
    div[data-testid="stMarkdown"]:has(.op-badge-marker) + div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 4px 12px !important;
        min-height: unset !important;
    }
    div[data-testid="stMarkdown"]:has(.op-badge-marker) + div[data-testid="stButton"] button:hover {
        color: #E2E8F0 !important;
        border: none !important;
        background: linear-gradient(135deg, #274690 0%, #16213e 100%) !important;
    }
    .timeline-main-text {
        font-size: 14px;
        color: #1E293B;
        font-weight: 600;
        margin-top: 2px;
    }
    .timeline-sub-text {
        font-size: 12.5px;
        color: #64748B;
        display: flex;
        gap: 8px;
        align-items: center;
    }
    .timeline-footer-block {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #F1F5F9;
        padding-top: 8px;
        font-size: 12px;
    }
    .timeline-eta {
        color: #475569;
        font-weight: 600;
    }
    
    /* BADGES DE ESTADO */
    .status-badge {
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-align: center;
    }
    .status-entregado { background-color: #DCFCE7; color: #15803D; }
    .status-transito { background-color: #FEF3C7; color: #B45309; }
    .status-despachar { background-color: #FFEDD5; color: #C2410C; }
    .status-proceso { background-color: #F1F5F9; color: #475569; }
    
    /* BADGES DE PAGO */
    .pago-badge {
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }
    .pago-si { background-color: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
    .pago-no { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }

    /* SECCIÓN YA ESTÁ PAGO EXCLUSIVA */
    .pago-exitoso-box {
        background-color: #ECFDF5;
        border: 2px dashed #10B981;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        color: #065F46;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.05);
    }
    
    /* ⏳ SISTEMA DE SEMÁFOROS MÓDULO 2 */
    .semaforo-box-p { 
        padding: 12px 18px; 
        border-radius: 10px; 
        margin-bottom: 8px; 
        font-size: 13.5px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        font-weight: 500;
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        color: #1E293B;
    }
    .sem-verde { border-left: 5px solid #10B981; background-color: #F0FDF4; }
    .sem-amarillo { border-left: 5px solid #F59E0B; background-color: #FEF3C7; }
    .sem-rojo { border-left: 5px solid #EF4444; background-color: #FEF2F2; }
    .sem-gris { border-left: 5px solid #64748B; background-color: #F8FAFC; }
    
    .empty-state-text {
        color: #94A3B8;
        font-size: 13.5px;
        font-style: italic;
        text-align: center;
        padding: 20px;
        background: #FFFFFF;
        border: 1px dashed #E2E8F0;
        border-radius: 12px;
    }

    /* 🚚 TARJETAS DE CONTENEDORES */
    .container-box-p { 
        background: #FFFFFF; 
        border: 1px solid #E2E8F0; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        overflow: hidden; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        width: 100%;
    }
    .container-header-p { 
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        color: #FFFFFF; 
        padding: 14px 18px; 
        font-size: 13.5px; 
        font-weight: 700; 
        display: flex; 
        justify-content: space-between; 
    }
    .container-body-p { 
        padding: 16px; 
        background-color: #F8FAFC; 
        display: flex; 
        flex-direction: column; 
        gap: 12px; 
    }
    .product-row-p { 
        background: #FFFFFF; 
        border: 1px solid #E2E8F0; 
        border-radius: 8px; 
        padding: 14px 16px; 
        font-size: 13.5px; 
        border-left: 4px solid #3B82F6; 
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .product-title-p { font-weight: 700; color: #1E293B; font-size:14px; }
    .product-subtitle-p { font-weight: 500; color: #64748B; }
    .product-meta-p { font-size: 12px; color: #475569; font-weight: 500; display: flex; gap: 8px; align-items: center; }

    /* 🚨 TARJETAS EN FABRICACIÓN */
    .dispatch-card-premium {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #EA580C; 
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: auto;
        margin-bottom: 16px;
    }
    .dispatch-card-premium:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px -3px rgba(234, 88, 12, 0.1);
        border-color: #F97316;
    }
    .dispatch-tag {
        background-color: #FFEDD5; 
        color: #C2410C; 
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 12px;
        width: fit-content;
    }
    .dispatch-model { font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 8px; }
    
    .dispatch-items-list {
        margin: 0 0 14px 0;
        padding: 0;
        list-style: none;
    }
    .dispatch-item-line {
        font-size: 13px;
        color: #475569;
        line-height: 1.5;
        position: relative;
        padding-left: 14px;
        margin-bottom: 4px;
    }
    .dispatch-item-line::before {
        content: "•";
        color: #EA580C;
        font-weight: bold;
        position: absolute;
        left: 0;
        top: 0;
    }

    .dispatch-meta-row { 
        display: flex; 
        justify-content: space-between; 
        background: #F8FAFC; 
        padding: 8px 12px; 
        border-radius: 8px; 
        font-size: 12px; 
        color: #64748B;
    }
    .dispatch-date {
        margin-top: 12px;
        font-size: 12.5px;
        color: #64748B;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* 🧭 SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        color: #F1F5F9;
        min-width: 300px !important;
        max-width: 300px !important;
    }
    [data-testid="stSidebarResizer"] { display: none !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p { color: #FFFFFF !important; }
    [data-testid="stSidebar"] .stRadio > label { color: #94A3B8 !important; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
    
    div.row-widget.stRadio div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 12px 16px !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
        width: 100%;
    }
    div.row-widget.stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: #3B82F6 !important;
        border-color: #3B82F6 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

def _resolver_paleta_tema(wb):
    """Extrae los 12 colores del tema del workbook (hex sin '#'), en el orden que usa
    openpyxl para el índice 'theme' de una celda: dk1, lt1, dk2, lt2, accent1..accent6, hlink, folHlink."""
    try:
        from xml.etree import ElementTree as ET
        theme_xml = wb.loaded_theme
        if not theme_xml:
            return None
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        root = ET.fromstring(theme_xml)
        esquema = root.find('.//a:clrScheme', ns)
        orden = ['dk1', 'lt1', 'dk2', 'lt2', 'accent1', 'accent2', 'accent3', 'accent4', 'accent5', 'accent6', 'hlink', 'folHlink']
        colores = []
        for tag in orden:
            nodo = esquema.find(f'a:{tag}', ns)
            hijo = list(nodo)[0]
            if hijo.tag.endswith('srgbClr'):
                colores.append(hijo.get('val'))
            elif hijo.tag.endswith('sysClr'):
                colores.append(hijo.get('lastClr', 'FFFFFF'))
            else:
                colores.append('FFFFFF')
        # Excel intercambia dk1/lt1 y dk2/lt2 respecto al índice 'theme' que usan las celdas
        colores[0], colores[1] = colores[1], colores[0]
        colores[2], colores[3] = colores[3], colores[2]
        return colores
    except Exception:
        return None

def _aplicar_tint(hex_color, tint):
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    def ajustar(c):
        return c * (1 + tint) if tint < 0 else c * (1 - tint) + (255 * tint)
    return tuple(int(round(min(max(ajustar(c), 0), 255))) for c in (r, g, b))

def detectar_filas_qty_azul(excel_bytes, sheet_name, col_nombre='QTY'):
    """Devuelve el set de índices de fila (0-based, relativos a los datos, sin encabezado)
    cuya celda de la columna indicada tiene relleno azul claro en el Excel original.
    Esto identifica cantidades que, según la convención del Plan, no se van a enviar.
    Resuelve tanto colores RGB directos (paleta Standard Colors) como colores de tema
    con tint (paleta Theme Colors), que es la fila superior del selector de relleno de Excel."""
    filas_azules = set()
    try:
        wb = openpyxl.load_workbook(io.BytesIO(excel_bytes), data_only=True)
        ws = wb[sheet_name]
        paleta_tema = _resolver_paleta_tema(wb)
        encabezados = [str(c.value).strip() if c.value is not None else "" for c in next(ws.iter_rows(min_row=1, max_row=1))]
        if col_nombre not in encabezados:
            return filas_azules
        col_idx = encabezados.index(col_nombre)

        for i, fila in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row)):
            celda = fila[col_idx]
            color = celda.fill.fgColor if celda.fill is not None else None
            rgb = None
            if color is not None:
                tipo_color = getattr(color, 'type', None)
                if tipo_color == 'rgb' and isinstance(color.rgb, str) and len(color.rgb) == 8:
                    rgb = (int(color.rgb[2:4], 16), int(color.rgb[4:6], 16), int(color.rgb[6:8], 16))
                elif tipo_color == 'theme' and paleta_tema is not None:
                    idx = color.theme
                    if isinstance(idx, int) and 0 <= idx < len(paleta_tema):
                        rgb = _aplicar_tint(paleta_tema[idx], color.tint or 0.0)

            if rgb:
                r, g, b = rgb
                # Heurística: azul claro -> el canal azul domina sobre rojo/verde y hay buena luminosidad
                if b > r + 15 and b > g + 5 and b > 150:
                    filas_azules.add(i)
    except Exception:
        return set()
    return filas_azules

def ejecutar_sincronizacion_onedrive():
    # Agregamos df_proyeccion para mapear la pestaña real del maestro
    resultado = {"df_plan": None, "df_maestro": None, "df_pagos": None, "df_proyeccion": None, "df_notas_credito": None, "error": None}
    try:
        sec = st.secrets["microsoft_graph"]
        tenant_id = sec["TENANT_ID"]
        client_id = sec["CLIENT_ID"]
        client_secret = sec["CLIENT_SECRET"]
        file_maestro_id = sec["FILE_ID_MAESTRO"]
        file_plan_id = sec["FILE_ID_PLAN"]
        
        url_auth = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        res_token = requests.post(url_auth, data=payload, timeout=10)
        if res_token.status_code != 200:
            resultado["error"] = f"Error de Autenticación Azure: {res_token.text}"
            return resultado
            
        token = res_token.json().get("access_token")
        headers = {'Authorization': f'Bearer {token}'}
        user_principal_name = "planeacion.proyectos@proyectosyservicios.net"
        
        # 1. Descarga del archivo EXCEL_MAESTRO
        url_m = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/drive/items/{file_maestro_id}/content"
        res_m = requests.get(url_m, headers=headers, timeout=15)
        
        # 2. Descarga del archivo PLAN DE PRODUCCIÓN (Fábrica)
        url_p = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/drive/items/{file_plan_id}/content"
        res_p = requests.get(url_p, headers=headers, timeout=15)
        
        # SOLUCIÓN CRÍTICA: Cargamos el archivo en un objeto ExcelFile una sola vez
        archivo_maestro_unico = pd.ExcelFile(io.BytesIO(res_m.content))
        
        # Extracción limpia de pestañas desde el mismo objeto cargado en memoria
        df_m = archivo_maestro_unico.parse(sheet_name="BASE_DATOS_MAESTRO")
        df_pagos = archivo_maestro_unico.parse(sheet_name="PAGOS FRA")
        
        try:
            df_proy = archivo_maestro_unico.parse(sheet_name="PROYECCION")
            df_proy.columns = df_proy.columns.str.strip()
        except Exception:
            df_proy = None

        try:
            # Ahora .parse funcionará perfectamente sin corromper la memoria, saltando las 3 filas muertas
            df_nc = archivo_maestro_unico.parse(sheet_name="NOTA CREDITO")
            df_nc.columns = df_nc.columns.str.strip()
            df_nc = df_nc.dropna(how='all')

            if 'DESCRIPCIÓN' in df_nc.columns:
                df_nc['DESCRIPCIÓN'] = df_nc['DESCRIPCIÓN'].astype(str).str.strip()
        except Exception as e_nc:
            # Guardamos el error en los logs internos por si el nombre de la hoja cambia
            print(f"Error parseando NOTAS CREDITO: {e_nc}")
            df_nc = None
            
        # Carga del Plan de Fábrica (Pestaña Hoja1 del archivo independiente)
        df_p = pd.read_excel(io.BytesIO(res_p.content), sheet_name="Hoja1")

        df_p.columns = df_p.columns.str.strip()

        # Marcamos las filas cuya celda QTY está resaltada en azul claro: son cantidades
        # pequeñas que no se van a enviar (se cancelan), según la convención del Plan.
        filas_qty_azul = detectar_filas_qty_azul(res_p.content, sheet_name="Hoja1", col_nombre="QTY")
        df_p['QTY_NO_SE_ENVIA'] = [i in filas_qty_azul for i in range(len(df_p))]
        df_m.columns = df_m.columns.str.strip()
        df_pagos.columns = df_pagos.columns.str.strip()
        
        columnas_fecha = ['EMISIÓN FRA', 'ETA', 'VENCIMIENTO 45 D - 2%', 'VENCIMIENTO 69D 1.5%', 'VENCIMIENTO 89D - 1%', 'VENCIMIENTO 120D - PLENO']
        for col in columnas_fecha:
            if col in df_m.columns:
                df_m[col] = pd.to_datetime(df_m[col], errors='coerce')
                
        resultado["df_plan"] = df_p
        resultado["df_maestro"] = df_m
        resultado["df_pagos"] = df_pagos
        resultado["df_proyeccion"] = df_proy
        resultado["df_notas_credito"] = df_nc
        
    except Exception as e_global:
        resultado["error"] = f"Excepción del sistema de enlace: {e_global}"
    return resultado

@st.cache_data(ttl=300)
def cargar_datos_seguros():
    return ejecutar_sincronizacion_onedrive()

# --- ASIGNACIÓN GLOBAL CORRECTA ---
data_response = cargar_datos_seguros()
df_plan = data_response.get("df_plan")              # Plan de Fábrica (Módulo 3)
df_maestro = data_response.get("df_maestro")        # Base de Datos principal (Módulo 1 y 2)
df_pagos = data_response.get("df_pagos")            # Pagos Facturas
df_proyeccion = data_response.get("df_proyeccion")  # Pestaña nueva Proyecciones (Módulo 2)
df_notas_credito = data_response.get("df_notas_credito")
error_detectado = data_response.get("error")

col_estado_pago = None
if df_maestro is not None:
    col_estado_pago = next((c for c in ['ESTADO_PAGO', 'ESTADO PAGO', 'Estado_Pago'] if c in df_maestro.columns), None)

# --- RESOLUCIÓN DE NAVEGACIÓN PENDIENTE (clic en badge de operación) ---
# Debe ejecutarse ANTES de instanciar el radio del menú, porque Streamlit no permite
# modificar st.session_state de un widget después de que ya fue creado en esta misma corrida.
if 'ir_a_detalle_operacion' in st.session_state:
    st.session_state['menu_radio'] = "🔍 Detalle de Operación"
    st.session_state['select_operacion_detalle'] = st.session_state.pop('ir_a_detalle_operacion')

# =========================================================================
# 4. MENÚ LATERAL
# =========================================================================
with st.sidebar:
    st.write("")
    if logo:
        try:
            # Streamlit reciente (ej. el desplegado en la nube): parámetro unificado width
            st.image(logo, width='stretch')
        except TypeError:
            # Streamlit local más antiguo (1.39.0): no conoce width='stretch'
            st.image(logo, use_column_width=True)
    else:
        st.markdown("<h2 style='margin-bottom:0px; font-size:22px;'>PROYECTOS Y SERVICIOS</h2>", unsafe_allow_html=True)
        
    st.markdown("<p style='color:#94A3B8; font-size:13px; margin-top:2px; margin-bottom:25px;'>Control e Inteligencia Logística</p>", unsafe_allow_html=True)
    st.markdown("<label style='color:#94A3B8; font-size:11px; font-weight:600; letter-spacing:0.05em;'>MÓDULOS DEL SISTEMA</label>", unsafe_allow_html=True)
    
    menu = st.radio(
        "Módulos Estratégicos:",
        ["📈 Trazabilidad e Historial", "🔍 Detalle de Operación", "🚨 Referencias en Producción"],
        label_visibility="collapsed",
        key="menu_radio"
    )
    
    st.write("")
    if st.button("🔄 Sincronizar Datos Nube", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("""
        <div class="sidebar-footer-p" style="
            width: 100%;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: 15px;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #475569;
            font-size: 12px;
            font-family: sans-serif;
        ">
        <strong style="color: #475569;">Proyectos y Servicios SAS</strong><br>
        Área de Planeación e Importaciones<br>
        <span style='font-size:10px; color:#475569;'>Enterprise System v4.5</span>
        </div> """, unsafe_allow_html=True)

# =========================================================================
# 5. PANTALLA PRINCIPAL
# =========================================================================
if error_detectado is not None:
    st.error(error_detectado)

elif df_plan is not None and df_maestro is not None and df_pagos is not None:
    fecha_hoy = datetime.now()
    col_cop_name = next((n for n in ['VALOR_NACIONALIZADO', 'VALOR NACIONALIZADO COP', 'VALOR_NACIONALIZADO_COP', 'VALOR NACIONALIZADO'] if n in df_maestro.columns), None)

# --- MÓDULO 1: TRAZABILIDAD E HISTORIAL (CONSOLIDADO LOGÍSTICO-FINANCIERO) ---
    if menu == "📈 Trazabilidad e Historial":
        st.title("Control general de operaciones")
        st.markdown("<p style='color: #64748B; font-size:14px;'>Consolidado estratégico de importaciones distribuido por estatus operativo y financiero de manera ejecutiva.</p>", unsafe_allow_html=True)

        # --- BARRA INFORMATIVA: LLEGADAS DEL MES ACTUAL (SEGUIMIENTO RÁPIDO, AUTOMÁTICA) ---
        df_eta_valido = df_maestro.dropna(subset=['ETA']).copy() if 'ETA' in df_maestro.columns else pd.DataFrame()

        if not df_eta_valido.empty:
            periodo_actual = pd.Period(fecha_hoy, freq='M')
            df_eta_valido['AÑO_MES'] = df_eta_valido['ETA'].dt.to_period('M')
            df_mes = df_eta_valido[df_eta_valido['AÑO_MES'] == periodo_actual]

            # Solo lo que falta por llegar: excluimos lo que el ESTADO DE DISTRIBUCION ya marca como entregado/llegado
            if 'ESTADO DE DISTRIBUCION' in df_mes.columns:
                estado_clean_mes = df_mes['ESTADO DE DISTRIBUCION'].astype(str).str.lower().str.replace('á', 'a', regex=False)
                ya_llego_mes = estado_clean_mes.str.contains('entregado', na=False) | estado_clean_mes.str.contains('llego', na=False)
                df_mes = df_mes[~ya_llego_mes]

            meses_es = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
            etiqueta_mes_actual = f"{meses_es[periodo_actual.month]} {periodo_actual.year}"

            operaciones_mes = sorted(df_mes['OPERACIÓN'].dropna().unique()) if 'OPERACIÓN' in df_mes.columns else []

            if not operaciones_mes:
                texto_barra = f"Sin operaciones programadas para llegar en {etiqueta_mes_actual}."
            elif len(operaciones_mes) == 1:
                texto_barra = f"En este mes llega la operación:&nbsp;<strong>{operaciones_mes[0]}</strong>."
            else:
                primeros = ", ".join(operaciones_mes[:-1])
                ultimo = operaciones_mes[-1]
                texto_barra = f"En este mes llegan las operaciones:&nbsp;<strong>{primeros}&nbsp;y&nbsp;{ultimo}</strong>."

            st.markdown(f"""
            <div style="background-color:#F5F4FF; border:1px solid #E3E1FA; border-radius:10px; padding:9px 16px; font-size:14px; color:#1E293B; display:flex; align-items:center;">
            📅 {texto_barra}
            </div>
            """, unsafe_allow_html=True)

            if st.button("Referencias que llegan"):
                st.session_state['mostrar_llegadas_mes'] = not st.session_state.get('mostrar_llegadas_mes', False)

            if st.session_state.get('mostrar_llegadas_mes') and 'REFERENCIA/MODELO' in df_mes.columns:
                df_mes_ref = df_mes.copy()
                df_mes_ref['REFERENCIA/MODELO'] = df_mes_ref['REFERENCIA/MODELO'].astype(str).str.strip().str.upper()
                tabla_llegadas = df_mes_ref.groupby(['REFERENCIA/MODELO', 'ETA']).agg({'CANTIDAD': 'sum'}).reset_index()
                tabla_llegadas = tabla_llegadas.sort_values('ETA')
                tabla_llegadas['ETA'] = tabla_llegadas['ETA'].dt.strftime('%Y-%m-%d')

                st.dataframe(
                    tabla_llegadas.rename(columns={'REFERENCIA/MODELO': 'Referencia', 'CANTIDAD': 'Cantidad', 'ETA': 'Fecha de llegada'}),
                    use_container_width=True,
                    hide_index=True
                )

        st.markdown("<hr style='margin:8px 0 18px 0; border:none; border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)

        # --- PROCESAMIENTO INTERNO DE LA PESTAÑA PAGOS FRA ---
        if 'df_pagos' not in locals() and 'df_pagos' not in globals():
            df_pagos = pd.DataFrame(columns=['OPERACIÓN', 'VALOR TOTAL FACTURA (USD)', 'VALOR ABONO (USD)', 'DESCUENTO APLICADO (USD)', 'NOTA APOYO PROVEEDOR (USD)', 'OBSERVACIÓN NOTA APOYO'])

        df_pagos_clean = df_pagos.copy()
        for col_f in ['VALOR TOTAL FACTURA (USD)', 'VALOR ABONO (USD)', 'DESCUENTO APLICADO (USD)', 'NOTA APOYO PROVEEDOR (USD)']:
            if col_f in df_pagos_clean.columns:
                df_pagos_clean[col_f] = pd.to_numeric(df_pagos_clean[col_f], errors='coerce').fillna(0)
            else:
                df_pagos_clean[col_f] = 0.0
                
        if 'OBSERVACIÓN NOTA APOYO' in df_pagos_clean.columns:
            df_pagos_clean['OBSERVACIÓN NOTA APOYO'] = df_pagos_clean['OBSERVACIÓN NOTA APOYO'].fillna('').astype(str).str.strip()
        else:
            df_pagos_clean['OBSERVACIÓN NOTA APOYO'] = ""
        
        # Consolidación agrupando por Operación en la tabla de PAGOS
        pagos_resumidos = df_pagos_clean.groupby('OPERACIÓN').agg({
            'VALOR TOTAL FACTURA (USD)': 'first',
            'VALOR ABONO (USD)': 'sum',
            'DESCUENTO APLICADO (USD)': 'sum',
            'NOTA APOYO PROVEEDOR (USD)': 'sum',
            'OBSERVACIÓN NOTA APOYO': lambda x: " | ".join([v for v in x.unique() if v != '' and pd.notna(v)])
        }).reset_index()
        
        pagos_resumidos['TOTAL_DESCUENTOS_REGISTRADOS'] = pagos_resumidos['DESCUENTO APLICADO (USD)'] + pagos_resumidos['NOTA APOYO PROVEEDOR (USD)']
        pagos_resumidos['SALDO_CONTABLE'] = pagos_resumidos['VALOR TOTAL FACTURA (USD)'] - (pagos_resumidos['VALOR ABONO (USD)'] + pagos_resumidos['TOTAL_DESCUENTOS_REGISTRADOS'])
        
        # --- IDENTIFICACIÓN DINÁMICA DE LA COLUMNA DE COSTOS ---
        # CORREGIDO: Se eliminó el error de escritura "RAM" que estaba aquí
        col_costo_maestro = 'VALOR TOTAL EQUIPOS (USD)'
        if col_costo_maestro not in df_maestro.columns and 'VALOR TOTAL (USD)' in df_maestro.columns:
            col_costo_maestro = 'VALOR TOTAL (USD)'

        # Bloques de KPIs principales basados en la data logística
        ckpi1, ckpi2, ckpi3 = st.columns(3)
        total_usd = df_maestro[col_costo_maestro].sum() if col_costo_maestro in df_maestro.columns else 0
        total_conts = df_maestro['CONTENEDOR'].nunique() if 'CONTENEDOR' in df_maestro.columns else 0
        total_unis = df_maestro['CANTIDAD'].sum() if 'CANTIDAD' in df_maestro.columns else 0
        
        with ckpi1: st.markdown(f'<div class="kpi-card-premium kpi-blue"><div class="kpi-val-p">USD {total_usd:,.2f}</div><div class="kpi-lbl-p">Inversión Total Equipos</div></div>', unsafe_allow_html=True)
        with ckpi2: st.markdown(f'<div class="kpi-card-premium kpi-indigo"><div class="kpi-val-p">{total_conts}</div><div class="kpi-lbl-p">Contenedores Gestión</div></div>', unsafe_allow_html=True)
        with ckpi3: st.markdown(f'<div class="kpi-card-premium kpi-emerald"><div class="kpi-val-p">{int(total_unis):,}</div><div class="kpi-lbl-p">Unidades Globales Importadas</div></div>', unsafe_allow_html=True)
        
        # --- PROCESAMIENTO DE CRUCE PARA INTEGRACIÓN EN TARJETAS ---
        if 'OPERACIÓN' in df_maestro.columns:
            columnas_fechas_tramos = ['VENCIMIENTO 45 D - 2%', 'VENCIMIENTO 69D 1.5%', 'VENCIMIENTO 89D - 1%', 'VENCIMIENTO 120D - PLENO']
            agg_dict_fechas = {}
            for col_f in columnas_fechas_tramos:
                if col_f in df_maestro.columns:
                    df_maestro[col_f] = pd.to_datetime(df_maestro[col_f], errors='coerce')
                    agg_dict_fechas[col_f] = 'first'

            agg_maestro_pagos = df_maestro.groupby('OPERACIÓN').agg(agg_dict_fechas).reset_index()
            
            df_tabla_consolidada = pd.merge(agg_maestro_pagos, pagos_resumidos, on='OPERACIÓN', how='left')
            df_tabla_consolidada['VALOR TOTAL FACTURA (USD)'] = df_tabla_consolidada['VALOR TOTAL FACTURA (USD)'].fillna(0)
            df_tabla_consolidada['VALOR ABONO (USD)'] = df_tabla_consolidada['VALOR ABONO (USD)'].fillna(0)
            df_tabla_consolidada['DESCUENTO APLICADO (USD)'] = df_tabla_consolidada['DESCUENTO APLICADO (USD)'].fillna(0)
            df_tabla_consolidada['NOTA APOYO PROVEEDOR (USD)'] = df_tabla_consolidada['NOTA APOYO PROVEEDOR (USD)'].fillna(0)
            df_tabla_consolidada['TOTAL_DESCUENTOS_REGISTRADOS'] = df_tabla_consolidada['TOTAL_DESCUENTOS_REGISTRADOS'].fillna(0)
            df_tabla_consolidada['SALDO_CONTABLE'] = df_tabla_consolidada['SALDO_CONTABLE'].fillna(0)
            df_tabla_consolidada['OBSERVACIÓN NOTA APOYO'] = df_tabla_consolidada['OBSERVACIÓN NOTA APOYO'].fillna('')

            # --- RENDERIZADO DE DISTRIBUCIÓN UNIFICADA ---
            st.markdown("<h3 style='margin-top:25px; margin-bottom:15px;'>📋 Monitoreo Unificado de Distribución y Pagos</h3>", unsafe_allow_html=True)
            col_izquierda, col_derecha = st.columns(2)
            
            agg_dict_ops = {
                'CONTENEDOR': 'nunique', 
                'CANTIDAD': 'sum', 
                col_costo_maestro: 'sum',
                'ESTADO DE DISTRIBUCION': lambda x: str(x.dropna().iloc[0]).strip() if not x.dropna().empty else "En Proceso",
                'ETA': lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NaT
            }
            if col_estado_pago:
                agg_dict_ops[col_estado_pago] = lambda x: str(x.dropna().iloc[0]).strip().upper() if not x.dropna().empty else ""

            ops_resumen = df_maestro.groupby('OPERACIÓN').agg(agg_dict_ops).reset_index()
            
            def renderizar_tarjeta_operacion(row_op, contexto):
                op_id = row_op['OPERACIÓN']
                eta_str = row_op['ETA'].strftime('%Y-%m-%d') if pd.notna(row_op['ETA']) else "Por Confirmar"
                estado_texto = row_op['ESTADO DE DISTRIBUCION']
                estado_clean = estado_texto.lower().replace('á', 'a')
                
                costo_equipos = row_op[col_costo_maestro]
                
                # Buscar cruce financiero
                match_finanzas = df_tabla_consolidada[df_tabla_consolidada['OPERACIÓN'] == op_id]
                
                val_factura = costo_equipos
                val_abonos = 0.0
                val_descuentos_ya_aplicados = 0.0
                val_nota = 0.0
                obs_nota = ""
                
                f_45, f_69, f_89, f_120 = pd.NaT, pd.NaT, pd.NaT, pd.NaT
                
                if not match_finanzas.empty:
                    val_factura = match_finanzas['VALOR TOTAL FACTURA (USD)'].iloc[0] if match_finanzas['VALOR TOTAL FACTURA (USD)'].iloc[0] > 0 else costo_equipos
                    val_abonos = match_finanzas['VALOR ABONO (USD)'].iloc[0]
                    val_descuentos_ya_aplicados = match_finanzas['DESCUENTO APLICADO (USD)'].iloc[0]
                    val_nota = match_finanzas['NOTA APOYO PROVEEDOR (USD)'].iloc[0]
                    obs_nota = match_finanzas['OBSERVACIÓN NOTA APOYO'].iloc[0]

                    if 'VENCIMIENTO 45 D - 2%' in match_finanzas.columns: f_45 = match_finanzas['VENCIMIENTO 45 D - 2%'].iloc[0]
                    if 'VENCIMIENTO 69D 1.5%' in match_finanzas.columns: f_69 = match_finanzas['VENCIMIENTO 69D 1.5%'].iloc[0]
                    if 'VENCIMIENTO 89D - 1%' in match_finanzas.columns: f_89 = match_finanzas['VENCIMIENTO 89D - 1%'].iloc[0]
                    if 'VENCIMIENTO 120D - PLENO' in match_finanzas.columns: f_120 = match_finanzas['VENCIMIENTO 120D - PLENO'].iloc[0]

                # --- ⚡ REGION DE LOGICA MODIFICADA ⚡ ---
                descuento_proyectado_porcentaje = 0.0
                valor_descuento_pronto_pago = 0.0
                
                if val_abonos > 0:
                    # CASO 1: LA FACTURA TIENE ABONOS REGISTRADOS
                    # Se ignora el calendario del sistema y calculamos el saldo neto exacto con tus datos del Excel
                    texto_vencimiento_especifico = "✅ Operación en proceso de abonos"
                    saldo_a_pagar_final = val_factura - val_abonos - val_descuentos_ya_aplicados - val_nota
                else:
                    # CASO 2: NO SE HA INICIADO NINGÚN ABONO (VALOR = 0)
                    # Funciona tal cual como funcionaba originalmente (simulación predictiva por fecha de hoy)
                    if pd.notna(f_45) and fecha_hoy <= f_45:
                        descuento_proyectado_porcentaje = 0.02
                        dias = (f_45 - fecha_hoy).days
                        texto_vencimiento_especifico = f"En {dias} {'día' if dias == 1 else 'días'} el 2% de descuento"
                    elif pd.notna(f_69) and fecha_hoy <= f_69:
                        descuento_proyectado_porcentaje = 0.015
                        dias = (f_69 - fecha_hoy).days
                        texto_vencimiento_especifico = f"En {dias} {'día' if dias == 1 else 'días'} el 1.5% de descuento"
                    elif pd.notna(f_89) and fecha_hoy <= f_89:
                        descuento_proyectado_porcentaje = 0.01
                        dias = (f_89 - fecha_hoy).days
                        texto_vencimiento_especifico = f"En {dias} {'día' if dias == 1 else 'días'} el 1% de descuento"
                    elif pd.notna(f_120):
                        if fecha_hoy <= f_120:
                            descuento_proyectado_porcentaje = 0.0
                            dias = (f_120 - fecha_hoy).days
                            texto_vencimiento_especifico = f"En {dias} {'día' if dias == 1 else 'días'} sin intereses"
                        else:
                            descuento_proyectado_porcentaje = 0.0
                            dias_atraso = (fecha_hoy - f_120).days
                            texto_vencimiento_especifico = f"🚨 VENCIDO hace {dias_atraso} días (Pleno fue {f_120.strftime('%Y-%m-%d')})"
                    else:
                        descuento_proyectado_porcentaje = 0.0
                        texto_vencimiento_especifico = "Límite Pago Pleno No Definido"

                    # El descuento predictivo se calcula sobre el costo de equipos
                    valor_descuento_pronto_pago = costo_equipos * descuento_proyectado_porcentaje
                    saldo_a_pagar_final = val_factura - val_abonos - val_descuentos_ya_aplicados - val_nota - valor_descuento_pronto_pago

                # Validar que el saldo final no se vuelva negativo por centavos o diferencias
                if saldo_a_pagar_final < 0: 
                    saldo_a_pagar_final = 0.0

                # CAMBIO CRUCIAL: El pago está completado SOLO si el saldo a pagar real es 0 (tolerancia 5 USD)
                pago_completado = (val_factura > 0) and (saldo_a_pagar_final <= 5.0)
                # ----------------------------------------

                with st.container(border=True):
                    chead1, chead2 = st.columns([1, 1])
                    with chead1:
                        st.markdown('<div class="op-badge-marker"></div>', unsafe_allow_html=True)
                        if st.button(op_id, key=f"badge_{contexto}_{op_id}", help="Ver detalle de esta operación"):
                            st.session_state['ir_a_detalle_operacion'] = op_id
                            st.rerun()
                    with chead2:
                        if pago_completado:
                            st.markdown('<div style="text-align:right;"><span class="pago-badge pago-si">💳 PAGO REALIZADO</span></div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="text-align:right;"><span class="pago-badge pago-no" style="background-color: #F1F5F9; color: #475569; border: 1px solid #CBD5E1;">⏳ PAGO PENDIENTE</span></div>', unsafe_allow_html=True)
                    
                    st.markdown(f"<div style='font-size:14px; font-weight:600; color:#1E293B; margin-top:8px;'>Equipos en Operación: {int(row_op['CANTIDAD']):,} Unidades</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size:12.5px; color:#64748B;'>📦 {row_op['CONTENEDOR']} Contenedor(es) | 💰 Costo de equipos: USD {costo_equipos:,.2f}</div>", unsafe_allow_html=True)
                    
                    if pago_completado:
                        st.markdown(f"""
                        <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px; border-radius: 6px; margin-top: 8px; font-size: 13px; color: #14532D;">
                            <strong>Estatus Financiero:</strong> Facturado: USD {val_factura:,.2f} | <strong>Operación Totalmente Liquidada de Pagos ✅</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background-color: #FFF7ED; border-left: 4px solid #EA580C; padding: 10px; border-radius: 6px; margin-top: 8px; font-size: 13px; color: #7C2D12;">
                            <strong>Estatus Cuenta:</strong> Factura total: USD {val_factura:,.2f} | Abonos: USD {val_abonos:,.2f}<br>
                            <span style="font-size:14px;"><strong>Por Pagar (A la fecha): <span style="color: #C2410C; font-weight:700;">USD {saldo_a_pagar_final:,.2f}</span></strong></span><br>
                            ⏳ <strong>Vence:</strong> <span style="color: #9A3412; font-weight:600;">{texto_vencimiento_especifico}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if val_descuentos_ya_aplicados > 0 or val_nota > 0 or valor_descuento_pronto_pago > 0 or (obs_nota and obs_nota != 'nan' and obs_nota != ''):
                        html_notas_contenido = ""
                        if valor_descuento_pronto_pago > 0:
                            html_notas_contenido += f"🔹 <strong>Descuento Proyectado Próximo Pago:</strong> USD {valor_descuento_pronto_pago:,.2f}<br>"
                        if val_descuentos_ya_aplicados > 0:
                            html_notas_contenido += f"🔹 <strong>Descuento Comercial Aplicado:</strong> USD {val_descuentos_ya_aplicados:,.2f}<br>"
                        if val_nota > 0:
                            html_notas_contenido += f"🔹 <strong>Nota de Apoyo Proveedor:</strong> USD {val_nota:,.2f}<br>"
                        if obs_nota and obs_nota != 'nan' and obs_nota != '':
                            html_notas_contenido += f"📝 <strong>Observaciones Soporte:</strong> <em>{obs_nota}</em>"
                            
                        st.markdown(f"""
                        <div style="background-color: #F8FAFC; border: 1px dashed #CBD5E1; padding: 10px; margin-top: 6px; border-radius: 6px; font-size: 12px; color: #475569;">
                            {html_notas_contenido}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("")
                    cfoot1, cfoot2 = st.columns([1, 1])
                    with cfoot1:
                        st.markdown(f"<span style='font-size:12px; color:#475569;'>🏁 Arribo (ETA): <strong>{eta_str}</strong></span>", unsafe_allow_html=True)
                    with cfoot2:
                        if 'entregado' in estado_clean or 'llego' in estado_clean:
                            clase_badge = "status-entregado"
                        elif 'transito' in estado_clean:
                            clase_badge = "status-transito"
                        elif 'despachar' in estado_clean:
                            clase_badge = "status-despachar"
                        else:
                            clase_badge = "status-proceso"
                        st.markdown(f'<div style="text-align:right;"><span class="status-badge {clase_badge}">{estado_texto}</span></div>', unsafe_allow_html=True)

            # Clasificar y renderizar en los paneles (paginado de a 8, con "Ver más")
            TAMANO_PAGINA_OPS = 8

            with col_izquierda:
                st.markdown("#### 🚢 En Tránsito")
                ops_transito = ops_resumen[ops_resumen['ESTADO DE DISTRIBUCION'].str.lower().str.replace('á', 'a').str.contains('transito|despachar', na=False)]
                if not ops_transito.empty:
                    n_mostrar_transito = st.session_state.get('n_mostrar_transito', TAMANO_PAGINA_OPS)
                    for _, row in ops_transito.head(n_mostrar_transito).iterrows():
                        renderizar_tarjeta_operacion(row, "transito")
                    if len(ops_transito) > n_mostrar_transito:
                        if st.button("Ver más", key="ver_mas_transito", use_container_width=True):
                            st.session_state['n_mostrar_transito'] = n_mostrar_transito + TAMANO_PAGINA_OPS
                            st.rerun()
                else:
                    st.markdown('<div class="empty-state-text">No hay operaciones registradas en tránsito.</div>', unsafe_allow_html=True)

            with col_derecha:
                st.markdown("#### 🏢 Ya Llegó / Entregado")
                ops_entregadas = ops_resumen[~ops_resumen['ESTADO DE DISTRIBUCION'].str.lower().str.replace('á', 'a').str.contains('transito|despachar', na=False)]
                if not ops_entregadas.empty:
                    n_mostrar_entregadas = st.session_state.get('n_mostrar_entregadas', TAMANO_PAGINA_OPS)
                    for _, row in ops_entregadas.head(n_mostrar_entregadas).iterrows():
                        renderizar_tarjeta_operacion(row, "entregadas")
                    if len(ops_entregadas) > n_mostrar_entregadas:
                        if st.button("Ver más", key="ver_mas_entregadas", use_container_width=True):
                            st.session_state['n_mostrar_entregadas'] = n_mostrar_entregadas + TAMANO_PAGINA_OPS
                            st.rerun()
                else:
                    st.markdown('<div class="empty-state-text">No hay operaciones finalizadas registradas.</div>', unsafe_allow_html=True)

        # --- SECCIÓN: HISTORIAL ANALÍTICO ---
        st.write("---")
        st.subheader("📊 Historial analítico de variaciones y costos de referencia")
        
        df_maestro['REFERENCIA/MODELO'] = df_maestro['REFERENCIA/MODELO'].astype(str).str.strip().str.upper()
        
        productos_disponibles = sorted(list(set(p for p in df_maestro['REFERENCIA/MODELO'].dropna().unique() if p != 'NAN' and p != '')))
        
        producto_sel = st.selectbox("Seleccione la referencia o modelo a analizar:", productos_disponibles)
        
        df_hist = df_maestro[df_maestro['REFERENCIA/MODELO'] == producto_sel].copy()
        df_hist = df_hist.dropna(subset=['EMISIÓN FRA', 'VALOR UNITARIO (USD)']).sort_values('EMISIÓN FRA')
        
        if not df_hist.empty:
            df_hist['Etiqueta_Grafico'] = df_hist.apply(lambda r: f"{r['OPERACIÓN']} ({r['EMISIÓN FRA'].strftime('%Y-%m-%d')})", axis=1)
            
            def limpiar_pesos_colombia_enteros(valor):
                if pd.isna(valor) or str(valor).strip().lower() in ['none', 'nan', '', 'null']:
                    return None
                if isinstance(valor, (int, float)):
                    return float(valor)
                val_str = str(valor).replace('$', '').replace(' ', '').strip()
                if ',' in val_str and '.' in val_str:
                    if val_str.rfind('.') > val_str.rfind(','):
                        val_str = val_str.replace(',', '')
                    else:
                        val_str = val_str.replace('.', '').replace(',', '.')
                elif '.' in val_str and ',' not in val_str:
                    partes = val_str.split('.')
                    if len(partes[-1]) == 2 and partes[-1].isdigit():
                        val_str = "".join(partes[:-1]) + "." + partes[-1]
                    else:
                        val_str = val_str.replace('.', '')
                elif ',' in val_str and '.' not in val_str:
                    val_str = val_str.replace(',', '')
                return pd.to_numeric(val_str, errors='coerce')

            df_hist['COP_Grafico'] = df_hist[col_cop_name].apply(limpiar_pesos_colombia_enteros) if col_cop_name else None

            df_graficos = df_hist.groupby('Etiqueta_Grafico').agg({
                'VALOR UNITARIO (USD)': 'mean',
                'COP_Grafico': 'mean'
            }).reset_index()

            cg1, cg2 = st.columns(2)
            with cg1:
                fig_usd = px.line(df_graficos, x='Etiqueta_Grafico', y='VALOR UNITARIO (USD)', markers=True, 
                                  title="Evolución del costo unitario internacional (USD)", color_discrete_sequence=['#1E3A8A'])
                fig_usd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                      xaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Operación"), 
                                      yaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Valor USD"))
                st.plotly_chart(fig_usd, use_container_width=True)
                
            with cg2:
                df_barras_cop = df_graficos.dropna(subset=['COP_Grafico'])
                if not df_barras_cop.empty:
                    fig_cop = px.bar(df_barras_cop, x='Etiqueta_Grafico', y='COP_Grafico', 
                                     title="Variación del costo unitario nacionalizado final (COP)", color_discrete_sequence=['#059669'])
                    fig_cop.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                          xaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Operación"), 
                                          yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickformat="$,.0f", title="Valor COP ($)"))
                    st.plotly_chart(fig_cop, use_container_width=True)
                else:
                    fig_vacio = px.bar(title="Variación del costo unitario nacionalizado final (COP)")
                    fig_vacio.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_vacio, use_container_width=True)
            
            st.markdown("**Desglose detallado de precios por operación histórica:**")
            columnas_mostrar = ['OPERACIÓN', 'EMISIÓN FRA', 'FRA', 'VALOR UNITARIO (USD)']
            if col_cop_name: 
                columnas_mostrar.append('COP_Grafico')
            
            df_resumen_tabla = df_hist[columnas_mostrar].drop_duplicates().copy()
            df_resumen_tabla['EMISIÓN FRA'] = df_resumen_tabla['EMISIÓN FRA'].dt.strftime('%Y-%m-%d')
            df_resumen_tabla['VALOR UNITARIO (USD)'] = df_resumen_tabla['VALOR UNITARIO (USD)'].apply(lambda x: f"USD ${x:,.2f}" if pd.notna(x) else "N/A")
            
            if col_cop_name:
                df_resumen_tabla['COP_Grafico'] = df_resumen_tabla['COP_Grafico'].apply(
                    lambda x: f"${int(x):,}".replace(",", ".") if pd.notna(x) else "Por Nacionalizar"
                )
                df_resumen_tabla = df_resumen_tabla.rename(columns={'COP_Grafico': 'VALOR NACIONALIZADO COP'})
            
            st.dataframe(
                df_resumen_tabla.rename(columns={'EMISIÓN FRA':'Fecha Emisión FRA', 'FRA':'Factura'}),
                use_container_width=True,
                hide_index=True
            )

# =========================================================================
    # --- MÓDULO 2: DETALLE DE OPERACIÓN (FILTRO POR ESTADO DE DISTRIBUCION) --
    # =========================================================================
    elif menu == "🔍 Detalle de Operación":
        st.title("Desglose analítico por operación")
        
        # --- FUNCIÓN DE TRM EN TIEMPO REAL BLINDADA ---
        def obtener_trm_actual_tiempo_real():
            import datetime
            fecha_base = datetime.datetime.now()
            fecha_consulta = fecha_base
            
            for intento in range(4):
                fecha_str_gob = fecha_consulta.strftime("%Y-%m-%dT00:00:00.000")
                url_gob = f"https://datos.gov.co/resource/ceb7-324e.json?vigenciadesde={fecha_str_gob}"
                try:
                    respuesta = requests.get(url_gob, timeout=4)
                    if respuesta.status_code == 200:
                        datos_json = respuesta.json()
                        if len(datos_json) > 0 and 'valor' in datos_json[0]:
                            return float(datos_json[0]['valor']), fecha_consulta
                except:
                    pass
                fecha_consulta = fecha_consulta - pd.Timedelta(days=1)
                
            try:
                url_respaldo = "https://open.er-api.com/v6/latest/USD"
                respuesta_res = requests.get(url_respaldo, timeout=4)
                if respuesta_res.status_code == 200:
                    datos_res = respuesta_res.json()
                    if 'rates' in datos_res and 'COP' in datos_res['rates']:
                        return float(datos_res['rates']['COP']), fecha_base
            except:
                pass
            
            return 3950.0, fecha_base

        if df_maestro is None or df_maestro.empty:
            st.error("⚠️ La base de datos maestro no se ha cargado correctamente.")
        else:
            lista_ops = sorted(df_maestro['OPERACIÓN'].dropna().unique())
            if 'select_operacion_detalle' in st.session_state and st.session_state['select_operacion_detalle'] not in lista_ops:
                del st.session_state['select_operacion_detalle']
            op_sel = st.selectbox("Seleccione el Código Operativo (M):", lista_ops, key="select_operacion_detalle")
            st.write("---")
            
            df_op = df_maestro[df_maestro['OPERACIÓN'] == op_sel].copy()
            if not df_op.empty:
                
                # -----------------------------------------------------------------
                # 🛠️ DETECTOR EXACTO DE TRÁNSITO POR ESTADO DE DISTRIBUCION
                # -----------------------------------------------------------------
                col_estado_actual = 'ESTADO DE DISTRIBUCION'
                estado_texto = ""
                
                if col_estado_actual in df_op.columns:
                    estado_texto = str(df_op[col_estado_actual].iloc[0]).strip().lower()
                
                # Evaluamos si contiene la raíz de la palabra en minúsculas sin importar tildes
                es_en_transito = ("transit" in estado_texto) or ("trán" in estado_texto) or ("tran" in estado_texto)
                # -----------------------------------------------------------------

                # Cabezote informativo de la operación
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"**📄 Número de BL:** `{df_op['BL'].iloc[0] if 'BL' in df_op.columns else 'N/A'}`")
                    st.markdown(f"**🚢 Línea Marítima (Naviera):** {df_op['NAVIERA'].iloc[0] if 'NAVIERA' in df_op.columns else 'N/A'}")
                with c2:
                    st.markdown(f"**🧾 Factura Comercial (FRA):** `{df_op['FRA'].iloc[0] if 'FRA' in df_op.columns else 'N/A'}`")
                    st.markdown(f"**📅 Fecha Arribo (ETA):** {df_op['ETA'].iloc[0].strftime('%Y-%m-%d') if 'ETA' in df_op.columns and pd.notna(df_op['ETA'].iloc[0]) else 'Pendiente'}")
                with c3:
                    num_conts = df_op['CONTENEDOR'].nunique() if 'CONTENEDOR' in df_op.columns else 1
                    flete_tot = df_op['VALOR FLETE FRA'].iloc[0] if 'VALOR FLETE FRA' in df_op.columns and pd.notna(df_op['VALOR FLETE FRA'].iloc[0]) else 0
                    st.markdown(f"**💰 Costo Equipos Operación:** USD {df_op['VALOR TOTAL EQUIPOS (USD)'].sum():,.2f}")
                    st.markdown(f"**💵 Flete Prorrateado:** USD {flete_tot / max(num_conts, 1):,.2f} por Contenedor")

                # =========================================================================
                # APARTADO DE PROYECCIÓN: SÓLO SI ESTÁ EN TRÁNSITO
                # =========================================================================
                if es_en_transito:
                    st.write("---")
                    st.markdown("### 📋 Proyección Comercial Avanzada de Importación (Operación en Tránsito)")
                    
                    df_op['VALOR UNITARIO (USD)'] = pd.to_numeric(df_op['VALOR UNITARIO (USD)'], errors='coerce').fillna(0)
                    referencias_op = sorted(df_op['REFERENCIA/MODELO'].dropna().unique())
                    ref_seleccionada = st.selectbox("Seleccione una referencia de esta operación para evaluar:", referencias_op)
                    
                    df_ref_actual = df_op[df_op['REFERENCIA/MODELO'] == ref_seleccionada].iloc[0]
                    costo_base_usd = float(df_ref_actual['VALOR UNITARIO (USD)'])
                    
                    arancel_real = 0.0
                    factor_promedio = 1.150
                    log_analitica = ""

                    # --- PROMEDIO EXCLUSIVO DE COLUMNAS QUE SON FECHAS ---
                    if 'df_proyeccion' in locals() or 'df_proyeccion' in globals():
                        if df_proyeccion is not None and not df_proyeccion.empty:
                            df_p = df_proyeccion.copy()
                            col_ref_proy = next((c for c in df_p.columns if 'MODELO' in str(c).upper() or 'REFERENCIA' in str(c).upper()), df_p.columns[0])
                            df_p[col_ref_proy] = df_p[col_ref_proy].fillna('').astype(str).str.strip().str.upper()
                            
                            fila_ref = df_p[df_p[col_ref_proy] == str(ref_seleccionada).strip().upper()]
                            if not fila_ref.empty:
                                col_aran = next((c for c in df_p.columns if 'ARANCEL' in str(c).upper()), None)
                                if col_aran and pd.notna(fila_ref[col_aran].iloc[0]):
                                    try:
                                        val_ar = float(str(fila_ref[col_aran].iloc[0]).replace('%', '').strip())
                                        arancel_real = val_ar / 100.0 if val_ar >= 1.0 else val_ar
                                    except: pass

                                valores_factores_limpios = []
                                for col_name in df_p.columns:
                                    es_columna_fecha = False
                                    try:
                                        if isinstance(col_name, (datetime, pd.Timestamp)):
                                            es_columna_fecha = True
                                        else:
                                            pd.to_datetime(str(col_name).strip(), format='%Y-%m-%d', errors='raise')
                                            es_columna_fecha = True
                                    except:
                                        try:
                                            pd.to_datetime(str(col_name).strip(), errors='raise')
                                            if len(str(col_name).strip()) >= 7:
                                                es_columna_fecha = True
                                        except: pass

                                    if es_columna_fecha:
                                        val_celda = fila_ref[col_name].iloc[0]
                                        val_numerico = pd.to_numeric(val_celda, errors='coerce')
                                        if pd.notna(val_numerico) and (1.0 <= float(val_numerico) <= 2.5):
                                            valores_factores_limpios.append(float(val_numerico))

                                if valores_factores_limpios:
                                    factor_promedio = sum(valores_factores_limpios) / len(valores_factores_limpios)
                                    log_analitica += f"✔️ **Análisis de Factores:** Se promediaron con éxito **{len(valores_factores_limpios)} factores históricos**.\n"

                    with st.spinner("Consultando TRM oficial en tiempo real..."):
                        trm_automatica, _ = obtener_trm_actual_tiempo_real()
                    log_analitica += f"🌐 **TRM del Día de la Búsqueda:** Tasa oficial de mercado: **${trm_automatica:,.2f} COP**.\n"
                    st.info(log_analitica)

                    # --- PARÁMETROS EDITABLES DEL SIMULADOR ---
                    st.markdown("#### ⚙️ Ajuste de Parámetros del Simulador")
                    c_fac1, c_fac2, c_fac3, c_fac4 = st.columns(4)
                    with c_fac1:
                        trm_input = st.number_input("💵 TRM Dinámica Aplicada ($ COP):", min_value=3000.0, max_value=6000.0, value=trm_automatica, step=10.0)
                    with c_fac2:
                        arancel_input = st.number_input("🧾 Arancel Base Aplicado (%):", min_value=0.0, max_value=100.0, value=arancel_real * 100.0, step=1.0) / 100.0
                    with c_fac3:
                        factor_input = st.number_input("✈️ Factor de Importación (Promedio Real):", min_value=1.0, max_value=3.0, value=factor_promedio, step=0.001, format="%.3f")
                    with c_fac4:
                        margen_input = st.number_input("📊 Margen Comercial Deseado (%):", min_value=0.0, max_value=95.0, value=30.0, step=1.0) / 100.0

                    # --- CÁLCULOS MATEMÁTICOS ---
                    costo_fob_cop = costo_base_usd * trm_input
                    costo_nacionalizado_cop = costo_fob_cop * factor_input * (1 + arancel_input)
                    precio_venta_final = costo_nacionalizado_cop / (1 - margen_input) if margen_input < 1.0 else costo_nacionalizado_cop

                    # --- KPI'S ESTILO EJECUTIVO ---
                    st.write("")
                    col_r1, col_r2, col_r3 = st.columns(3)
                    with col_r1:
                        st.markdown(f"""
                        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; text-align: center;">
                            <div style="color: #64748B; font-size: 11px; font-weight: 600; text-transform: uppercase;">Costo FOB Unitario</div>
                            <div style="color: #1E293B; font-size: 20px; font-weight: 700; margin-top: 5px;">USD ${costo_base_usd:,.2f}</div>
                            <div style="color: #475569; font-size: 12px; margin-top: 2px;">≈ {costo_fob_cop:,.0f} COP</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_r2:
                        st.markdown(f"""
                        <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 15px; border-radius: 8px; text-align: center;">
                            <div style="color: #16A34A; font-size: 11px; font-weight: 600; text-transform: uppercase;">Costo de equipos (Nacionalizado)</div>
                            <div style="color: #14532D; font-size: 20px; font-weight: 700; margin-top: 5px;">${costo_nacionalizado_cop:,.0f} COP</div>
                            <div style="color: #15803D; font-size: 11px; margin-top: 2px;">Factor Ø: {factor_input:.3f} | Arancel: {arancel_input*100:.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_r3:
                        st.markdown(f"""
                        <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 15px; border-radius: 8px; text-align: center; border-left: 5px solid #2563EB;">
                            <div style="color: #2563EB; font-size: 11px; font-weight: 600; text-transform: uppercase;">🚀 Precio Mínimo de Venta Sugerido</div>
                            <div style="color: #1E3A8A; font-size: 22px; font-weight: 800; margin-top: 5px;">${precio_venta_final:,.0f} COP</div>
                            <div style="color: #3B82F6; font-size: 11px; margin-top: 2px;">Margen Comercial Reservado: {margen_input*100:.0f}%</div>
                        </div>
                        """, unsafe_allow_html=True)

                # --- CONTROL DE VENCIMIENTOS (ORIGINAL) ---
                st.write("---")
                st.subheader("⏳ Control de vencimientos financieros")
                
                pago_operacion = str(df_op[col_estado_pago].iloc[0]).strip().upper() if col_estado_pago and not df_op[col_estado_pago].isna().all() else ""
                
                if "PAGADO" in pago_operacion:
                    st.markdown('<div class="pago-exitoso-box">🎉 YA ESTÁ PAGO</div>', unsafe_allow_html=True)
                else:
                    def renderizar_linea_vencimiento_semaforo(fecha_limite, tramo_label):
                        if pd.isna(fecha_limite):
                            return f'<div class="semaforo-box-p sem-gris"><span>{tramo_label}</span><strong>Fecha no parametrizada</strong></div>'
                        dias_restantes = (fecha_limite - fecha_hoy).days
                        if dias_restantes < 0:
                            clase_sem = "sem-rojo"
                            mensaje = f"Plazo vencido hace {abs(dias_restantes)} días"
                        elif dias_restantes <= 15:
                            clase_sem = "sem-amarillo"
                            mensaje = f"Alerta de vencimiento cercano — Quedan {dias_restantes} días"
                        else:
                            clase_sem = "sem-verde"
                            mensaje = f"Plazo vigente y seguro — Quedan {dias_restantes} días"
                        return f'<div class="semaforo-box-p {clase_sem}"><strong>Vencimiento de pago — {tramo_label}</strong><span>{mensaje} ({fecha_limite.strftime("%Y-%m-%d")})</span></div>'

                    if 'VENCIMIENTO 45 D - 2%' in df_op.columns:
                        st.markdown(renderizar_linea_vencimiento_semaforo(df_op['VENCIMIENTO 45 D - 2%'].iloc[0], "Tramo 45 días (Descuento 2%)"), unsafe_allow_html=True)
                    if 'VENCIMIENTO 69D 1.5%' in df_op.columns:
                        st.markdown(renderizar_linea_vencimiento_semaforo(df_op['VENCIMIENTO 69D 1.5%'].iloc[0], "Tramo 69 días (Descuento 1.5%)"), unsafe_allow_html=True)
                    if 'VENCIMIENTO 89D - 1%' in df_op.columns:
                        st.markdown(renderizar_linea_vencimiento_semaforo(df_op['VENCIMIENTO 89D - 1%'].iloc[0], "Tramo 89 días (Descuento 1%)"), unsafe_allow_html=True)
                    if 'VENCIMIENTO 120D - PLENO' in df_op.columns:
                        st.markdown(renderizar_linea_vencimiento_semaforo(df_op['VENCIMIENTO 120D - PLENO'].iloc[0], "Límite 120 días (Pago plato)"), unsafe_allow_html=True)

                # =========================================================================
                # RENDERIZACIÓN DE TARJETAS DE CONTENEDORES (TU LÓGICA ORIGINAL EXCEL)
                # =========================================================================
                st.write("")
                st.subheader("🚚 Referencias por contenedor")
                if 'CONTENEDOR' in df_op.columns:
                    contenedores_sistema = df_op['CONTENEDOR'].dropna().unique()
                    if len(contenedores_sistema) > 0:
                        grid_visual = st.columns(min(len(contenedores_sistema), 2))
                        for idx, cont_id in enumerate(contenedores_sistema):
                            df_items_contenedor = df_op[df_op['CONTENEDOR'] == cont_id]
                            col_actual = grid_visual[idx % len(grid_visual)]
                            with col_actual:
                                html_total_contenedor = f'<div class="container-box-p"><div class="container-header-p"><span>Contenedor: {cont_id}</span><span>Tipo: 40HQ Estándar</span></div><div class="container-body-p">'
                                for _, p_row in df_items_contenedor.iterrows():
                                    val_usd = p_row['VALOR TOTAL EQUIPOS (USD)'] if 'VALOR TOTAL EQUIPOS (USD)' in p_row else 0
                                    cant = p_row['CANTIDAD'] if 'CANTIDAD' in p_row else 0
                                    ref = p_row['REFERENCIA/MODELO'] if 'REFERENCIA/MODELO' in p_row else 'Sin Ref'
                                    
                                    if col_cop_name and pd.notna(p_row[col_cop_name]) and str(p_row[col_cop_name]).strip().lower() != 'none':
                                        try:
                                            val_cop_num = float(p_row[col_cop_name])
                                            texto_costo_variable = f" | Costo Nac. x U: ${val_cop_num:,.0f} COP"
                                        except:
                                            texto_costo_variable = f" | Costo Nac. x U: {p_row[col_cop_name]} COP"
                                    elif 'VALOR UNITARIO (USD)' in p_row:
                                        texto_costo_variable = f" | Valor: ${p_row['VALOR UNITARIO (USD)']:,.2f} USD"
                                    else:
                                        texto_costo_variable = ""

                                    html_total_contenedor += f'<div class="product-row-p"><span class="product-title-p">{int(cant)} unidades <span class="product-subtitle-p">— {ref}</span></span><span class="product-meta-p">💰 Bloque: ${val_usd:,.2f} USD {texto_costo_variable}</span></div>'
                                html_total_contenedor += '</div></div>'
                                st.markdown(html_total_contenedor, unsafe_allow_html=True)
                            
    # --- MÓDULO 3: REFERENCIAS EN PRODUCCIÓN ---
    elif menu == "🚨 Referencias en Producción":
        st.title("Referencias en producción")
        st.markdown("<p style='color: #64748B; font-size:14px;'>Monitoreo predictivo de órdenes agrupadas por modelo pendientes por asignación de BL y fecha de zarpe.</p>", unsafe_allow_html=True)
        st.write("---")
        
        df_plan_copy = df_plan.copy()
        if 'BL' in df_plan_copy.columns:
            df_plan_copy['BL_aux'] = df_plan_copy['BL'].astype(str).str.strip().str.upper()
            mascara_sin_bl = (df_plan_copy['BL'].isna()) | (df_plan_copy['BL_aux'] == 'NAN') | (df_plan_copy['BL_aux'] == '') | (df_plan_copy['BL_aux'] == 'POR ASIGNAR')

            # Un BL asignado solo deja de estar en producción cuando ya fue
            # registrado en la tabla maestra (operación en tránsito).
            bl_maestro = set()
            if df_maestro is not None and 'BL' in df_maestro.columns:
                bl_maestro = set(
                    df_maestro['BL'].dropna().astype(str).str.strip().str.upper()
                )
                bl_maestro -= {'', 'NAN', 'POR ASIGNAR'}

            mascara_bl_pendiente = ~df_plan_copy['BL_aux'].isin(bl_maestro)
            df_pendientes_despacho = df_plan_copy[mascara_sin_bl | mascara_bl_pendiente].copy()
        else:
            df_pendientes_despacho = df_plan_copy

        # --- EXCLUSIÓN DE CANTIDADES MARCADAS EN AZUL Y MENORES A 10 UNIDADES (NO SE VAN A ENVIAR / SE CANCELAN) ---
        # Si está en azul pero supera las 10 unidades, sí se envía y se mantiene en el listado.
        if 'QTY_NO_SE_ENVIA' in df_pendientes_despacho.columns:
            qty_numerico = pd.to_numeric(df_pendientes_despacho['QTY'], errors='coerce').fillna(0)
            mascara_cancelado = df_pendientes_despacho['QTY_NO_SE_ENVIA'] & (qty_numerico < 10)
            unidades_canceladas = qty_numerico[mascara_cancelado].sum()
            df_pendientes_despacho = df_pendientes_despacho[~mascara_cancelado].copy()
            if unidades_canceladas > 0:
                st.caption(f"ℹ️ Se excluyeron {int(unidades_canceladas)} unidades resaltadas en azul y con menos de 10 unidades (no se enviarán ).")

        if not df_pendientes_despacho.empty:
            df_pendientes_despacho['Modelo'] = df_pendientes_despacho['Modelo'].fillna('Modelo desconocido').astype(str)
            df_pendientes_despacho['Description'] = df_pendientes_despacho['Description'].fillna('Sin descripción técnica.').astype(str)
            df_pendientes_despacho['No PI'] = df_pendientes_despacho['No PI'].fillna('Pendiente').astype(str)
            df_pendientes_despacho['QTY'] = pd.to_numeric(df_pendientes_despacho['QTY'], errors='coerce').fillna(0).astype(int)
            
            def formatear_fecha(x):
                if pd.isna(x): return 'No parametrizado'
                if isinstance(x, datetime): return x.strftime('%Y-%m-%d')
                return str(x).split(" ")[0]
                
            if 'Forecast ETD' in df_pendientes_despacho.columns:
                df_pendientes_despacho['Fecha_Format'] = df_pendientes_despacho['Forecast ETD'].apply(formatear_fecha)
            else:
                df_pendientes_despacho['Fecha_Format'] = 'No parametrizado'

            df_agrupado = df_pendientes_despacho.groupby('Modelo').agg({
                'QTY': 'sum',
                'Description': lambda x: sorted(list(set(x.dropna()))),
                'No PI': lambda x: ", ".join(sorted(set(x.astype(str)))),
                'Fecha_Format': lambda x: x.iloc[0]
            }).reset_index()

            st.markdown("### Modelos en fabricación")
            
            columnas_grid = st.columns(3)
            for idx, fila in df_agrupado.iterrows():
                modelo_label = fila['Modelo']
                qty_label = fila['QTY']
                lista_descripciones = fila['Description']
                pi_label = fila['No PI']
                etd_label = fila['Fecha_Format']

                html_items_descripcion = '<ul class="dispatch-items-list">'
                for desc in lista_descripciones:
                    if desc.strip():
                        html_items_descripcion += f'<li class="dispatch-item-line">{desc}</li>'
                html_items_descripcion += '</ul>'

                col_actual = columnas_grid[idx % 3]
                with col_actual:
                    html_tarjeta = f"""
                    <div class="dispatch-card-premium">
                      <div>
                          <div class="dispatch-tag">Fábrica - Pendiente BL</div>
                          <div class="dispatch-model">{modelo_label}</div>
                          {html_items_descripcion}
                      </div>
                      <div>
                          <div class="dispatch-meta-row">
                              <span>Cant: <strong>{qty_label} u</strong></span>
                              <span>PI: <strong>{pi_label}</strong></span>
                          </div>
                          <div class="dispatch-date">
                              📅 Est. Despacho (ETD): {etd_label}
                          </div>
                      </div>
                    </div>
                    """
                    st.markdown(html_tarjeta, unsafe_allow_html=True)
        else:
            st.info("No se registran referencias pendientes por despachar en el plan actual.")


