import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WhatsAppMonitor:
    def __init__(self, target_group="Motoristas secretarias de obras"):
        self.target_group = target_group
        self.driver = None
        
    def setup_driver(self):
        """Sets up Chrome Driver with persistent profile."""
        options = Options()
        # Use a user data directory to save session (login)
        user_data_dir = os.path.join(os.getcwd(), "whatsapp_profile")
        options.add_argument(f"user-data-dir={user_data_dir}")
        
        # Additional options for stability
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        
        print("🚀 Iniciando navegador...")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    def start(self, message_handler_callback):
        """
        Starts the monitoring loop.
        :param message_handler_callback: Function to call when a new message is found.
        """
        if not self.driver:
            self.setup_driver()
            
        print("🌐 Abrindo WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")
        
        print("⏳ Aguardando login... (Escaneie o QR Code se necessário)")
        # Wait for chat list to load (indicating login success)
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "pane-side"))
            )
            print("✅ Login detectado!")
        except:
            print("⚠️ Tempo de espera esgotado. Verifique se o login foi feito.")
            # Continue anyway, user might login later
        
        self.find_and_open_group()
        self.monitor_messages(message_handler_callback)
        
    def find_and_open_group(self):
        """Searches and opens the specific group."""
        print(f"🔍 Procurando grupo: '{self.target_group}'...")
        while True:
            try:
                # Try to find group in the list using title attribute
                # This XPath matches span with title='Group Name'
                group_xpath = f"//span[@title='{self.target_group}']"
                group_element = self.driver.find_element(By.XPATH, group_xpath)
                group_element.click()
                print(f"✅ Grupo '{self.target_group}' aberto!")
                break
            except Exception:
                # If not found, maybe scroll or search? 
                # For simplicity, we ask user to ensure group is visible or search manually if needed first time
                # But let's try to simple wait
                print("⏳ Grupo não encontrado na tela visível. Aguardando 5s... (Role a lista se necessário)")
                time.sleep(5)

    def monitor_messages(self, callback):
        """Loop to read new messages."""
        print("👀 Monitorando novas mensagens...")
        processed_messages = set()
        
        while True:
            try:
                # Get all message elements (bubbles)
                # Note: Classes change often. We try a generic approach or common classes.
                # In 2024/2025, message-in typically has 'message-in' class
                messages = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")
                
                for msg in messages[-5:]: # Check only last 5 to be efficient
                    try:
                        text_element = msg.find_element(By.CLASS_NAME, "_11JPr") # Common text class, might need adjustment
                        # Fallback if class changed: try generic span inside
                        # text = msg.text
                    except:
                        # Fallback to getting full text of message div
                        text = msg.text
                        
                    # Use a hash or just text to identify processed
                    # Simple check: if we processed this specific object text content recently
                    # Using (text, timestamp) or just raw text if unique enough
                    
                    if text and text not in processed_messages:
                        print(f"📩 Nova mensagem detectada: {text[:30]}...")
                        callback(text)
                        processed_messages.add(text)
                        
            except Exception as e:
                # print(f"⚠️ Erro no loop de monitoramento: {e}")
                pass
            
            time.sleep(2) # Poll interval

    def close(self):
        if self.driver:
            self.driver.quit()
