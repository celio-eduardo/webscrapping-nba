from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from salvar_quarto import *

#funções auxiliares

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Função para fechar o popup, se presente
def fechar_popup():
    try:
        # Usar JavaScript para selecionar e clicar no elemento
        driver.execute_script("""
            var modal_close = document.querySelector('#modal-close');
            if (modal_close) {
                modal_close.click();
            } else {
                console.log('Elemento não encontrado');
            }
        """)
        time.sleep(0.25)
    except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException) as e:
        print(f"Popup não encontrado ou não interagível, continuando... Detalhes: {e}")

# Função para fechar o banner de cookies, se presente
def fechar_banner_cookies():
    try:
        # Tentar encontrar o botão de fechar usando XPath com contains
        banner_fechar_botao = driver.find_element(By.XPATH, "//*[contains(@class, 'osano-cm-deny')]")
        banner_fechar_botao.click()
        time.sleep(0.5)
    except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException) as e:
        pass
    
# Função para clicar em um elemento com tratamento de bloqueios
def clicar_elemento(xpath):
    try:
        elemento = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        # Scroll para o elemento
        driver.execute_script("arguments[0].scrollIntoView();", elemento)
        elemento.click()
        time.sleep(2)
    except ElementClickInterceptedException:
        print(f"Elemento bloqueado por outro, tentando fechar banners...")
        fechar_banner_cookies()
        elemento = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView();", elemento)
        elemento.click()
        time.sleep(3)
    except ElementNotInteractableException:
        print(f"Elemento com XPath {xpath} não está interagível.")
    except NoSuchElementException:
        print(f"Elemento com XPath {xpath} não encontrado.")