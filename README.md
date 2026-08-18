## Sobre
Sistema de organização acadêmica para estudantes.

## Integrantes
- Lucas Thierry
- Matheus Fabricio

## Rodando
Siga as instruções abaixo para configurar o ambiente do projeto após clonar o repositório.

### 1. Criando e Ativando o Ambiente Virtual
```bash
python -m venv venv  
venv\Scripts\Activate.ps1
```

### 2. Instalando as Dependências
```bash
pip install -r requirements.txt  
```

### 3. Aplicando as Migrações
```bash
python manage.py migrate  
```

### 4. Criando um Superusuário
```bash
python manage.py createsuperuser  
```

Siga as instruções e defina um nome de usuário, e-mail e senha.

### 5. Executando o Servidor

```bash
python manage.py runserver  
```

### 6. Acessando o Django Admin

Abra o navegador e acesse:

```
http://127.0.0.1:8000/admin/
```

Faça login com o superusuário criado anteriormente.

Agora o **IntelIF** está pronto para ser utilizado!