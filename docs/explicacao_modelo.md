# Documentação Técnica do Modelo

## Análise de Sensibilidade Aplicada a Portfólio de Investimentos

---

## 1. O que é Análise de Sensibilidade?

A Análise de Sensibilidade é uma técnica de modelagem analítica que avalia como a variação em um ou mais parâmetros de entrada afeta os resultados de um modelo. Em finanças, ela é amplamente utilizada para mensurar o impacto de oscilações de preços, taxas e outros fatores de mercado sobre o desempenho de investimentos.

No contexto dos Sistemas de Apoio à Decisão (SAD), a Análise de Sensibilidade é classificada como uma análise *what-if* estruturada, permitindo ao tomador de decisão compreender a robustez do seu portfólio diante de diferentes cenários de mercado.

---

## 2. Como foi Aplicada ao Portfólio

O modelo simula variações percentuais nos preços dos ativos do portfólio, calculando o novo valor de cada posição e, consequentemente, o impacto no valor total da carteira.

A variação é aplicada diferenciadamente:
- **Ações e Fundos Imobiliários:** sensibilidade plena ao cenário (beta = 1,0).
- **Renda Fixa:** sensibilidade mínima (beta = 0,05), refletindo a baixa correlação desses títulos com oscilações de bolsa no curto prazo.

---

## 3. Fórmulas Utilizadas

### 3.1 Valor Investido por Ativo

```
Valor_Investido_i = Quantidade_i × Preço_Atual_i
```

### 3.2 Participação Percentual

```
Participação_i = Valor_Investido_i / Σ Valor_Investido_i
```

### 3.3 Preço Simulado

```
Preço_Simulado_i = Preço_Atual_i × (1 + Variação × Beta_i)
```

Onde:
- `Variação` é o percentual de variação de mercado (ex.: −0,10 para −10%)
- `Beta_i = 1,0` para ações e FIIs
- `Beta_i = 0,05` para renda fixa

### 3.4 Valor Simulado

```
Valor_Simulado_i = Quantidade_i × Preço_Simulado_i
```

### 3.5 Impacto Financeiro por Ativo

```
Impacto_i = Valor_Simulado_i − Valor_Investido_i
```

### 3.6 Retorno do Cenário

```
Retorno_Cenário = (Σ Valor_Simulado_i − Σ Valor_Investido_i) / Σ Valor_Investido_i
```

### 3.7 Retorno Esperado Ponderado do Portfólio

```
Retorno_Esperado = Σ (Retorno_Esperado_i × Participação_i)
```

### 3.8 Risco Médio Ponderado (Volatilidade do Portfólio — Simplificada)

```
Risco_Ponderado = Σ (Volatilidade_i × Participação_i)
```

> **Nota:** Esta é uma estimativa simplificada que não considera a correlação entre ativos. Uma estimativa mais precisa usaria a matriz de covariância (Teoria Moderna de Portfólio de Markowitz).

---

## 4. Como o Retorno foi Calculado

O retorno esperado de cada ativo é fornecido como dado de entrada no CSV (coluna `retorno_esperado`), representando a expectativa anual de valorização. O retorno do portfólio é calculado como a média ponderada dos retornos individuais, usando a participação de cada ativo como peso.

O retorno do cenário simulado, por sua vez, é calculado comparando o valor total após a aplicação da variação de mercado com o valor inicial.

---

## 5. Como o Risco Ponderado foi Estimado

O risco é representado pela volatilidade anualizada de cada ativo (coluna `volatilidade` no CSV). A volatilidade do portfólio é estimada pela média ponderada das volatilidades individuais — uma abordagem simplificada mas didaticamente clara.

Valores de referência utilizados:
- PETR4: 35% (alta volatilidade)
- VALE3: 30% (alta volatilidade)
- ITUB4: 22% (volatilidade moderada)
- BBDC4: 20% (volatilidade moderada)
- MGLU3: 55% (muito alta volatilidade)
- Tesouro Selic: 1% (praticamente sem risco de mercado)
- FIIs: 12-14% (volatilidade moderada-baixa)

---

## 6. Limitações do Modelo

1. **Correlação ignorada:** O modelo não considera a correlação entre ativos, o que pode superestimar ou subestimar o risco real do portfólio.
2. **Beta simplificado:** O beta dos ativos foi simplificado (0 ou 1). Na prática, cada ativo tem um beta específico em relação ao mercado.
3. **Dados sintéticos:** Os dados utilizados são simulados. A análise com dados reais históricos seria mais precisa.
4. **Horizonte único:** O modelo não considera o horizonte temporal de investimento nem o efeito dos juros compostos no longo prazo.
5. **Sem custos de transação:** Corretagens, impostos e spreads não são considerados.

---

## 7. Possíveis Melhorias Futuras

- Implementar a Teoria Moderna de Portfólio (Markowitz) com matriz de covariâncias.
- Integrar dados históricos reais via APIs (Yahoo Finance, B3).
- Adicionar simulação de Monte Carlo para distribuição de cenários probabilísticos.
- Calcular o Value at Risk (VaR) e o Conditional VaR (CVaR).
- Permitir otimização automática da alocação (fronteira eficiente).
- Adicionar análise de índice de Sharpe para comparação de desempenho ajustado ao risco.
