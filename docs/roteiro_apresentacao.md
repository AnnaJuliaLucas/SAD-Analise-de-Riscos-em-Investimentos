# Roteiro de Apresentação Oral — TVC 2
## SAD: Análise de Riscos em Investimentos com Análise de Sensibilidade
**Duração total:** até 10 minutos

---

## Parte 1 — Contextualização do Problema (1 min)

> "Imagine que você é um investidor com uma carteira diversificada de ativos na Bolsa brasileira. O mercado oscila diariamente — às vezes sobe, às vezes cai. Como saber quanto você pode perder em um dia ruim? Ou quanto pode ganhar em um rali? Essa é a questão central que este trabalho responde."

- Apresentar o **Problema 13**: Análise de Riscos em Investimentos (Análise de Sensibilidade)
- Contextualizar: volatilidade do mercado financeiro, necessidade de gerenciar riscos
- Mencionar que este é um problema real enfrentado por qualquer investidor

---

## Parte 2 — Objetivo (1 min)

> "Desenvolvemos um Sistema de Apoio à Decisão — um SAD — que permite ao investidor simular diferentes cenários de mercado e ver, em tempo real, o impacto no seu portfólio."

- **Objetivo geral:** construir um SAD para análise de risco de portfólio
- **Objetivos específicos:**
  1. Simular cenários de alta e queda (−20% a +20%)
  2. Calcular impacto em cada ativo e no portfólio total
  3. Gerar recomendações automáticas de alocação

---

## Parte 3 — Metodologia (2 min)

> "A técnica central é a Análise de Sensibilidade — uma abordagem what-if que pergunta: o que acontece com o resultado se eu mudar este parâmetro?"

- Explicar o **portfólio simulado**: 8 ativos reais do mercado brasileiro (ações, renda fixa, FIIs)
- Mostrar a **tabela do CSV** com os ativos
- Explicar a fórmula central:
  - Preço simulado = Preço atual × (1 + variação × beta)
  - Ativos de renda fixa têm beta = 0,05 (quase não oscilam)
  - Ações e FIIs têm beta = 1,0
- Mencionar o desenvolvimento em **Python + Streamlit**

---

## Parte 4 — Demonstração do Dashboard (3 min)

> "Agora vou mostrar o sistema funcionando."

### Roteiro de demonstração:

1. **Abrir o sistema** com `streamlit run app.py`
2. Mostrar os **KPIs** (valor investido, retorno esperado, risco, maior exposição)
3. Mostrar a **tabela da carteira** inicial
4. Selecionar o cenário **Neutro (0%)** — mostrar que nada muda
5. Mudar para **Queda Forte (−20%)** — mostrar o impacto dramático
6. Usar o **slider** para ajustar manualmente a variação
7. Mostrar os **4 gráficos**:
   - Pizza da alocação
   - Barras comparativas (inicial vs. simulado)
   - Impacto por ativo (barras verdes/vermelhas)
   - Curva de sensibilidade (linha de −30% a +30%)
8. Mostrar a **tabela de todos os cenários**
9. Mostrar as **recomendações automáticas**

---

## Parte 5 — Resultados Encontrados (1,5 min)

> "O sistema revelou insights importantes sobre este portfólio."

- Em queda de **20%**, o portfólio perde apenas **10,8%** — bem menos do que a bolsa, graças ao Tesouro Selic
- O **VALE3** é o ativo com maior impacto absoluto
- O **MGLU3** tem a maior volatilidade (55% a.a.) — maior risco
- O Tesouro Selic **amortece** os choques negativos
- O portfólio tem **boa diversificação setorial** mas concentração moderada em renda variável

---

## Parte 6 — Recomendações (1 min)

> "Com base nos resultados, o sistema gera recomendações automáticas."

- Manter a proporção de renda fixa como âncora defensiva
- Considerar redução da exposição ao MGLU3 (muito volátil)
- O portfólio demonstra boa resiliência a quedas leves (−5%)
- Para perfil mais conservador: aumentar renda fixa ou FIIs defensivos

---

## Parte 7 — Conclusão (0,5 min)

> "Este trabalho demonstrou como a Análise de Sensibilidade, implementada como um SAD interativo, pode transformar dados financeiros em decisões mais informadas."

- O SAD permite ao investidor **ver o risco** antes de sentir na carteira
- A ferramenta é **interativa, visual e acessível** — sem necessidade de planilhas complexas
- **Trabalhos futuros:** incorporar Teoria de Markowitz, Monte Carlo e VaR

---

## Dica Final para a Apresentação

- Abra o sistema **antes** da apresentação e deixe rodando
- Comece com o cenário neutro e vá mudando progressivamente para queda forte
- Destaque a **curva de sensibilidade** — ela resume o comportamento do portfólio de forma visual
- Se houver perguntas sobre a metodologia, mencione as equações do relatório
