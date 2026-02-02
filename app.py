import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor de Estoque", layout="wide")

st.title("📦 Sistema de Endereçamento")

# 1. Upload do arquivo
uploaded_file = st.file_uploader("Suba sua planilha (.xlsx)", type="xlsx")

if uploaded_file:
    # Usar session_state para os dados não sumirem ao clicar
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_excel(uploaded_file)
    
    # Atalho para o dataframe
    df = st.session_state.df

    # 2. Filtro de Rua (Dropdown)
    # Garantimos que a coluna 'Endereço' seja texto para não dar erro
    df['Endereço'] = df['Endereço'].astype(str)
    lista_ruas = sorted(df['Endereço'].unique())
    
    rua_selecionada = st.selectbox("Selecione a Rua:", ["Todas"] + lista_ruas)

    # 3. Mostrar a tabela filtrada
    if rua_selecionada != "Todas":
        df_filtrado = df[df['Endereço'] == rua_selecionada]
    else:
        df_filtrado = df
    
    st.dataframe(df_filtrado, use_container_width=True)

    # 4. Formulário de Edição Simples
    st.divider()
    with st.expander("➕ Editar Localização de Produto", expanded=True):
        with st.form("meu_formulario"):
            cod_input = st.text_input("Código do Produto")
            nova_loc = st.text_input("Nova Locação")
            submit = st.form_submit_button("Atualizar na Lista")

            if submit:
                # Verificando se o código existe (como string)
                cod_input = cod_input.strip()
                if cod_input in df['Código'].astype(str).values:
                    # Faz a alteração
                    mask = df['Código'].astype(str) == cod_input
                    st.session_state.df.loc[mask, 'Endereço'] = nova_loc
                    st.success(f"Alterado: {cod_input} agora está em {nova_loc}")
                    # A tabela vai atualizar sozinha na próxima interação
                else:
                    st.error("Código não encontrado na planilha!")

    # 5. Botão de Download
    st.divider()
    csv = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar Planilha Final para o Sistema",
        data=csv,
        file_name="estoque_atualizado.csv",
        mime="text/csv",
    )
