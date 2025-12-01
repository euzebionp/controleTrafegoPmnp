from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Sum, Count, Q, Max
from django.utils import timezone
from datetime import timedelta
from .models import Motorista, Veiculo, Viagem, Manutencao, Multa
from .forms import MotoristaForm, VeiculoForm, ViagemForm, ManutencaoForm, MultaForm


# Authentication Views
def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'logistics/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


# Dashboard View
@login_required
def dashboard_view(request):
    """Main dashboard with statistics"""
    # Get counts
    total_motoristas = Motorista.objects.count()
    total_veiculos = Veiculo.objects.count()
    total_viagens = Viagem.objects.count()
    total_multas = Multa.objects.count()
    
    # Get recent data
    recent_viagens = Viagem.objects.select_related('motorista', 'veiculo').order_by('-data', '-hora_saida')[:5]
    recent_multas = Multa.objects.select_related('motorista', 'veiculo').order_by('-data')[:5]
    
    # Get maintenance alerts
    manutencoes_pendentes = []
    veiculos = Veiculo.objects.all()
    for veiculo in veiculos:
        ultima_manutencao = Manutencao.objects.filter(veiculo=veiculo).order_by('-data').first()
        if ultima_manutencao:
            is_due, message = ultima_manutencao.is_due()
            if is_due:
                manutencoes_pendentes.append({
                    'veiculo': veiculo,
                    'message': message,
                    'manutencao': ultima_manutencao
                })
    
    # Calculate total fines value
    total_multas_valor = Multa.objects.aggregate(total=Sum('valor'))['total'] or 0
    
    context = {
        'total_motoristas': total_motoristas,
        'total_veiculos': total_veiculos,
        'total_viagens': total_viagens,
        'total_multas': total_multas,
        'total_multas_valor': total_multas_valor,
        'recent_viagens': recent_viagens,
        'recent_multas': recent_multas,
        'manutencoes_pendentes': manutencoes_pendentes,
    }
    
    return render(request, 'logistics/dashboard.html', context)


# Motorista Views
@login_required
def motorista_list(request):
    """List all drivers"""
    motoristas = Motorista.objects.all()
    return render(request, 'logistics/motorista_list.html', {'motoristas': motoristas})


@login_required
def motorista_create(request):
    """Create a new driver"""
    if request.method == 'POST':
        form = MotoristaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motorista cadastrado com sucesso!')
            return redirect('motorista_list')
    else:
        form = MotoristaForm()
    
    return render(request, 'logistics/motorista_form.html', {'form': form, 'action': 'Cadastrar'})


@login_required
def motorista_update(request, pk):
    """Update an existing driver"""
    motorista = get_object_or_404(Motorista, pk=pk)
    
    if request.method == 'POST':
        form = MotoristaForm(request.POST, instance=motorista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motorista atualizado com sucesso!')
            return redirect('motorista_list')
    else:
        form = MotoristaForm(instance=motorista)
    
    return render(request, 'logistics/motorista_form.html', {'form': form, 'action': 'Atualizar'})


@login_required
def motorista_delete(request, pk):
    """Delete a driver"""
    motorista = get_object_or_404(Motorista, pk=pk)
    
    if request.method == 'POST':
        motorista.delete()
        messages.success(request, 'Motorista excluído com sucesso!')
        return redirect('motorista_list')
    
    return render(request, 'logistics/motorista_confirm_delete.html', {'motorista': motorista})


# Veiculo Views
@login_required
def veiculo_list(request):
    """List all vehicles"""
    veiculos = Veiculo.objects.all()
    return render(request, 'logistics/veiculo_list.html', {'veiculos': veiculos})


@login_required
def veiculo_create(request):
    """Create a new vehicle"""
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('veiculo_list')
    else:
        form = VeiculoForm()
    
    return render(request, 'logistics/veiculo_form.html', {'form': form, 'action': 'Cadastrar'})


@login_required
def veiculo_update(request, pk):
    """Update an existing vehicle"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('veiculo_list')
    else:
        form = VeiculoForm(instance=veiculo)
    
    return render(request, 'logistics/veiculo_form.html', {'form': form, 'action': 'Atualizar'})


@login_required
def veiculo_delete(request, pk):
    """Delete a vehicle"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST':
        veiculo.delete()
        messages.success(request, 'Veículo excluído com sucesso!')
        return redirect('veiculo_list')
    
    return render(request, 'logistics/veiculo_confirm_delete.html', {'veiculo': veiculo})


# Viagem Views
@login_required
def viagem_list(request):
    """List all travels"""
    viagens = Viagem.objects.select_related('motorista', 'veiculo').all()
    return render(request, 'logistics/viagem_list.html', {'viagens': viagens})


@login_required
def viagem_create(request):
    """Create a new travel"""
    if request.method == 'POST':
        form = ViagemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viagem cadastrada com sucesso!')
            return redirect('viagem_list')
    else:
        form = ViagemForm()
    
    return render(request, 'logistics/viagem_form.html', {'form': form, 'action': 'Cadastrar'})


@login_required
def viagem_update(request, pk):
    """Update an existing travel"""
    viagem = get_object_or_404(Viagem, pk=pk)
    
    if request.method == 'POST':
        form = ViagemForm(request.POST, instance=viagem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viagem atualizada com sucesso!')
            return redirect('viagem_list')
    else:
        form = ViagemForm(instance=viagem)
    
    return render(request, 'logistics/viagem_form.html', {'form': form, 'action': 'Atualizar'})


@login_required
def viagem_delete(request, pk):
    """Delete a travel"""
    viagem = get_object_or_404(Viagem, pk=pk)
    
    if request.method == 'POST':
        viagem.delete()
        messages.success(request, 'Viagem excluída com sucesso!')
        return redirect('viagem_list')
    
    return render(request, 'logistics/viagem_confirm_delete.html', {'viagem': viagem})


# Manutencao Views
@login_required
def manutencao_list(request):
    """List all maintenance records"""
    manutencoes = Manutencao.objects.select_related('veiculo').all()
    return render(request, 'logistics/manutencao_list.html', {'manutencoes': manutencoes})


@login_required
def manutencao_create(request):
    """Create a new maintenance record"""
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manutenção cadastrada com sucesso!')
            return redirect('manutencao_list')
    else:
        form = ManutencaoForm()
    
    return render(request, 'logistics/manutencao_form.html', {'form': form, 'action': 'Cadastrar'})


@login_required
def manutencao_update(request, pk):
    """Update an existing maintenance record"""
    manutencao = get_object_or_404(Manutencao, pk=pk)
    
    if request.method == 'POST':
        form = ManutencaoForm(request.POST, instance=manutencao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manutenção atualizada com sucesso!')
            return redirect('manutencao_list')
    else:
        form = ManutencaoForm(instance=manutencao)
    
    return render(request, 'logistics/manutencao_form.html', {'form': form, 'action': 'Atualizar'})


@login_required
def manutencao_delete(request, pk):
    """Delete a maintenance record"""
    manutencao = get_object_or_404(Manutencao, pk=pk)
    
    if request.method == 'POST':
        manutencao.delete()
        messages.success(request, 'Manutenção excluída com sucesso!')
        return redirect('manutencao_list')
    
    return render(request, 'logistics/manutencao_confirm_delete.html', {'manutencao': manutencao})


# Multa Views
@login_required
def multa_list(request):
    """List all fines"""
    multas = Multa.objects.select_related('motorista', 'veiculo').all()
    return render(request, 'logistics/multa_list.html', {'multas': multas})


@login_required
def multa_create(request):
    """Create a new fine"""
    if request.method == 'POST':
        form = MultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Multa cadastrada com sucesso!')
            return redirect('multa_list')
    else:
        form = MultaForm()
    
    return render(request, 'logistics/multa_form.html', {'form': form, 'action': 'Cadastrar'})


@login_required
def multa_update(request, pk):
    """Update an existing fine"""
    multa = get_object_or_404(Multa, pk=pk)
    
    if request.method == 'POST':
        form = MultaForm(request.POST, instance=multa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Multa atualizada com sucesso!')
            return redirect('multa_list')
    else:
        form = MultaForm(instance=multa)
    
    return render(request, 'logistics/multa_form.html', {'form': form, 'action': 'Atualizar'})


@login_required
def multa_delete(request, pk):
    """Delete a fine"""
    multa = get_object_or_404(Multa, pk=pk)
    
    if request.method == 'POST':
        multa.delete()
        messages.success(request, 'Multa excluída com sucesso!')
        return redirect('multa_list')
    
    return render(request, 'logistics/multa_confirm_delete.html', {'multa': multa})


# Reports View
@login_required
def reports_view(request):
    """Generate reports and statistics"""
    # Multas por motorista
    multas_por_motorista = Multa.objects.values('motorista__nome').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    ).order_by('-total')
    
    # Multas por veículo
    multas_por_veiculo = Multa.objects.values('veiculo__placa').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    ).order_by('-total')
    
    # Viagens por motorista
    viagens_por_motorista = Viagem.objects.values('motorista__nome').annotate(
        total=Count('id'),
        distancia_total=Sum('distancia')
    ).order_by('-total')
    
    # Manutenções por veículo
    manutencoes_por_veiculo = Manutencao.objects.values('veiculo__placa').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    ).order_by('-total')
    
    context = {
        'multas_por_motorista': multas_por_motorista,
        'multas_por_veiculo': multas_por_veiculo,
        'viagens_por_motorista': viagens_por_motorista,
        'manutencoes_por_veiculo': manutencoes_por_veiculo,
    }
    
    return render(request, 'logistics/reports.html', context)
