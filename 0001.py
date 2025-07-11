import streamlit as st

# Emojis para cada cor
cores = {
    "C": "🔴",  # Casa
    "V": "🔵",  # Visitante
    "E": "🟡",  # Empate
}

# Inicializa o histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Configuração da página
st.set_page_config(page_title="FS Padrões Pro", layout="centered")
st.title("📊 FS Padrões Pro – Análise de Colunas e Blocos")

# Botões para entrada
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🔴 Casa"):
        st.session_state.historico.insert(0, "C")
with col2:
    if st.button("🔵 Visitante"):
        st.session_state.historico.insert(0, "V")
with col3:
    if st.button("🟡 Empate"):
        st.session_state.historico.insert(0, "E")
with col4:
    if st.button("↩️ Desfazer") and st.session_state.historico:
        st.session_state.historico.pop(0)
with col5:
    if st.button("🧹 Limpar"):
        st.session_state.historico = []

st.divider()

# Mostrar histórico em blocos de 27 (3 linhas de 9)
def mostrar_blocos(historico):
    blocos = [historico[i:i+27] for i in range(0, len(historico), 27)]
    for idx, bloco in enumerate(blocos):
        st.markdown(f"### 🧱 Ciclo {idx + 1}")
        for linha in range(3):
            ini = linha * 9
            fim = ini + 9
            linha_jogadas = bloco[ini:fim]
            visual = " ".join(cores.get(x, x) for x in linha_jogadas)
            st.markdown(visual)

st.markdown("## 📋 Histórico por blocos (cada 27 jogadas)")
if st.session_state.historico:
    mostrar_blocos(st.session_state.historico)
else:
    st.info("Nenhuma jogada ainda registrada.")

# Função para codificar coluna em estrutura simbólica
def codificar_coluna(coluna):
    mapa = {}
    codigo = []
    letra = "A"
    for cor in coluna:
        if cor not in mapa:
            mapa[cor] = letra
            letra = chr(ord(letra) + 1)
        codigo.append(mapa[cor])
    return "".join(codigo)

# Montar colunas verticais de 3 resultados
def formar_colunas(historico):
    linhas = [historico[i:i+9] for i in range(0, len(historico), 9)]
    if len(linhas) < 3:
        return []
    colunas = []
    for i in range(min(9, len(linhas[0]))):
        if all(len(linha) > i for linha in linhas[:3]):
            coluna = [linhas[0][i], linhas[1][i], linhas[2][i]]
            colunas.append(coluna)
    return colunas

# Detectar se coluna atual reescreve estrutura anterior
def detectar_reescrita(colunas):
    if len(colunas) < 2:
        return None
    atual = colunas[0]
    estrutura_atual = codificar_coluna(atual)
    for i in range(1, len(colunas)):
        anterior = colunas[i]
        if codificar_coluna(anterior) == estrutura_atual:
            return {
                "coluna_atual": atual,
                "coluna_reescrita": anterior,
                "estrutura": estrutura_atual,
                "indice_original": i,
                "cor_sugerida": st.session_state.historico[(i * 3) - 1] if (i * 3) - 1 < len(st.session_state.historico) else None
            }
    return None

# Análise por colunas (a partir de 9 jogadas)
if len(st.session_state.historico) >= 9:
    st.divider()
    st.markdown("## 🔎 Análise por colunas verticais (mín. 9 jogadas)")

    colunas = formar_colunas(st.session_state.historico[:27])
    for i, col in enumerate(colunas):
        estrutura = " ".join([cores.get(c, c) for c in col])
        st.markdown(f"**Coluna {i + 1}**: {estrutura}")

    resultado = detectar_reescrita(colunas)
    if resultado:
        st.success(f"🔁 A coluna 1 reescreve a coluna {resultado['indice_original'] + 1} com estrutura `{resultado['estrutura']}`")
        col_antiga = " ".join([cores.get(c, c) for c in resultado["coluna_reescrita"]])
        col_atual = " ".join([cores.get(c, c) for c in resultado["coluna_atual"]])
        st.write(f"🔹 Coluna antiga: {col_antiga}")
        st.write(f"🔹 Coluna atual: {col_atual}")
        if resultado["cor_sugerida"]:
            st.markdown("### 🧠 Sugestão de próxima jogada")
            st.info(f"Próxima cor provável: {cores.get(resultado['cor_sugerida'])}")
    else:
        st.warning("Nenhuma reescrita estrutural detectada nas colunas.")
else:
    st.info("Adicione pelo menos 9 jogadas para ativar a análise.")
