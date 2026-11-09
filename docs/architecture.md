# Responsabilidades

As rotas e templates são adaptadores HTTP; `domain/auth.py` define os contratos
`Account` e `Users` e o caso de uso `Authentication`, sem dependência de Flask.
`infrastructure/users.py` adapta SQLAlchemy e `services/auth_service.py` monta
o serviço para as rotas. A factory registra extensões e comandos explícitos.

O navegador recebe somente cookie de sessão assinado e campos CSRF; o segredo
de assinatura e o banco ficam no servidor. Cookies Flask são assinados, não
criptografados: não coloque credenciais ou dados sensíveis na sessão.
Configuração de implantação vem do ambiente. O processo recusa segredo fraco.
Nenhum usuário é criado automaticamente ao importar ou iniciar a aplicação.

Os testes exercitam login, proteção de dashboard, logout POST, hash, rejeição
de chave fraca e o fluxo real de CSRF. Não se afirma TDD retroativo.
