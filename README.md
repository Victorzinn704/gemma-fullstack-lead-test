# Flask Login Lab

Aplicação didática de login e dashboard com sessões no servidor de aplicação,
hashes de senha, CSRF e contratos de autenticação separados da persistência.
Python 3.10+.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
cp .env.example .env
# Preencha SECRET_KEY no arquivo local com um valor aleatório de pelo menos 32 caracteres.
.venv/bin/flask --app run:app init-db
.venv/bin/flask --app run:app create-user meuusuario
.venv/bin/flask --app run:app run --host 127.0.0.1
.venv/bin/python -m pytest -q
```

Não há usuário/senha padrão e a senha é solicitada sem eco pelo comando de
criação. Não versione `.env` ou `instance/`. `COOKIE_SECURE=0` é apenas para
HTTP em localhost. Em HTTPS, configure `COOKIE_SECURE=1`.

Este laboratório não foi implantado. Antes de produção faltam migrações,
limitação distribuída de tentativas, recuperação de conta, observabilidade e
revisão de operação. Respostas genéricas de login evitam revelar diretamente
contas, mas não eliminam diferenças de tempo de execução.

Veja [arquitetura](docs/architecture.md) e [segurança](SECURITY.md).
