import streamlit as st
import db_handler
import utils
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_pdf(df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("Relatório de Multas", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Summary
    total_multas = len(df)
    total_valor = df['valor'].sum()
    elements.append(Paragraph(f"Total de Multas: {total_multas}", styles['Normal']))
    elements.append(Paragraph(f"Valor Total Arrecadado: R$ {total_valor:,.2f}", styles['Normal']))
    elements.append(Spacer(1, 24))
    
    # Table Data
    data = [['ID', 'Data', 'Motorista', 'Veículo', 'Tipo', 'Valor']]
    for index, row in df.iterrows():
        data.append([
            str(row['id']),
            utils.format_date_br(row['data']),  # Format date to dd/mm/yyyy
            row['motorista'],
            row['veiculo_placa'],
            row['tipo_infracao'],
            f"R$ {row['valor']:.2f}"
        ])
    
    # Table Style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

def reports_page():
    st.header("Relatórios")
    
    df = db_handler.get_fines_df()
    
    if df.empty:
        st.info("Não há dados para gerar relatório.")
        return
        
    st.dataframe(df)
    
    if st.button("Gerar PDF"):
        pdf_buffer = generate_pdf(df)
        st.download_button(
            label="Baixar Relatório PDF",
            data=pdf_buffer,
            file_name="relatorio_multas.pdf",
            mime="application/pdf"
        )
