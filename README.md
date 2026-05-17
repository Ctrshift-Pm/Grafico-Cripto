# 📊 Dominância Cripto - Dashboard Desktop Real-Time

Um aplicativo desktop standalone moderno, de alta performance, desenvolvido em Python. Ele calcula e visualiza a dominância real das 5 categorias mais importantes do mercado de criptomoedas em tempo real, integrando-se diretamente à API da CoinGecko e gerando um gráfico de rosca (Donut Chart) de alto impacto estético.

---

## 📸 Interface e Design

A interface gráfica foi desenhada seguindo os princípios de design minimalista:
*   **Tema **: Fundo preto absoluto (`#000000`), cartões e elementos estruturais no tom de cinza escuro (`#0A0A0A`), com linhas divisórias de extrema sutileza (`#1C1C1E`).
*   **Donut Chart Simétrico**: Gráfico de rosca elegante com separador preto generoso de `8px` entre as fatias.
*   **Logotipos Embutidos (Originais & Transparentes)**: Os ícones originais e crus de cada ativo flutuam diretamente sobre suas respectivas fatias.
    *   **Aspect Ratio Perfeito**: Imagens redimensionadas sem achatamento ou distorções, usando o algoritmo de escala proporcional `.thumbnail` do PIL.
    *   **Destaque do OTHERS.D**: O ícone do segmento "OTHERS" foi ampliado para o tamanho máximo de **`48px`** (mesmo destaque do Bitcoin!), realçando a marca de forma espetacular.
*   **Responsividade Real e Footer Fixo**: O aplicativo se adapta perfeitamente a redimensionamentos verticais e horizontais. A barra de título superior e o rodapé com o status e botão de atualização são ancorados de forma rígida, de modo que **nunca desaparecem ou são cropados verticalmente**.

---

## 💎 Os 5 Segmentos de Mercado Precisos

Diferente de visualizações genéricas de dominância, este sistema divide o mercado em 5 pilares cirúrgicos:

1.  **Bitcoin (BTC.D)**: O percentual de dominância real extraído diretamente da API.
2.  **Ethereum (ETH.D)**: O percentual de dominância real do maior ecossistema de Smart Contracts.
3.  **Stablecoins (USDT, USDC, DAI, etc.)**: O porto seguro de liquidez do mercado. Agrupa e soma de forma dinâmica a fatia de todas as stablecoins principais.
4.  **Top 10 Altcoins (BNB, SOL, XRP, ADA, DOGE, etc.)**: A força motriz das altcoins de maior cap. Soma a dominância dos maiores projetos de utilidade do mercado cripto.
5.  **OTHERS.D (Cauda Longa / Resto do Mercado)**: O resíduo exato e real do mercado global. Abrange as mais de 14.000 micro-caps ativas na blockchain (calculado de forma matemática ultra-precisa como: $100\% - BTC - ETH - Stablecoins - Top10Alts$).

---

## 🚀 Como Executar o Projeto em Desenvolvimento

### Requisitos Prévios
*   Python 3.10 ou superior instalado.
*   Bibliotecas do sistema operacional para suporte gráfico (instalado por padrão no Windows).

### Passo 1: Clonar o Repositório e Instalar Dependências
No seu shell/terminal, execute:
```bash
pip install -r requirements.txt
```
*(As dependências principais são: `requests`, `pillow` (PIL), `matplotlib` e `pyinstaller`).*

### Passo 2: Executar o Aplicativo
Inicie a aplicação executando o arquivo principal:
```bash
python main.py
```

### Passo 3: Executar a Suíte de Testes
Para rodar a suite completa de testes automatizados unitários e de integração (que executa 100% offline em menos de 0.4 segundos usando mocks):
```bash
python -m unittest tests/test_crypto_dominance.py
```

---

## 📦 Compilando um Executável Standalone (.exe) no Windows

O projeto acompanha um script automatizado de empacotamento (`build_exe.py`). Para gerar o seu executável nativo do Windows que abre com clique duplo diretamente na GUI (sem abrir telas pretas de terminal de comando):

Execute no PowerShell ou CMD na raiz do projeto:
```powershell
python build_exe.py
```

### O que o Auto-Builder faz por baixo dos panos?
1.  **Geração do Ícone de Alta Qualidade**: Converte o logotipo original do Bitcoin da pasta `images/` em um arquivo multi-resolução de ícone do Windows (`images/icon.ico`).
2.  **Compilação via PyInstaller**: Empacota todo o código, imagens e dependências em um único arquivo standalone leve no diretório `dist/DominanciaCripto.exe`.
3.  **Criação de Atalho Resiliente**: Cria de forma totalmente automatizada um atalho chamado **`Dominancia Cripto.lnk`** na sua **Área de Trabalho (Desktop)** que aponta para o binário compilado.

### Metadados do executável
O build do Windows agora injeta metadados de versão no `.exe`, incluindo:
*   **Fornecedor/CompanyName**: `Pedro Matheus Chaves de Freitas`
*   **Nome do produto/ProductName**: `Dominância Cripto`
*   **Descrição do arquivo/FileDescription**: Dashboard desktop de dominância do mercado cripto em tempo real
*   **Versão**: `1.0.0.0`

Esses dados melhoram a apresentação na aba **Propriedades > Detalhes** do Windows, mas não substituem assinatura digital de código.

### Para parecer confiável ao Windows de verdade
Para deixar de aparecer como **Unknown Publisher** ou reduzir alertas do SmartScreen, o caminho correto é:
1.  Assinar o `.exe` com um certificado de code signing.
2.  Publicar versões consistentes com o mesmo nome, produto e certificado.
3.  Considerar distribuição via Microsoft Store ou serviço de assinatura confiável da Microsoft.

---

## 🛡️ Estrutura do Código-Fonte

*   [main.py](file:///c:/Users/NathanG/Pictures/raber/main.py): Ponto de entrada do software. Configura o Logger e inicia a interface gráfica.
*   [gui.py](file:///c:/Users/NathanG/Pictures/raber/gui.py): Camada de interface gráfica Tkinter e layout responsivo Apple Pro. Trata do cronômetro fluído e atualizações em segundo plano.
*   [api/coingecko.py](file:///c:/Users/NathanG/Pictures/raber/api/coingecko.py): Responsável pela comunicação assíncrona, robusta e segura com a API REST da CoinGecko.
*   [utils/calculations.py](file:///c:/Users/NathanG/Pictures/raber/utils/calculations.py): Motor matemático encarregado de classificar, agrupar e deduzir os 5 segmentos de mercado sem renormalizações artificiais.
*   [charts/pie_chart.py](file:///c:/Users/NathanG/Pictures/raber/charts/pie_chart.py): Constrói o Donut Chart premium com os ícones transparentes e alinhados simetricamente no centro do anel.
*   [build_exe.py](file:///c:/Users/NathanG/Pictures/raber/build_exe.py): Script de empacotamento, compilação de ícones e criação automática de atalhos no Desktop.
*   [tests/test_crypto_dominance.py](file:///c:/Users/NathanG/Pictures/raber/tests/test_crypto_dominance.py): Suíte completa de testes de cobertura.
