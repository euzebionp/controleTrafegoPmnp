import streamlit as st
import db_handler
import utils
import plotly.express as px
import pandas as pd

def dashboard_page():
    st.header("Dashboard de Multas")
    
    # Check for expired CNH
    drivers_df = db_handler.get_drivers()
    expired_count = 0
    expiring_soon_count = 0
    expired_drivers = []
    
    for index, row in drivers_df.iterrows():
        days = utils.days_until_expiration(row['validade_cnh'])
        if days < 0:
            expired_count += 1
            expired_drivers.append((row['nome'], utils.format_date_br(row['validade_cnh'])))
        elif days <= 30:
            expiring_soon_count += 1
    
    # Display CNH alerts
    if expired_count > 0 or expiring_soon_count > 0:
        st.divider()
        col_alert1, col_alert2 = st.columns(2)
        
        if expired_count > 0:
            with col_alert1:
                st.error(f"🔴 **{expired_count} CNH(s) Vencida(s)**")
                for driver_name, validade in expired_drivers:
                    st.write(f"• {driver_name} - Venceu em {validade}")
        
        if expiring_soon_count > 0:
            with col_alert2:
                st.warning(f"⚠️ **{expiring_soon_count} CNH(s) Vencendo em até 30 dias**")
        
        st.divider()
    
    # Check for maintenance alerts
    maintenance_alerts = db_handler.get_maintenance_alerts()
    if not maintenance_alerts.empty:
        st.divider()
        st.error(f"🔧 **ALERTA DE MANUTENÇÃO: {len(maintenance_alerts)} veículo(s) precisam de atenção!**")
        
        # Display each vehicle alert
        for index, row in maintenance_alerts.iterrows():
            km_diff = row['proximo_servico_km'] - row['km_atual']
            
            if km_diff < 0:
                status_msg = f"🔴 **VENCIDA** por {abs(km_diff):.0f} km"
                st.error(f"**{row['modelo']} ({row['placa']})** - Km Atual: {row['km_atual']:.0f} km - Próxima Revisão: {row['proximo_servico_km']:.0f} km - {status_msg}")
            else:
                status_msg = f"⚠️ **Próxima** em {km_diff:.0f} km"
                st.warning(f"**{row['modelo']} ({row['placa']})** - Km Atual: {row['km_atual']:.0f} km - Próxima Revisão: {row['proximo_servico_km']:.0f} km - {status_msg}")
        
        st.divider()
    
    # Fines data
    df = db_handler.get_fines_df()
    
    if df.empty:
        st.info("Nenhuma multa cadastrada para exibir estatísticas.")
        return

    # Metrics
    total_multas = len(df)
    total_arrecadado = df['valor'].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("Total de Multas", total_multas)
    col2.metric("Total Arrecadado", f"R$ {total_arrecadado:,.2f}")
    
    st.divider()
    
    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Multas por Tipo")
        fig_type = px.pie(df, names='tipo_infracao', title='Distribuição por Tipo de Infração')
        st.plotly_chart(fig_type, use_container_width=True)
        
    with c2:
        st.subheader("Multas por Mês")
        df['data'] = pd.to_datetime(df['data'])
        df['mes'] = df['data'].dt.strftime('%m/%Y')  # Brazilian format MM/YYYY
        multas_por_mes = df.groupby('mes').size().reset_index(name='count')
        fig_month = px.bar(multas_por_mes, x='mes', y='count', title='Evolução Mensal')
        st.plotly_chart(fig_month, use_container_width=True)
        
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("Ranking de Motoristas")
        top_drivers = df['motorista'].value_counts().reset_index()
        top_drivers.columns = ['motorista', 'multas']
        fig_driver = px.bar(top_drivers.head(5), x='multas', y='motorista', orientation='h', title='Top 5 Motoristas Infratores')
        st.plotly_chart(fig_driver, use_container_width=True)

    with c4:
        st.subheader("Ranking de Veículos")
        top_vehicles = df['veiculo_modelo'].value_counts().reset_index()
        top_vehicles.columns = ['veiculo', 'multas']
        fig_vehicle = px.bar(top_vehicles.head(5), x='multas', y='veiculo', orientation='h', title='Top 5 Veículos Multados')
        st.plotly_chart(fig_vehicle, use_container_width=True)
