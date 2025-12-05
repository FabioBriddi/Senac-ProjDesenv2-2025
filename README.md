# BRD Hub  
### Sistema de Monitoramento e Análise de Streams Musicais  

---

## 📘 Resumo do Projeto

O avanço do consumo de música em plataformas digitais provocou um aumento expressivo na geração de dados relacionados ao desempenho de artistas, faixas e catálogos. No entanto, a ausência de ferramentas simples, unificadas e acessíveis torna difícil consolidar, armazenar e interpretar esses dados de forma eficiente.

Este projeto apresenta o **BRD Hub**, uma aplicação web desenvolvida com o objetivo de possibilitar o upload, o processamento e a visualização de dados de streaming musical. A solução utiliza **FastAPI** no backend, **SQLite** como banco de dados local e uma interface web elaborada em **HTML, CSS e JavaScript**, incluindo gráficos gerados com **Chart.js**.

O BRD Hub tem caráter didático e prático, permitindo a estudantes e iniciantes compreender as interações entre API, banco de dados, manipulação de arquivos e visualização de métricas.

---

## 🎯 Definição do Problema

A indústria da música digital é marcada por uma grande diversidade de plataformas — como Spotify, YouTube e Apple Music —, cada uma fornecendo relatórios próprios em formatos muitas vezes distintos. Essa fragmentação gera dificuldades como:

- consolidação de dados oriundos de fontes diferentes;
- interpretação limitada de métricas agregadas;
- elevado esforço manual para monitorar desempenhos;
- falta de histórico centralizado de informações.

Relatórios internacionais, como o IFPI Global Music Report, reforçam a relevância de soluções que organizem estes dados de forma estruturada.

Durante a fase inicial deste trabalho, observou-se que estudantes e profissionais iniciantes encontram desafios principalmente em:

- manipular arquivos CSV extensos,
- interpretar colunas e métricas,
- visualizar dados de forma acessível.

Para contextualizar a posição do BRD Hub, apresenta-se uma tabela comparativa simplificada:

| Plataforma             | Centralização de Dados | Visualização Gráfica | Custo        | Foco Educacional |
|-----------------------|-------------------------|------------------------|--------------|------------------|
| Ferramenta A          | Parcial                 | Sim                    | Pago         | Não              |
| Ferramenta B          | Completa                | Sim                    | Pago         | Não              |
| **BRD Hub (proposto)**| **Sim**                 | **Sim**                | **Gratuito** | **Sim**          |

> **[INSERIR AQUI IMAGEM OU TABELA COMPLETA DE BENCHMARKING]**

---

## 🎯 Objetivos

### Objetivo Geral

Criar uma solução web capaz de centralizar dados de streaming musical, recebidos via upload de arquivos CSV, armazenando-os em banco de dados e apresentando visualizações simples e intuitivas para análise.

### Objetivos Específicos

- Implementar um backend em **FastAPI** para receber arquivos CSV e disponibilizar relatórios.
- Modelar um banco de dados **SQLite** para armazenar eventos de streaming.
- Criar uma interface web funcional para upload, navegação e consulta.
- Desenvolver gráficos e tabelas que complementem a interpretação dos dados.
- Possibilitar futura expansão para conectores reais de plataformas digitais.

---

## 🛠️ Stack Tecnológico

- **FastAPI** — backend e processamento dos arquivos.
- **Python 3** — linguagem principal do projeto.
- **SQLite** — armazenamento local dos dados.
- **HTML + CSS + JavaScript** — desenvolvimento da interface.
- **Chart.js** — geração de gráficos.
- **Fetch API** — comunicação entre front-end e backend.

---

## 🧩 Descrição da Solução

O BRD Hub é composto por:

### **1. Interface Web**
Permite:
- navegação por módulos (insights, uploads, conectores, usuários);
- envio de arquivos CSV;
- visualização de métricas resumidas;
- exibição de gráficos e tabelas.

> **[INSERIR AQUI IMAGEM DA TELA INICIAL DO SISTEMA]**

> **[INSERIR AQUI IMAGEM DA TELA DE INSIGHTS COM GRÁFICOS]**

### **2. Backend FastAPI**
Responsável por:
- ingestão dos arquivos enviados;
- tratamento e validação dos dados;
- inserção no banco de dados;
- consultas agregadas para relatórios;
- histórico de uploads processados.

### **3. Banco de Dados SQLite**
Estrutura básica:
- **sources**  
- **ingestions**  
- **stream_events**

> **[INSERIR AQUI DIAGRAMA ENTIDADE-RELACIONAMENTO (DER)]**

---

## 🏗️ Arquitetura da Aplicação

Representação simplificada da arquitetura:

┌───────────────────────────────────────┐ <br>
│ Front-end                             │ <br>
│ HTML • CSS • JavaScript • Chart.js    │ <br>
└───────────────────────────────────────┘ <br>
↓ REST <br>
┌───────────────────────────────────────┐ <br>
│ FastAPI                               │ <br>
│ Uploads • Relatórios • Processamento  │ <br>
└───────────────────────────────────────┘ <br>
↓ SQL <br>
┌───────────────────────────────────────┐ <br>
│ SQLite                                │ <br>
│ Ingestions • Stream Events • Sources  │ <br>
└───────────────────────────────────────┘<br>

> **[INSERIR AQUI DIAGRAMA DE ARQUITETURA EM IMAGEM]**

---

## 🔍 Validação do Sistema

A validação foi conduzida por meio de testes funcionais, incluindo:

- uploads repetidos de arquivos CSV de diferentes estruturas;
- verificação do armazenamento correto no banco de dados;
- análise da exibição de métricas e gráficos no front-end;
- comparação dos resultados apresentados com os valores esperados dos arquivos.

Casos extremos também foram testados, como:

- CSVs com colunas ausentes;
- arquivos vazios;
- valores inconsistentes.

> **[INSERIR PRINTS DE TESTES E RESULTADOS]**

---

## 📊 Estratégia de Análise

O sistema organiza os dados para permitir interpretações como:

- volume total de streams armazenados;
- número de artistas únicos;
- artistas mais executados;
- plataformas com maior participação;
- número total de uploads processados.

Essas análises visam oferecer uma visão exploratória simples, porém útil, do comportamento dos dados inseridos.

> **[INSERIR GRÁFICOS EXPORTADOS DO BRD HUB]**

---

## 📈 Consolidação dos Resultados

Após os testes, concluiu-se que:

- o sistema processa corretamente arquivos de diferentes origens;
- a API retorna resultados consistentes nos relatórios;
- o dashboard favorece a compreensão inicial das métricas principais;
- a organização modular do código facilita expansões futuras.

---

## 🏁 Conclusões

O BRD Hub demonstrou viabilidade como uma ferramenta compacta e intuitiva para centralização e visualização de dados de streaming musical. A aplicação cumpre o propósito educacional e técnico, permitindo compreender na prática:

- a construção de uma API REST moderna;
- a modelagem e manipulação de dados;
- a integração front-end ↔ back-end;
- a geração de insights a partir de dados estruturados.

O projeto estabelece uma base sólida para desenvolvimentos futuros, podendo evoluir para uma solução robusta e completa.

---

## 🚧 Limitações e Trabalhos Futuros

### Limitações identificadas
- Ausência de autenticação e perfis de usuário;
- Falta de filtros avançados (por período, país, faixa etc.);
- Dependência de uploads manuais de arquivos CSV;
- Visualizações ainda introdutórias.

### Propostas de aprimoramento
- Implementação de login com controle de sessão;
- Desenvolvimento de conectores reais (APIs de distribuidoras);
- Sistema de relatórios exportáveis (PDF, Excel);
- Deploy em servidores cloud;
- Dashboard avançado com filtros interativos.

---

## 📚 Referências

- IFPI – International Federation of the Phonographic Industry. *Global Music Report*.
- FastAPI Documentation — https://fastapi.tiangolo.com/
- SQLite Documentation — https://sqlite.org/docs.html
- Chart.js Documentation — https://www.chartjs.org/docs/latest/
- WAZLAWICK, Raul Sidnei. *Metodologia de Pesquisa em Ciência da Computação*.

---

## ✨ Autor

> **Nome do(a) aluno(a):** _(preencher)_  
> **Curso:** _(preencher)_  
> **Instituição:** _(preencher)_  
> **GitHub:** _(preencher)_  

