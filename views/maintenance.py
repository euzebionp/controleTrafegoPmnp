import streamlit as st
import db_handler
import utils
from datetime import datetime, timedelta
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io


def generate_maintenance_pdf(maintenance_df):
    """Generate PDF report of maintenance history."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Relatório de Manutenções", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary
    total_records = len(maintenance_df)
    total_cost = maintenance_df["valor"].sum()
    elements.append(Paragraph(f"Total de Registros: {total_records}", styles["Normal"]))
    elements.append(Paragraph(f"Custo Total: R$ {total_cost:,.2f}", styles["Normal"]))
    elements.append(Spacer(1, 24))

    # Table Data
    data = [["Data", "Veículo", "Serviço", "Km", "Valor"]]

    for index, row in maintenance_df.iterrows():
        formatted_date = utils.format_date_br(row["data"])
        data.append(
            [
                formatted_date,
                row["veiculo_placa"],
                row["tipo_servico"],
                f"{row['km_realizado']:.0f} km",
                f"R$ {row['valor']:.2f}",
            ]
        )

    # Table Style
    table = Table(data, colWidths=[70, 100, 150, 80, 80])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
            ]
        )
    )

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer


def maintenance_page():
    st.header("Controle de Manutenções")

    # Check for alerts
    alerts_df = db_handler.get_maintenance_alerts()
    if not alerts_df.empty:
        st.error(
            f"⚠️ **ALERTA DE MANUTENÇÃO:** {len(alerts_df)} veículo(s) precisam de atenção!"
        )
        with st.expander("Ver Veículos com Manutenção Próxima/Vencida"):
            for index, row in alerts_df.iterrows():
                km_diff = row["proximo_servico_km"] - row["km_atual"]
                status_msg = ""
                if km_diff < 0:
                    status_msg = f"🔴 VENCIDA por {abs(km_diff):.0f} km"
                else:
                    status_msg = f"⚠️ Vence em {km_diff:.0f} km"

                st.write(
                    f"**{row['modelo']} ({row['placa']})** - Km Atual: {row['km_atual']:.0f} - Próx. Serviço: {row['proximo_servico_km']:.0f} - **{status_msg}**"
                )

    # Tabs
    tab1, tab2 = st.tabs(["Registrar Manutenção", "Histórico de Manutenções"])

    with tab1:
        st.subheader("Nova Manutenção")

        vehicles_df = db_handler.get_vehicles()
        if vehicles_df.empty:
            st.warning("Cadastre veículos antes de registrar manutenções.")
        else:
            vehicle_options = {
                f"{row['placa']} - {row['modelo']}": row["id"]
                for _, row in vehicles_df.iterrows()
            }

            with st.form("maintenance_form"):
                col1, col2 = st.columns(2)
                with col1:
                    selected_vehicle_label = st.selectbox(
                        "Veículo", list(vehicle_options.keys())
                    )
                    data = st.date_input("Data do Serviço")
                    tipo_servico = st.selectbox(
                        "Tipo de Serviço",
                        [
                            "Troca de Óleo",
                            "Revisão Geral",
                            "Troca de Pneus",
                            "Freios",
                            "Outros",
                        ],
                    )

                with col2:
                    # Try to get current km of selected vehicle to suggest
                    selected_vehicle_id = vehicle_options[selected_vehicle_label]
                    vehicle_data = db_handler.get_vehicle_by_id(selected_vehicle_id)
                    current_km = vehicle_data["km_atual"] if vehicle_data else 0

                    km_realizado = st.number_input(
                        "Quilometragem Atual (Km)",
                        min_value=0.0,
                        value=float(current_km),
                        step=1.0,
                    )
                    valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

                st.markdown("---")
                st.write("**Previsão do Próximo Serviço**")

                # Calculate next service km based on service type
                if tipo_servico == "Troca de Óleo":
                    default_next_km = km_realizado + 10000
                    km_help = "Troca de óleo: automaticamente +10.000km"
                elif tipo_servico == "Revisão Geral":
                    default_next_km = km_realizado + 20000
                    km_help = "Revisão geral: sugestão de +20.000km"
                elif tipo_servico == "Troca de Pneus":
                    default_next_km = km_realizado + 40000
                    km_help = "Troca de pneus: sugestão de +40.000km"
                elif tipo_servico == "Freios":
                    default_next_km = km_realizado + 30000
                    km_help = "Freios: sugestão de +30.000km"
                else:
                    default_next_km = km_realizado + 10000
                    km_help = "Defina a quilometragem da próxima revisão"

                col3, col4 = st.columns(2)
                with col3:
                    proximo_km = st.number_input(
                        "Próxima Revisão (Km)",
                        min_value=0.0,
                        value=float(default_next_km),
                        step=100.0,
                        help=km_help,
                    )
                with col4:
                    proximo_data = st.date_input(
                        "Data Prevista",
                        value=datetime.now() + timedelta(days=180),
                        help="Estimativa de 6 meses",
                    )

                descricao = st.text_area("Observações / Detalhes do Serviço")

                submit_button = st.form_submit_button("💾 Salvar Manutenção")

                if submit_button:
                    if tipo_servico and valor > 0:
                        success, message = db_handler.add_maintenance(
                            selected_vehicle_id,
                            str(data),
                            tipo_servico,
                            descricao,
                            km_realizado,
                            proximo_km,
                            str(proximo_data),
                            valor,
                        )

                        # Also update vehicle km if the input km is greater than current
                        if km_realizado > current_km:
                            db_handler.update_vehicle(
                                vehicle_data["id"],
                                vehicle_data["placa"],
                                vehicle_data["modelo"],
                                vehicle_data["ano"],
                                vehicle_data["renavam"],
                                km_realizado,
                            )

                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Preencha os campos obrigatórios.")

    with tab2:
        st.subheader("Histórico")
        maintenance_df = db_handler.get_maintenances()

        if maintenance_df.empty:
            st.info("Nenhuma manutenção registrada.")
        else:
            # Print button
            col_print, col_space = st.columns([1, 3])
            with col_print:
                if st.button("🖨️ Imprimir Relatório", use_container_width=True):
                    pdf_buffer = generate_maintenance_pdf(maintenance_df)
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=pdf_buffer,
                        file_name="relatorio_manutencao.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )

            for index, row in maintenance_df.iterrows():
                formatted_date = utils.format_date_br(row["data"])
                with st.expander(
                    f"🔧 {formatted_date} - {row['veiculo_modelo']} - {row['tipo_servico']}"
                ):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(
                            f"**Veículo:** {row['veiculo_placa']} - {row['veiculo_modelo']}"
                        )
                        st.write(f"**Serviço:** {row['tipo_servico']}")
                        st.write(f"**Km Realizado:** {row['km_realizado']:.0f} km")
                        st.write(f"**Valor:** R$ {row['valor']:.2f}")
                        st.write(
                            f"**Próxima Revisão:** {row['proximo_servico_km']:.0f} km"
                        )
                        st.write(f"**Descrição:** {row['descricao']}")

                    with col2:
                        if st.button("🗑️ Excluir", key=f"del_maint_{row['id']}"):
                            success, msg = db_handler.delete_maintenance(row["id"])
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
