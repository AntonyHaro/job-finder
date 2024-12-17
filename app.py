import streamlit as st
import pandas as pd
import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def formatar_data(data_str):
    """Formata a data do formato da API para exibição em português"""
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        return data.strftime("%d/%m/%Y %H:%M")
    except:
        return data_str


def buscar_vagas(
    keywords,
    geo_code=106057199,
    date_posted="Any time",
    start=0,
    company_ids=None,
    experience_levels=None,
    onsite_remotes=None,
):
    """Função para buscar vagas na API com filtros adicionais"""
    url = "https://fresh-linkedin-profile-data.p.rapidapi.com/search-jobs"

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
    }

    payload = {
        "keywords": keywords,
        "geo_code": geo_code,
        "date_posted": date_posted,
        "experience_levels": experience_levels if experience_levels else [],
        "company_ids": company_ids if company_ids else [],
        "title_ids": [],
        "onsite_remotes": onsite_remotes if onsite_remotes else [],
        "functions": [],
        "industries": [],
        "job_types": [],
        "sort_by": "Most relevant",
        "easy_apply": "false",
        "under_10_applicants": "false",
        "start": start,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        st.error(f"Erro ao buscar vagas: {str(e)}")
        return None


def main():
    st.set_page_config(page_title="Buscador de Vagas", layout="wide")

    # Configuração do layout principal
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        .stButton>button {
            width: 100%;
        }
        .job-card {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Título centralizado
    st.markdown(
        "<h1 style='text-align: center;'>🔍 Buscador de Vagas</h1>",
        unsafe_allow_html=True,
    )

    # Barra lateral com filtros
    with st.sidebar:
        st.header("Filtros de Busca")

        keywords = st.text_input("Palavras-chave", "")

        # Filtros adicionais
        experience_options = {
            "": [],
            "Estágio": ["INTERNSHIP"],
            "Júnior": ["ENTRY_LEVEL"],
            "Pleno": ["MID_SENIOR"],
            "Sênior": ["SENIOR"],
            "Diretor": ["DIRECTOR"],
        }
        experience = st.selectbox(
            "Nível de Experiência", options=list(experience_options.keys())
        )

        work_type_options = {
            "": [],
            "Presencial": ["ONSITE"],
            "Remoto": ["REMOTE"],
            "Híbrido": ["HYBRID"],
        }
        work_type = st.selectbox(
            "Tipo de Trabalho", options=list(work_type_options.keys())
        )

        date_options = {
            "Qualquer período": "Any time",
            "Última 24 horas": "Past 24 hours",
            "Última semana": "Past week",
            "Último mês": "Past month",
        }
        date_posted = st.selectbox(
            "Data de publicação", options=list(date_options.keys())
        )

        # Empresas específicas (opcional)
        company_filter = st.text_input("Filtrar por empresa (opcional)", "")

    # Container principal para os resultados
    main_container = st.container()

    # Botão de busca centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_clicked = st.button("Buscar Vagas")

    if search_clicked:
        if keywords:
            with st.spinner("Buscando vagas..."):
                # Preparar filtros
                experience_levels = experience_options[experience]
                onsite_remotes = work_type_options[work_type]
                company_ids = [1035] if company_filter.lower() == "microsoft" else []

                resultados = buscar_vagas(
                    keywords=keywords,
                    date_posted=date_options[date_posted],
                    experience_levels=experience_levels,
                    onsite_remotes=onsite_remotes,
                    company_ids=company_ids,
                )

                if resultados and isinstance(resultados, dict) and "data" in resultados:
                    vagas = resultados["data"]

                    if not vagas:
                        st.warning(
                            "Nenhuma vaga encontrada com os filtros selecionados."
                        )
                    else:
                        st.success(f"Encontradas {len(vagas)} vagas!")

                        # Criar DataFrame para melhor visualização
                        df = pd.DataFrame(vagas)

                        # Formatar as datas
                        if "posted_time" in df.columns:
                            df["posted_time"] = df["posted_time"].apply(formatar_data)

                        # Exibir vagas em cards com layout melhorado
                        for idx, vaga in df.iterrows():
                            with main_container:
                                st.markdown(
                                    """
                                    <div class="job-card">
                                """,
                                    unsafe_allow_html=True,
                                )

                                col1, col2 = st.columns([1, 4])

                                with col1:
                                    if "company_logo" in vaga and vaga["company_logo"]:
                                        st.image(
                                            vaga["company_logo"],
                                            width=100,
                                            caption=vaga["company"],
                                        )
                                    else:
                                        st.markdown(f"### {vaga['company']}")

                                with col2:
                                    st.subheader(vaga["job_title"])
                                    st.markdown(
                                        f"""
                                        🏢 **Empresa:** {vaga['company']}  
                                        📍 **Localização:** {vaga['location']}  
                                        {'🏠 **Modalidade:** ' + vaga['remote'] if 'remote' in vaga else ''}  
                                        {'💰 **Salário:** ' + vaga['salary'] if 'salary' in vaga else ''}  
                                        📅 **Publicado em:** {vaga['posted_time']}
                                    """
                                    )
                                    if "job_url" in vaga:
                                        st.markdown(
                                            f"[Ver vaga no LinkedIn]({vaga['job_url']})"
                                        )

                                st.markdown(
                                    """
                                    </div>
                                """,
                                    unsafe_allow_html=True,
                                )
        else:
            st.warning("Por favor, insira palavras-chave para a busca.")


if __name__ == "__main__":
    main()
