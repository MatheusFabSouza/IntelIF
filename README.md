# Sobre

O **IntelIF** é um sistema desenvolvido para auxiliar estudantes na organização da sua rotina acadêmica pessoal. A proposta da plataforma é reunir, em um único ambiente, recursos como matérias, arquivos, anotações, tarefas, calendário e quadros de organização, facilitando o acompanhamento das atividades do meio acadêmico de forma prática e centralizada.

Este projeto foi idealizado como parte de um trabalho acadêmico, com foco em criar uma ferramenta funcional e voltada às necessidades reais dos estudantes, permitindo maior controle sobre estudos, prazos e conteúdos, focado no Instituto Federal do Rio Grande do Norte.

## Funcionalidades principais

- Cadastro e organização de matérias
- Separação entre matérias institucionais e pessoais
- Upload e acesso de arquivos e documentos
- Criação de tópicos e anotações por matéria
- Filtros por data, bimestre e tipo de conteúdo
- Calendário com provas, trabalhos e eventos
- Criação de listas e tarefas de forma dinâmica
- Personalização de perfil do usuário
- Visualização de desempenho das matérias
- Integração com perfis de aluno, professor e gestor

## Tecnologias Utilizadas

- HTML5
- CSS3
- JavaScript
- Bootstrap

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

## Integrantes

- Lucas Thierry
- Matheus Fabricio
