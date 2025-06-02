## Testes de Segurança com Foco em IDOR usando "IDOR Scanner CLI" ## /

Este manual foi elaborado para guiar você no universo dos testes de segurança de aplicações, com um foco especial na vulnerabilidade IDOR (Insecure Direct Object Reference) e no uso da ferramenta "IDOR Scanner CLI".

🎯 O Que São Testes de Segurança de Aplicações?
Testes de segurança são processos cruciais para identificar e corrigir falhas em softwares que poderiam ser exploradas por invasores. O objetivo é garantir a confidencialidade, integridade e disponibilidade dos dados e funcionalidades da aplicação.

Neste manual, nosso foco é a IDOR, uma das vulnerabilidades mais comuns e impactantes.

Parte 1: Entendendo a Vulnerabilidade IDOR
✅ O QUE É IDOR?
IDOR (Insecure Direct Object Reference), ou Referência Direta Insegura a Objeto, ocorre quando uma aplicação web permite que um usuário acesse diretamente objetos (como arquivos, registros de banco de dados, IDs de usuários) sem verificar adequadamente se ele tem permissão para tal.

Simplificando: o sistema confia demais no que o usuário envia (ex: um ID na URL) e não checa se aquele recurso específico pode ser acessado por ele.

🔍 EXEMPLO CLÁSSICO DE IDOR
Imagine a seguinte URL para visualizar uma conta:
https://sistema.com/conta/visualizar?id=1234

Se o usuário João acessa este link, ele vê sua conta (ID 1234). Tudo certo.
Agora, se João altera o ID na URL para id=1235 e, com isso, consegue ver a conta de Maria, temos uma falha IDOR. O sistema não validou se João (usuário autenticado) tinha permissão para ver o recurso com id=1235.

🛠️ COMO ELA PODE SER EXPLORADA?
Um atacante pode tentar explorar uma IDOR de várias formas:

Enumeração de IDs: Alterar sequencialmente o valor do ID na URL ou em um parâmetro.
Ex: /documento/42 → /documento/43, /documento/44...
Brute Force Automatizado: Usar scripts ou ferramentas (Burp Suite, OWASP ZAP, curl) para testar milhares de IDs rapidamente.
Fuzzing: Enviar parâmetros aleatórios ou previsíveis para descobrir quais objetos estão acessíveis.
Manipulação de Formulários: Interceptar e modificar requisições (ex: POST, PUT) usando ferramentas como Burp Suite para alterar dados de outro usuário (ex: redefinir senha, mudar e-mail).
🔓 RISCOS: QUAIS DADOS E SISTEMAS PODEM SER COMPROMETIDOS?
A exploração de IDOR pode comprometer uma vasta gama de recursos e dados sensíveis:

📄 Dados Sensíveis:
Informações pessoais (nome, CPF, e-mail, endereço)
Documentos confidenciais (contratos, laudos, prontuários médicos)
Dados financeiros (faturas, saldo, extratos)
🔐 Funcionalidades Sensíveis:
Alterar dados de outros usuários
Baixar arquivos restritos
Excluir registros de outros usuários
Acessar logs, relatórios internos, e até mesmo senhas (em casos mal implementados)
📉 CONSEQUÊNCIAS DIRETAS
Violação de privacidade: Exposição de dados pessoais, ferindo leis como LGPD (Brasil) e GDPR (Europa).
Roubo de identidade: Uso indevido de informações pessoais.
Modificação ou exclusão de dados de terceiros: Impacto direto na integridade dos dados.
Acesso não autorizado a informações corporativas: Risco para segredos de negócio e dados estratégicos.
Comprometimento da reputação institucional: Perda de confiança de clientes e parceiros.
Parte 2: Prevenção e Mitigação de IDOR
🔐 COMO PREVENIR IDOR?
Controle de Acesso Rígido: A regra de ouro! Para cada requisição, o backend DEVE verificar se o usuário autenticado tem permissão para acessar/modificar o objeto solicitado.
Evitar IDs Previsíveis: Em vez de usar números sequenciais (ex: id=1, id=2), opte por UUIDs (Identificadores Únicos Universais), que são longos e difíceis de adivinhar (ex: id=5c4f20a1-f0f3-4b3b-95c4-b8e47ed32f3e).
Validação no Backend (Servidor): Nunca confie apenas em validações feitas no frontend (navegador do usuário), pois elas podem ser facilmente burladas. Toda validação crítica deve ocorrer no servidor.
Auditoria e Logs: Monitore requisições suspeitas, especialmente aquelas que parecem enumeração de objetos. Logs detalhados ajudam na investigação de incidentes.
Testes de Segurança Regulares: Realize testes de invasão (pentests) e análises dinâmicas (DAST) com foco em IDOR. Esta vulnerabilidade está contemplada na categoria "Broken Access Control" (Controle de Acesso Quebrado) do OWASP Top 10.
🧩 A RELAÇÃO ENTRE IDOR E PHISHING
Embora diferentes, IDOR e Phishing compartilham similaridades e podem ser devastadores juntos:

Confiança Excessiva:
Phishing: Engana o usuário para que confie em um link/e-mail falso.
IDOR: Explora a confiança do sistema em parâmetros fornecidos pelo usuário.
Vazamento de Dados:
Phishing: Pode capturar credenciais e dados via sites falsos.
IDOR: Permite acesso direto a dados de outros usuários.
Ataques Combinados (Encadeados):
Um Phishing bem-sucedido pode dar ao atacante credenciais válidas (sessões, tokens).
Com essas credenciais, o atacante pode explorar IDORs para acessar ainda mais dados.
Prevenção em Duas Frentes:
Phishing: Usuários devem ser treinados para desconfiar e verificar.
IDOR: Desenvolvedores devem implementar controles de acesso robustos.
Em campanhas de conscientização, use frases como:

"Um clique descuidado (Phishing) pode abrir a porta. Uma falha no sistema (IDOR) pode deixá-la escancarada."
"Phishing engana pessoas. IDOR engana sistemas. Juntos, o estrago é maior."

Parte 3: A Ferramenta "IDOR Scanner CLI"
💡 O QUE É O "IDOR SCANNER CLI"?
O "IDOR Scanner CLI" é um script Python desenvolvido para auxiliar na detecção de vulnerabilidades IDOR em ambientes de teste controlados e autorizados. Ele automatiza o processo de testar diferentes IDs em um parâmetro de URL, comparando as respostas para identificar potenciais acessos indevidos.

⚠️ CONSIDERAÇÕES ÉTICAS E LEGAIS IMPORTANTÍSSIMAS!
USO RESTRITO: Esta ferramenta SÓ PODE SER USADA em sistemas que você possui, administra, ou tem autorização expressa e formal para testar.
ILEGALIDADE: Testar sistemas de terceiros sem consentimento é crime (no Brasil, Lei nº 12.737/2012 - Lei Carolina Dieckmann, e Art. 154-A do Código Penal; além do Marco Civil da Internet).
FOCO DIDÁTICO E CONTROLADO: Use para aprendizado, treinamento de equipes de segurança/desenvolvimento, ou em ambientes de CTF (Capture The Flag) e laboratórios internos.
NÃO NOS RESPONSABILIZAMOS PELO MAU USO DESTA FERRAMENTA OU DAS INFORMAÇÕES AQUI CONTIDAS.

📦 REQUISITOS
Para usar o "IDOR Scanner CLI", você precisará ter Python instalado e as seguintes bibliotecas:

requests: Para fazer as requisições HTTP.
rich: Para exibir tabelas coloridas e formatadas no terminal.
fpdf: Para gerar relatórios em PDF.
🔧 INSTALAÇÃO DAS BIBLIOTECAS
Abra seu terminal ou prompt de comando e execute:

Bash

pip install requests rich fpdf
Parte 4: Usando o "IDOR Scanner CLI"
O script é projetado para testar uma lista de alvos, cada um com sua configuração específica.

⚙️ CONFIGURAÇÃO DOS ALVOS (NO SCRIPT idor_scanner.py)
Você precisará editar o script Python (idor_scanner.py ou nome similar) e localizar a variável ALVOS. Ela é uma lista de dicionários, onde cada dicionário representa um sistema a ser testado.

Estrutura de um alvo:

Python

ALVOS = [
    {
        "nome": "Nome Descritivo do Sistema Testado",  # Ex: "Sistema de Pedidos Interno - API v1"
        "base_url": "http://seu.sistema.controlado/recurso?parametro_id=", # Ex: "http://localhost/app_teste/ver_perfil?usuario_id="
        "id_valido": "ID_QUE_VOCE_TEM_ACESSO_VALIDO", # Ex: "100" (um ID que você sabe que existe e pode acessar)
        "id_range": range(ID_INICIAL_TESTE, ID_FINAL_TESTE_MAIS_1) # Ex: range(101, 110) -> testa de 101 a 109
    },
    {
        "nome": "Outro Sistema de Teste",
        "base_url": "https://ambiente.homologacao/api/documentos?doc_id=",
        "id_valido": "user_A_doc_5", # Pode ser string também
        "id_range": [f"user_B_doc_{i}" for i in range(1, 6)] # Exemplo de IDs não numéricos em um range
    }
    # Adicione mais dicionários de alvos aqui, se necessário
]
nome: Um nome para identificar o alvo no relatório.
base_url: A URL base do endpoint que você quer testar, incluindo o parâmetro de ID e o sinal de igual (=) no final.
id_valido: Um ID que você tem permissão para acessar e que retornará uma resposta "base" ou "esperada". O conteúdo desta resposta será usado como referência.
id_range: Uma sequência de IDs que você quer testar. Pode ser um range() para números sequenciais ou uma lista de strings para IDs mais complexos.
🚀 PASSO A PASSO PARA EXECUÇÃO
Prepare os Sistemas de Teste:

Identifique as URLs e os parâmetros de ID que você suspeita serem vulneráveis ou que deseja testar.
Obtenha um id_valido para cada sistema.
Defina o id_range para os testes.
Lembre-se: Use apenas ambientes próprios ou autorizados (ex: DVWA, OWASP Juice Shop, Mutillidae, ou seus sistemas em ambiente de homologação/desenvolvimento).
Edite o Array ALVOS no Script:

Abra o arquivo .py do IDOR Scanner CLI em um editor de texto ou IDE.
Modifique a variável ALVOS conforme o exemplo acima, adicionando as informações dos sistemas que você vai testar.
Execute o Script:

Certifique-se de que os sistemas alvo estão acessíveis pela máquina onde o script será executado (ex: mesma rede, VPN, localhost).
No terminal, navegue até o diretório onde o script está salvo e execute:
Bash

python idor_scanner.py
(Substitua idor_scanner.py pelo nome real do seu arquivo, se for diferente).
📊 INTERPRETANDO OS RESULTADOS
O script fornecerá saídas em dois lugares:

No Terminal:

Uma tabela será exibida para cada alvo, mostrando:
ID: O ID que foi testado.
Status: O código de status HTTP da resposta (ex: 200 para OK, 403 para Proibido, 404 para Não Encontrado).
Diferente da Resposta Base?: SIM ou NÃO.
SIM: Indica que o conteúdo da página para este ID testado foi DIFERENTE do conteúdo da página do id_valido.
NÃO: Indica que o conteúdo foi igual.
URL Testada: A URL completa que foi acessada.
Mitigação Sugerida: Uma sugestão genérica de correção.
Atenção aqui:

Um Status: 200 (OK) junto com Diferente da Resposta Base?: SIM é um FORTE INDICATIVO DE IDOR! Significa que o sistema retornou conteúdo diferente (possivelmente de outro usuário/objeto) e permitiu o acesso.
Outros status (401, 403, 404) com SIM geralmente são esperados, pois indicam que o acesso foi negado ou o recurso não existe, o que é bom.
Um Status: 200 com NÃO pode indicar que o sistema está retornando a sua própria página ou uma página de erro genérica com status 200, o que requer análise manual.
Relatórios em PDF:

Para cada alvo testado, um relatório em PDF será gerado e salvo na pasta ./resultados_idor (esta pasta será criada automaticamente se não existir).
O nome do arquivo PDF será algo como relatorio_idor_Nome do sistema.pdf.
O PDF conterá as mesmas informações da tabela do terminal, servindo como evidência dos testes.
🔐 (OPCIONAL) ADICIONANDO AUTENTICAÇÃO (HEADERS, COOKIES)
Se os sistemas que você está testando requerem autenticação (ex: um token Bearer, um cookie de sessão):

Adicione headers ou cookies ao dicionário do alvo:

Python

ALVOS = [
    {
        "nome": "Sistema com Autenticação",
        "base_url": "http://auth.sistema.controlado/api/dados?item_id=",
        "id_valido": "meu_item_1",
        "id_range": range(1, 10),
        "headers": {
            "Authorization": "Bearer SEU_TOKEN_JWT_AQUI",
            "X-Custom-Header": "ValorCustomizado"
        },
        # Ou para cookies:
        # "cookies": {
        #     "session_id": "VALOR_DO_SEU_COOKIE_DE_SESSAO"
        # }
    }
]
Modifique a chamada requests.get() no script:
O script fornecido no contexto original já parece ter uma lógica para buscar headers ou cookies no dicionário do alvo e usá-los na requisição requests.get(). Se o seu script não tiver, você precisaria ajustar a parte onde requests.get() é chamado, algo como:

Python

# Dentro da função analisar_alvo() ou similar
# ...
target_headers = alvo.get("headers", {})
target_cookies = alvo.get("cookies", {})
resposta = requests.get(url, headers=target_headers, cookies=target_cookies, timeout=10)
# ...
Verifique a implementação do seu script específico.

Parte 5: Boas Práticas e Próximos Passos
✨ BOAS PRÁTICAS EM TESTES DE IDOR
Sempre em Ambientes Homologados ou Sandbox: Nunca teste em produção sem autorização explícita e planejamento cuidadoso (e mesmo assim, é arriscado).
Autorização Formal: Tenha permissão por escrito do proprietário do sistema antes de iniciar qualquer teste.
Documente Tudo: Mantenha registros dos testes realizados, configurações, resultados e evidências. Os relatórios PDF ajudam nisso.
Integre em Pipelines de Segurança (DevSecOps): Testes de segurança, incluindo para IDOR, devem ser parte do ciclo de desenvolvimento de software.
Não Confie Apenas em Ferramentas: A ferramenta auxilia, mas a análise humana é crucial para confirmar vulnerabilidades e entender o contexto.
📄 DOCUMENTAÇÃO TÉCNICA RESUMIDA DO "IDOR SCANNER CLI" (Conforme Contexto Fornecido)
Objetivo: Detectar potenciais IDORs comparando respostas de um ID autorizado com outros IDs.
Funcionamento:
Configuração de Alvos: Define ALVOS com nome, base_url, id_valido, id_range (e opcionalmente headers/cookies).
Fase de Testes: Para cada alvo:
Acessa id_valido para obter conteúdo base.
Varre id_range, acessando cada ID.
Compara conteúdo da resposta com o base.
Registra status HTTP e se houve diferença.
Relatórios: Gera tabela no terminal e PDF em ./resultados_idor com os achados.
Mitigações Sugeridas (Pelo Script): "Restringir acesso baseado em sessão/autorização."
🛠️ MITIGAÇÕES SUGERIDAS (E POR QUE SÃO IMPORTANTES)
Quando o script sugere "Restringir acesso baseado em sessão/autorização", ele está apontando para a causa raiz da maioria das IDORs:

Validar Propriedade: Antes de exibir ou permitir a alteração de um objeto (ex: documento com id=105), o sistema DEVE verificar: "O usuário atualmente logado (identificado pela sua sessão/token) é o dono deste documento ou tem permissão explícita para acessá-lo?".
Controles no Backend: Esta validação deve ocorrer no servidor (backend), não apenas no cliente (frontend).
Mapeamento Indireto (Opcional, mas bom): Em vez de expor IDs diretos do banco de dados na URL, use um mapeamento para IDs específicos da sessão do usuário. Por exemplo, em vez de /documento?id=123, poderia ser /meus_documentos/1 (onde '1' é o primeiro documento daquele usuário).
🔮 EXTENSÕES FUTURAS POSSÍVEIS (PARA DESENVOLVEDORES DO SCRIPT)
Suporte mais robusto a diferentes tipos de autenticação.
Detecção de outros tipos de fragilidades (ex: enumeração de usuários, exposição de dados sensíveis em respostas que não sejam IDOR direto).
Exportação de relatórios para outros formatos (CSV, JSON, HTML).
Envio automático de relatórios por e-mail.
Interface gráfica (CLI mais interativa ou interface Web básica).
Conclusão
A vulnerabilidade IDOR é séria, mas compreensível e, mais importante, prevenível. O uso consciente e ético de ferramentas como o "IDOR Scanner CLI" em ambientes controlados pode ser um grande aliado para desenvolvedores e testadores na construção de aplicações mais seguras.

Lembre-se: a segurança é um processo contínuo, e a responsabilidade é compartilhada!