# 🦆 DuckScript Runner para CircuitPython

Execute scripts DuckScript (USB Rubber Ducky) diretamente no seu microcontrolador CircuitPython.  
Com feedback visual por LED, logs completos e suporte a múltiplos layouts de teclado (incluindo ABNT2 brasileiro).

---

## 📦 Conteúdo do repositório

- `code.py` – script principal
- `config.txt` – arquivo de configuração (layout e delay)
- `payload.txt` – exemplo de script DuckScript
- `lib/` – pasta onde você deve instalar as bibliotecas (vazia no repositório)

> **Nota:** As bibliotecas não estão incluídas no repositório. Você deve baixá‑las separadamente (veja abaixo).

---

## 🚀 Instalação passo a passo

### 1. Baixe este repositório

- **Opção 1 (Git):**  
  ```bash
  git clone https://github.com/seu-usuario/ducky-runner-circuitpython.git
  ```


· Opção 2 (ZIP):
    Clique em "Code" → "Download ZIP" e extraia.

2. Prepare sua placa CircuitPython

· Instale o firmware CircuitPython 10.x (se ainda não tiver):
    https://circuitpython.org/downloads
· Conecte a placa ao computador. Ela aparecerá como uma unidade chamada CIRCUITPY.

3. Copie os arquivos do repositório para a placa

Copie os seguintes arquivos para a raiz da unidade CIRCUITPY:

· code.py
· config.txt (edite se necessário – veja seção de configuração)
· payload.txt (ou crie o seu próprio)

4. Instale as bibliotecas necessárias

Você precisará de dois conjuntos de bibliotecas. Ambas devem ser copiadas para a pasta lib/ na raiz do CIRCUITPY.

🔹 Bibliotecas base (Adafruit)

· Baixe o bundle CircuitPython 10.x da Adafruit:
    https://circuitpython.org/libraries
· Extraia o .zip e copie os seguintes itens para lib/ da placa:
  · adafruit_hid/ (pasta inteira)
  · adafruit_ducky.mpy
  · adafruit_logging.mpy

🔹 Bibliotecas de layouts internacionais

· Baixe o bundle de layouts do repositório oficial:
    https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/releases
· Escolha a versão compatível com CircuitPython 10.x (circuitpython-keyboard-layouts-10.x-mpy-YYYYMMDD.zip).
· Extraia e copie os arquivos relativos ao seu layout para lib/ da placa.
    Exemplo para português brasileiro (ABNT2):
  · keyboard_layout_win_br.mpy
  · keycode_win_br.mpy

Se precisar de outro idioma (espanhol, francês, alemão…), copie o par correspondente.

5. Configure o layout e o delay

Edite o arquivo config.txt (já copiado para a placa). Exemplo de conteúdo:

```
keyboard_layout_win_br
3000
```

· Linha 1: nome do layout (sem a extensão .mpy). Valores comuns:
  · keyboard_layout_us (padrão, sem acentos)
  · keyboard_layout_win_br (ABNT2)
  · keyboard_layout_win_es (espanhol)
  · keyboard_layout_win_fr (francês)
· Linha 2: delay inicial em milissegundos antes da execução (recomendado: 2000 a 5000).

6. Crie ou edite o script DuckScript

O arquivo payload.txt deve conter os comandos no formato DuckScript. Exemplo:

```ducky
DELAY 3000
STRING Olá mundo com acentuação!
ENTER
STRING Teste de ç, ã, é, í, ó, ú
ENTER
```

Comandos suportados: DELAY, STRING, ENTER, GUI, CTRL, ALT, SHIFT, WINDOWS, MENU, setas, etc.
Consulte a documentação do DuckScript para mais detalhes.

---

▶️ Executando

1. Conecte a placa ao computador ou dispositivo alvo.
2. Aguarde alguns segundos (respeitando o delay configurado).
3. O script será executado automaticamente.

Feedback do LED

· Pisca 2 vezes → início da execução
· LED aceso → durante a execução de cada linha
· Pisca 5 vezes rápido → erro em alguma linha
· Pisca 3 vezes → fim da execução (sucesso)

Logs

Após a execução, você pode ler o arquivo execution_log.txt na raiz da placa. Ele contém:

· Data/hora de cada evento
· Linhas executadas com sucesso
· Erros (com número da linha)
· Resumo total de linhas

Também é possível acompanhar os logs ao vivo via console serial (115200 baud).

---

🛠️ Resolução de problemas

Problema Possível solução
Acentos saem errados Verifique se os arquivos do layout (keyboard_layout_win_br.mpy e keycode_win_br.mpy) estão em lib/ e se o config.txt aponta para o layout correto.
LED não pisca Sua placa pode não ter LED onboard. Altere o código para usar um pino GPIO externo (ex: board.GP25).
Erro ImportError Confirme que todas as bibliotecas foram copiadas para a pasta lib/ e que a versão do bundle corresponde ao firmware (10.x).
Nada é digitado Aumente o delay inicial no config.txt (ex: 5000). Verifique se a placa está conectada em uma porta USB que suporte HID.

---

🔗 Links úteis

· Baixar firmware CircuitPython
· Bibliotecas Adafruit (bundle 10.x)
· Bibliotecas de layouts internacionais
· Documentação DuckScript

---

📜 Licença

MIT License. Livre para usar, modificar e distribuir.
