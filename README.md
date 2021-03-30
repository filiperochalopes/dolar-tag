# Django Contabilidade Residencial

## Iniciando projeto
```sh
# Para rodar o pyenv, disponibilizando-o no shell
source ~/.bashrc # Python 3.9.2
python manage.py runserver 0.0.0.0:8000
```

## Comando importantes
```sh
# Criar migration atualizada com base nas classes
python manage.py makemigrations
```

## To watch/compile sass
```sh
python manage.py sass contabilidade_residencial/core/static/scss/ contabilidade_residencial/core/static/css/ --watch
python manage.py sass contabilidade_residencial/core/static/scss/ contabilidade_residencial/core/static/css/ -t compressed
```