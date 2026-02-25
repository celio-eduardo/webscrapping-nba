from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from jogadores_dados import *

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

# Função para extrair informações de um jogador
def extrair_informacoes_jogador(url_jogador):
    driver.get(url_jogador)
    
    time.sleep(0.25)  # Esperar a página carregar
    
    # Fechar o popup e o banner de cookies, se presente
    fechar_popup()
    fechar_banner_cookies()

    # Sucessão de cliques
    try:
        # Verificar se o link "Game Log" está presente
        try:
            primeiro_botao = WebDriverWait(driver, 0.75).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="tfooter_last5"]/p/a[3]'))
            )
            primeiro_botao.click()
            time.sleep(0.5)  # Esperar a página carregar ou o estado mudar
        except TimeoutException:
            print("Link 'Game Log' não encontrado, gerando CSV com cabeçalho padrão...")
            print(link)
            # Nome do jogador
            # Verificar se o jogador tem foto
            try:
                driver.find_element(By.CLASS_NAME, 'media-item')
                # Se o jogador tem foto
                elemento_jogador = driver.find_element(By.XPATH, '//*[@id="meta"]/div[2]/h1/span')
            except NoSuchElementException:
                # Se o jogador não tem foto
                elemento_jogador = driver.find_element(By.XPATH, '//*[@id="meta"]/div/h1/span')
            except Exception as e:
                # Retorna outras exceções não especificadas
                print('Não passou da parte Game Log')
                print(link)
                driver.quit()
                raise e
            
            #Extrair o texto do elemento
            nome_jogador = elemento_jogador.text.split(' 2024-25')[0]
            
            # Extrair o texto do elemento da equipe
            try:
                elemento_equipe_pai = driver.find_element(By.XPATH, '//p[strong[text()="Team"]]')
                elemento_equipe = elemento_equipe_pai.find_element(By.TAG_NAME, 'a')
                nome_equipe = elemento_equipe.text
            except NoSuchElementException:
                print("Elemento da equipe não encontrado")
            except Exception as e:
                # Retorna outras exceções não especificadas
                print('Não conseguiu extrair o nome do time corretamente')
                print(link)
                driver.quit()
                raise e
            
            diretorio_base = f'C:\\Users\\SuperUser\\Documents\\Workspace\\Basquete Análise de Dados\\Times'
            gerar_csv_padrao(nome_equipe, nome_jogador, diretorio_base)
            
            return
        
        # Fechar o popup, se presente
        fechar_popup()
        
        # Verificar se o botão para expandir a biografia está presente
        try:
            expandir_biografia = driver.find_element(By.XPATH, '//*[@id="meta_more_button"]')
            expandir_biografia.click()
            time.sleep(0.25)  # Esperar a página carregar ou o estado mudar
        except NoSuchElementException:
            pass
        except Exception as e:
            # Retorna outras exceções não especificadas
            print('Problemas com a expansão da biografia')
            print(link)
            driver.quit()
            raise e
        
        # Acionar o hover para abrir as opções de exportação"
        try:
            elemento_hover = driver.find_element(By.XPATH, '//*[@id="pgl_basic_sh"]/div/ul/li[1]')  # Elemento específico que queremos acionar
            acao = ActionChains(driver)
            acao.move_to_element(elemento_hover).perform()
            time.sleep(0.25)  # Esperar o menu aparecer
        except Exception as e:
            print('Problema com o botão do Hover que abre as opções da tabela de dados')
            print(link)
            driver.quit()
            raise e
        
        #Clicar no botão de Get table as CSV (for Excel)
        try:
            botao_csv = driver.find_element(By.XPATH, '//*[@id="pgl_basic_sh"]/div/ul/li[1]/div/ul/li[3]/button')
            botao_csv.click()
            time.sleep(0.25)  # Esperar a ação do clique
        except Exception as e:
            print('Problema ao clicar no botão de Geração do CSV')
            print(link)
            driver.quit()
            raise e
        
        # Pega o nome do jogador
        # Verifica se o jogador tem foto
        try:
            driver.find_element(By.CLASS_NAME, 'media-item')
            # Se o jogador tem foto
            elemento_jogador = driver.find_element(By.XPATH, '//*[@id="meta"]/div[2]/h1/span')
        except NoSuchElementException:
            # Se o jogador não tem foto
            elemento_jogador = driver.find_element(By.XPATH, '//*[@id="meta"]/div/h1/span')
        except Exception as e:
            print('Problema ao acessar o nome do jogador')
            print(link)
            driver.quit()
            raise e

        # Variável que guarda o nome do jogador
        nome_jogador = elemento_jogador.text.split(' 2024-25')[0]
        
        # Pega o nome da equipe
        try:
            elemento_equipe_pai = driver.find_element(By.XPATH, '//p[strong[text()="Team"]]')
            elemento_equipe = elemento_equipe_pai.find_element(By.TAG_NAME, 'a')
            nome_equipe = elemento_equipe.text
        except NoSuchElementException:
            print("Elemento da equipe não encontrado")
            print(link)
            driver.quit()
        except Exception as e:
            print('Problema ao tentar acessar o nome da equipe')
            print(link)
            driver.quit()
            raise e
    
        try:
            # Extrair dados do elemento correto
            elemento_dados = driver.find_element(By.ID, 'csv_pgl_basic')
            dados = elemento_dados.text
        except Exception as e:
            print('Problema ao acessar os dados em CSV disponibilizados pelo site')
            print(link)
            driver.quit()
            raise e
        
        #diretorio raiz principal
        diretorio_base = f'C:\\Users\\SuperUser\\Documents\\Workspace\\Basquete Análise de Dados\\Times'
        
        #rotina para salvar os arquivos obtidos
        processar_arquivos_xls(nome_jogador, nome_equipe, dados, diretorio_base)
        
    except Exception as e:
        print(f"Erro ao realizar a sucessão de cliques: {e}")
        print(link)
        driver.quit()

#retorna uma lista com todos os jogadores do time
def programa_hum(url_time):
    driver.get(url_time)

    # Esperar a página carregar
    time.sleep(0.25)

    # Fechar o banner de cookies, se presente
    fechar_banner_cookies()
    
    
    try:
        # Encontrar todas as linhas da tabela de jogadores
        rows = driver.find_elements(By.XPATH, '//*[@id="roster"]/tbody/tr')
    except Exception as e:
        print(f"Erro ao acessar a tabela de jogadores da equipe")
        print(url_time)
        driver.quit()

    # Iterar sobre cada linha e extrair o link do jogador
    player_links = []
    for row in rows:
        try:
            link_element = row.find_element(By.XPATH, './td[1]/a')
            link = link_element.get_attribute('href')
            player_links.append(link)
        except Exception as e:
            print(f"Erro ao extrair link da linha: {e}")
            driver.quit()
    
    return player_links

#inicio do programa hum  
with open('faltantes_hoje.txt', 'r') as file:
    input_data = file.read().split('\n')
    for links in input_data:
        # Configurar o ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        player_links = programa_hum(links)
        for link in player_links:
            extrair_informacoes_jogador(link)
        driver.quit()

'''player_links = programa_hum('https://www.basketball-reference.com/teams/NYK/2025.html')
for link in player_links:
    extrair_informacoes_jogador(link)
driver.quit()'''
