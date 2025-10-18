import pandas as pd

def filtro_interativo(arquivo='provas_banca_superior.csv'):
    """Recebe o arquivo bruto contendo todas as provas de determinada banca e filtra de acordo com palavras chave, ano, orgão"""
    df = pd.read_csv(arquivo, delimiter=',')
    df.columns = df.columns.str.strip()

    entrada_palavras = input("Palavras Chaves separadas por ',' (pressione Enter para não filtrar): ").strip()
    if entrada_palavras:
        palavras_chave = [p.strip() for p in entrada_palavras.split(',') if p.strip()]
    else:
        palavras_chave = []

    entrada_ano = input("Ano mínimo (pressione Enter para não filtrar): ").strip()
    ano_minimo = int(entrada_ano) if entrada_ano.isdigit() else None

    entrada_orgao = input("Órgão(s) separados por ',' (pressione Enter para não filtrar): ").strip()
    if entrada_orgao:
        orgaos = [o.strip() for o in entrada_orgao.split(',') if o.strip()]
    else:
        orgaos = []

    if palavras_chave:
        filtro_palavras = df['titulo'].str.contains('|'.join(palavras_chave), case=False, na=False)
    else:
        filtro_palavras = pd.Series([True] * len(df))

    if ano_minimo is not None:
        filtro_ano = df['ano'].astype(str).astype(int) >= ano_minimo
    else:
        filtro_ano = pd.Series([True] * len(df))
        
    if orgaos:
        filtro_orgao = df['orgao'].str.contains('|'.join(orgaos), case=False, na=False)
    else:
        filtro_orgao = pd.Series([True] * len(df))

    if not palavras_chave and ano_minimo is None and not orgaos:
        print("Nenhum filtro aplicado. Exibindo todos os registros.")

    df_filtrado = df[filtro_palavras & filtro_ano & filtro_orgao]

    nome_arquivo = 'provas_fcc_filtradas.xlsx'
    df_filtrado.to_excel(nome_arquivo, index=False)

    print(f"\n\nFiltro aplicado. {len(df_filtrado)} registros encontrados.")
    print(f"Arquivo salvo como {nome_arquivo}")
    
    if palavras_chave:
        print(f"Palavras-chave aplicadas: {', '.join(palavras_chave)}")
    if ano_minimo:
        print(f"Ano mínimo: {ano_minimo}")
    if orgaos:
        print(f"Órgãos filtrados: {', '.join(orgaos)}")