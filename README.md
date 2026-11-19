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
git clone <URL-DO-REPOSITORIO>
cd metodos-numericos-2gq
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev,notebook]"
```

## Utilização

```python
from custos_nuvem import carregar_csv, montar_sistema, custos_unitarios

df = carregar_csv("data/consumo_servicos.csv")
A, b = montar_sistema(df, servicos=[...], coluna_total="...")
x = custos_unitarios(A, b)
```

Para rodar o notebook:

```bash
jupyter notebook notebooks/analise_custos.ipynb
```

Para rodar os testes:

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

## Resultados e limitações

_Preencher após rodar o notebook: custos unitários, erros da verificação, custo previsto, serviço escolhido e economia._
