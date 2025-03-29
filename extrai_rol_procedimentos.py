import tabula
import pandas as pd
import zipfile
import os
import re
from PyPDF2 import PdfReader

diretorio_dados = os.path.join(os.path.dirname(__file__), "dados")
pdf_path = os.path.join(diretorio_dados, "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")

if not os.path.exists(diretorio_dados):
    os.makedirs(diretorio_dados)
    print(f"Diretório de dados criado: {diretorio_dados}")

if not os.path.exists(pdf_path):
    print(f"ATENÇÃO: O arquivo PDF não foi encontrado em: {pdf_path}")
    print(f"Por favor, copie o arquivo para o diretório: {diretorio_dados}")
    exit(1)

def extrair_legenda(pdf_path):
    reader = PdfReader(pdf_path)
    legenda = {}
    
    for page in reader.pages:
        text = page.extract_text()
        
        od_match = re.search(r'OD\s*=\s*([^;]+)', text)
        amb_match = re.search(r'AMB\s*=\s*([^;]+)', text)
        
        if od_match and 'OD' not in legenda:
            legenda['OD'] = od_match.group(1).strip()
        
        if amb_match and 'AMB' not in legenda:
            legenda['AMB'] = amb_match.group(1).strip()
        
        if 'OD' in legenda and 'AMB' in legenda:
            break
            
    return legenda

def extrair_tabelas_pdf():
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    
    print(f"Extraindo dados de {num_pages} páginas...")
    
    dfs = tabula.read_pdf(
        pdf_path, 
        pages='all', 
        multiple_tables=True,
        lattice=True,
        stream=True,
        guess=False
    )
    
    tabelas_processadas = []
    for idx, df in enumerate(dfs):
        if not df.empty:
            df.columns = [str(col).strip() for col in df.columns]
            tabelas_processadas.append(df)
            print(f"Tabela {idx+1} encontrada com {len(df)} linhas e {len(df.columns)} colunas")
    
    if tabelas_processadas:
        colunas_principais = max(tabelas_processadas, key=lambda x: len(x.columns)).columns.tolist()
        
        for i in range(len(tabelas_processadas)):
            for col in colunas_principais:
                if col not in tabelas_processadas[i].columns:
                    tabelas_processadas[i][col] = None
            
            tabelas_processadas[i] = tabelas_processadas[i][colunas_principais]
        
        tabela_final = pd.concat(tabelas_processadas, ignore_index=True)
        return tabela_final
    else:
        print("Não foram encontradas tabelas no PDF.")
        return None

def substituir_abreviacoes(df, legenda):
    if 'OD' in legenda and 'OD' in df.columns:
        df.rename(columns={'OD': legenda['OD']}, inplace=True)
    
    if 'AMB' in legenda and 'AMB' in df.columns:
        df.rename(columns={'AMB': legenda['AMB']}, inplace=True)
    
    return df

def main():
    print("Iniciando extração de dados do PDF...")
    
    legenda = extrair_legenda(pdf_path)
    print(f"Legenda encontrada: {legenda}")
    
    df = extrair_tabelas_pdf()
    
    if df is not None:
        df = substituir_abreviacoes(df, legenda)
        
        csv_path = "rol_procedimentos.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Arquivo CSV salvo em: {csv_path}")
        
        zip_filename = "Teste_Gilberto_de_Paiva_Melo.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(csv_path, os.path.basename(csv_path), compress_type=zipfile.ZIP_DEFLATED)
        
        print(f"Arquivo compactado criado: {zip_filename}")
        
        print("\nAmostra dos dados extraídos:")
        print(df.head())
        
        print(f"\nTotal de registros extraídos: {len(df)}")
    else:
        print("Não foi possível extrair os dados do PDF.")

if __name__ == "__main__":
    main()
