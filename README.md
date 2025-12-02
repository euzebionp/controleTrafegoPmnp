# Sistema de Gestão Logística - PMNP

Sistema web para gerenciamento de frota, viagens, multas e manutenções de veículos desenvolvido em Django.

![Dashboard](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## 📋 Funcionalidades

### 🚗 Gestão de Veículos
- Cadastro completo de veículos (placa, modelo, ano, RENAVAM)
- Controle automático de quilometragem
- Histórico de viagens e manutenções

### 👨‍✈️ Gestão de Motoristas
- Cadastro de motoristas com CPF e CNH
- Controle de validade da CNH
- Histórico de viagens e multas

### 🛣️ Gestão de Viagens
- Registro de viagens com origem, destino e distância
- **Campo de KM atual do veículo** com atualização automática
- **Sistema de alertas de manutenção** baseado em quilometragem

### ⚠️ Gestão de Multas
- Registro de infrações de trânsito
- Vinculação com motorista, veículo e viagem
- Controle de valores e tipos de infração

### 🔧 Gestão de Manutenções
- Registro de serviços realizados
- Programação de próximas manutenções (KM e data)
- **Alertas automáticos** quando a manutenção está próxima ou vencida

### 📊 Dashboard
- Visão geral com estatísticas de todos os módulos
- **Alertas de manutenção** em destaque
- Interface responsiva e moderna

## 🚨 Sistema de Alertas de Manutenção

O sistema possui três níveis de alerta baseados na quilometragem:

- 🔴 **ERRO**: Manutenção vencida (KM atual ≥ KM programado)
- 🟡 **AVISO**: Manutenção próxima (faltam ≤ 1000 km)
- ℹ️ **INFO**: Lembrete (faltam ≤ 2000 km)

Os alertas são exibidos automaticamente ao registrar uma viagem com o campo "KM Atual do Veículo" preenchido.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5.3, Font Awesome
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Formulários**: django-crispy-forms + crispy-bootstrap5
- **Autenticação**: Django Auth System

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/euzebionp/controleTrafegoPmnp.git
cd controleTrafegoPmnp
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências**
```bash
cd multas_django
pip install -r requirements.txt
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **(Opcional) Migre dados do sistema legado**
```bash
python manage.py migrate_data
```

8. **Inicie o servidor de desenvolvimento**
```bash
python manage.py runserver
```

9. **Acesse o sistema**
Abra seu navegador e acesse: `http://127.0.0.1:8000`

## 👤 Credenciais Padrão

Se você executou a migração de dados, use:
- **Usuário**: `admin`
- **Senha**: `admin123`

⚠️ **Importante**: Altere a senha padrão em produção!

## 📁 Estrutura do Projeto

```
multas_django/
├── config/                      # Configurações do projeto
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # URLs principais
│   └── wsgi.py                 # WSGI config
├── core/                        # App principal
│   ├── management/
│   │   └── commands/
│   │       └── migrate_data.py # Comando de migração de dados
│   ├── migrations/             # Migrações do banco
│   ├── templates/              # Templates HTML
│   │   ├── base.html          # Template base
│   │   ├── dashboard.html     # Dashboard
│   │   ├── drivers/           # Templates de motoristas
│   │   ├── vehicles/          # Templates de veículos
│   │   ├── travels/           # Templates de viagens
│   │   ├── fines/             # Templates de multas
│   │   ├── maintenance/       # Templates de manutenções
│   │   └── registration/      # Templates de autenticação
│   ├── models.py              # Modelos do banco de dados
│   ├── views.py               # Views (controladores)
│   ├── forms.py               # Formulários customizados
│   ├── signals.py             # Signals para lógica automática
│   ├── apps.py                # Configuração do app
│   └── urls.py                # URLs do app
├── manage.py                   # Script de gerenciamento Django
└── requirements.txt            # Dependências do projeto
```

## 🔐 Autenticação

Todas as páginas do sistema requerem autenticação. Usuários não autenticados são redirecionados para a página de login.

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- 💻 Desktops
- 📱 Tablets
- 📱 Smartphones

## 🚀 Deploy em Produção

### Configurações Importantes

1. **Altere a SECRET_KEY** em `config/settings.py`
2. **Configure DEBUG = False**
3. **Configure ALLOWED_HOSTS** com seu domínio
4. **Use PostgreSQL** ao invés de SQLite
5. **Configure arquivos estáticos**:
```bash
python manage.py collectstatic
```

### Exemplo com PostgreSQL

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seu_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testes

Para executar os testes:
```bash
python manage.py test core
```

## 📝 Comandos Úteis

### Criar migrações após alterar models
```bash
python manage.py makemigrations
```

### Aplicar migrações
```bash
python manage.py migrate
```

### Acessar o shell do Django
```bash
python manage.py shell
```

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Migrar dados do sistema legado
```bash
python manage.py migrate_data
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de uso interno da PMNP.

## 👨‍💻 Autor

**Euzébio NP**
- GitHub: [@euzebionp](https://github.com/euzebionp)

## 📞 Suporte

Para suporte, entre em contato através do GitHub ou abra uma issue no repositório.

---

**Desenvolvido com ❤️ para a PMNP**
