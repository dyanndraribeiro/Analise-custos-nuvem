# Projeto Métodos Numéricos 2ºGQ — Problema 1: Análise de Custos de Serviços em Nuvem

Aplicação de métodos numéricos (sistemas de equações lineares) para determinar o custo unitário de cinco serviços de computação em nuvem a partir de cinco meses de consumo e faturamento, verificar os resultados, prever o custo do próximo mês e estimar economias.

**Grupo:** Dyanndra, Gilberto, Crystal, Eduardo e Guilherme.

## Modelagem

Cada mês gera uma equação: soma de (quantidade consumida × custo unitário) = total pago. Com 5 meses e 5 serviços obtemos um sistema linear 5×5, `A·x = b`, em que `A` guarda as quantidades, `x` os custos unitários e `b` os totais mensais.

## Estrutura

```
src/custos_nuvem/
    linear_systems.py   # Gauss com pivoteamento parcial e decomposição LU
    analise.py          # itens (a) a (d) do problema
    dados.py            # leitura dos CSVs
tests/                  # testes automatizados (pytest)
notebooks/              # notebook que usa o pacote para resolver o problema
data/                   # consumo_servicos.csv e previsao.csv
```

Os métodos numéricos são implementados no pacote, sem funções prontas que resolvam diretamente os sistemas. O notebook apenas importa e utiliza essas funções.

## Instalação

Requer Python 3.9 ou superior.

```bash
git clone https://github.com/dyanndraribeiro/Analise-custos-nuvem.git
cd Analise-custos-nuvem
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev,notebook]"
```

> **Problemas na instalação?** Em versões muito novas do Python (ex.: 3.15) no Windows, o `pip` pode falhar ao compilar o `pyyaml`, uma dependência do Jupyter. Nesse caso, instale apenas o necessário (`pip install -e ".[dev]"` e `pip install ipykernel`) ou use o Python 3.13. As únicas dependências do próprio pacote são `numpy` e `pandas`.

## Utilização

```python
from custos_nuvem import (
    carregar_csv, vetor_previsao, montar_sistema,
    custos_unitarios, custo_previsto, melhor_reducao,
)

SERVICOS = ["cpu_horas", "armazenamento_tb", "banco_horas",
            "transferencia_gb", "funcoes_mil"]

consumo = carregar_csv("data/consumo_servicos.csv")
previsao = carregar_csv("data/previsao.csv")

A, b = montar_sistema(consumo, SERVICOS, coluna_total="custo_total")
x = custos_unitarios(A, b)                      # (a) Gauss com pivoteamento parcial

q = vetor_previsao(previsao, SERVICOS)
print(custo_previsto(q, x))                     # (c) 2371.0
print(melhor_reducao(q, x, SERVICOS)["servico"])  # (d) armazenamento_tb
```

Para rodar o notebook:

```bash
jupyter notebook notebooks/analise_custos.ipynb
```

Para rodar os testes (15 testes: solver, verificação dos totais, previsão e economia):

```bash
pytest
```

## Divisão do trabalho

| Integrante | Parte |
|---|---|
| Dyanndra | Estrutura do repositório, README, integração e apresentação |
| Gilberto | Solver de sistemas lineares (`linear_systems.py`) e item (a) |
| Crystal | Verificação dos totais (item b) e testes |
| Eduardo | Previsão e economia (itens c e d) |
| Guilherme | Notebook, interpretações e limitações |

## Resultados

Custos unitários (item a), obtidos por eliminação de Gauss com pivoteamento parcial (conferidos com LU):

| Serviço | Custo unitário |
|---|---|
| CPU (hora) | 2,50 |
| Armazenamento (TB) | 15,00 |
| Banco de dados (hora) | 4,00 |
| Transferência (GB) | 0,80 |
| Funções (mil) | 1,50 |

- **(b)** Os totais recalculados reproduzem os cinco valores originais (1255, 1479, 1695, 1881 e 2060), com erro zero.
- **(c)** Custo total previsto para o mês 6: **2371,00**.
- **(d)** Reduzir 20% do armazenamento dá a maior economia: **135,00 por mês**, novo custo total **2236,00**, e **1620,00** em 12 meses.

## Escolha dos métodos

O sistema é pequeno (5×5) e denso, então usamos um **método direto**: eliminação de Gauss com pivoteamento parcial, que escolhe como pivô o maior elemento em módulo da coluna e evita dividir por valores pequenos. A decomposição LU (também com pivoteamento) serve como conferência e dá o mesmo resultado, com diferença da ordem de 1e-15.

Métodos iterativos como Jacobi e Gauss-Seidel **não são adequados** aqui: a matriz não é diagonalmente dominante em nenhuma linha (por exemplo, na linha 1 o elemento da diagonal é 100, mas a soma dos demais é 450), então a convergência não é garantida.

## Limitações

- **Arredondamento em ponto flutuante:** os custos saem com erro da ordem de 1e-15 (por exemplo, 2,5000000000000027 em vez de 2,5). Os valores foram arredondados na apresentação, e o resíduo `|A·x − b|` é praticamente nulo.
- **Condicionamento:** o número de condição da matriz (norma infinito) é cerca de **330**. Isso significa que erros relativos nos totais faturados podem ser amplificados em até ~330 vezes nos custos unitários. Com dados exatos isso não aparece, mas com faturas reais, que têm arredondamento, apareceria.
- **Sem folga estatística:** são 5 equações para 5 incógnitas, então a solução reproduz os totais por construção. Bater com os dados originais não prova que o modelo está certo. Com mais meses de dados, um ajuste por mínimos quadrados permitiria validar o modelo.
- **Modelo linear com preço constante:** assume que cada serviço tem custo unitário fixo, sem descontos por volume, faixas de preço ou taxas fixas.
- **Previsão e economia:** o custo do mês 6 depende de `previsao.csv`, e o modelo só converte consumo em custo. A economia de 12 meses supõe consumo constante, como pede o enunciado. Como o consumo vem crescendo, a economia real tenderia a ser maior.
