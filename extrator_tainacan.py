import requests 
import time
import csv
import re
from urllib.parse import urlparse

def extrair_nome_museu(url):
    """Extrai o nome do museu a partir do domínio da URL."""
    dominio = urlparse(url).netloc
    nome = dominio.split('.')[0]
    return nome.lower().replace("-", "_")

def fetch_all_items(base_url, per_page=96, delay=0.5):
    """
    Busca todos os itens de uma coleção Tainacan paginando automaticamente via API.
    """
    all_items = []
    page = 1

    while True:
        url = f"{base_url}&perpage={per_page}&paged={page}&fetch_only_meta=all"
        print(f"Buscando página {page}...")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erro na requisição: {response.status_code}")
            break

        data = response.json()
        items = data.get('items', [])

        if not items:
            print("Nenhum item encontrado nesta página. Finalizando.")
            break

        all_items.extend(items)
        page += 1
        time.sleep(delay)

    return all_items

def extrair_nome_colecao_dos_metadados(itens):
    """
    Tenta inferir o nome da coleção a partir dos metadados dos itens.
    """
    for item in itens:
        metadata = item.get("metadata", {})
        for meta in metadata.values():
            valor = meta.get("value_as_string", "")
            if isinstance(valor, str) and valor.strip():
                valor_limpo = re.sub(r'[^a-zA-Z\s]', '', valor).strip()
                return valor_limpo
    return "colecao_desconhecida"

def salvar_csv(lista_de_itens, nome_museu, nome_colecao):
    """
    Salva os itens extraídos em um arquivo CSV.
    """
    if not lista_de_itens:
        print("Nenhum item para salvar.")
        return

    campo_base = ['id', 'title', 'slug', 'colecao']
    metadados = set()

    for item in lista_de_itens:
        metadata = item.get('metadata', {})
        for meta_id, meta_obj in metadata.items():
            metadados.add(meta_obj.get('name'))

    campos_csv = campo_base + sorted(metadados)
    nome_colecao_formatado = re.sub(r'[^a-zA-Z\s]', '', nome_colecao).lower().replace(' ', '_')
    nome_csv = f"{nome_museu}_{nome_colecao_formatado}.csv"

    with open(nome_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos_csv)
        writer.writeheader()

        for item in lista_de_itens:
            linha = {
                'id': item.get('id'),
                'title': item.get('title'),
                'slug': item.get('slug'),
                'colecao': nome_colecao
            }
            metadata = item.get('metadata', {})
            for meta_id, meta_obj in metadata.items():
                nome = meta_obj.get('name')
                valor_bruto = meta_obj.get('value')

                if isinstance(valor_bruto, list):
                    valor = ", ".join(
                        v.get("name", str(v)) if isinstance(v, dict) else str(v)
                        for v in valor_bruto
                    )
                elif isinstance(valor_bruto, dict):
                    valor = valor_bruto.get("name", str(valor_bruto))
                else:
                    valor = valor_bruto

                linha[nome] = valor

            writer.writerow(linha)

    print(f"\n✅ Arquivo CSV salvo como: {nome_csv}")

# Execução principal
if __name__ == "__main__":
    base_items_url = "https://museuregionaldecaete.acervos.museus.gov.br/wp-json/tainacan/v2/collection/848/items/?perpage=96&order=ASC&orderby=date&paged=1"

    nome_museu = extrair_nome_museu(base_items_url)
    itens = fetch_all_items(base_items_url)
    nome_colecao = extrair_nome_colecao_dos_metadados(itens)

    salvar_csv(itens, nome_museu, nome_colecao)
