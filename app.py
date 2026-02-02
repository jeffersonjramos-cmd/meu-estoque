import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Gestor de Estoque", layout="wide")

st.title("📦 Sistema de Endereçamento de Produtos")

# 1. Carregar o arquivo
uploaded_file = st.file_uploader("Escolha a planilha Excel", type="xlsx")

if uploaded_file:
    # Criamos um "estado" para manter os dados salvos durante o uso
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_excel(uploaded_file)
    
    df = st.session_state.df

    # 2. Seleção da Rua (Dropdown)
    # Extraímos as ruas únicas da coluna 'Endereço'
    lista_ruas = sorted(df['Endereço'].dropna().unique())
    rua_selecionada = st.selectbox("Selecione a Rua para editar:", ["Todas"] + lista_ruas)

    # Filtrar a tabela visualmente
    if rua_selecionada != "Todas":
        tabela_visual = df[df['Endereço'] == rua_selecionada]
    else:
        tabela_visual = df

    st.write(f"Exibindo itens da: {rua_selecionada}")
    st.dataframe(tabela_visual, use_container_width=True)

    # 3. Formulário de Edição
    st.divider()
    st.subheader("📝 Atualizar Locação")
    
    with st.form("form_edicao", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            cod_input = st.text_input("Código do Produto")
        with col2:
            nova_loc = st.text_input("Nova Locação (Ex: L01-10)")
        
        btn_salvar = st.form_submit_button("Salvar Alteração")

        if btn_salvar:
            if cod_input in df['Código'].astype(str).values:
                # Atualiza no DataFrame que está na memória
                idx = df.index[df['Código'].astype(str) == cod_input].tolist()[0]
                df.at[idx, 'Endereço'] = nova_loc
                st.session_state.df = df # Atualiza o estado
                st.success(f"✅ Produto {cod_input} movido para {nova_loc}!")
                st.rerun() # Atualiza a tela
            else:
                st.error("❌ Código não encontrado!")

    # 4. Exportação
    st.divider()
    st.subheader("📤 Finalizar e Exportar")
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="Baixar Arquivo para o Sistema",
        data=csv,
        file_name="estoque_atualizado.csv",
        mime="text/csv",
    )
