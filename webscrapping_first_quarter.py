from auxiliar_geral import *

# Função para extrair informações das partidas
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

#retorna uma lista com todos os jogos a serem consultados
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
mes_atual = 'march'

#inicio do programa
pagina_inicial = 'https://www.basketball-reference.com/'
driver.get(pagina_inicial)
botao_calendario = driver.find_element(By.XPATH, '//*[@id="teams"]/p[1]/small/a[2]')
botao_calendario.click()
# Procura o link do mês atual dentro da div com a classe 'filter'
div_meses = driver.find_element(By.CLASS_NAME, 'filter')
link_mes_atual = div_meses.find_element(By.XPATH, f".//a[contains(@href, '{mes_atual}')]")
link_mes_atual.click()
tabela_inteira = driver.find_element(By.XPATH, '//*[@id="div_schedule"]')

# Acionar o hover para abrir as opções de exportação"
try:
    elemento_hover = driver.find_element(By.XPATH, '//*[@id="schedule_sh"]/div/ul/li/span')  # Elemento específico que queremos acionar
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
    botao_csv = driver.find_element(By.XPATH, '//*[@id="schedule_sh"]/div/ul/li/div/ul/li[3]/button')
    botao_csv.click()
    time.sleep(0.25)  # Esperar a ação do clique
except Exception as e:
    print('Problema ao clicar no botão de Geração do CSV')
    print(link)
    driver.quit()
    raise e
        



player_links.append(link)


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

