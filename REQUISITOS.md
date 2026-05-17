# 📋 Requisitos do Sistema - Dominância Cripto

Este documento detalha todos os requisitos funcionais, não-funcionais, especificações técnicas, dependências externas e ativos gráficos que constituem o aplicativo desktop de **Dominância Cripto**.

---

## 🛠️ 1. Requisitos Funcionais (RF)

*   **RF01 - Consulta de Dados Globais**: O sistema deve buscar em tempo real os dados globais de capitalização de mercado e dominâncias a partir do endpoint `/global` oficial da API CoinGecko.
*   **RF02 - Agrupamento e Dedução de 5 Segmentos**: O sistema deve processar o payload JSON bruto da API e segmentar a dominância de mercado nas seguintes 5 categorias:
    1.  *Bitcoin (BTC.D)*
    2.  *Ethereum (ETH.D)*
    3.  *Stablecoins (soma das dominâncias individuais das stablecoins conhecidas)*
    4.  *Top 10 Altcoins (soma das altcoins mais representativas no topo)*
    5.  *OTHERS.D (resto do mercado menor, deduzido via subtração: $100 - BTC - ETH - Stablecoins - Top10Alts$)*
*   **RF03 - Donut Chart Interativo**: O sistema deve gerar dinamicamente um gráfico de rosca (donut chart) com fatias coloridas, rótulos textuais indicando nome e porcentagem precisa, e anel central escuro limpo (sem textos ou distorções).
*   **RF04 - Logotipos Embutidos Simétricos**: O sistema deve embutir os logotipos originais e transparentes de cada categoria diretamente sobre a área correspondente do gráfico de rosca, centralizados no raio `0.68` e mantendo a proporção de aspecto nativa (sem achatamento).
*   **RF05 - Cronômetro de Atualização (Countdown)**: O sistema deve exibir um cronômetro regressivo no rodapé indicando os segundos restantes para a próxima atualização automática.
*   **RF06 - Botão de Atualização Manual**: A interface gráfica deve conter um botão "Atualizar" que força uma nova consulta imediata à API, zerando o contador de tempo.
*   **RF07 - Cards Laterais**: A sidebar à direita do gráfico deve exibir a listagem completa dos 5 segmentos de forma estruturada, com cartões estilizados, cores representativas, valores precisos e nomes de cada categoria.
*   **RF08 - Tratamento de Erros e Cache**: Se a conexão com a API falhar ou ocorrer rate limiting, o sistema deve registrar a falha amigavelmente no status da interface e manter em exibição o último gráfico válido sem interromper a execução do aplicativo.

---

## 🚀 2. Requisitos Não-Funcionais (RNF)

*   **RNF01 - Responsividade e Fixed-Footer**: O layout deve ser flexível para que apenas a área do gráfico e dos cards laterais seja encolhida em caso de redimensionamento da janela. O título do cabeçalho e o rodapé de controle devem permanecer fixados e totalmente visíveis sob qualquer resolução a partir de `900x600`.
*   **RNF02 - Performance Gráfica**: A geração de gráficos deve operar 100% em memória RAM (canvas dinâmico). O Matplotlib não deve realizar gravações físicas de arquivos de imagem no HD/SSD a cada atualização, otimizando drasticamente a velocidade e vida útil do hardware.
*   **RNF03 - Controle de Rate Limit da API**: Para evitar o erro `429 Too Many Requests` (bloqueios de IP pela CoinGecko), as requisições automáticas do aplicativo em segundo plano devem respeitar o limite de segurança de 60 segundos por tick de atualização real de dados.
*   **RNF04 - Standalone e Portabilidade**: O aplicativo deve ser empacotado em um único arquivo executável standalone (`.exe` de ~30MB) que execute no Windows sem a necessidade de instalar Python, interpretadores ou bibliotecas externas de forma nativa.

---

## 📦 3. Pilha Tecnológica e Dependências

A aplicação foi estruturada usando a seguinte stack estável:
1.  **Linguagem Core**: Python 3.10 ou superior.
2.  **Interface Gráfica (GUI)**: `tkinter` (Nativo do Python).
3.  **Visualização Gráfica**: `matplotlib` (Para renderização matemática das fatias).
4.  **Processamento de Imagem**: `pillow` (PIL - Para leitura e redimensionamento proporcional dos logotipos).
5.  **Comunicação de Rede**: `requests` (Para consumo assíncrono da API REST da CoinGecko).
6.  **Empacotamento de Binário**: `pyinstaller` (Para compilar o script Python em executável nativo Windows).

### Lista de Dependências (`requirements.txt`):
```text
requests>=2.31.0
pillow>=10.1.0
matplotlib>=3.8.0
pyinstaller>=6.2.0
```

---

## 📂 4. Diretório de Ativos Gráficos (Imagens)

O sistema depende de uma estrutura de arquivos de imagem local para o carregamento dos logotipos. Os arquivos devem estar localizados no diretório `/images` na raiz do projeto:

| Nome do Arquivo | Segmento Relacionado | Formato Necessário |
| :--- | :--- | :--- |
| `bitcoin.png` | Bitcoin (BTC.D) | PNG Transparente (RGB/RGBA) |
| `ethereum.png` | Ethereum (ETH.D) | PNG Transparente (RGB/RGBA) |
| `tether.png` | Stablecoins | PNG Transparente (RGB/RGBA) |
| `doge.png` | Top 10 Altcoins | PNG Transparente (RGB/RGBA) |
| `others.svg` | OTHERS.D | SVG |

---

## 🛡️ 5. Limites e Regras de Segurança Operacional
*   **Timeouts de Rede**: Todas as conexões HTTP para a API CoinGecko devem possuir limites de timeout rígidos de `15 segundos` para evitar travamentos da interface em conexões de internet instáveis.
*   **Tratamento de Threads**: As requisições HTTP da API CoinGecko devem ser executadas em uma `Thread` em segundo plano assíncrona, impedindo que a janela gráfica da GUI do usuário congele ou apresente comportamento de "Não respondendo" durante a busca por dados.
