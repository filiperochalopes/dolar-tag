# Dólar Tag v2

Um projeto facilitar a análise de despesas, etiquetando cada transação de forma prática. Queremos saber para onde o dólar foi! A versão 2 está reformulada para atingir um MVP funcional de registro de despesas com Flask. 

A manipulação de usuários é dado por cli utilizando Typer

## Experimento ChatGPT

Para agilizar o processo, conhecendo dos frameworks utilizados, lancei mão do ChatGPT-4 para facilitar a construção desse MVP

A conversa pode ser [acessada nesse link](https://chatgpt.com/share/62ca6ff5-135c-4662-b08d-66d5b916992c)

## Executando ambiente de desenvolvimento

```sh
python run.py
flask db upgrade
python cli.py create-user username password
```