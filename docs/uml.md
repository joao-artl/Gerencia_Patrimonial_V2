# Diagramas UML (Unified Modeling Language)

## <a>1. Introdução</a>

Este documento descreve o diagrama de classes e pacotes do projeto. Os diagramas apresentam as classes principais do sistema, detalhando seus atributos, métodos e os tipos de relações que elas estabelecem entre si. Com essa representação, é possível compreender a estrutura do sistema e a distribuição das responsabilidades, além de servir como um guia para o desenvolvimento e a evolução da aplicação.

## <a>2. Diagrama de Classes</a>

O **diagrama de classes** é uma representação visual que ilustra a estrutura de um sistema, detalhando suas classes, atributos, métodos e os relacionamentos entre elas. Ele permite compreender como os componentes do sistema estão conectados e organizados, fornecendo uma visão clara e objetiva para apoiar tanto o design quanto o desenvolvimento da aplicação.

### <a>2.1. Diagrama</a>

<center>

<iframe src="./assets/DiagramaDeClasses.pdf" width="100%" height="600px" allowfullscreen></iframe>

_Fonte: [João Artur Leles](https://github.com/joao-artl)_

</center>

## <a>3. Diagrama de Pacotes</a>

O **diagrama de pacotes** é uma representação visual que organiza os elementos do sistema em unidades lógicas. Para este projeto, ele foi desenvolvido para espelhar a estrutura de aplicativos (apps) do [Django](https://docs.djangoproject.com/en/5.2/), que é o framework utilizado.

Isso significa que cada pacote no diagrama representa um app, evidenciando a modularização da aplicação e mostrando como eles se relacionam entre si. Ele serve como um guia visual para estruturar o projeto de forma coesa e escalável, garantindo a separação de responsabilidades.

### <a>3.1 Diagrama</a>

<center>

<iframe src="./assets/DiagramaDePacotes.pdf" width="100%" height="600px" allowfullscreen></iframe>

_Fonte: [João Artur Leles](https://github.com/joao-artl)_

</center>

## <a>Bibliografia</a>

> 1.</a> Fowler, M. (2004). _UML Distilled: A Brief Guide to the Standard Object Modeling Language_. Addison-Wesley.

> 2.</a> Larman, C. (2001). _Applying UML and Patterns_. Prentice Hall.

## <a>Histórico de versão</a>

| Versão | Data | Descrição | 
| :------: | :----------: | :-----------: |
| `1.0` | 09/05/2025 | Criação do documento dos diagramas UML |
| `1.1` | 01/06/2025 | Revisa e adapta diagrama de classes para convenções Python |
| `1.2` | 12/06/2025 | Adiciona usuários ao diagrama de classes e adapta diagrama de pacotes para o Django |