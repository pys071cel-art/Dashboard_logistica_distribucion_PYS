import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import io
from PIL import Image

# Intentar cargar el logo corporativo con manejo de excepción por seguridad
try:
    logo = Image.open("logo_PYS.jpg")
except Exception:
    logo = None

# =========================================================================
# 1. CONFIGURACIÓN DE PÁGINA (Estilo Corporativo Premium)
# =========================================================================
st.set_page_config(
    page_title="Logística de Distribución - PYS",
    page_icon="logo_PYS.jpg" if logo else "📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# 2. ESTILO CSS AVANZADO UI/UX (Executive Dark & Light Cohesive)
# =========================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Container */
    .block-container { 
        padding-top: 1.5rem; 
        padding-bottom: 2rem; 
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
    }
    
    h1, h2, h3, h4 { color: #0F172A; font-weight: 700; letter-spacing: -0.02em; }
    
    /* 📈 TARJETAS KPI SUPERIORES */
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
    
    /* 📋 FILAS DE TRAZABILIDAD EXECUTIVE */
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
    .op-badge-p { 
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); 
        color: white; 
        padding: 8px 16px; 
        font-weight: 700; 
        border-radius: 8px; 
        font-size: 14px; 
    }
    
    /* ⏳ SEMÁFOROS FINANCIEROS */
    .semaforo-box-p { 
        padding: 12px 18px; 
        border-radius: 10px; 
        margin-bottom: 8px; 
        font-size: 13.5px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        font-weight: 500;
    }
    .status-g-p { background-color: #ECFDF5; border: 1px solid #A7F3D0; color: #065F46; border-left: 5px solid #10B981; }
    .status-y-p { background-color: #FFFBEB; border: 1px solid #FDE68A; color: #92400E; border-left: 5px solid #F59E0B; }
    .status-r-p { background-color: #FEF2F2; border: 1px solid #FEE2E2; color: #991B1B; border-left: 5px solid #EF4444; }
    
    /* 🚚 ESTRUCTURA INYECTADA DE CONTENEDORES (FIXED COMPONENT) */
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

    /* 🚨 TARJETAS DIDÁCTICAS: POR DESPACHAR */
    .dispatch-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 16px;
        margin-top: 15px;
    }
    .dispatch-card-premium {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #F59E0B;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .dispatch-card-premium:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px -3px rgba(245, 158, 11, 0.08);
        border-color: #FCD34D;
    }
    .dispatch-tag {
        background-color: #FEF3C7;
        color: #D97706;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 12px;
    }
    .dispatch-model { font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 4px; }
    .dispatch-desc { font-size: 13px; color: #475569; line-height: 1.4; margin-bottom: 12px; }
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
        color: #EF4444;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* 🧭 SIDEBAR PREMIUM COMPONENT */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        color: #F1F5F9;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p { color: #FFFFFF !important; }
    [data-testid="stSidebar"] .stRadio > label { color: #94A3B8 !important; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
    
    /* Custom Sidebar Radio Buttons Style */
    div.row-widget.stRadio > div {
        background-color: transparent !important;
        gap: 6px;
    }
    div.row-widget.stRadio div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 12px 16px !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    div.row-widget.stRadio div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    div.row-widget.stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: #3B82F6 !important;
        border-color: #3B82F6 !important;
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    .sidebar-footer-p { 
        font-size: 11px; 
        color: #64748B; 
        text-align: left; 
        margin-top: 40px; 
        padding-top: 20px; 
        border-top: 1px solid rgba(255,255,255,0.08); 
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# 3. CONEXIÓN CORPORATIVA (ONEDRIVE - GRAPH API)
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
        
        # Descarga total del Maestro
        url_m = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/drive/items/{file_maestro_id}/content"
        res_m = requests.get(url_m, headers=headers, timeout=15)
        if res_m.status_code != 200:
            resultado["error"] = "Error al descargar el archivo Maestro desde OneDrive."
            return resultado
            
        # Descarga total del Plan
        url_p = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/drive/items/{file_plan_id}/content"
        res_p = requests.get(url_p, headers=headers, timeout=15)
        if res_p.status_code != 200:
            resultado["error"] = "Error al descargar el archivo de Planificación desde OneDrive."
            return resultado
            
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
# 4. MENÚ LATERAL DE NAVEGACIÓN RECONSTRUIDO EXECUTIVE
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
        ["📈 Trazabilidad e Historial", "🔍 Detalle de Operación", "🚨 Alertas: Por Despachar"],
        label_visibility="collapsed"
    )
    
    st.write("")
    if st.button("🔄 Sincronizar Datos Nube", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.markdown("""
        <div class="sidebar-footer-p" style="text-align: center; width: 100%;">
            <strong>Proyectos y Servicios SAS</strong><br>
            Área de planeación y Distribución<br>
            <span style='font-size:10px; color:#475569;'>Enterprise System v4.0</span>
        </div>
    """, unsafe_allow_html=True)

# =========================================================================
# 5. CONTROL DE PANTALLA PRINCIPAL
# =========================================================================
if error_detectado is not None:
    st.title("🔧 Diagnóstico de Conexión")
    st.error(error_detectado)

elif df_plan is not None and df_maestro is not None:
    fecha_hoy = datetime.now()

    # --- MÓDULO 1: TRAZABILIDAD GLOBAL ---
    if menu == "📈 Trazabilidad e Historial":
        st.title("Control General de Operaciones")
        st.markdown("<p style='color: #64748B; font-size:14px;'>Consolidado estratégico de importaciones e historial analítico de costos.</p>", unsafe_allow_html=True)
        st.write("---")
        
        total_usd_comprado = df_maestro['VALOR TOTAL (USD)'].sum() if 'VALOR TOTAL (USD)' in df_maestro.columns else 0
        total_contenedores_global = df_maestro['CONTENEDOR'].nunique() if 'CONTENEDOR' in df_maestro.columns else 0
        total_unidades_global = df_maestro['CANTIDAD'].sum() if 'CANTIDAD' in df_maestro.columns else 0
        
        ckpi1, ckpi2, ckpi3 = st.columns(3)
        with ckpi1:
            st.markdown(f'<div class="kpi-card-premium kpi-blue"><div class="kpi-val-p">USD {total_usd_comprado:,.2f}</div><div class="kpi-lbl-p">Inversión Total Equipos</div></div>', unsafe_allow_html=True)
        with ckpi2:
            st.markdown(f'<div class="kpi-card-premium kpi-indigo"><div class="kpi-val-p">{total_contenedores_global}</div><div class="kpi-lbl-p">Contenedores Gestión</div></div>', unsafe_allow_html=True)
        with ckpi3:
            st.markdown(f'<div class="kpi-card-premium kpi-emerald"><div class="kpi-val-p">{int(total_unidades_global):,}</div><div class="kpi-lbl-p">Unidades Globales Importadas</div></div>', unsafe_allow_html=True)
            
        st.subheader("📋 Estado Actual de Flujos Logísticos")
        
        if 'OPERACIÓN' in df_maestro.columns:
            ops_resumen = df_maestro.groupby('OPERACIÓN').agg({
                'CONTENEDOR': 'nunique',
                'CANTIDAD': 'sum',
                'VALOR TOTAL (USD)': 'sum',
                'ESTADO DE DISTRIBUCION': lambda x: str(x.dropna().iloc[0]).strip() if not x.dropna().empty else "En Proceso",
                'ETA': lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NaT
            }).reset_index()
            
            for _, row in ops_resumen.iterrows():
                eta_str = row['ETA'].strftime('%Y-%m-%d') if pd.notna(row['ETA']) else "Por Confirmar"
                estado_dist = row['ESTADO DE DISTRIBUCION']
                
                badge_style = "background-color: #DCFCE7; color: #16A34A;" if "Entregado" in estado_dist else "background-color: #FEF3C7; color: #D97706;"
                badge_html = f'<span style="{badge_style} padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight:600;">{estado_dist}</span>'

                st.markdown(f"""
                <div class="timeline-container-p">
                    <div style="display: flex; align-items: center; gap: 24px;">
                        <div class="op-badge-p">{row['OPERACIÓN']}</div>
                        <div>
                            <strong style="color: #0F172A; font-size: 15px;">Monto de Operación: USD {row['VALOR TOTAL (USD)']:,.2f}</strong><br>
                            <span style="color: #64748B; font-size: 13px;">📦 {row['CONTENEDOR']} Contenedor(es) | 🔢 {int(row['CANTIDAD']):,} Equipos de Carga</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 13px; color: #475569; font-weight: 500;">📅 ETA: {eta_str}</span><br>
                        <div style="margin-top: 6px;">{badge_html}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.write("---")
        
        st.subheader("📊 Gráficos Analíticos de Tendencia")
        productos_disponibles = sorted(df_maestro['REFERENCIA/MODELO'].dropna().unique())
        producto_sel = st.selectbox("Seleccione Referencia o Modelo a Evaluar:", productos_disponibles)
        
        df_hist = df_maestro[df_maestro['REFERENCIA/MODELO'] == producto_sel].copy()
        df_hist = df_hist.dropna(subset=['EMISIÓN FRA', 'VALOR UNITARIO (USD)']).sort_values('EMISIÓN FRA')
        
        if not df_hist.empty:
            col_cop_name = next((n for n in ['VALOR_NACIONALIZADO', 'VALOR NACIONALIZADO COP', 'VALOR_NACIONALIZADO_COP', 'VALOR NACIONALIZADO'] if n in df_maestro.columns), None)
            df_hist['Etiqueta_Grafico'] = df_hist.apply(lambda r: f"{r['OPERACIÓN']} ({r['EMISIÓN FRA'].strftime('%Y-%m-%d')})", axis=1)
            
            cg1, cg2 = st.columns(2)
            with cg1:
                fig_usd = px.line(df_hist, x='Etiqueta_Grafico', y='VALOR UNITARIO (USD)', markers=True, 
                                  title="Evolución Costo Unitario (USD FOB/CIF)", color_discrete_sequence=['#1E3A8A'])
                fig_usd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                      xaxis=dict(showgrid=True, gridcolor='#E2E8F0'), yaxis=dict(showgrid=True, gridcolor='#E2E8F0'))
                st.plotly_chart(fig_usd, use_container_width=True)
                
            with cg2:
                if col_cop_name and df_hist[col_cop_name].notna().any():
                    df_hist['COP_Grafico'] = pd.to_numeric(df_hist[col_cop_name], errors='coerce')
                    fig_cop = px.bar(df_hist, x='Etiqueta_Grafico', y='COP_Grafico', 
                                     title="Historial de Costo Unitario Nacionalizado (COP)", color_discrete_sequence=['#059669'])
                    fig_cop.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                          xaxis=dict(showgrid=True, gridcolor='#E2E8F0'), yaxis=dict(showgrid=True, gridcolor='#E2E8F0'))
                    st.plotly_chart(fig_cop, use_container_width=True)
                else:
                    st.info("💡 Datos en COP no disponibles para el gráfico de esta referencia.")
            
            st.markdown("**Desglose de Precios por Operación Histórica:**")
            columnas_mostrar = ['OPERACIÓN', 'EMISIÓN FRA', 'FRA', 'VALOR UNITARIO (USD)']
            if col_cop_name: columnas_mostrar.append(col_cop_name)
            df_resumen_tabla = df_hist[columnas_mostrar].drop_duplicates().copy()
            df_resumen_tabla['EMISIÓN FRA'] = df_resumen_tabla['EMISIÓN FRA'].dt.strftime('%Y-%m-%d')
            st.dataframe(df_resumen_tabla.rename(columns={'EMISIÓN FRA':'Fecha Emisión FRA', 'FRA':'Factura'}), use_container_width=True, hide_index=True)

    # --- MÓDULO 2: DETALLE DE OPERACIÓN E INVENTARIO (IMPECABLE RENDERING) ---
    elif menu == "🔍 Detalle de Operación":
        st.title("Desglose Analítico por Operación")
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
            st.subheader("⏳ Semáforo de Vencimientos Financieros")
            
            def renderizar_semaforo(fecha_limite, titulo_tramo, descuento_label):
                if pd.isna(fecha_limite):
                    return f'<div class="semaforo-box-p status-y-p"><span>{titulo_tramo}</span><strong>Fecha no parametrizada</strong></div>'
                dias_restantes = (fecha_limite - fecha_hoy).days
                if dias_restantes > 15:
                    clase_css, mensaje = "status-g-p", f"Vigente — Quedan {dias_restantes} días para el beneficio"
                elif 0 <= dias_restantes <= 15:
                    clase_css, mensaje = "status-y-p", f"Alerta de Cierre — Próximo a vencer ({dias_restantes} días restantes)"
                else:
                    clase_css, mensaje = "status-r-p", "Plazo Expirado"
                    
                return f'<div class="semaforo-box-p {clase_css}"><strong>{descuento_label} — {titulo_tramo}</strong><span>{mensaje} ({fecha_limite.strftime("%Y-%m-%d")})</span></div>'

            if 'VENCIMIENTO 45 D - 2%' in df_op.columns:
                st.markdown(renderizar_semaforo(df_op['VENCIMIENTO 45 D - 2%'].iloc[0], "Pronto Pago Inicial", "Descuento del 2%"), unsafe_allow_html=True)
            if 'VENCIMIENTO 69D 1.5%' in df_op.columns:
                st.markdown(renderizar_semaforo(df_op['VENCIMIENTO 69D 1.5%'].iloc[0], "Segundo Tramo de Pago", "Descuento del 1.5%"), unsafe_allow_html=True)
            if 'VENCIMIENTO 89D - 1%' in df_op.columns:
                st.markdown(renderizar_semaforo(df_op['VENCIMIENTO 89D - 1%'].iloc[0], "Tercer Tramo de Pago", "Descuento del 1%"), unsafe_allow_html=True)
            if 'VENCIMIENTO 120D - PLENO' in df_op.columns:
                st.markdown(renderizar_semaforo(df_op['VENCIMIENTO 120D - PLENO'].iloc[0], "Límite de Crédito Neto", "Pago Pleno"), unsafe_allow_html=True)

            st.write("")
            st.subheader("🚚 Distribución Física de Carga por Contenedor")
            
            if 'CONTENEDOR' in df_op.columns:
                contenedores_sistema = df_op['CONTENEDOR'].dropna().unique()
                
                if len(contenedores_sistema) > 0:
                    grid_visual = st.columns(min(len(contenedores_sistema), 2))
                    
                    for idx, cont_id in enumerate(contenedores_sistema):
                        df_items_contenedor = df_op[df_op['CONTENEDOR'] == cont_id]
                        col_actual = grid_visual[idx % len(grid_visual)]
                        
                        with col_actual:
                            # SE CONSTRUYE TODO EL CONTENEDOR EN UNA SOLA CADENA TOTALMENTE DE APERTURA A CIERRE
                            html_total_contenedor = ""
                            html_total_contenedor += '<div class="container-box-p">'
                            html_total_contenedor += '  <div class="container-header-p">'
                            html_total_contenedor += f'      <span>🆔 CONTENEDOR: {cont_id}</span>'
                            html_total_contenedor += '      <span>📦 TIPO: 40HQ ESTÁNDAR</span>'
                            html_total_contenedor += '  </div>'
                            html_total_contenedor += '  <div class="container-body-p">'
                            
                            for _, p_row in df_items_contenedor.iterrows():
                                val_usd = p_row['VALOR TOTAL (USD)'] if 'VALOR TOTAL (USD)' in p_row else 0
                                cant = p_row['CANTIDAD'] if 'CANTIDAD' in p_row else 0
                                ref = p_row['REFERENCIA/MODELO'] if 'REFERENCIA/MODELO' in p_row else 'Sin Ref'
                                
                                col_cop_name = next((n for n in ['VALOR_NACIONALIZADO', 'VALOR NACIONALIZADO COP', 'VALOR_NACIONALIZADO_COP', 'VALOR NACIONALIZADO'] if n in df_op.columns), None)
                                
                                if col_cop_name and pd.notna(p_row[col_cop_name]):
                                    try:
                                        valor_numerico_cop = pd.to_numeric(p_row[col_cop_name])
                                        texto_costo_variable = f" | 🇨🇴 Nac: ${valor_numerico_cop:,.2f} COP"
                                    except (ValueError, TypeError):
                                        texto_costo_variable = f" | 🇨🇴 Nac: {p_row[col_cop_name]} COP"
                                elif 'VALOR UNITARIO (USD)' in p_row:
                                    texto_costo_variable = f" | 💵 Unitario: ${p_row['VALOR UNITARIO (USD)']:,.2f} USD"
                                else:
                                    texto_costo_variable = ""

                                # Agregar la fila de producto al bloque sin romper strings
                                html_total_contenedor += '      <div class="product-row-p">'
                                html_total_contenedor += f'          <span class="product-title-p">{int(cant)} Unidades <span class="product-subtitle-p">— {ref}</span></span>'
                                html_total_contenedor += f'          <span class="product-meta-p">💰 Total Bloque: ${val_usd:,.2f} USD {texto_costo_variable}</span>'
                                html_total_contenedor += '      </div>'
                            
                            html_total_contenedor += '  </div>'
                            html_total_contenedor += '</div>'
                            
                            # Renderizado masivo forzado
                            st.markdown(html_total_contenedor, unsafe_allow_html=True)

# --- MÓDULO 3: POR DESPACHAR (DISEÑO RESTRUCTURADO Y BLINDADO) ---
    elif menu == "🚨 Alertas: Por Despachar":
        st.title("Módulo de Control: Embarques en Planeación")
        st.markdown("<p style='color: #64748B; font-size:14px;'>Monitoreo predictivo de órdenes en fábrica pendientes por confirmación de BL y zarpe.</p>", unsafe_allow_html=True)
        st.write("---")
        
        df_plan['BL_aux'] = df_plan['BL'].astype(str).str.strip().str.upper()
        mascara_sin_bl = (df_plan['BL'].isna()) | (df_plan['BL_aux'] == 'NAN') | (df_plan['BL_aux'] == '') | (df_plan['BL_aux'] == 'POR ASIGNAR')
        df_pendientes_despacho = df_plan[mascara_sin_bl].copy()
        
        if not df_pendientes_despacho.empty:
            st.markdown(f"### ⚠️ Órdenes Críticas sin Zarpe Detectadas (`{len(df_pendientes_despacho)}` Referencias)")
            
            # Configuramos un sistema de 3 columnas nativas de Streamlit para el Grid interactivo
            columnas_grid = st.columns(3)
            
            for idx, fila in df_pendientes_despacho.reset_index().iterrows():
                pi_label = fila['No PI'] if pd.notna(fila['No PI']) else 'Pendiente'
                desc_label = fila['Description'] if pd.notna(fila['Description']) else 'Sin descripción técnica parametrizada.'
                modelo_label = fila['Modelo'] if pd.notna(fila['Modelo']) else 'Modelo Desconocido'
                qty_label = int(fila['QTY']) if pd.notna(fila['QTY']) else 0
                
                # Manejo limpio de fechas para evitar formatos extensos con horas
                if pd.notna(fila['Forecast ETD']):
                    if isinstance(fila['Forecast ETD'], datetime):
                        etd_label = fila['Forecast ETD'].strftime('%Y-%m-%d')
                    else:
                        etd_label = str(fila['Forecast ETD']).split(" ")[0]
                else:
                    etd_label = 'No Parametrizado'
                
                # Seleccionamos la columna correspondiente del Grid de Streamlit de manera cíclica
                col_actual = columnas_grid[idx % 3]
                
                with col_actual:
                    # Construcción horizontal sin saltos de línea físicos para evitar escapes a texto plano
                    html_tarjeta = ""
                    html_tarjeta += '<div class="dispatch-card-premium">'
                    html_tarjeta += '  <div class="dispatch-tag">Fábrica - Pendiente BL</div>'
                    html_tarjeta += f'  <div class="dispatch-model">📦 {modelo_label}</div>'
                    html_tarjeta += f'  <div class="dispatch-desc">{desc_label}</div>'
                    html_tarjeta += '  <div class="dispatch-meta-row">'
                    html_tarjeta += f'      <span><strong>Cant:</strong> {qty_label:,} un.</span>'
                    html_tarjeta += f'      <span><strong>Proforma:</strong> {pi_label}</span>'
                    html_tarjeta += '  </div>'
                    html_tarjeta += f'  <div class="dispatch-date">🚨 <strong>Forecast ETD:</strong> {etd_label}</div>'
                    html_tarjeta += '</div>'
                    
                    # Inyección segura e individual por tarjeta
                    st.markdown(html_tarjeta, unsafe_allow_html=True)
                    st.write("") # Espaciado estético inferior entre filas del grid
        else:
            st.success("🎉 ¡Excelente control operativo! No se registran referencias pendientes por despachar en el plan actual.")
