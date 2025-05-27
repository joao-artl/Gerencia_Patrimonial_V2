# Gerencia Patrimonial V2
documentos do projeto:
- [Padrão de contribuição](https://joao-artl.github.io/Gerencia_Patrimonial_V2/#/./padraoCommit)
- [Backlog](https://joao-artl.github.io/Gerencia_Patrimonial_V2/#/./backlog)
- [UML](https://joao-artl.github.io/Gerencia_Patrimonial_V2/#/./uml)

## Como rodar

Na raiz do projeto:
```docker-compose up --build```

Com isso será possivel acessar http://localhost:8000

Além disso é possivel executar alguns comandos, 

*Para acessar o banco de dados:*

```docker-compose exec db psql -U admin -d gerenciapatrimonio```

*Para rodar os testes:*

```docker-compose exec web python manage.py test```

*ou:*
```docker-compose run --rm tests```
