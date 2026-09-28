# Listagem de Requisitos

## Requisitos Funcionais (RF)

| Código | Nome | Descrição | Categoria |
| :--- | :--- | :--- | :--- |
| **RF001** | Realizar login via SUAP | O sistema deve permitir que alunos, servidores e gestores realizem autenticação utilizando sua conta institucional do SUAP. | Alta |
| **RF002** | Diferenciar permissões por perfil | O sistema deve identificar automaticamente o perfil do usuário autenticado (Aluno, Servidor ou Gestor) e conceder as permissões correspondentes. | Alta |
| **RF003** | Exibir calendário acadêmico | O sistema deve exibir um calendário com os eventos acadêmicos e pessoais do usuário autenticado. | Alta |
| **RF004** | Exibir eventos próximos | O sistema deve apresentar os próximos eventos, como provas, trabalhos, atividades e lembretes no dashboard pessoal do usuário. | Alta |
| **RF005** | Gerenciar eventos pessoais | O sistema deve permitir que alunos e professores criem, editem e excluam eventos pessoais em seus calendários. | Média |
| **RF006** | Classificar eventos | O sistema deve permitir classificar eventos por categorias, como prova, trabalho, estudo e evento pessoal. | Média |
| **RF007** | Restringir visualização de eventos pessoais | O sistema deve garantir que os eventos pessoais criados pelo aluno sejam visíveis apenas para seu proprietário. | Alta |
| **RF008** | Visualizar disciplinas institucionais | O sistema deve obter e exibir automaticamente as disciplinas do usuário por meio da integração com as APIs do Google Classroom e do SUAP. | Alta |
| **RF009** | Criar matérias personalizadas | O sistema deve permitir ao aluno criar matérias personalizadas. | Alta |
| **RF010** | Separar disciplinas institucionais e pessoais | O sistema deve distinguir as disciplinas importadas da instituição das matérias criadas pelo usuário. | Alta |
| **RF011** | Criar tópicos nas matérias | O sistema deve permitir a criação de tópicos dentro das matérias. | Média |
| **RF012** | Adicionar conteúdos | O sistema deve permitir adicionar arquivos, links e anotações dentro dos tópicos das matérias. | Alta |
| **RF013** | Registrar data dos conteúdos | O sistema deve registrar automaticamente a data de criação dos conteúdos adicionados. | Baixa |
| **RF014** | Associar conteúdos ao período letivo | O sistema deve permitir associar conteúdos a bimestres ou períodos letivos. | Média |
| **RF015** | Filtrar conteúdos | O sistema deve permitir filtrar conteúdos por disciplina, tipo, data e período letivo. | Alta |
| **RF016** | Definir status das matérias | O sistema deve permitir que o aluno classifique suas matérias com cores relacionadas ao status do usuário em relação a matéria. | Baixa |
| **RF017** | Destacar matérias com baixo desempenho | O sistema pode destacar matérias classificadas com baixo desempenho. | Baixa |
| **RF018** | Visualizar turmas | O sistema deve permitir que professores visualizem suas turmas. | Alta |
| **RF019** | Criar eventos para turmas | O sistema deve permitir que professores, grêmio e gestão e alunos com perfil de Líder criem eventos para suas turmas. | Alta |
| **RF020** | Compartilhar eventos com alunos | O sistema deve permitir que eventos criados pelos professores e líderes sejam exibidos no calendário dos alunos da turma correspondente. | Média |
| **RF021** | Visualizar turmas e atividades | O sistema deve permitir que gestores visualizem turmas, disciplinas e atividades acadêmicas. | Alta |
| **RF022** | Publicar comunicados da gestão | O sistema deve permitir que gestores publiquem comunicados e eventos relacionados à gestão acadêmica dos alunos. | Média |
| **RF023** | Monitorar utilização do sistema | O sistema deve permitir que gestores acompanhem indicadores de utilização da plataforma. | Média |
| **RF024** | Publicar avisos gerais | O sistema deve permitir que usuários do perfil Grêmio publiquem avisos gerais para toda a comunidade acadêmica, sem vínculo com turmas específicas. | Média |
| **RF025** | Criar quadros de organização | O sistema deve permitir a criação de quadros (*boards*) para organização pessoal. | Média |
| **RF026** | Criar listas | O sistema deve permitir criar listas como "A Fazer", "Fazendo" e "Concluído". | Baixa |
| **RF027** | Criar tarefas | O sistema deve permitir adicionar tarefas dentro das listas criadas pelo usuário. | Baixa |
| **RF028** | Gerenciar perfil | O sistema deve permitir que o usuário personalize informações do seu perfil, como foto e dados pessoais permitidos. | Baixa |
| **RF029** | Registrar histórico de acesso | O sistema deve registrar informações de auditoria, incluindo último login, usuário responsável pela ação e data/hora das operações realizadas. | Média |

---

## Requisitos Não Funcionais (RNF)

*(Nota: Corrigida a numeração de RF para RNF referente aos Requisitos Não Funcionais)*

| Código | Nome | Descrição | Categoria |
| :--- | :--- | :--- | :--- |
| **RNF001** | Segurança de autenticação | O sistema deve permitir acesso apenas a usuários autenticados por meio da conta institucional do SUAP. | Alta |
| **RNF002** | Responsividade | O sistema deve ser responsivo, permitindo sua utilização em computadores, tablets e dispositivos móveis. | Alta |
| **RNF003** | Usabilidade | O sistema deve possuir uma interface intuitiva, organizada e adequada ao ambiente acadêmico. | Alta |
| **RNF004** | Desempenho | O sistema deve apresentar tempo de resposta adequado durante a navegação e o carregamento das funcionalidades. | Alta |
| **RNF005** | Paginação | O sistema deve utilizar paginação ou carregamento progressivo para grandes volumes de dados, garantindo melhor desempenho. | Média |
| **RNF006** | Identidade visual | O sistema deve utilizar elementos visuais compatíveis com a identidade institucional do IFRN. | Média |
| **RNF007** | Consistência da interface | O sistema deve manter um padrão visual entre todas as telas e módulos da aplicação. | Média |
| **RNF008** | Disponibilidade das integrações | O sistema deve tratar falhas nas integrações com as APIs do SUAP e do Google Classroom, informando o usuário quando houver indisponibilidade dos serviços externos. | Alta |
| **RNF009** | Auditoria | O sistema deve registrar informações de auditoria, como último login, usuário responsável pelas ações e data/hora das operações realizadas de cada tipo de usuário. | Média |
| **RNF010** | Privacidade dos dados | O sistema deve garantir que eventos pessoais, conteúdos e informações privadas sejam acessíveis apenas aos usuários autorizados. | Alta |
| **RNF011** | APIs utilizadas | O sistema utilizará as APIs do Google Classroom e do Sistema Unificado de Administração Pública (SUAP). | Alta |