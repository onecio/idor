import requests
import os
from rich.console import Console
from rich.table import Table
from rich.progress import track
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuração
ALVOS = [
    {
        "nome": "Recurso Público",
        "base_url": "https://example.com/resource?id=",
        "id_valido": "100",
        "id_range": range(101, 110)
    },
    # Adicione mais alvos conforme necessário
]

OUTPUT_DIR = "./resultados_idor"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Inicialização
console = Console()

def analisar_alvo(alvo):
    nome = alvo["nome"]
    base_url = alvo["base_url"]
    id_valido = alvo["id_valido"]
    id_range = alvo["id_range"]
    resultados = []
    conteudo_base = None

    try:
        resposta_base = requests.get(base_url + id_valido, timeout=10)
        resposta_base.raise_for_status()
        conteudo_base = resposta_base.text
    except requests.RequestException as e:
        console.print(f"[bold red]Erro ao acessar URL base '{nome}': {e}[/bold red]")
        return None

    console.print(f"\n[bold yellow]Iniciando varredura IDOR em: {nome}[/bold yellow]\n")

    for id_testado in track(id_range, description=f"Testando {nome}...", console=console, transient=True):
        url = f"{base_url}{id_testado}"
        try:
            resposta = requests.get(url, timeout=10)
            conteudo = resposta.text
            diferente = conteudo_base is not None and conteudo != conteudo_base
            resultados.append({
                "id": id_testado,
                "status": resposta.status_code,
                "diferente": diferente,
                "url": url
            })
        except requests.RequestException as e:
            resultados.append({
                "id": id_testado,
                "status": "ERRO",
                "diferente": False,
                "url": url,
                "erro": str(e)
            })
    return nome, resultados

def gerar_relatorio(nome, resultados):
    table = Table(title=f"Resultado IDOR - {nome}")
    table.add_column("ID")
    table.add_column("Status")
    table.add_column("Conteúdo diferente?", justify="center")
    table.add_column("URL Testada")
    table.add_column("Mitigação")

    for r in resultados:
        vulneravel = r.get("diferente")
        mitigacao = "Restringir acesso baseado em sessão/autorização" if vulneravel else "Sem vulnerabilidade detectada"
        table.add_row(str(r["id"]), str(r["status"]), "SIM" if vulneravel else "NÃO", r["url"], mitigacao)

    console.print(table)

    pdf_file = os.path.join(OUTPUT_DIR, f"relatorio_idor_{nome.replace(' ', '_')}.pdf")
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 40, f"Relatório de Teste IDOR - {nome}")
    c.drawString(100, height - 60, f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    linha_y = height - 90
    for r in resultados:
        vulneravel = r.get("diferente")
        mitigacao = "Restringir acesso baseado em sessão/autorização" if vulneravel else "Sem vulnerabilidade detectada"
        linha = f"ID: {r['id']} | Status: {r['status']} | Dif: {'SIM' if vulneravel else 'NÃO'} | URL: {r['url']} | Mitigação: {mitigacao}"
        if 'erro' in r:
            linha += f" | Erro: {r['erro']}"
        c.drawString(30, linha_y, linha)
        linha_y -= 15
        if linha_y < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            linha_y = height - 40

    c.save()
    console.print(f"\n[bold green]Relatório salvo em:[/bold green] {pdf_file}\n")

# Execução principal do aplicativo Idor
for alvo in ALVOS:
    resultado = analisar_alvo(alvo)
    if resultado:
        nome, resultados = resultado
        gerar_relatorio(nome, resultados)
    else:
        console.print(f"[bold red]Análise do alvo '{alvo['nome']}' não foi possível.[/bold red]")
