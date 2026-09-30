# Controle de Peças: Qualidade e Armazenamento

Protótipo em Python desenvolvido para a disciplina Algoritmos e Lógica de Programação (UniFECAF). O programa recebe os dados de cada peça produzida, decide se ela está aprovada ou reprovada, guarda as aprovadas em caixas de 10 unidades e emite um relatório final.

Vídeo de apresentação: COLE_AQUI_O_LINK_DO_VIDEO

## Como funciona

Cada peça tem quatro dados: identificador (ID), peso, cor e comprimento. Ao cadastrar, o programa confere os critérios de qualidade abaixo, com os limites incluídos:

| Critério | Valor aceito |
|---|---|
| Peso | de 95 g a 105 g |
| Cor | azul ou verde |
| Comprimento | de 10 cm a 20 cm |

A peça que cumpre os três critérios fica aprovada. A que falha em algum deles fica reprovada, e o programa guarda todos os motivos, porque uma mesma peça pode falhar em mais de um critério.

As peças aprovadas entram nas caixas na ordem de cadastro, e cada caixa comporta 10 peças. Quando a décima peça entra, a caixa fecha, e a próxima peça aprovada abre uma caixa nova.

O programa calcula as caixas a partir da lista de peças aprovadas a cada consulta. Por isso, ao remover uma peça aprovada, as caixas são reagrupadas sozinhas e a contagem continua coerente com as peças cadastradas. Uma consequência dessa escolha é que, se a peça removida estava em uma caixa já fechada, as aprovadas seguintes avançam para ocupar a vaga.

### Menu

1. **Cadastrar nova peça**: pede identificador, peso, cor e comprimento, valida as entradas e mostra o resultado na hora. Recusa identificador repetido (maiúsculas e minúsculas contam como iguais), texto ou valor menor ou igual a zero nos campos numéricos. Aceita vírgula ou ponto nos decimais.
2. **Listar peças aprovadas/reprovadas**: mostra os dois grupos, com o motivo de cada reprovação.
3. **Remover peça cadastrada**: apaga a peça pelo identificador.
4. **Listar caixas fechadas**: mostra cada caixa completa com os identificadores das peças e avisa quando existe uma caixa em andamento.
5. **Gerar relatório final**: total de aprovadas, total de reprovadas com a contagem por motivo e quantidade de caixas utilizadas.
0. **Sair**.

## Como rodar

1. Instale o Python 3.8 ou superior (https://www.python.org/downloads/). Para conferir a instalação, abra o terminal e digite `python --version`.
2. Baixe o arquivo `controle_pecas.py` deste repositório.
3. No terminal, entre na pasta onde o arquivo está.
4. Execute:

```
python controle_pecas.py
```

Em alguns computadores o comando é `python3 controle_pecas.py`.

O programa usa apenas a biblioteca padrão do Python, então não há nada para instalar. Os dados ficam na memória e somem quando o programa fecha. Para interromper o programa no meio de uma pergunta, use Ctrl+C.

## Exemplos de entradas e saídas

Os exemplos abaixo vêm de uma mesma sessão: P001 aprovada, P002 reprovada, P003 a P011 aprovadas, P012 reprovada por comprimento (96 g, azul, 21 cm) e P013 aprovada.

**Peça aprovada**

```
Escolha uma opção: 1

--- Cadastrar nova peça ---
ID da peça: P001
Peso (g): 100
Cor: Azul
Comprimento (cm): 15
  Peça APROVADA.
```

**Peça reprovada por mais de um motivo**

```
Escolha uma opção: 1

--- Cadastrar nova peça ---
ID da peça: P002
Peso (g): 90
Cor: vermelho
Comprimento (cm): 25
  Peça REPROVADA: peso fora do intervalo (90g); cor não aceita (vermelho); comprimento fora do intervalo (25cm).
```

**Entrada inválida e identificador repetido**

```
Escolha uma opção: 1

--- Cadastrar nova peça ---
ID da peça: P003
Peso (g): abc
  Digite um número válido, por exemplo 100 ou 99,5.
Peso (g): -5
  O valor precisa ser maior que zero.
Peso (g): 100
Cor: verde
Comprimento (cm): 12
  Peça APROVADA.

Escolha uma opção: 1

--- Cadastrar nova peça ---
ID da peça: p001
  Já existe uma peça com esse ID. Cadastro cancelado.
```

**Listagem de peças** (com P001, P002 e P003 cadastradas)

```
--- Peças aprovadas e reprovadas ---

Aprovadas (2):
  ID P001 | 100g | azul | 15cm
  ID P003 | 100g | verde | 12cm

Reprovadas (1):
  ID P002 | 90g | vermelho | 25cm -> peso fora do intervalo (90g); cor não aceita (vermelho); comprimento fora do intervalo (25cm)
```

**Caixa fechada** (ao cadastrar P011, a décima peça aprovada)

```
Escolha uma opção: 1

--- Cadastrar nova peça ---
ID da peça: P011
Peso (g): 100
Cor: verde
Comprimento (cm): 12
  Peça APROVADA.
  Caixa 1 completou 10 peças e foi fechada.
```

**Listagem de caixas** (após cadastrar P013)

```
--- Caixas fechadas ---
  Caixa 1 (10/10): P001, P003, P004, P005, P006, P007, P008, P009, P010, P011
  (Caixa 2 em andamento: 1/10 peças)
```

**Relatório final** (no mesmo momento)

```
=========== RELATÓRIO FINAL ===========
Total de peças cadastradas: 13
Total de peças aprovadas:   11
Total de peças reprovadas:  2

Motivos de reprovação (uma peça pode ter mais de um):
  peso fora do intervalo: 1
  cor não aceita: 1
  comprimento fora do intervalo: 2

Caixas utilizadas: 2
  Fechadas: 1
  Aberta: 1, com 1 de 10 peças
=======================================
```

**Remoção de peça** (P003 removida da sessão acima)

```
Escolha uma opção: 3

--- Remover peça cadastrada ---
ID da peça a remover: P003
  Peça removida. As caixas foram reagrupadas com as aprovadas restantes.

Escolha uma opção: 4

--- Caixas fechadas ---
  Caixa 1 (10/10): P001, P004, P005, P006, P007, P008, P009, P010, P011, P013
```

A Caixa 2 tinha apenas a P013. Sem a P003, restam 10 peças aprovadas, e a P013 sobe para completar a Caixa 1.

## Organização do código

- `avaliar_peca`: aplica os critérios e devolve a lista de motivos de reprovação. Lista vazia significa peça aprovada.
- `montar_caixas`: divide as peças aprovadas em caixas de 10 e devolve as caixas fechadas e a caixa em andamento.
- `buscar_peca`: localiza uma peça pelo identificador.
- `ler_texto` e `ler_numero`: leitura com validação, que repete a pergunta até vir um valor válido.
- Uma função para cada opção do menu, chamadas pelo laço principal em `main` por meio de um dicionário.
- Os limites de qualidade e a capacidade da caixa ficam em constantes no início do arquivo, o que permite mudar uma regra em um só lugar.

## Limitações

Os dados ficam apenas na memória. Em um cenário real, eles seriam gravados em um banco de dados, e as medidas viriam de sensores, sem digitação. Além disso, como as caixas são recalculadas a cada consulta, a remoção de uma peça de uma caixa já fechada reagrupa as aprovadas seguintes, o que não seria possível com uma caixa lacrada de verdade.
