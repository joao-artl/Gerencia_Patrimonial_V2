# Histórias de Usuário 

## <a>1. Introdução </a>

De acordo PRESSMAN e MAXIM(2016)<a>^1^</a>, uma história de usuário é descrita como um elemento que descreve os resultados, características e funcionalidades que os usuários finais esperam do software a ser desenvolvido.

Em seu livro, PRESSMAN e MAXIM(2016)<a>^1^</a> também definem que a elaboração de uma história do usuário envolve o ato de escutar relatos do cliente que detalham as funcionalidades, características e resultados esperados do software. O cliente, por sua vez, atribui um valor de prioridade a cada história, baseando-se na importância relativa da funcionalidade para o negócio. Posteriormente, os membros da equipe avaliam cada história e determinam o custo associado, expresso em semanas de desenvolvimento, proporcionando uma base para a alocação de recursos e planejamento.

## <a>2. Metodologia </a>

A Tabela 1 a seguir apresenta um template para a elaboração de histórias de usuário dentro do projeto. A tabela é dividida em quatro colunas principais: ID, Título, Descrição e Critérios de Aceitação. Facilitando a organização e a referência cruzada das informações.

<center>

<font size="3"><p style="text-align: center"><b>Tabela 1</b> - Template de tabela para histórias de usuário.</p></font>

| **ID**|**Título** |**Descrição** | **Critérios de Aceitação** | 
| :-----|-- |:--------|------------------------------ | 
| USXX  |Título da História de Usuário|Eu, como um_ [tipo usuário],<br> _gostaria que_ [compromisso com as tarefas], <br> _afim de que_ [objetivo a ser alcançado].|<a>1</a> - "*Critério nº1*" <br> <a>2</a> - "*Critério nº2*" <br>... |

<font size="3">Fonte: [João Artur](https://github.com/joao-artl).</font>

</center>

## <a>3. Histórias de Usuário </a>

A **Tabela 2** a seguir apresenta um resumo detalhado das histórias de usuário desenvolvidas para o projeto, seguindo os elementos descritos no **template da Tabela 1**.

<center>

<font size="3"><p style="text-align: center"><b>Tabela 2</b> - Histórias de Usuários e seus elementos.</p></font>

| **ID**  | **Título**     | **Descrição**      | **Critérios de Aceitação**      |
|---------|----------------------|-------------|--------------|
| **US01**| Cadastro de Empresa            | Eu, como administrador do sistema, gostaria de cadastrar novas empresas (nome, CNPJ, email, etc.), a fim de manter um registro completo. | <a>1</a> - Validar CNPJ e email. <br><a>2</a> - Campos obrigatórios: nome, CNPJ, email.                        |
| **US02**| Adicionar Filial               | Eu, como gestor, gostaria de adicionar filiais a uma empresa matriz, a fim de organizar a estrutura hierárquica.          | <a>1</a> - Vincular filial a empresa existente. <br><a>2</a> - Listar filiais por empresa.                     |
| **US03**| Cadastro de Itens de Patrimônio| Eu, como responsável pelo patrimônio, gostaria de cadastrar itens (veículos, imóveis, etc.), a fim de controlar os bens. | <a>1</a> - Definir tipo específico (veículo/imobiliário). <br><a>2</a> - Campos obrigatórios: nome, valor, quantidade. |
| **US04**| Listagem de Patrimônios        | Eu, como auditor, gostaria de visualizar todos os itens de uma filial, a fim de realizar inventários.                     | <a>1</a> - Incluir nome, tipo e valor total. <br><a>2</a> - Filtrar por tipo (ex: veículos).                   |
| **US05**| Atualização de Veículos        | Eu, como gestor de frota, gostaria de atualizar dados de veículos (cor, modelo), a fim de manter informações precisas.    | <a>1</a> - Restringir edição a usuários autorizados. <br><a>2</a> - Campos obrigatórios: modelo, fabricante.    |
| **US06**| Relatório de Imóveis           | Eu, como diretor financeiro, gostaria de gerar relatório de imóveis, a fim de avaliar investimentos.                      | <a>1</a> Calcular valor total por filial.                                 |
| **US07**| Busca de Utilitários           | Eu, como funcionário do almoxarifado, gostaria de buscar utilitários por função, a fim de localizá-los rapidamente.       | <a>1</a> - Aceitar termos parciais (ex: "chave"). <br><a>2</a> - Mostrar quantidade disponível.                |

<font size="3">Fonte: [João Artur](https://github.com/joao-artl)</font>

</center>

## <a>Referência Bibliográfica</a>
> <a>1.</a> PRESSMAN, Roger S.; MAXIM, Bruce R.. Engenharia de software: uma abordagem profissional. 8 Porto Alegre: AMGH, 2016.

## <a>Histórico de versão</a>

| Versão | Data | Descrição | 
| :------: | :----------: | :-----------: |
| `1.0` | 09/05/2025 | Criação do documento de histórias de usuário |