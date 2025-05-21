# 🏛️ Extrator de Metadados Tainacan

Este repositório contém um script Python para extrair metadados de uma coleção hospedada na plataforma [Tainacan](https://tainacan.org/), utilizando sua API pública JSON.

## 🚀 Funcionalidades

- Realiza paginação automática até obter todos os itens da coleção.
- Extrai os metadados de todos os itens disponíveis.
- Gera um arquivo `.csv` com os dados estruturados.
- Nomeia o arquivo de forma automática com base no museu e coleção extraída.

## 🔧 Requisitos

- Python 3.7+
- Biblioteca `requests`

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## 📦 Como usar

1. Edite o valor da variável `base_items_url` no final do script para a URL da coleção que deseja extrair (encontrada via API do Tainacan).
2. Execute o script:

```bash
python extrator_tainacan.py
```

3. O CSV será salvo com o nome no formato: `nome_do_museu_nome_da_colecao.csv`.

## 📁 Estrutura do Projeto

```
extrator_tainacan/
├── extrator_tainacan.py      # Script principal
├── README.md                 # Documentação
├── requirements.txt          # Dependências
└── .gitignore                # Arquivos ignorados
```

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
