"""
PDF Report Generation Module
Generates PDF reports for all entities in the logistics system
"""
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from .models import Motorista, Veiculo, Multa, Manutencao, Viagem


def generate_motoristas_pdf():
    """Generate PDF report for all drivers"""
    # Create buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Title
    title = Paragraph("Relatório de Motoristas", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Get data
    motoristas = Motorista.objects.all().order_by('nome')
    
    # Table data
    data = [['Nome', 'CPF', 'CNH', 'Validade CNH']]
    
    for motorista in motoristas:
        data.append([
            motorista.nome,
            motorista.cpf,
            motorista.cnh,
            motorista.validade_cnh.strftime('%d/%m/%Y')
        ])
    
    # Create table
    table = Table(data, colWidths=[3.5*inch, 2*inch, 2*inch, 1.5*inch])
    
    # Table style
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF from buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_motoristas.pdf"'
    response.write(pdf)
    
    return response


def generate_veiculos_pdf():
    """Generate PDF report for all vehicles"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("Relatório de Veículos", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    veiculos = Veiculo.objects.all().order_by('placa')
    
    data = [['Placa', 'Modelo', 'Ano', 'RENAVAM', 'KM Atual']]
    
    for veiculo in veiculos:
        data.append([
            veiculo.placa,
            veiculo.modelo,
            str(veiculo.ano),
            veiculo.renavam,
            f"{veiculo.km_atual:,} km".replace(',', '.'),
        ])
    
    table = Table(data, colWidths=[1.5*inch, 3*inch, 1*inch, 2*inch, 1.5*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_veiculos.pdf"'
    response.write(pdf)
    
    return response


def generate_multas_pdf():
    """Generate PDF report for all fines"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("Relatório de Multas", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    multas = Multa.objects.select_related('motorista', 'veiculo').all().order_by('-data')
    
    data = [['Data', 'Motorista', 'Veículo', 'Infração', 'Local', 'Valor']]
    
    for multa in multas:
        tipo_infracao = multa.tipo_infracao
        if len(tipo_infracao) > 30:
            tipo_infracao = tipo_infracao[:30] + '...'
            
        data.append([
            multa.data.strftime('%d/%m/%Y'),
            multa.motorista.nome if multa.motorista else '-',
            multa.veiculo.placa if multa.veiculo else '-',
            tipo_infracao,
            multa.local,
            f"R$ {multa.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        ])
    
    table = Table(data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2.5*inch, 1.3*inch, 1.3*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_multas.pdf"'
    response.write(pdf)
    
    return response


def generate_manutencoes_pdf():
    """Generate PDF report for all maintenance records"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("Relatório de Manutenções", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    manutencoes = Manutencao.objects.select_related('veiculo').all().order_by('-data')
    
    data = [['Data', 'Veículo', 'Tipo de Serviço', 'Descrição', 'Valor', 'KM Realizado']]
    
    for manutencao in manutencoes:
        data.append([
            manutencao.data.strftime('%d/%m/%Y'),
            manutencao.veiculo.placa,
            manutencao.tipo_servico,
            manutencao.descricao[:40] + '...' if len(manutencao.descricao) > 40 else manutencao.descricao,
            f"R$ {manutencao.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            f"{manutencao.km_realizado:,} km".replace(',', '.')
        ])
    
    table = Table(data, colWidths=[1.2*inch, 1.2*inch, 1.5*inch, 2.5*inch, 1.3*inch, 1.3*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_manutencoes.pdf"'
    response.write(pdf)
    
    return response


def generate_viagens_pdf():
    """Generate PDF report for all travels"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("Relatório de Viagens", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    viagens = Viagem.objects.select_related('motorista', 'veiculo').all().order_by('-data')
    
    data = [['Data', 'Motorista', 'Veículo', 'Origem', 'Destino', 'Distância']]
    
    for viagem in viagens:
        data.append([
            viagem.data.strftime('%d/%m/%Y'),
            viagem.motorista.nome,
            viagem.veiculo.placa,
            viagem.origem[:20] + '...' if len(viagem.origem) > 20 else viagem.origem,
            viagem.destino[:20] + '...' if len(viagem.destino) > 20 else viagem.destino,
            f"{viagem.distancia:,.1f} km".replace(',', 'X').replace('.', ',').replace('X', '.')
        ])
    
    table = Table(data, colWidths=[1.2*inch, 3*inch, 1.2*inch, 1.5*inch, 1.5*inch, 1.3*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_viagens.pdf"'
    response.write(pdf)
    
    return response
