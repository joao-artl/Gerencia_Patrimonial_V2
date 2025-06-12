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
| **US01**| Cadastro de Empresa | Eu, como administrador do sistema, gostaria de cadastrar novas empresas (nome, CNPJ, email, etc.), a fim de manter um registro completo. | <a>1</a> - Validar CNPJ e email. <br><a>2</a> - Campos obrigatórios: nome, CNPJ, email.|
| **US02**| Cadastro de Filial  | Eu, como gestor da empresa, gostaria de cadastrar filiais a uma empresa matriz, a fim de organizar a estrutura hierárquica. | <a>1</a> - Vincular filial a empresa existente. <br><a>2</a> - Listar filiais por empresa.                     |
| **US03**| Cadastro de Itens de Patrimônio| Eu, como funcionário responsável pelo patrimônio, gostaria de cadastrar itens (veículos, imóveis e utilitários.), a fim de controlar os bens. | <a>1</a> - Definir tipo específico (veículo/imobiliário/utilitário). <br><a>2</a> - Campos obrigatórios: nome, valor, quantidade. |
| **US04**| Listagem Consolidada de Patrimônios da Empresa | Eu, como gestor da empresa, gostaria de visualizar uma listagem consolidada de todos os itens de patrimônio pertencentes à empresa, a fim de realizar um inventário geral e ter uma visão macro dos ativos. | <a>1</a> - A listagem deve incluir: nome do item, tipo, valor individual e a filial à qual o item pertence. <br><a>2</a> - Deve ser apresentado o valor total consolidado de todos os patrimônios da empresa. <br><a>3</a> - Permitir a visualização de subtotais de valor por filial.|
| **US05**| Listagem de Patrimônios da Filial   | Eu, como gestor da empresa, gostaria de visualizar todos os itens de uma filial, a fim de realizar inventários.   |<a>1</a> - O sistema deve permitir que o gestor da empresa primeiro selecione a filial cujos patrimônios deseja visualizar. <br> <a>2</a> - A listagem deve incluir: nome, tipo e valor individual do patrimônio. <br><a>3</a> - Permitir filtrar os patrimônios por tipo (ex: veículos). |
| **US06**| Atualização de Dados de Item de Patrimônio | Eu, como funcionário responsável pelo patrimônio, gostaria de atualizar os dados cadastrais de um item de patrimônio, a fim de manter as informações atualizadas no sistema.  | <a>1</a> - O sistema deve permitir selecionar um item de patrimônio existente para edição. <br><a>2</a> - Devem ser apresentados os campos editáveis do item de patrimônio selecionado. <br><a>3</a> -  O sistema deve validar que campos definidos como obrigatórios para o tipo de patrimônio (ex: Nome) não fiquem vazios ou inválidos após a edição. |
| **US07**| Busca de Itens de Patrimônio | Eu, como funcionário da filial, gostaria de buscar itens de patrimônio utilizando diferentes critérios (ex: nome, tipo), a fim de localizá-los mais rapidamente. | <a>1</a> - O sistema deve oferecer campos de busca para múltiplos atributos  <br><a>2</a> -  Os resultados da busca devem ser apresentados em uma listagem clara, exibindo informações que permitam a identificação|
| **US08** | Edição de Informações da Empresa | Eu, como administrador do sistema, gostaria de poder editar as informações de uma empresa já existente, a fim de manter os dados sempre atualizados.| <a>1</a> - O CNPJ da empresa não pode ser alterado após o cadastro inicial. <br><a>2</a> - Todas as outras informações (nome, email, telefone, endereço) podem ser editadas. |
| **US09** | Edição de Informações da Filial | Eu, como gestor da empresa, gostaria de poder editar as informações de uma filial já existente, a fim de manter os dados da filial sempre atualizados.| <a>1</a> - O  CNPJ a empresa matriz à qual ela está vinculada não podem ser alterados após o cadastro inicial da filial. <br><a>2</a> - Todas as outras informações cadastrais da filial  podem ser editadas.|
| **US10**| Acessibilidade e Responsividade da Interface | Eu, como usuário do sistema, gostaria que todas as páginas e funcionalidades sejam acessíveis e se adaptem a diferentes dispositivos, a fim de garantir uma experiência de uso agradável, independentemente do dispositivo.| <a>1</a> - A interface do sistema deve se adaptar a diferentes resoluções de tela (desktops, tablets e smartphones), mantendo a legibilidade e usabilidade de todos os elementos. <br><a>2</a> - Todos os elementos interativos (botões, links, campos de formulário) devem ser facilmente acessíveis, visíveis e operáveis em telas de toque e com mouse/teclado.

<font size="3">Fonte: [João Artur](https://github.com/joao-artl)</font>

</center>

## <a>Referência Bibliográfica</a>
> <a>1.</a> PRESSMAN, Roger S.; MAXIM, Bruce R.. Engenharia de software: uma abordagem profissional. 8 Porto Alegre: AMGH, 2016.

## <a>Histórico de versão</a>

| Versão | Data | Descrição | 
| :------: | :----------: | :-----------: |
| `1.0` | 09/05/2025 | Criação do documento de histórias de usuário |
| `1.1` | 01/06/2025 | Atualizando e adicionando novas histórias de usuário |