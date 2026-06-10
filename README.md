# SAD — Análise de Riscos em Investimentos com Análise de Sensibilidade

**Disciplina:** Sistemas de Apoio à Decisão (DCC166) — UFJF  
**Atividade:** TVC 2 — Trabalho de Verificação de Conhecimento  
**Problema:** 13 — Análise de Riscos em Investimentos (Análise de Sensibilidade)  
**Ano/Semestre:** 2026.1

---

## Objetivo

Desenvolver um Sistema de Apoio à Decisão (SAD) para análise de risco de um portfólio de investimentos, permitindo simular diferentes cenários de oscilação de mercado e avaliar o impacto no valor total da carteira, no retorno esperado, no risco e na alocação dos ativos.

---

## Estrutura do Projeto

```
tvc2 - SAD Análise de Riscos em Investimentos/
│
├── app.py                        # Aplicação Streamlit principal
├── requirements.txt              # Dependências Python
├── README.md                     # Este arquivo
├── dados/
│   └── portfolio_simulado.csv    # Base de dados simulada do portfólio
├── relatorio/
│   └── relatorio_sbc.tex         # Relatório acadêmico no formato SBC
├── imagens/
│   └── graficos_gerados.png      # Gráficos exportados pelo sistema
└── docs/
    └── explicacao_modelo.md      # Documentação técnica do modelo
```

---

## Como Instalar as Dependências

Certifique-se de ter o Python 3.10+ instalado. No terminal, na pasta do projeto, execute:

```bash
pip install -r requirements.txt
```

---

## Como Executar o Sistema

```bash
python -m streamlit run app.py
```

O sistema abrirá automaticamente no navegador padrão, geralmente em `http://localhost:8501`.

> **Nota:** Use `python -m streamlit` em vez de apenas `streamlit` caso o comando não seja
> reconhecido no terminal — isso acontece quando o executável não foi adicionado ao PATH do sistema.

---

## Cenários de Análise de Sensibilidade

| Cenário            | Variação |
|--------------------|----------|
| Queda Forte        | −20%     |
| Queda Moderada     | −10%     |
| Queda Leve         | −5%      |
| Neutro             | 0%       |
| Alta Leve          | +5%      |
| Alta Moderada      | +10%     |
| Alta Forte         | +20%     |

Além dos cenários predefinidos, o usuário pode ajustar manualmente a variação de −30% a +30% usando o slider na barra lateral.

---

## Composição da Carteira Simulada

| Ativo         | Classe             | Perfil de Risco |
|---------------|--------------------|-----------------|
| PETR4         | Ação               | Alto            |
| VALE3         | Ação               | Alto            |
| ITUB4         | Ação               | Médio           |
| BBDC4         | Ação               | Médio           |
| MGLU3         | Ação               | Alto            |
| TESOURO_SELIC | Renda Fixa         | Baixo           |
| HGLG11        | Fundo Imobiliário  | Médio           |
| XPML11        | Fundo Imobiliário  | Médio           |

---

## Como Interpretar os Gráficos

- **Gráfico de pizza:** mostra a distribuição percentual do portfólio entre os ativos.
- **Barras comparativas:** permite visualizar o valor de cada ativo antes e após a simulação.
- **Impacto financeiro:** exibe o ganho ou perda em reais para cada ativo no cenário escolhido.
- **Curva de sensibilidade:** mostra como o valor total do portfólio varia conforme a oscilação de mercado de −30% a +30%.

---

## Como o Sistema Apoia a Tomada de Decisão

O sistema gera automaticamente recomendações baseadas nos resultados:

- Alerta de **concentração excessiva** quando um ativo representa mais de 35% da carteira.
- Alerta de **excesso de risco** quando mais de 50% da carteira está em ativos de alto risco.
- Alerta de **alta sensibilidade a quedas** quando a perda supera 10% em queda moderada.
- Destaque de **boa resiliência** quando a carteira mantém perdas baixas em cenários adversos leves.

---

## Observações Técnicas

- O projeto **não depende de internet** ou APIs externas.
- Os dados são simulados, coerentes com ativos reais do mercado brasileiro.
- Ativos de **renda fixa** têm sensibilidade reduzida (beta ≈ 0,05) em relação a variações de mercado.
- Compatível com **Windows**, macOS e Linux.
