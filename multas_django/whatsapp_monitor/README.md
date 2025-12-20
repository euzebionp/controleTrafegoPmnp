# 🤖 Monitor de WhatsApp - Motoristas

Este script automatiza o monitoramento de um grupo do WhatsApp ("Motoristas secretarias de obras"), extrai informações de viagens (Nome, Placa, KM) e salva em uma planilha Excel.

## 📋 Pré-requisitos

1.  Python 3.8 ou superior instalado.
2.  Google Chrome instalado.

## 🚀 Instalação

1.  Abra o terminal na pasta do projeto:
    ```bash
    cd whatsapp_monitor
    ```

2.  Instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Como Rodar

1.  Execute o script principal:
    ```bash
    python main.py
    ```

2.  **Primeira vez**: O navegador Chrome irá abrir. Se necessário, escaneie o QR Code do WhatsApp Web.
    *   *Nota: O login ficará salvo na pasta `whatsapp_profile` para as próximas vezes.*

3.  **Funcionamento**:
    *   O robô irá procurar o grupo "Motoristas secretarias de obras".
    *   Ele ficará "escutando" novas mensagens.
    *   Quando encontrar uma mensagem no padrão correto, os dados serão salvos no arquivo `dados_extraidos.xlsx` na mesma pasta.

## 📝 Formato da Mensagem Esperado

O robô procura por mensagens contendo "Registro de Viagem" e campos como:
```text
📄 Registro de Viagem
Nome: [Nome]
Placa: [Placa]
Km Inicial: [valor]
Destino: [Destino]
Km final: [valor]
```

## ⚠️ Solução de Problemas

*   **Grupo não encontrado**: Se o robô não clicar no grupo, certifique-se de que o grupo está visível na lista de conversas (role para cima se necessário) ou que o nome está exatamente igual a "Motoristas secretarias de obras".
*   **Erro de Driver**: Se o Chrome não abrir, verifique se o seu Google Chrome está atualizado. O `webdriver-manager` deve baixar a versão correta automaticamente.
