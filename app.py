import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import io
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
    
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
    .kpi-val-p { font-size: 30px; font-weight: 700; color: #1E293B; line-height: 1; }
    .kpi-lbl-p { font-size: 11px; color: #64748B; text-transform: uppercase; margin-top: 8px; letter-spacing: 0.05em; font-weight: 600; }
    
    /* 📋 FILAS DE TRAZABILIDAD */
    .timeline-container-p {
        background-color: #FFFFFF; 
        border: 1px solid #E2E8F0; 
        border-radius: 12px;
        padding: 16px 22px; 
        margin-bottom: 12px; 
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .timeline-container-p:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.04);
        border-color: #CBD5E1;
    }
    .timeline-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .op-badge-p { 
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); 
        color: white; 
        padding: 12px 0px; 
        font-weight: 700; 
        border-radius: 10px; 
        font-size: 14px; 
        width: 54px;
        text-align: center;
        flex-shrink: 0;
    }
    .timeline-info {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .timeline-main-text {
        font-size: 14px;
        color: #1E293B;
        font-weight: 600;
    }
    .timeline-sub-text {
        font-size: 13px;
        color: #64748B;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    .timeline-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 8px;
        font-size: 13px;
    }
    .timeline-eta {
        color: #64748B;
        font-weight: 500;
    }
    
    /* BADGES DE ESTADO */
    .status-badge {
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }
    .status-entregado { background-color: #DCFCE7; color: #15803D; }
    .status-transito { background-color: #FEF3C7; color: #B45309; }
    .status-despachar { background-color: #FFEDD5; color: #C2410C; }
    .status-proceso { background-color: #F1F5F9; color: #475569; }
    
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
    .dispatch-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 16px;
        margin-top: 15px;
    }
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

# =========================================================================
# 3. CONEXIÓN CORPORATIVA (ONEDRIVE)
# =========================================================================
def ejecutar_sincronizacion_onedrive():
    resultado = {"df_plan": None, "df_maestro": None, "error": None}
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
        
        url_m = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/drive/items/{file_maestro_id}/content"
        res_m = requests.get(url_m, headers=headers, timeout=15)
        
        url_p = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/drive/items/{file_plan_id}/content"
        res_p = requests.get(url_p, headers=headers, timeout=15)
        
        df_m = pd.read_excel(io.BytesIO(res_m.content), sheet_name="BASE_DATOS_MAESTRO")
        df_p = pd.read_excel(io.BytesIO(res_p.content), sheet_name="Hoja1")
            
        df_p.columns = df_p.columns.str.strip()
        df_m.columns = df_m.columns.str.strip()
        
        columnas_fecha = ['EMISIÓN FRA', 'ETA', 'VENCIMIENTO 45 D - 2%', 'VENCIMIENTO 69D 1.5%', 'VENCIMIENTO 89D - 1%', 'VENCIMIENTO 120D - PLENO']
        for col in columnas_fecha:
            if col in df_m.columns:
                df_m[col] = pd.to_datetime(df_m[col], errors='coerce')
                
        resultado["df_plan"] = df_p
        resultado["df_maestro"] = df_m
        
    except Exception as e_global:
        resultado["error"] = f"Excepción del sistema de enlace: {e_global}"
    return resultado

@st.cache_data(ttl=300)
def cargar_datos_seguros():
    return ejecutar_sincronizacion_onedrive()

data_response = cargar_datos_seguros()
df_plan = data_response["df_plan"]
df_maestro = data_response["df_maestro"]
error_detectado = data_response["error"]

# =========================================================================
# 4. MENÚ LATERAL
# =========================================================================
with st.sidebar:
    st.write("")
    if logo:
        st.image(logo, use_column_width=True)
    else:
        st.markdown("<h2 style='margin-bottom:0px; font-size:22px;'>PROYECTOS Y SERVICIOS</h2>", unsafe_allow_html=True)
        
    st.markdown("<p style='color:#94A3B8; font-size:13px; margin-top:2px; margin-bottom:25px;'>Control e Inteligencia Logística</p>", unsafe_allow_html=True)
    st.markdown("<label style='color:#94A3B8; font-size:11px; font-weight:600; letter-spacing:0.05em;'>MÓDULOS DEL SISTEMA</label>", unsafe_allow_html=True)
    
    menu = st.radio(
        "Módulos Estratégicos:",
        ["📈 Trazabilidad e Historial", "🔍 Detalle de Operación", "🚨 Referencias en Producción"],
        label_visibility="collapsed"
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
        Área de planeación y Distribución<br>
        <span style='font-size:10px; color:#475569;'>Enterprise System v4.0</span>
        </div> """, unsafe_allow_html=True)

# =========================================================================
# 5. PANTALLA PRINCIPAL
# =========================================================================
if error_detectado is not None:
    st.error(error_detectado)

elif df_plan is not None and df_maestro is not None:
    fecha_hoy = datetime.now()

    # --- ENCONTRAR COLUMNA COP ---
    col_cop_name = next((n for n in ['VALOR_NACIONALIZADO', 'VALOR NACIONALIZADO COP', 'VALOR_NACIONALIZADO_COP', 'VALOR NACIONALIZADO'] if n in df_maestro.columns), None)

    # --- MÓDULO 1: TRAZABILIDAD E HISTORIAL ---
    if menu == "📈 Trazabilidad e Historial":
        st.title("Control general de operaciones")
        st.markdown("<p style='color: #64748B; font-size:14px;'>Consolidado estratégico de importaciones distribuido por estatus operativo y financiero.</p>", unsafe_allow_html=True)
        st.write("---")
        
        ckpi1, ckpi2, ckpi3 = st.columns(3)
        total_usd = df_maestro['VALOR TOTAL (USD)'].sum() if 'VALOR TOTAL (USD)' in df_maestro.columns else 0
        total_conts = df_maestro['CONTENEDOR'].nunique() if 'CONTENEDOR' in df_maestro.columns else 0
        total_unis = df_maestro['CANTIDAD'].sum() if 'CANTIDAD' in df_maestro.columns else 0
        
        with ckpi1: st.markdown(f'<div class="kpi-card-premium kpi-blue"><div class="kpi-val-p">USD {total_usd:,.2f}</div><div class="kpi-lbl-p">Inversión Total Equipos</div></div>', unsafe_allow_html=True)
        with ckpi2: st.markdown(f'<div class="kpi-card-premium kpi-indigo"><div class="kpi-val-p">{total_conts}</div><div class="kpi-lbl-p">Contenedores Gestión</div></div>', unsafe_allow_html=True)
        with ckpi3: st.markdown(f'<div class="kpi-card-premium kpi-emerald"><div class="kpi-val-p">{int(total_unis):,}</div><div class="kpi-lbl-p">Unidades Globales Importadas</div></div>', unsafe_allow_html=True)
            
        st.subheader("📋 Distribución de flujos logísticos y financieros")
        
        if 'OPERACIÓN' in df_maestro.columns:
            # Asegurar existencia de las columnas de estado de forma limpia
            if 'ESTADO_PAGO' not in df_maestro.columns:
                df_maestro['ESTADO_PAGO'] = None
                
            if 'ESTADO DE DISTRIBUCION' in df_maestro.columns:
                df_maestro['ESTADO DE DISTRIBUCION'] = df_maestro['ESTADO DE DISTRIBUCION'].astype(str).str.strip()
            else:
                df_maestro['ESTADO DE DISTRIBUCION'] = "En tránsito"
                
            # Agrupación directa y exacta por Operación
            ops_resumen = df_maestro.groupby('OPERACIÓN').agg({
                'CONTENEDOR': 'nunique', 
                'CANTIDAD': 'sum', 
                'VALOR TOTAL (USD)': 'sum',
                'ESTADO DE DISTRIBUCION': lambda x: x.dropna().iloc[0] if not x.dropna().empty else "En tránsito",
                'ESTADO_PAGO': lambda x: str(x.dropna().iloc[0]).strip() if not x.dropna().empty else "",
                'ETA': lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NaT
            }).reset_index()
            
            # --- SEPARACIÓN EN DOS COLUMNAS REFORZADA ---
            col_izq, col_der = st.columns(2)
            
            with col_izq:
                st.markdown("#### 🚢 En Tránsito")
                # Filtro exacto ignorando diferencias de mayúsculas
                df_transito = ops_resumen[ops_resumen['ESTADO DE DISTRIBUCION'].str.lower() == 'en tránsito']
                
                if df_transito.empty:
                    st.info("No hay operaciones registradas en tránsito.")
                else:
                    for _, row in df_transito.iterrows():
                        eta_str = row['ETA'].strftime('%Y-%m-%d') if pd.notna(row['ETA']) else "Por Confirmar"
                        
                        # Validación e indicador de pago
                        es_pago = str(row['ESTADO_PAGO']).strip() != "" and str(row['ESTADO_PAGO']).lower() != "nan"
                        badge_pago_html = (
                            '<span style="background-color: #DCFCE7; color: #15803D; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:600; margin-left:8px;">✅ YA ESTÁ PAGO</span>'
                            if es_pago else 
                            '<span style="background-color: #FEE2E2; color: #991B1B; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:600; margin-left:8px;">🚨 PENDIENTE PAGO</span>'
                        )
                        
                        html_linea = f"""
                        <div class="timeline-container-p" style="border-left: 5px solid #F59E0B;">
                            <div class="timeline-left">
                                <div class="op-badge-p">{row['OPERACIÓN']}</div>
                                <div class="timeline-info">
                                    <div class="timeline-main-text">Monto: USD {row['VALOR TOTAL (USD)']:,.2f} {badge_pago_html}</div>
                                    <div class="timeline-sub-text">
                                        <span>📦 {row['CONTENEDOR']} Contenedor(es)</span> | <span>🔢 {int(row['CANTIDAD']):,} Equipos</span>
                                    </div>
                                </div>
                            </div>
                            <div class="timeline-right">
                                <div class="timeline-eta">📅 ETA: {eta_str}</div>
                                <div class="status-badge status-transito">{row['ESTADO DE DISTRIBUCION']}</div>
                            </div>
                        </div>
                        """
                        st.markdown(html_linea, unsafe_allow_html=True)
            
            with col_der:
                st.markdown("#### 🏢 Ya Llegó / Entregado")
                # Filtro exacto para la columna derecha
                df_entrega = ops_resumen[ops_resumen['ESTADO DE DISTRIBUCION'].str.lower() == 'entregado']
                
                if df_entrega.empty:
                    st.info("No hay operaciones registradas como entregadas.")
                else:
                    for _, row in df_entrega.iterrows():
                        eta_str = row['ETA'].strftime('%Y-%m-%d') if pd.notna(row['ETA']) else "Finalizado"
                        
                        html_linea = f"""
                        <div class="timeline-container-p" style="border-left: 5px solid #10B981;">
                            <div class="timeline-left">
                                <div class="op-badge-p" style="background: linear-gradient(135deg, #059669 0%, #064E3B 100%);">{row['OPERACIÓN']}</div>
                                <div class="timeline-info">
                                    <div class="timeline-main-text">Monto: USD {row['VALOR TOTAL (USD)']:,.2f}</div>
                                    <div class="timeline-sub-text">
                                        <span>📦 {row['CONTENEDOR']} Contenedor(es)</span> | <span>🔢 {int(row['CANTIDAD']):,} Equipos</span>
                                    </div>
                                </div>
                            </div>
                            <div class="timeline-right">
                                <div class="timeline-eta">🏁 Arribo: {eta_str}</div>
                                <div class="status-badge status-entregado">{row['ESTADO DE DISTRIBUCION']}</div>
                            </div>
                        </div>
                        """
                        st.markdown(html_linea, unsafe_allow_html=True)

        st.write("---")
        
        # HISTORIAL ANALÍTICO DE VARIACIÓN DE COSTOS
        st.subheader("📊 Historial analítico de variaciones y costos de referencia")
        st.markdown("<p style='color: #475569; font-size:13.5px; margin-top:-10px;'>Monitoreo de volatilidad de precios internacionales (USD) y comportamiento del costo nacionalizado (COP) indexado por operation.</p>", unsafe_allow_html=True)
        
        productos_disponibles = sorted(df_maestro['REFERENCIA/MODELO'].dropna().unique())
        producto_sel = st.selectbox("Seleccione la referencia o modelo a analizar:", productos_disponibles)
        
        df_hist = df_maestro[df_maestro['REFERENCIA/MODELO'] == producto_sel].copy()
        df_hist = df_hist.dropna(subset=['EMISIÓN FRA', 'VALOR UNITARIO (USD)']).sort_values('EMISIÓN FRA')
        
        if not df_hist.empty:
            df_hist['Etiqueta_Grafico'] = df_hist.apply(lambda r: f"{r['OPERACIÓN']} ({r['EMISIÓN FRA'].strftime('%Y-%m-%d')})", axis=1)
            
            def limpiar_pesos_colombia_enteros(valor):
                if pd.isna(valor) or str(valor).strip().lower() in ['none', 'nan', '']:
                    return None
                val_str = str(valor).replace('$', '').replace(' ', '').replace(',', '').strip()
                if '.' in val_str:
                    partes = val_str.split('.')
                    if len(partes[-1]) == 2 and partes[-1].isdigit():
                        val_str = "".join(partes[:-1])
                    else:
                        val_str = val_str.replace('.', '')
                return pd.to_numeric(val_str, errors='coerce')

            if col_cop_name:
                df_hist['COP_Grafico'] = df_hist[col_cop_name].apply(limpiar_pesos_colombia_enteros)
            else:
                df_hist['COP_Grafico'] = None

            cg1, cg2 = st.columns(2)
            with cg1:
                fig_usd = px.line(df_hist, x='Etiqueta_Grafico', y='VALOR UNITARIO (USD)', markers=True, 
                                  title="Evolución del costo unitario internacional (USD)", color_discrete_sequence=['#1E3A8A'])
                fig_usd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                      xaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Operación"), yaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Valor USD"))
                st.plotly_chart(fig_usd, use_container_width=True)
                
            with cg2:
                df_barras_cop = df_hist.dropna(subset=['COP_Grafico'])
                if not df_barras_cop.empty:
                    fig_cop = px.bar(df_barras_cop, x='Etiqueta_Grafico', y='COP_Grafico', 
                                     title="Variación del costo unitario nacionalizado final (COP)", color_discrete_sequence=['#059669'])
                    fig_cop.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', 
                        paper_bgcolor='rgba(0,0,0,0)', 
                        xaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Operación"), 
                        yaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Valor COP ($)", tickformat=",d")
                    )
                    st.plotly_chart(fig_cop, use_container_width=True)
                else:
                    fig_vacio = px.bar(title="Variación del costo unitario nacionalizado final (COP)")
                    fig_vacio.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_vacio, use_container_width=True)
            
            st.markdown("**Desglose detallado de precios por operación histórica:**")
            columnas_mostrar = ['OPERACIÓN', 'EMISIÓN FRA', 'FRA', 'VALOR UNITARIO (USD)']
            if col_cop_name: 
                columnas_mostrar.append(col_cop_name)
            
            df_resumen_tabla = df_hist[columnas_mostrar].drop_duplicates().copy()
            df_resumen_tabla['EMISIÓN FRA'] = df_resumen_tabla['EMISIÓN FRA'].dt.strftime('%Y-%m-%d')
            
            if col_cop_name:
                df_resumen_tabla[col_cop_name] = df_resumen_tabla[col_cop_name].apply(lambda x: "None" if pd.isna(x) or str(x).strip().lower()=='none' else x)
                
            st.dataframe(df_resumen_tabla.rename(columns={'EMISIÓN FRA':'Fecha Emisión FRA', 'FRA':'Factura', 'VALOR UNITARIO (USD)': 'VALOR UNITARIO (USD)'}), use_container_width=True, hide_index=True)

    # --- MÓDULO 2: DETALLE DE OPERACIÓN ---
    elif menu == "🔍 Detalle de Operación":
        st.title("Desglose analítico por operación")
        lista_ops = sorted(df_maestro['OPERACIÓN'].dropna().unique())
        op_sel = st.selectbox("Seleccione el Código Operativo (M):", lista_ops, index=0)
        st.write("---")
        
        df_op = df_maestro[df_maestro['OPERACIÓN'] == op_sel].copy()
        if not df_op.empty:
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
                st.markdown(f"**💰 Costo Equipos Operación:** USD {df_op['VALOR TOTAL (USD)'].sum():,.2f}")
                st.markdown(f"**💵 Flete Prorrateado:** USD {flete_tot / max(num_conts, 1):,.2f} por Contenedor")

            st.write("")
            st.subheader("⏳ Control de vencimientos financieros")
            
            # --- EVALUACIÓN GLOBAL DE ESTADO_PAGO PARA LOS SEMÁFOROS ---
            tiene_registro_pago = False
            if 'ESTADO_PAGO' in df_op.columns:
                valor_pago = str(df_op['ESTADO_PAGO'].iloc[0]).strip()
                if valor_pago != "" and valor_pago.lower() != "nan":
                    tiene_registro_pago = True

            if tiene_registro_pago:
                st.markdown("""
                    <div class="semaforo-box-p" style="border-left: 6px solid #10B981; background-color: #F0FDF4; padding: 20px; font-size: 16px;">
                        <span style="color: #15803D; font-weight: 700;">🟢 YA ESTÁ PAGO</span>
                        <span style="color: #475569; font-size:13.5px;">Esta obligación financiera se encuentra totalmente solventada y conciliada.</span>
                    </div>
                """, unsafe_allow_html=True)
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
                    st.markdown(renderizar_linea_vencimiento_semaforo(df_op['VENCIMIENTO 120D - PLENO'].iloc[0], "Límite 120 días (Pago plazo)"), unsafe_allow_html=True)

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
                                val_usd = p_row['VALOR TOTAL (USD)'] if 'VALOR TOTAL (USD)' in p_row else 0
                                cant = p_row['CANTIDAD'] if 'CANTIDAD' in p_row else 0
                                ref = p_row['REFERENCIA/MODELO'] if 'REFERENCIA/MODELO' in p_row else 'Sin Ref'
                                
                                if col_cop_name and pd.notna(p_row[col_cop_name]) and str(p_row[col_cop_name]).strip().lower() != 'none':
                                    texto_costo_variable = f" | Costo Nac: {p_row[col_cop_name]} COP"
                                elif 'VALOR UNITARIO (USD)' in p_row:
                                    texto_costo_variable = f" | Valor: ${p_row['VALOR UNITARIO (USD)']:,.2f} USD"
                                else:
                                    texto_costo_variable = ""

                                html_total_contenedor += f"""
                                <div class="product-row-p">
                                    <div class="product-title-p">{ref}</div>
                                    <div class="product-subtitle-p">Cantidad: {int(cant)} unidades</div>
                                    <div class="product-meta-p">Total FOB: USD {val_usd:,.2f}{texto_costo_variable}</div>
                                </div>
                                """
                            html_total_contenedor += "</div></div>"
                            st.markdown(html_total_contenedor, unsafe_allow_html=True)

    # --- MÓDULO 3: REFERENCIAS EN PRODUCCIÓN ---
    elif menu == "🚨 Referencias en Producción":
        st.title("Plan de fabricación y despacho")
        st.markdown("<p style='color: #64748B; font-size:14px;'>Monitoreo preventivo de referencias actualmente en cola de producción antes del zarpe internacional.</p>", unsafe_allow_html=True)
        st.write("---")
        
        if df_plan is not None and not df_plan.empty:
            st.markdown('<div class="dispatch-grid">', unsafe_allow_html=True)
            for _, r_plan in df_plan.iterrows():
                ref_m = r_plan.get('REFERENCIA / MODELO', 'N/A')
                cant_m = r_plan.get('CANTIDAD', 0)
                obs_m = r_plan.get('OBSERVACIONES', 'Sin novedades registradas')
                id_m = r_plan.get('ID', 'N/A')
                
                html_card = f"""
                <div class="dispatch-card-premium">
                    <div>
                        <div class="dispatch-tag">En Línea de Ensamble</div>
                        <div class="dispatch-model">{ref_m}</div>
                        <ul class="dispatch-items-list">
                            <li class="dispatch-item-line"><strong>Cantidad base:</strong> {int(cant_m) if pd.notna(cant_m) else 0} Unidades</li>
                            <li class="dispatch-item-line"><strong>Estado actual:</strong> {obs_m}</li>
                        </ul>
                    </div>
                    <div class="dispatch-meta-row">
                        <span>Orden Ref: #{id_m}</span>
                        <span>Fábrica Asignada</span>
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No existen órdenes activas en el plan de producción actual.")
