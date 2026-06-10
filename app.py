"""
TVC2 - SAD: Análise de Riscos em Investimentos com Análise de Sensibilidade
Disciplina: Sistemas de Apoio à Decisão - UFJF
Problema 13: Análise de Riscos em Investimentos (Análise de Sensibilidade)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import os

# ─────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SAD — Análise de Riscos em Investimentos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS customizado
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #0f3460;
        margin-bottom: 0.5rem;
    }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #0f3460; }
    .kpi-label { font-size: 0.85rem; color: #666; margin-top: 0.2rem; }
    .rec-box {
        background: #f0f7ff;
        border: 1px solid #b3d4f5;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .rec-title { font-weight: 700; color: #0f3460; margin-bottom: 0.5rem; }
    .alert-box {
        background: #fff3e0;
        border: 1px solid #ffcc80;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 0.5rem;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f3460;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #0f3460;
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Funções utilitárias
# ─────────────────────────────────────────────

def carregar_portfolio(caminho: str) -> pd.DataFrame:
    """Carrega e enriquece o CSV do portfólio."""
    df = pd.read_csv(caminho)
    df["valor_investido"] = df["quantidade"] * df["preco_atual"]
    total = df["valor_investido"].sum()
    df["participacao"] = df["valor_investido"] / total
    return df


def calcular_cenario(df: pd.DataFrame, variacao: float) -> pd.DataFrame:
    """
    Aplica a variação percentual aos preços e recalcula valores.
    Ativos de renda fixa têm sensibilidade reduzida (beta ≈ 0.05).
    """
    dfc = df.copy()
    # Renda fixa quase não oscila com o mercado
    beta = dfc["classe"].apply(lambda c: 0.05 if c == "Renda Fixa" else 1.0)
    dfc["preco_simulado"] = dfc["preco_atual"] * (1 + variacao * beta)
    dfc["valor_simulado"] = dfc["quantidade"] * dfc["preco_simulado"]
    dfc["impacto_rs"] = dfc["valor_simulado"] - dfc["valor_investido"]
    dfc["impacto_pct"] = dfc["impacto_rs"] / dfc["valor_investido"]
    total_sim = dfc["valor_simulado"].sum()
    dfc["nova_participacao"] = dfc["valor_simulado"] / total_sim
    return dfc


def risco_ponderado(df: pd.DataFrame) -> float:
    """Risco médio ponderado pela participação."""
    return float((df["volatilidade"] * df["participacao"]).sum())


def retorno_ponderado(df: pd.DataFrame) -> float:
    """Retorno esperado ponderado pela participação."""
    return float((df["retorno_esperado"] * df["participacao"]).sum())


def gerar_recomendacao(df: pd.DataFrame, variacao: float, dfc: pd.DataFrame) -> "list[str]":
    """Gera lista de recomendações textuais baseadas nos indicadores."""
    recomendacoes = []
    total_ini = df["valor_investido"].sum()
    total_fim = dfc["valor_simulado"].sum()
    perda_pct = (total_fim - total_ini) / total_ini

    max_part = df["participacao"].max()
    ativo_maior = df.loc[df["participacao"].idxmax(), "ativo"]

    alto_risco_pct = df.loc[df["perfil_risco"] == "alto", "participacao"].sum()
    risco_med = risco_ponderado(df)

    if variacao < 0 and perda_pct < -0.10:
        recomendacoes.append(
            "⚠️ **Alta sensibilidade a quedas:** O portfólio apresenta perda superior a 10% "
            "em cenário de queda moderada. Recomenda-se maior diversificação entre classes de ativos."
        )

    if max_part > 0.35:
        recomendacoes.append(
            f"🔴 **Concentração excessiva:** O ativo **{ativo_maior}** representa "
            f"{max_part:.1%} do portfólio. Uma concentração acima de 35% aumenta "
            "significativamente o risco idiossincrático. Considere rebalancear."
        )

    if alto_risco_pct > 0.50:
        recomendacoes.append(
            f"📉 **Excesso de ativos de alto risco:** {alto_risco_pct:.1%} do portfólio está "
            "alocado em ativos de perfil de risco alto. Recomenda-se aumentar a participação "
            "em ativos defensivos, como renda fixa ou fundos imobiliários de menor volatilidade."
        )

    if variacao < -0.04 and perda_pct > -0.05:
        recomendacoes.append(
            "✅ **Boa resiliência:** O portfólio demonstra estabilidade em quedas leves, "
            "com impacto inferior a 5%. A diversificação atual está contribuindo positivamente."
        )

    if risco_med < 0.15:
        recomendacoes.append(
            "🟢 **Risco controlado:** O risco médio ponderado do portfólio está abaixo de 15%, "
            "indicando uma carteira relativamente conservadora."
        )

    if not recomendacoes:
        recomendacoes.append(
            "ℹ️ O portfólio apresenta características equilibradas para o cenário selecionado. "
            "Continue monitorando os indicadores de risco periodicamente."
        )

    return recomendacoes


def salvar_grafico_png(fig_mpl, caminho: str):
    """Salva figura matplotlib em PNG."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    fig_mpl.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig_mpl)


# ─────────────────────────────────────────────
# Carregamento dos dados
# ─────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "dados", "portfolio_simulado.csv")

@st.cache_data
def load_data():
    return carregar_portfolio(CSV_PATH)

df_original = load_data()

CENARIOS_FIXOS = {
    "Queda Forte (−20%)": -0.20,
    "Queda Moderada (−10%)": -0.10,
    "Queda Leve (−5%)": -0.05,
    "Neutro (0%)": 0.00,
    "Alta Leve (+5%)": 0.05,
    "Alta Moderada (+10%)": 0.10,
    "Alta Forte (+20%)": 0.20,
}


# ─────────────────────────────────────────────
# Cabeçalho
# ─────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>📊 SAD — Análise de Riscos em Investimentos</h1>
    <p style="font-size:1.05rem; opacity:0.85; margin:0">
        Análise de Sensibilidade aplicada à avaliação de risco de portfólio<br>
        <em>TVC 2 — Sistemas de Apoio à Decisão · UFJF · 2026</em>
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar — controles
# ─────────────────────────────────────────────

st.sidebar.header("⚙️ Parâmetros da Simulação")

st.sidebar.markdown("**Cenário predefinido:**")
cenario_selecionado = st.sidebar.selectbox(
    "Selecione um cenário",
    list(CENARIOS_FIXOS.keys()),
    index=3,
)
var_predefinida = CENARIOS_FIXOS[cenario_selecionado]

st.sidebar.markdown("---")
st.sidebar.markdown("**Ou ajuste manualmente:**")
variacao_manual = st.sidebar.slider(
    "Variação de mercado (%)",
    min_value=-30,
    max_value=30,
    value=int(var_predefinida * 100),
    step=1,
    format="%d%%",
)
variacao = variacao_manual / 100.0

st.sidebar.markdown("---")
st.sidebar.markdown("**Exportar gráficos:**")
exportar = st.sidebar.button("💾 Salvar gráfico PNG")

st.sidebar.markdown("---")
st.sidebar.info(
    "Este sistema simula o impacto de oscilações de mercado sobre um portfólio "
    "de investimentos brasileiro, auxiliando na tomada de decisão sobre alocação de ativos."
)


# ─────────────────────────────────────────────
# Cálculos do cenário selecionado
# ─────────────────────────────────────────────

dfc = calcular_cenario(df_original, variacao)

total_inicial = df_original["valor_investido"].sum()
total_final = dfc["valor_simulado"].sum()
ganho_perda = total_final - total_inicial
retorno_cenario = ganho_perda / total_inicial
ret_esperado = retorno_ponderado(df_original)
risco_med = risco_ponderado(df_original)
maior_ativo = df_original.loc[df_original["participacao"].idxmax(), "ativo"]
maior_part = df_original["participacao"].max()

ativo_maior_ganho = dfc.loc[dfc["impacto_rs"].idxmax()]
ativo_maior_perda = dfc.loc[dfc["impacto_rs"].idxmin()]


# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────

st.markdown('<div class="section-title">Indicadores do Portfólio</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">R$ {total_inicial:,.2f}</div>
        <div class="kpi-label">Valor Total Investido</div>
    </div>""", unsafe_allow_html=True)

with k2:
    cor = "green" if ret_esperado >= 0 else "red"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:{cor}">{ret_esperado:.2%}</div>
        <div class="kpi-label">Retorno Esperado (ponderado)</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:#e65100">{risco_med:.2%}</div>
        <div class="kpi-label">Risco Médio Ponderado (vol.)</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{maior_ativo} ({maior_part:.1%})</div>
        <div class="kpi-label">Maior Exposição no Portfólio</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Tabela da carteira inicial
# ─────────────────────────────────────────────

st.markdown('<div class="section-title">Composição da Carteira Inicial</div>', unsafe_allow_html=True)

df_display = df_original[[
    "ativo", "nome", "classe", "quantidade", "preco_atual",
    "valor_investido", "participacao", "retorno_esperado", "volatilidade", "perfil_risco"
]].copy()

df_display.columns = [
    "Ativo", "Nome", "Classe", "Qtd.", "Preço Atual (R$)",
    "Valor Investido (R$)", "Participação", "Retorno Esp. a.a.", "Volatilidade a.a.", "Risco"
]

df_display["Preço Atual (R$)"] = df_display["Preço Atual (R$)"].map("R$ {:,.2f}".format)
df_display["Valor Investido (R$)"] = df_display["Valor Investido (R$)"].map("R$ {:,.2f}".format)
df_display["Participação"] = df_display["Participação"].map("{:.2%}".format)
df_display["Retorno Esp. a.a."] = df_display["Retorno Esp. a.a."].map("{:.2%}".format)
df_display["Volatilidade a.a."] = df_display["Volatilidade a.a."].map("{:.2%}".format)

st.dataframe(df_display, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# Resultado do Cenário Simulado
# ─────────────────────────────────────────────

st.markdown(f'<div class="section-title">Resultado do Cenário: {cenario_selecionado} ({variacao:+.0%})</div>',
            unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.metric("Valor Inicial", f"R$ {total_inicial:,.2f}")
with r2:
    st.metric("Valor Simulado", f"R$ {total_final:,.2f}")
with r3:
    cor_delta = "normal" if ganho_perda >= 0 else "inverse"
    st.metric("Ganho / Perda", f"R$ {ganho_perda:,.2f}", delta=f"{retorno_cenario:+.2%}")
with r4:
    if variacao != 0:
        if dfc["impacto_rs"].max() > 0:
            st.metric("Maior Ganho", f'{ativo_maior_ganho["ativo"]}', delta=f'R$ {ativo_maior_ganho["impacto_rs"]:+,.2f}')
        else:
            st.metric("Maior Perda", f'{ativo_maior_perda["ativo"]}', delta=f'R$ {ativo_maior_perda["impacto_rs"]:+,.2f}', delta_color="inverse")
    else:
        st.metric("Variação", "0%  — Cenário Neutro")


# ─────────────────────────────────────────────
# Gráficos
# ─────────────────────────────────────────────

st.markdown('<div class="section-title">Visualizações</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

# --- Gráfico 1: Pizza de alocação atual
with col_a:
    st.markdown("**Alocação Atual do Portfólio**")
    cores = px.colors.qualitative.Set2
    fig_pizza = go.Figure(go.Pie(
        labels=df_original["ativo"],
        values=df_original["valor_investido"],
        hole=0.4,
        marker_colors=cores,
        textinfo="label+percent",
        hovertemplate="%{label}<br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
    ))
    fig_pizza.update_layout(
        margin=dict(t=30, b=10, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        height=360,
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

# --- Gráfico 2: Barras — Valor inicial vs simulado
with col_b:
    st.markdown("**Valor Inicial × Valor Simulado por Ativo**")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Valor Inicial",
        x=dfc["ativo"],
        y=dfc["valor_investido"],
        marker_color="#0f3460",
    ))
    fig_bar.add_trace(go.Bar(
        name="Valor Simulado",
        x=dfc["ativo"],
        y=dfc["valor_simulado"],
        marker_color="#e94560" if variacao < 0 else "#2ecc71",
    ))
    fig_bar.update_layout(
        barmode="group",
        xaxis_title="Ativo",
        yaxis_title="R$",
        yaxis_tickformat=",.0f",
        legend=dict(orientation="h", yanchor="bottom", y=-0.35),
        margin=dict(t=30, b=10, l=10, r=10),
        height=360,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

col_c, col_d = st.columns(2)

# --- Gráfico 3: Impacto financeiro por ativo
with col_c:
    st.markdown("**Impacto Financeiro por Ativo (R$)**")
    cores_impacto = ["#e94560" if v < 0 else "#2ecc71" for v in dfc["impacto_rs"]]
    fig_impacto = go.Figure(go.Bar(
        x=dfc["ativo"],
        y=dfc["impacto_rs"],
        marker_color=cores_impacto,
        text=dfc["impacto_rs"].map("R$ {:+,.0f}".format),
        textposition="outside",
        hovertemplate="%{x}<br>Impacto: R$ %{y:+,.2f}<extra></extra>",
    ))
    fig_impacto.update_layout(
        xaxis_title="Ativo",
        yaxis_title="Impacto (R$)",
        yaxis_tickformat=",.0f",
        margin=dict(t=30, b=10, l=10, r=10),
        height=360,
    )
    st.plotly_chart(fig_impacto, use_container_width=True)

# --- Gráfico 4: Curva de sensibilidade (linha) de −20% a +20%
with col_d:
    st.markdown("**Curva de Sensibilidade do Portfólio**")
    variacoes_range = np.linspace(-0.30, 0.30, 61)
    valores_range = []
    for v in variacoes_range:
        dfv = calcular_cenario(df_original, v)
        valores_range.append(dfv["valor_simulado"].sum())

    fig_linha = go.Figure()
    fig_linha.add_trace(go.Scatter(
        x=variacoes_range * 100,
        y=valores_range,
        mode="lines",
        line=dict(color="#0f3460", width=2.5),
        name="Valor do Portfólio",
    ))
    # Linha de referência no ponto atual
    fig_linha.add_vline(x=variacao * 100, line_dash="dash", line_color="#e94560",
                        annotation_text=f"Cenário atual: {variacao:+.0%}", annotation_position="top right")
    fig_linha.add_hline(y=total_inicial, line_dash="dot", line_color="#666",
                        annotation_text="Valor inicial", annotation_position="bottom right")
    fig_linha.update_layout(
        xaxis_title="Variação de Mercado (%)",
        yaxis_title="Valor Total (R$)",
        yaxis_tickformat=",.0f",
        margin=dict(t=30, b=10, l=10, r=10),
        height=360,
    )
    st.plotly_chart(fig_linha, use_container_width=True)


# ─────────────────────────────────────────────
# Tabela de impacto por cenário (todos)
# ─────────────────────────────────────────────

st.markdown('<div class="section-title">Análise de Sensibilidade — Todos os Cenários</div>',
            unsafe_allow_html=True)

linhas = []
for nome_c, var_c in CENARIOS_FIXOS.items():
    dfv = calcular_cenario(df_original, var_c)
    total_v = dfv["valor_simulado"].sum()
    gp = total_v - total_inicial
    linhas.append({
        "Cenário": nome_c,
        "Valor Final (R$)": f"R$ {total_v:,.2f}",
        "Ganho/Perda (R$)": f"R$ {gp:+,.2f}",
        "Retorno (%)": f"{gp/total_inicial:+.2%}",
        "Ativo com Maior Impacto": dfv.loc[dfv["impacto_rs"].abs().idxmax(), "ativo"],
    })

df_cenarios = pd.DataFrame(linhas)
st.dataframe(df_cenarios, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# Recomendações automáticas
# ─────────────────────────────────────────────

st.markdown('<div class="section-title">Recomendações de Alocação</div>', unsafe_allow_html=True)

recomendacoes = gerar_recomendacao(df_original, variacao, dfc)

st.markdown('<div class="rec-box"><div class="rec-title">Análise e Recomendações do Sistema:</div>', unsafe_allow_html=True)
for rec in recomendacoes:
    st.markdown(rec)
st.markdown('</div>', unsafe_allow_html=True)

# Resumo textual acadêmico
alto_risco_pct = df_original.loc[df_original["perfil_risco"] == "alto", "participacao"].sum()
if alto_risco_pct > 0.50 and variacao < -0.05:
    st.markdown("""
    <div class="alert-box">
    <strong>Parecer analítico:</strong> Observa-se que o portfólio apresenta elevada sensibilidade
    a oscilações negativas do mercado, principalmente devido à concentração em ativos de maior
    volatilidade. Recomenda-se reduzir a exposição aos ativos de maior risco e aumentar a
    participação em ativos defensivos, como renda fixa, a fim de melhorar a estabilidade da carteira.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Exportação de gráfico PNG
# ─────────────────────────────────────────────

if exportar:
    fig_exp, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig_exp.suptitle(
        f"Análise de Sensibilidade do Portfólio — Cenário: {variacao:+.0%}",
        fontsize=14, fontweight="bold"
    )

    # Subplot 1: Pizza
    ax1 = axes[0, 0]
    ax1.pie(df_original["valor_investido"], labels=df_original["ativo"], autopct="%1.1f%%", startangle=90)
    ax1.set_title("Alocação do Portfólio")

    # Subplot 2: Barras comparativas
    ax2 = axes[0, 1]
    x = np.arange(len(dfc))
    ax2.bar(x - 0.2, dfc["valor_investido"], 0.4, label="Inicial", color="#0f3460")
    ax2.bar(x + 0.2, dfc["valor_simulado"], 0.4, label="Simulado", color="#e94560" if variacao < 0 else "#2ecc71")
    ax2.set_xticks(x)
    ax2.set_xticklabels(dfc["ativo"], rotation=30, ha="right")
    ax2.set_title("Valor Inicial × Simulado")
    ax2.legend()
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"R${v:,.0f}"))

    # Subplot 3: Impacto
    ax3 = axes[1, 0]
    cores_bar = ["#e94560" if v < 0 else "#2ecc71" for v in dfc["impacto_rs"]]
    ax3.bar(dfc["ativo"], dfc["impacto_rs"], color=cores_bar)
    ax3.set_title("Impacto por Ativo (R$)")
    ax3.axhline(0, color="black", linewidth=0.8)
    ax3.set_xticklabels(dfc["ativo"], rotation=30, ha="right")
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"R${v:+,.0f}"))

    # Subplot 4: Curva de sensibilidade
    ax4 = axes[1, 1]
    ax4.plot(variacoes_range * 100, valores_range, color="#0f3460", linewidth=2)
    ax4.axvline(variacao * 100, color="#e94560", linestyle="--", label=f"Atual: {variacao:+.0%}")
    ax4.axhline(total_inicial, color="#666", linestyle=":", label="Valor inicial")
    ax4.set_xlabel("Variação (%)")
    ax4.set_ylabel("Valor Total (R$)")
    ax4.set_title("Curva de Sensibilidade")
    ax4.legend()
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"R${v:,.0f}"))

    plt.tight_layout()
    img_path = os.path.join(BASE_DIR, "imagens", "graficos_gerados.png")
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    fig_exp.savefig(img_path, dpi=150, bbox_inches="tight")
    plt.close(fig_exp)

    with open(img_path, "rb") as f:
        st.sidebar.download_button(
            "⬇️ Baixar PNG",
            data=f,
            file_name="graficos_gerados.png",
            mime="image/png",
        )
    st.sidebar.success("Gráfico salvo em imagens/graficos_gerados.png")


# ─────────────────────────────────────────────
# Rodapé
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<small>TVC 2 · Sistemas de Apoio à Decisão · UFJF · 2026 — "
    "Problema 13: Análise de Riscos em Investimentos (Análise de Sensibilidade)</small>",
    unsafe_allow_html=True,
)
