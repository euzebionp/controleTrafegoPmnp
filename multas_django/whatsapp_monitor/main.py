import sys
from bot import WhatsAppMonitor
from parser import parse_message
from exporter import save_to_excel

def handle_new_message(text):
    """
    Callback function to process new messages found by the bot.
    """
    print(f"🔄 Processando mensagem...")
    
    # 1. Parse Data
    data = parse_message(text)
    
    if data:
        print(f"✅ Dados extraídos: {data}")
        # 2. Export to Excel
        save_to_excel([data])
    else:
        print("ℹ️ Mensagem ignorada (não corresponde ao padrão de viagem).")
        # Optional: Log ignored message to error log
        # with open("ignored_log.txt", "a", encoding="utf-8") as f:
        #     f.write(f"IGNORED: {text}\n---\n")

def main():
    print("🤖 WhatsApp Monitor - Motoristas")
    print("---------------------------------")
    
    try:
        # Create Monitor Instance
        monitor = WhatsAppMonitor(target_group="Motoristas secretarias de obras")
        
        # Start Monitoring with Callback
        monitor.start(handle_new_message)
        
    except KeyboardInterrupt:
        print("\n🛑 Encerrando monitoramento...")
        if 'monitor' in locals():
            monitor.close()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
