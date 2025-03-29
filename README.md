# Extração de Dados do Rol de Procedimentos e Eventos em Saúde

Este projeto extrai os dados da tabela "Rol de Procedimentos e Eventos em Saúde" do PDF Anexo I, 
os estrutura em um arquivo CSV e compacta o resultado em um arquivo ZIP.

## Funcionalidades

- Extração de tabelas de todas as páginas do PDF
- Substituição das abreviações OD e AMB pelas descrições completas conforme a legenda
- Geração de arquivo CSV estruturado
- Compactação do CSV em arquivo ZIP

## Requisitos

- Python 3.7+
- Java Runtime Environment (JRE) - necessário para a biblioteca tabula-py

## Instalação

1. Clone este repositório:
```
git clone <repositório>
cd teste2
```

2. Instale as dependências necessárias:
```
pip install -r requirements.txt
```

3. Copie o arquivo PDF para o diretório de dados:
```
mkdir -p dados
cp /caminho/para/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf dados/
```

## Execução

Execute o script principal:
```
python extrai_rol_procedimentos.py
```

## Saída

O script irá gerar:
- Um arquivo CSV com os dados extraídos: `rol_procedimentos.csv`
- Um arquivo ZIP contendo o CSV: `Teste_Gilberto_de_Paiva_Melo.zip`

## Estrutura do Projeto

```
teste2/
├── extrai_rol_procedimentos.py  # Script principal 
├── requirements.txt             # Dependências do projeto
├── README.md                    # Este arquivo
├── .gitignore                   # Arquivos ignorados pelo git
├── dados/                       # Diretório para armazenar o arquivo PDF
│   └── Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf  # Arquivo de entrada
├── rol_procedimentos.csv        # Arquivo CSV gerado (não versionado)
└── Teste_Gilberto_de_Paiva_Melo.zip # Arquivo ZIP gerado (não versionado)
```

## Autor

Gilberto de Paiva Melo
