
> **Espaço para inserir diagrama de arquitetura (PNG/JPG)**

### Artefatos adicionais sugeridos (mínimo 5):

- Benchmarking (comparação com soluções reais)  
- Project Canvas / MVP Canvas  
- Personas  
- Casos de uso e User Stories  
- Diagrama ER das tabelas  
- Protótipo do layout (Figma ou similar)  
- Backlog / Kanban do desenvolvimento  

> **Espaço para linkar artefatos do repositório**

---

## 🔍 Validação

A validação do sistema foi realizada por meio de testes manuais:

- Upload de arquivos CSV reais fornecidos durante o desenvolvimento.  
- Análise do impacto dos uploads nas tabelas SQLite.  
- Validação da resposta dos endpoints `/reports/*`.  
- Conferência visual das métricas, gráficos e tabelas no dashboard.  

Também foram realizados testes com casos extremos, como:

- Arquivos vazios  
- Campos faltantes  
- CSVs com ordem de colunas diferente  

Esse processo permitiu ajustar o fluxo de ingestão e garantir que a aplicação respondesse de forma consistente.

---

## 📊 Estratégia

Para comprovar o alcance dos objetivos, foram aplicados alguns métodos simples:

- **Simulação de uso real:** enviando múltiplos arquivos de diferentes artistas.  
- **Testes exploratórios:** navegando pelas telas como um usuário comum.  
- **Análise de logs do backend:** garantindo o processamento adequado de cada upload.  
- **Comparação com métricas esperadas:** verificando se os números consolidados batiam com os dados de origem.

Futuramente, essa estratégia pode ser ampliada com entrevistas e questionários para usuários da área.

---

## 📈 Consolidação dos Dados Coletados

Os testes iniciais demonstraram que:

- O sistema consegue consolidar dados de múltiplos artistas.  
- Os insights são atualizados automaticamente após cada upload.  
- Os gráficos permitem identificar tendências e diferenças entre plataformas.  
- O SQLite foi suficiente para manter desempenho e simplicidade no desenvolvimento.

> **Espaço para adicionar gráficos reais exportados do BRD Hub**

---

## 🏁 Conclusões

O BRD Hub demonstrou ser uma solução funcional para centralização e visualização de métricas de streaming musical. O sistema atende ao problema proposto ao permitir que usuários importem arquivos CSV e visualizem instantaneamente informações relevantes sobre artistas e plataformas.

O trabalho também serviu como oportunidade de aprendizado nas áreas de:

- APIs REST com FastAPI  
- Modelagem de banco de dados  
- Manipulação de CSV e ingestão de dados  
- Construção de dashboards com JavaScript  
- Arquitetura modular de sistemas  

---

## 🚧 Limitações e Perspectivas Futuras

### Limitações atuais
- Não possui autenticação de usuários  
- Não possui edição direta de registros  
- Não integra com APIs reais de plataformas digitais  
- Dashboards ainda básicos (apenas alguns gráficos simples)

### Futuras melhorias
- Implementação de login/admin com JWT  
- Conectores com FUGA, Vydia e The Orchard  
- Sistema de permissões  
- Dashboard avançado com filtros e drilldown  
- Exportação de relatórios em PDF/Excel  
- Deploy em ambiente cloud

---

## 📚 Referências Bibliográficas

- IFPI. *Global Music Report*. Internacional Federation of the Phonographic Industry, 2023.  
- WAZLAWICK, Raul Sidnei. **Metodologia de pesquisa para ciência da computação**. Elsevier, 2009.  
- FastAPI Documentation. https://fastapi.tiangolo.com/  
- SQLite Documentation. https://sqlite.org/docs.html  
- Chart.js Documentation. https://www.chartjs.org/docs/latest/

---

## ✨ Autor
> Nome do aluno: **(Adicionar aqui)**  
> Curso: **(Adicionar aqui)**  
> Instituição: **(Adicionar aqui)**  
> GitHub: **(Adicionar aqui)**

