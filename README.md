# Sistema de Gerenciamento de APIs de Distribuição Musical
#### Plataforma Web Full-Stack para Gerenciamento Centralizado de Distribuidoras Musicais Digitais

Fábio Briddi

Este documento apresenta a documentação do projeto desenvolvido na unidade curricular Projeto de Desenvolvimento II do curso de Análise e Desenvolvimento de Sistemas do Centro Universitário Senac-RS. O sistema proposto visa unificar o gerenciamento de informações de distribuições musicais através das APIs das principais distribuidoras digitais (FUGA, The Orchard e Vydia) em uma interface integrada.

-----

## Resumo do Projeto

O presente projeto consiste no desenvolvimento de um sistema web full-stack para gerenciamento centralizado de APIs de distribuidoras musicais digitais. A fragmentação atual do ecossistema de distribuição digital, onde artistas e profissionais precisam lidar com interfaces distintas e dados dispersos entre diferentes distribuidoras, constitui um problema significativo de eficiência operacional. A solução proposta estabelece uma camada de abstração sobre as APIs das distribuidoras FUGA, The Orchard e Vydia, proporcionando interface unificada para gerenciamento de distribuições digitais. Como consequência, espera-se redução significativa no tempo dedicado a operações administrativas e melhoria na capacidade de análise comparativa de performance, permitindo que usuários concentrem esforços em aspectos criativos e estratégicos de suas carreiras musicais.

## Definição do Problema

No atual cenário da indústria musical digital, artistas independentes, gravadoras e agregadores enfrentam desafios significativos no gerenciamento de suas distribuições musicais. As principais distribuidoras digitais - FUGA, The Orchard e Vydia - operam de forma isolada, cada uma com sua própria API, padrões de dados, interfaces de usuário e processos operacionais distintos. Esta fragmentação resulta em diversos problemas práticos que impactam diretamente a produtividade e a capacidade competitiva dos profissionais da indústria musical.

Primeiramente, a necessidade de acessar múltiplas plataformas separadamente demanda tempo considerável e aumenta a probabilidade de erros operacionais. Profissionais precisam alternar entre diferentes sistemas, memorizar diferentes fluxos de trabalho e lidar com inconsistências nos formatos de dados retornados por cada distribuidora. Segundo dados da indústria, gestores de catálogo dedicam aproximadamente 40% de seu tempo apenas navegando entre diferentes plataformas e consolidando informações manualmente.

Em segundo lugar, a ausência de uma visão consolidada dificulta a análise comparativa de performance, impossibilitando a tomada de decisões estratégicas baseadas em dados agregados de todas as plataformas de distribuição. A falta de padronização nos relatórios e métricas entre distribuidoras torna o processo de benchmarking extremamente trabalhoso e propenso a interpretações inconsistentes.

Adicionalmente, pequenos artistas e gravadoras independentes frequentemente carecem de recursos técnicos para desenvolver integrações customizadas com cada API, limitando sua capacidade de competir efetivamente no mercado digital. A complexidade técnica das integrações, que exige conhecimento em autenticação OAuth, tratamento de rate limiting e normalização de dados heterogêneos, representa barreira significativa à entrada no mercado de distribuição digital.

O contexto atual demanda uma solução que simplifique o acesso às APIs das distribuidoras, centralize o gerenciamento de credenciais, padronize a visualização de dados e automatize operações comuns. Esta necessidade é corroborada pela crescente adoção de agregadores musicais, que segundo a IFPI (International Federation of the Phonographic Industry), representam canal crescente de distribuição, especialmente para artistas independentes que buscam otimizar seus processos operacionais.

### Projetos Correlatos

A análise de sistemas existentes no mercado revela que, embora existam plataformas de gerenciamento musical, nenhuma oferece integração abrangente e unificada com as demais distribuidoras simultaneamente. As Plataformas funcionam como distribuidoras próprias e não agregam dados de múltiplas distribuidoras externas. Esta lacuna no mercado justifica o desenvolvimento da solução proposta, que se diferencia por sua natureza integradora.

## Objetivos

### Objetivo Geral

Desenvolver uma plataforma web integrada que permita o gerenciamento centralizado de distribuições musicais através das APIs das distribuidoras digitais com a qual a cliente BRD tem relacionamento, proporcionando uma interface unificada para consulta, análise e administração de catálogos musicais.

### Objetivos Específicos

- Implementar sistema de autenticação robusto e seguro, garantindo controle de acesso com diferentes níveis de permissão;

- Desenvolver módulos de integração com as APIs das distribuidoras FUGA, The Orchard e Vydia, permitindo operações de consulta, cadastro e atualização de artistas e metadados musicais através de adaptadores especializados;

- Criar dashboards interativos com visualizações gráficas que consolidem dados de múltiplas distribuidoras, facilitando a análise comparativa de performance e métricas de distribuição;

- Estabelecer sistema seguro de gerenciamento de credenciais API;

- Desenvolver interface responsiva e intuitiva, seguindo padrões modernos de UX/UI estabelecidos pelo Material Design, reduzindo a curva de aprendizado e aumentando a produtividade dos usuários;

- Estabelecer sistema de logs e auditoria;

- Implementar arquitetura escalável utilizando serviços em nuvem, preparando o sistema para crescimento futuro e aumento de carga através de escalabilidade horizontal.

## Stack Tecnológico

A arquitetura tecnológica do projeto escolhida considerando requisitos de escalabilidade, segurança, performance e manutenibilidade, conforme recomendações de engenharia de software moderna. A solução adota uma arquitetura monorepo full-stack com separação clara entre camadas de apresentação e lógica de negócios.

### Backend

O backend foi desenvolvido utilizando Node.js, escolha justificada por sua arquitetura orientada a eventos que proporciona alta performance em operações I/O-bound, características essenciais para integração com múltiplas APIs externas. 

O framework Express.js foi selecionado para construção da API RESTful pela sua maturidade, extensibilidade através de middlewares e vasta comunidade de desenvolvimento. A escolha do TypeScript como linguagem principal justifica-se pela tipagem estática que melhora significativamente a manutenibilidade do código através de IntelliSense e refatoração automática.

### Frontend

A interface de usuário foi construída com React, biblioteca JavaScript que se tornou padrão de mercado para construção de interfaces de usuário componetizadas. A escolha do React justifica-se por sua arquitetura baseada em virtual DOM que proporciona performance otimizada, vasto ecossistema de bibliotecas complementares e suporte corporativo de longo prazo.


## Descrição da Solução

A solução desenvolvida consiste em uma plataforma web full-stack que estabelece uma camada de abstração sobre as APIs das distribuidoras musicais FUGA, The Orchard e Vydia, proporcionando interface unificada para gerenciamento de distribuições digitais. A arquitetura do sistema foi projetada seguindo princípios SOLID de design orientado a objetos e padrões de arquitetura em camadas, garantindo separação de responsabilidades, testabilidade e manutenibilidade do código.

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  ┌────────────┐  ┌────────────┐  ┌───────────────────┐ │
│  │ Components │  │  Services  │  │  State Management │ │
│  └────────────┘  └────────────┘  └───────────────────┘ │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTPS/REST
┌─────────────────────▼───────────────────────────────────┐
│              Backend API (Express/Node.js)               │
│  ┌────────────┐  ┌────────────┐  ┌───────────────────┐ │
│  │Controllers │  │  Services  │  │   Repositories    │ │
│  └────────────┘  └────────────┘  └───────────────────┘ │
└─────┬──────────────┬──────────────┬────────────────────┘
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  FUGA    │  │ The      │  │  Vydia   │
│   API    │  │ Orchard  │  │   API    │
│          │  │   API    │  │          │
└──────────┘  └──────────┘  └──────────┘
      │              │              │
      └──────────────┴──────────────┘
                     │
                     ▼
            ┌────────────────┐
            │    Firestore   │
            │   (Database)   │
            └────────────────┘
```

## Arquitetura

O repositório completo do projeto com todos os artefatos desenvolvidos está disponível em: https://github.com/FabioBriddi/brd-music-api.git

### Artefatos Desenvolvidos

Esta seção apresenta a relação de artefatos gerados durante o processo de desenvolvimento do sistema. Os artefatos estão organizados no repositório do projeto e documentam decisões arquiteturais, requisitos funcionais, modelos de dados e processos de validação.


## Validação

A validação do sistema será realizada através de abordagem metodológica estruturada envolvendo múltiplas técnicas complementares para garantir que os objetivos estabelecidos foram adequadamente alcançados.

### Estratégia

A estratégia de validação está fundamentada em três pilares principais: validação técnica através de testes automatizados, validação funcional através de casos de teste de aceitação, e validação de usabilidade através de avaliação heurística e testes com usuários reais.

A validação técnica abrangerá testes unitários com cobertura mínima de 80% do código backend, testes de integração verificando comunicação entre componentes e com APIs externas, e testes end-to-end simulando fluxos completos de usuário. Esta abordagem segue práticas estabelecidas pela pirâmide de testes de Cohn (2009).

A validação funcional será conduzida através de casos de teste de aceitação baseados nos requisitos funcionais especificados, verificando se cada funcionalidade atende aos critérios de aceitação definidos. Os testes seguirão metodologia BDD (Behavior-Driven Development) com cenários escritos em linguagem Gherkin.

A validação de usabilidade será realizada em duas etapas: primeiro através de avaliação heurística conduzida por especialistas em UX utilizando as dez heurísticas de Nielsen (1994), identificando problemas graves de usabilidade antes de testes com usuários; posteriormente através de testes de usabilidade com grupo de cinco a oito participantes representativos do público-alvo, executando tarefas específicas enquanto pensam em voz alta, permitindo identificação de obstáculos na interação.

### Consolidação dos Dados Coletados

A consolidação de dados da validação ocorrerá na próxima fase do projeto, após execução completa do plano de validação descrito. Os resultados serão apresentados através de métricas quantitativas (cobertura de testes, taxa de sucesso em casos de teste, tempo de execução de tarefas) e análise qualitativa de feedback dos participantes de testes de usabilidade. Gráficos comparativos ilustrarão evolução de métricas entre iterações de desenvolvimento e identificarão áreas que necessitam refinamento.

## Conclusões

Esta entrega parcial apresentou a concepção e desenvolvimento inicial do Sistema de Gerenciamento de APIs de Distribuição Musical, abordando desde a identificação do problema até a implementação da arquitetura base do sistema. Os objetivos estabelecidos para esta fase foram alcançados com sucesso, resultando em plataforma funcional que integra três principais distribuidoras musicais digitais através de interface unificada.

A escolha do stack tecnológico revelou-se apropriada, com TypeScript proporcionando robustez através de tipagem estática, React oferecendo componentes reutilizáveis para interface responsiva, e Firestore garantindo escalabilidade automática para persistência de dados. A arquitetura em camadas implementada facilita manutenção e extensibilidade futura do sistema.

O desenvolvimento seguiu metodologia ágil com entregas incrementais, permitindo validação contínua de decisões arquiteturais e ajustes conforme necessário. A implementação de múltiplas camadas de segurança garante proteção adequada de dados sensíveis dos usuários, requisito crítico considerando natureza das credenciais gerenciadas pelo sistema.

Os próximos passos incluem expansão de funcionalidades, refinamento da interface baseado em feedback de usuários, e implementação completa do plano de validação proposto. O sistema demonstra potencial significativo para resolver problemas reais enfrentados por profissionais da indústria musical digital.

## Limitações do Projeto e Perspectivas Futuras

### Limitações Atuais

O projeto em seu estágio atual apresenta algumas limitações que serão endereçadas em fases futuras. A integração com as APIs das distribuidoras ainda não cobre totalidade de endpoints disponíveis, limitando-se a operações essenciais de consulta e visualização. A implementação completa de operações de escrita (criação e atualização de releases) está planejada para próxima iteração.

O sistema de caching implementado utiliza abordagem em memória simples, adequada para ambiente de desenvolvimento mas que necessitará migração para solução distribuída como Redis em ambiente de produção para garantir consistência entre múltiplas instâncias da aplicação.

A interface atual, embora funcional, ainda não passou por processo completo de testes de usabilidade com usuários reais, podendo existir aspectos de experiência de usuário que necessitem refinamento baseado em feedback prático.

### Perspectivas Futuras

As perspectivas futuras do projeto incluem múltiplas frentes de evolução. Do ponto de vista funcional, planeja-se implementar sistema de notificações em tempo real alertando usuários sobre mudanças em status de releases, módulo de análise preditiva utilizando machine learning para identificar tendências em dados de distribuição, e integração com plataformas de streaming (Spotify, Apple Music) para consolidação de dados de performance pós-distribuição.

Do ponto de vista técnico, prevê-se migração para arquitetura de microsserviços conforme sistema escale, implementação de sistema de filas para processamento assíncrono de operações pesadas, e adoção de GraphQL como alternativa ao REST para otimização de transferência de dados em conexões limitadas.

Do ponto de vista de negócio, planeja-se desenvolvimento de aplicativo móvel nativo para iOS e Android, implementação de diferentes planos de assinatura para monetização do sistema, e expansão para suporte a distribuidoras adicionais baseado em demanda de mercado.

## Referências Bibliográficas

ABRAMOV, Dan. **React Documentation**: Optimizing Performance. Facebook Inc., 2015. Disponível em: https://react.dev/learn/render-and-commit. Acesso em: 02 out. 2025.

BECK, Kent. **Test-Driven Development**: By Example. Boston: Addison-Wesley Professional, 2003.

COHN, Mike. **Succeeding with Agile**: Software Development Using Scrum. Boston: Addison-Wesley Professional, 2009.

GAO, Zheng et al. To Type or Not to Type: Quantifying Detectable Bugs in JavaScript. In: **International Conference on Software Engineering (ICSE)**, 2017, Buenos Aires. Proceedings... IEEE, 2017. p. 758-769.

HUMBLE, Jez; FARLEY, David. **Continuous Delivery**: Reliable Software Releases through Build, Test, and Deployment Automation. Boston: Addison-Wesley Professional, 2010.

IFPI. **Global Music Report 2024**: State of the Industry. International Federation of the Phonographic Industry, 2024. Disponível em: https://www.ifpi.org/resources/. Acesso em: 02 out. 2025.

KIM, Gene et al. **The DevOps Handbook**: How to Create World-Class Agility, Reliability, and Security in Technology Organizations. Portland: IT Revolution Press, 2016.

MARTIN, Robert C. **Clean Code**: A Handbook of Agile Software Craftsmanship. Upper Saddle River: Prentice Hall, 2008.

NIELSEN, Jakob. **Usability Engineering**. Boston: Academic Press, 1994.

OWASP. **OWASP Top Ten 2021**: The Ten Most Critical Web Application Security Risks. OWASP Foundation, 2021. Disponível em: https://owasp.org/www-project-top-ten/. Acesso em: 02 out. 2025.

PRESSMAN, Roger S.; MAXIM, Bruce R. **Engenharia de Software**: Uma Abordagem Profissional. 8. ed. Porto Alegre: AMGH, 2016.

TILKOV, Stefan; VINOSKI, Steve. Node.js: Using JavaScript to Build High-Performance Network Programs. **IEEE Internet Computing**, v. 14, n. 6, p. 80-83, 2010.
