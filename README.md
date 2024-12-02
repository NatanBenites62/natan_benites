# natan_benites



- [natan\_benites](#natan_benites)
- [1. Introdução](#1-introdução)
- [2. Descrição do negócio](#2-descrição-do-negócio)
- [3. Visão geral do sistema](#3-visão-geral-do-sistema)
- [4. Diagrama ER](#4-diagrama-er)
- [5. Diagrama de classe](#5-diagrama-de-classe)
- [6. Casos de uso](#6-casos-de-uso)
  - [6.1. Histórias de usuário](#61-histórias-de-usuário)
- [7. Diagrama de Componentes](#7-diagrama-de-componentes)
- [8. Diagrama de Implantação](#8-diagrama-de-implantação)
- [9. Protótipo de telas](#9-protótipo-de-telas)
- [10. Diagrama e navegação de telas](#10-diagrama-e-navegação-de-telas)
- [11. Pilha tecnológica](#11-pilha-tecnológica)
- [12. Requisitos de sistema](#12-requisitos-de-sistema)
- [13. Considerações sobre segurança](#13-considerações-sobre-segurança)
- [14. Manutenção e instalação](#14-manutenção-e-instalação)
- [15. Glossário](#15-glossário)
- [16. Script SQL](#16-script-sql)
  - [16.1 Comandos CREATE Table](#161-comandos-create-table)
  - [16.2 Comandos INSERT gerando dados fictícios](#162-comandos-insert-gerando-dados-fictícios)


# 1. Introdução

    O projeto de a seguir apresenta um sistema desenvolvidor para uma petshop. A empresa é considerada micro e iniciou as atividades recentemente. Ao possuir serviços exclusivos, os sistemas presentes no mercado não se enquadram, desta forma, os proprietários decidiram desenvolver uma solução própria.

# 2. Descrição do negócio

Descrição do cenário onde o sistema deverá funcionar:

1. Marcar animais com RFID.
2. Uma clínica veterinária atende apenas os animais: gatos e cachorros.
3. Os clientes devem fazer um cadastro de si e dos animais.
4. Os clientes devem informar o tipo de ração que o animal come.
5. O cliente deve informar hábitos do animal.
6. Para cada animal é possível que mais de um veterinário o atenda.
7. Os animais podem chegar e serem atendidos de acordo com uma agenda do dia.
8. Cada animal atendido receberá uma ficha e um prontuário.
9. Outros dono podem querer marcar horários de atendimento futuro.
10. O atendimento gera uma receita para o animal.
11. Quando um cliente chega na clínica veterinária ele é atendido por um atendente.
12. O atendente deve verificar se existe agenda disponível com um veterinário.
13. O atendente deve colocar o cliente e seu animal na fila de espera, se for o caso.
14. O atendente deve levar o cliente e o animal até o veterinário.
15.  veterinário deve realizar uma entrevista com o dono do animal.
16.  O resultado da entrevista deve ir para um formulário
17.  O veterinário deverá examinar o animal e anotar em prontuário(ficha) suas observações.
18.  Dependendo da situação do animal este receberá uma receita.
19.  Registrar um histórico de visitas do animal.
20.  Comércio de roupas e brinquedos para os animais.
21.  Banho e tosa dos animais.
22.  Receita ganha com cada cliente

# 3. Visão geral do sistema

# 4. Diagrama ER

```mermaid

erDiagram
    CLIENTE {
        int id_cliente PK
        string nome
        string telefone
        string endereco
        string pagamento_permuta
    }

   ANIMAL {
        int id_animal PK
        string nome
        string tipo
        string raca
        string habitos
        string rfid
    }
    
    VETERINARIO {
        int id_veterinario PK
        string nome
        string especialidade
        string telefone
    }
    
    ATENDENTE {
        int id_atendente PK
        string nome
    }
    
    RECEITA {
        int id_receita PK
        string descricao
        date data
    }
    
    FICHA {
        int id_ficha PK
        string observacoes
    }
    
    PRONTUARIO {
        int id_prontuario PK
        int id_animal FK
        int id_ficha FK
    }

    VISITA {
        int id_visita PK
        date data
        int id_animal FK
        int id_veterinario FK
        int id_ficha FK
        int id_receita FK
    }

    AGENDA {
        int id_agenda PK
        date data
        int id_veterinario FK
        int id_animal FK
    }
    
    PRODUTO {
        int id_produto PK
        string nome
        float preco
    }
    
    SERVICO {
        int id_servico PK
        string descricao
        float preco
    }
    CLIENTE ||--o{ ANIMAL : "possui"
    ANIMAL ||--o{ VETERINARIO : "é atendido por"
    VETERINARIO ||--o{ VISITA : "realiza"
    CLIENTE ||--o{ VISITA : "marca"
    ANIMAL ||--o{ VISITA : "participa"
    VETERINARIO ||--o{ AGENDA : "tem"
    ANIMAL ||--o{ AGENDA : "é agendado para"
    VISITA ||--o{ RECEITA : "gera"
    VISITA ||--o{ FICHA : "gera"
    FICHA ||--o{ PRONTUARIO : "é parte de"
    CLIENTE ||--o{ PRODUTO : "compra"
    CLIENTE ||--o{ SERVICO : "solicita"
    CLIENTE ||--o{ ATENDENTE : "é atendido por"
```
# 5. Diagrama de classe

```mermaid

classDiagram
    class Cliente {
        +int id
        +String nome
        +String telefone
        +String endereco
        +boolean pagamentoPermuta
        +registrarAnimal(Animal animal)
        +comprarProduto(Produto produto)
        +solicitarServico(Servico servico)
        +agendarAtendimento(Animal animal, Veterinario vet)
    }

    class Animal {
        +int id
        +String nome
        +String tipo (gato/cachorro)
        +String raca
        +String habitos
        +String rfid
        +String tipoRacao
        +receberAtendimento()
        +adicionarFicha(Ficha ficha)
        +gerarProntuario()
    }

    class Veterinario {
        +int id
        +String nome
        +String especialidade
        +String telefone
        +entrevistarCliente(Cliente cliente, Animal animal)
        +examinarAnimal(Animal animal)
        +registrarReceita(Receita receita)
    }

    class Atendente {
        +int id
        +String nome
        +verificarAgenda(Veterinario vet)
        +colocarNaFila(Cliente cliente, Animal animal)
        +levarParaVeterinario(Cliente cliente, Animal animal, Veterinario vet)
    }

    class Receita {
        +int id
        +String descricao
        +Date data
    }

    class Ficha {
        +int id
        +String observacoes
    }

    class Prontuario {
        +int id
        +Animal animal
        +Ficha ficha
        +gerarReceita()
    }

    class Visita {
        +int id
        +Date data
        +Animal animal
        +Veterinario veterinario
        +Ficha ficha
        +Receita receita
    }

    class Agenda {
        +int id
        +Date data
        +Veterinario veterinario
        +Animal animal
    }

    class Produto {
        +int id
        +String nome
        +float preco
    }

    class Servico {
        +int id
        +String descricao
        +float preco
    }

    Cliente "1" --o "*" Animal : "possui"
    Animal "1" --o "*" Veterinario : "é atendido por"
    Veterinario "1" --o "*" Visita : "realiza"
    Cliente "1" --o "*" Visita : "marca"
    Animal "1" --o "*" Visita : "participa"
    Veterinario "1" --o "*" Agenda : "tem"
    Animal "1" --o "*" Agenda : "é agendado para"
    Visita "1" --o "1" Receita : "gera"
    Visita "1" --o "1" Ficha : "gera"
    Ficha "1" --o "1" Prontuario : "é parte de"
    Cliente "1" --o "*" Produto : "compra"
    Cliente "1" --o "*" Servico : "solicita"
    Cliente "1" --o "1" Atendente : "é atendido por"
```

# 6. Casos de uso

## 6.1. Histórias de usuário

# 7. Diagrama de Componentes

# 8. Diagrama de Implantação

# 9. Protótipo de telas

# 10. Diagrama e navegação de telas

```mermaid
graph TD
    Login[Login] -->|Acesso Válido| Menu[Menu Principal]
    Login -->|Acesso Inválido| Erro[Mensagem de Erro]
    
    Menu --> Cadastro[Cadastro de Cliente e Animal]
    Menu --> Agendamento[Agendamento]
    Menu --> Atendimento[Atendimento]
    Menu --> Comercio[Comércio]
    Menu --> BanhoETosa[Banho e Tosa]
    Menu --> Historico[Histórico de Visitas]

    Cadastro --> CadastroCliente[Cadastro de Cliente]
    Cadastro --> CadastroAnimal[Cadastro de Animal]

    Agendamento --> AgendarConsulta[Agendar Consulta]
    Agendamento --> FilaEspera[Fila de Espera]

    Atendimento --> Entrevista[Entrevista com Dono]
    Atendimento --> Exame[Exame do Animal]
    Atendimento --> Receita[Prescrição de Receita]
    Atendimento --> Prontuario[Atualização de Prontuário]

    Comercio --> Produtos[Roupas e Brinquedos]
    Comercio --> Pagamento[Pagamento]

    BanhoETosa --> MarcarBanho[Agendar Banho]
    BanhoETosa --> MarcarTosa[Agendar Tosa]

    Historico --> ConsultarHistorico[Consultar Histórico]
    Historico --> DetalhesConsulta[Detalhes da Consulta]
```

# 11. Pilha tecnológica

```mermaid
graph TB
    Frontend[Frontend] --> Backend[Backend]
    Backend --> Database[Database]
    Backend --> RFID[RFID Scanner API]
    Backend --> AuthService[Serviço de Autenticação]
    Backend --> Scheduler[Gerenciador de Agendamento]
    Backend --> ProntuarioService[Serviço de Prontuário]
    Backend --> PaymentGateway[Gateway de Pagamento]

    Frontend --> Web["Web Application (React/Angular)"]
    Frontend --> Mobile["Mobile App (Flutter/React Native)"]

    Database --> RelationalDB[(PostgreSQL/MySQL)]
    Database --> NoSQLDB[(MongoDB para histórico e prontuários)]
    Database --> Cache[Redis para Cache de Dados]

    RFID --> Hardware[RFID Scanner Hardware]
    AuthService --> OAuth[OAuth/JWT]
    PaymentGateway --> ExternalAPI[API de Processamento de Pagamentos]

    Scheduler --> NotificationService[Serviço de Notificações]
    NotificationService --> Email[Email]
    NotificationService --> SMS[SMS]
    NotificationService --> Push[Push Notifications]
```

# 12. Requisitos de sistema

# 13. Considerações sobre segurança

# 14. Manutenção e instalação

# 15. Glossário

# 16. Script SQL

## 16.1 Comandos CREATE Table 

## 16.2 Comandos INSERT gerando dados fictícios