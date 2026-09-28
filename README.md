# \# 🛡️ Sompo Risk MVP

# 

# \*\*Challenge FIAP × Sompo Seguros — Entrega final (Sprint 4)\*\*

# 

# Sistema integrado de \*\*monitoramento de risco de equipamentos\*\*: coleta dados de sensores, valida e trata inconsistências, gera um \*\*score de risco de 0 a 100\*\* com um modelo preditivo, emite \*\*alertas com recomendações preventivas\*\* e produz \*\*dashboard e relatórios\*\* para diferentes perfis de usuário.

# 

# | Integrante | RM |

# |---|---|

# | Douglas Felicio | RM572312 |

# | Gabriel Kaique | RM572500 |

# | Richard Wrobel dos Santos | RM573998 |

# 

# 🎥 \*\*Vídeo de demonstração:\*\* \[colar o link do YouTube aqui]

# 

# \---

# 

# \## 📌 Sumário

# 

# 1\. \[Problema e solução](#1-problema-e-solução)

# 2\. \[Arquitetura consolidada](#2-arquitetura-consolidada)

# 3\. \[Fluxo de ponta a ponta](#3-fluxo-de-ponta-a-ponta)

# 4\. \[Estrutura do projeto](#4-estrutura-do-projeto)

# 5\. \[Como executar](#5-como-executar)

# 6\. \[Como o score é gerado](#6-como-o-score-é-gerado)

# 7\. \[Alertas e relatórios](#7-alertas-e-relatórios)

# 8\. \[Segurança](#8-segurança)

# 9\. \[Testes](#9-testes)

# 10\. \[Decisões técnicas e justificativas](#10-decisões-técnicas-e-justificativas)

# 11\. \[Evolução ao longo das quatro Sprints](#11-evolução-ao-longo-das-quatro-sprints)

# 12\. \[Limitações e próximos passos](#12-limitações-e-próximos-passos)

# 

# \---

# 

# \## 1. Problema e solução

# 

# \*\*Problema:\*\* equipamentos que falham sem aviso geram paradas, prejuízos e sinistros. Sem monitoramento estruturado, a manutenção é reativa.

# 

# \*\*Solução (MVP):\*\* um pipeline em Python que transforma leituras brutas de sensores em \*\*decisões preventivas\*\*:

# 

# \- Coleta dados ambientais e operacionais (temperatura, umidade, vibração, carga, horas de operação e dias desde a última manutenção).

# \- Trata dados sujos automaticamente (duplicatas, valores impossíveis e nulos).

# \- Estima a probabilidade de falha e a converte em um \*\*score de 0 a 100\*\* com \*\*nível de risco\*\*.

# \- Aponta o \*\*fator que mais pesou\*\* e sugere uma \*\*ação preventiva\*\*.

# \- Entrega \*\*dashboard interativo\*\* e relatórios em \*\*CSV e PDF\*\*, com controle de acesso por perfil.

# 

# \*\*Público-alvo:\*\* gestores de risco (visão executiva), analistas (investigação) e operadores de manutenção (ação).

# 

# \---

# 

# \## 2. Arquitetura consolidada

# 

# ```mermaid

# flowchart LR

# &#x20;   A\[Entrada de dados<br/>CSV · JSON · simulador] --> B\[Validação<br/>e transformação]

# &#x20;   B --> C\[Modelo preditivo<br/>Random Forest]

# &#x20;   C --> D\[(Banco SQLite<br/>risk\_scores · alerts)]

# &#x20;   D --> E\[Alertas]

# &#x20;   D --> F\[Dashboard<br/>Streamlit + Plotly]

# &#x20;   E --> G\[Exportação<br/>CSV · PDF]

# &#x20;   S{{Segurança transversal<br/>RBAC · criptografia · auditoria}} -.-> F

# &#x20;   S -.-> G

# ```

# 

# | Camada | Responsabilidade | Módulos |

# |---|---|---|

# | \*\*Entrada\*\* | Ler CSV/JSON ou gerar dados simulados reprodutíveis | `src/data/ingestion.py` |

# | \*\*Validação e transformação\*\* | Checar colunas, faixas físicas, duplicatas e nulos; criar variáveis derivadas | `src/data/validation.py`, `src/data/transformation.py` |

# | \*\*Modelo\*\* | Treinar, avaliar e gerar o score | `src/models/train.py`, `evaluate.py`, `predict.py` |

# | \*\*Persistência\*\* | Gravar e ler os resultados em SQLite | `src/data/database.py` |

# | \*\*Relatórios\*\* | Alertas, dashboard e exportação | `src/reports/alerts.py`, `dashboard.py`, `export.py` |

# | \*\*Segurança\*\* | Login por perfil, criptografia e trilha de auditoria | `src/security/auth.py`, `encryption.py`, `audit.py` |

# | \*\*Transversal\*\* | Configuração, logs e exceções padronizados | `src/config/`, `src/utils/` |

# 

# O fluxo é \*\*unidirecional\*\* e as camadas são separadas por pasta. O dashboard lê \*\*apenas do banco\*\*, sem depender do pipeline em execução. O `main.py` orquestra tudo.

# 

# \---

# 

# \## 3. Fluxo de ponta a ponta

# 

# 1\. \*\*Coleta:\*\* `ingestion.py` lê um CSV/JSON de sensores ou gera 3.000 leituras simuladas (com nulos, outliers e duplicatas injetados de propósito).

# 2\. \*\*Validação:\*\* `validation.py` exige as colunas esperadas, converte tipos, remove duplicatas (`machine\_id` + `timestamp`), trata valores fora de faixa como nulos e imputa pela \*\*mediana da própria máquina\*\*. Gera um relatório de qualidade.

# 3\. \*\*Transformação:\*\* `transformation.py` cria 4 variáveis derivadas (ver \[seção 6](#6-como-o-score-é-gerado)).

# 4\. \*\*Treino e avaliação:\*\* `train.py` treina o modelo (75% dos dados) e `evaluate.py` mede desempenho em 25% reservados para teste. O modelo é salvo em `src/models/artifacts/`.

# 5\. \*\*Score:\*\* `predict.py` calcula o `risk\_score` (0–100), o `risk\_level` e o `top\_factor` de cada leitura.

# 6\. \*\*Persistência:\*\* os resultados vão para as tabelas `risk\_scores` e `alerts` do SQLite.

# 7\. \*\*Alertas:\*\* `alerts.py` seleciona o estado mais recente de cada máquina em nível \*\*ALTO\*\* ou \*\*CRÍTICO\*\* e associa uma recomendação preventiva.

# 8\. \*\*Relatórios:\*\* `export.py` gera `alerts.csv` e `report.pdf`; o `dashboard.py` exibe tudo, com acesso conforme o perfil.

# 9\. \*\*Auditoria:\*\* logins, exportações e execuções do pipeline são registrados em `logs/audit.jsonl`.

# 

# \---

# 

# \## 4. Estrutura do projeto

# 

# ```text

# sompo-risk-mvp/

# ├── main.py                     # Ponto de entrada: executa o pipeline completo

# ├── requirements.txt

# ├── .env.example                # Template de variáveis de ambiente

# ├── src/

# │   ├── config/                 # settings.py (configurações) · constants.py (domínio)

# │   ├── data/                   # ingestion · validation · transformation · database

# │   ├── models/                 # train · predict · evaluate · artifacts/

# │   ├── security/               # auth · encryption · audit

# │   ├── reports/                # dashboard · alerts · export

# │   └── utils/                  # logger · exceptions · helpers

# ├── tests/                      # test\_ingestion · test\_validation · test\_model · test\_integration

# ├── data/                       # raw/ · processed/ · simulated/

# ├── notebooks/                  # exploratory\_analysis.ipynb

# ├── docs/                       # architecture.md · decisions.md · user\_stories.md

# ├── outputs/                    # alerts.csv · report.pdf · report.csv (gerado na execução)

# └── logs/                       # app.log · audit.jsonl (gerado na execução)

# ```

# 

# \---

# 

# \## 5. Como executar

# 

# \*\*Pré-requisito:\*\* Python 3.10 ou superior.

# 

# \### 5.1 Instalação

# 

# ```bash

# git clone <URL\_DO\_REPOSITORIO>

# cd sompo-risk-mvp

# 

# python -m venv .venv

# source .venv/bin/activate          # Windows: .venv\\Scripts\\activate

# pip install -r requirements.txt

# ```

# 

# \### 5.2 Configuração (opcional)

# 

# O projeto lê as configurações de \*\*variáveis de ambiente\*\* (não carrega o `.env` automaticamente). Sem configuração, usa valores padrão de desenvolvimento.

# 

# ```bash

# cp .env.example .env               # edite as senhas e a chave de criptografia

# set -a; source .env; set +a        # Linux/macOS: exporta as variáveis

# \# Windows (PowerShell): $env:SOMPO\_ADMIN\_PASSWORD = "sua-senha"

# ```

# 

# Para gerar uma chave de criptografia:

# 

# ```bash

# python -c "from cryptography.fernet import Fernet; print(Fernet.generate\_key().decode())"

# ```

# 

# | Variável | Função |

# |---|---|

# | `SOMPO\_ENV` | `dev` ou `prod` (nível de log) |

# | `SOMPO\_DB\_PATH` | Caminho do banco SQLite |

# | `SOMPO\_ENCRYPTION\_KEY` | Chave Fernet (sem ela, é gerada uma chave temporária) |

# | `SOMPO\_ADMIN\_PASSWORD` / `SOMPO\_ANALYST\_PASSWORD` / `SOMPO\_OPERATOR\_PASSWORD` | Senhas dos perfis |

# | `SOMPO\_RANDOM\_SEED` | Semente de reprodutibilidade (padrão: 42) |

# 

# \### 5.3 Executar o pipeline

# 

# ```bash

# python main.py                          # usa dados simulados

# python main.py --input data/raw/sensores.csv   # usa um CSV próprio

# python main.py --n 5000                 # quantidade de leituras simuladas

# ```

# 

# \*\*Formato do CSV de entrada:\*\* `machine\_id, timestamp, temperature, humidity, vibration, load\_pct, operating\_hours, days\_since\_maintenance` e a coluna `failure` (0/1), necessária para o treino.

# 

# \### 5.4 Abrir o dashboard

# 

# Execute o pipeline \*\*antes\*\*, pois o dashboard lê o banco gerado por ele.

# 

# ```bash

# streamlit run src/reports/dashboard.py

# ```

# 

# Acesse `http://localhost:8501`.

# 

# | Usuário | Senha padrão (apenas desenvolvimento) | Acesso |

# |---|---|---|

# | `admin` | `admin123` | Alertas, histórico, gráficos e exportação |

# | `analista` | `analista123` | Alertas, histórico, gráficos e exportação |

# | `operador` | `operador123` | Somente indicadores e alertas |

# 

# > ⚠️ Troque as senhas padrão pelas variáveis de ambiente antes de qualquer uso fora de demonstração.

# 

# \### 5.5 Testes

# 

# ```bash

# pytest -q

# ```

# 

# \---

# 

# \## 6. Como o score é gerado

# 

# \*\*Variáveis de entrada (10):\*\*

# 

# \- \*\*Sensores (6):\*\* `temperature`, `humidity`, `vibration`, `load\_pct`, `operating\_hours`, `days\_since\_maintenance`.

# \- \*\*Derivadas (4):\*\*

# &#x20; - `thermal\_stress` = temperatura × carga ÷ 100

# &#x20; - `vib\_per\_load` = vibração ÷ (carga + 1)

# &#x20; - `maintenance\_overdue` = 1 se a última manutenção foi há mais de 90 dias

# &#x20; - `humidity\_high` = 1 se a umidade passa de 80%

# 

# \*\*Modelo:\*\* `RandomForestClassifier` (200 árvores, profundidade máxima 10, `min\_samples\_leaf=5`, `class\_weight="balanced"`, semente 42), com divisão estratificada 75% treino / 25% teste.

# 

# \*\*Score:\*\* a probabilidade de falha (`predict\_proba`) multiplicada por 100.

# 

# | Score | Nível |

# |---|---|

# | 0 – 30 | 🟢 BAIXO |

# | 30 – 60 | 🟡 MÉDIO |

# | 60 – 80 | 🟠 ALTO |

# | 80 – 100 | 🔴 CRÍTICO |

# 

# \*\*Explicabilidade:\*\* para cada leitura, o `top\_factor` combina o desvio acima da média de cada variável com a importância dela no modelo. Ele alimenta a recomendação do alerta.

# 

# \*\*Desempenho na execução de referência (dados simulados, 25% de teste):\*\*

# 

# | Métrica | Valor |

# |---|---|

# | ROC-AUC | 0,83 |

# | Precisão / Recall / F1 | 0,54 / 0,54 / 0,54 |

# 

# > ⚠️ Os dados são \*\*simulados\*\*: o modelo aprende a regra usada para gerá-los. Essas métricas validam o funcionamento do pipeline, \*\*não\*\* o desempenho em produção.

# 

# \---

# 

# \## 7. Alertas e relatórios

# 

# \*\*Alertas preventivos:\*\* só entram máquinas em nível \*\*ALTO\*\* ou \*\*CRÍTICO\*\*, com base na leitura mais recente, ordenadas do maior para o menor score. Cada alerta traz o fator principal e uma ação, por exemplo:

# 

# | Fator | Recomendação |

# |---|---|

# | `vibration` | Inspecionar rolamentos, alinhamento e fixações do equipamento |

# | `temperature` | Verificar refrigeração/lubrificação e reduzir carga até normalizar |

# | `thermal\_stress` | Reduzir carga e verificar refrigeração (estresse térmico) |

# | `maintenance\_overdue` | Agendar manutenção preventiva (prazo vencido) |

# | `humidity\_high` | Checar vedação e ambiente; umidade acima do limite |

# 

# \*\*Relatórios por perfil:\*\*

# 

# | Saída | Público | Conteúdo |

# |---|---|---|

# | Dashboard Streamlit | Operador / Analista / Gestor | Indicadores, alertas, evolução do risco por máquina e distribuição de scores |

# | `outputs/alerts.csv` | Analista | Lista de alertas com recomendação |

# | `outputs/report.pdf` | Gestão | Distribuição por nível, top 10 máquinas e tabela de alertas |

# | Tabelas `risk\_scores` e `alerts` (SQLite) | Integrações | Histórico completo de scores |

# 

# \---

# 

# \## 8. Segurança

# 

# \- \*\*Autenticação:\*\* senhas protegidas com \*\*PBKDF2-SHA256\*\* (200 mil iterações e \*salt\* aleatório), comparação em tempo constante.

# \- \*\*Autorização (RBAC):\*\* três perfis (`admin`, `analista`, `operador`) com permissões distintas, aplicadas no dashboard.

# \- \*\*Criptografia:\*\* \*\*Fernet (AES)\*\* para dados sensíveis e pseudonimização de identificadores por hash.

# \- \*\*Auditoria:\*\* log em `logs/audit.jsonl` com \*\*hash encadeado\*\* (cada registro contém o hash do anterior), o que permite detectar adulteração com `verify\_chain()`.

# \- \*\*Boas práticas:\*\* segredos por variável de ambiente, `.env` fora do controle de versão, exceções customizadas e logs padronizados.

# 

# \---

# 

# \## 9. Testes

# 

# Sete testes automatizados com `pytest`, cobrindo:

# 

# | Arquivo | O que valida |

# |---|---|

# | `test\_ingestion.py` | Estrutura e reprodutibilidade dos dados simulados |

# | `test\_validation.py` | Limpeza de dados e erro para colunas ausentes |

# | `test\_model.py` | Treino, AUC mínimo e scores entre 0 e 100 |

# | `test\_integration.py` | Pipeline completo, segurança (login, permissões, criptografia) e integridade da auditoria |

# 

# Os testes usam pastas temporárias e \*\*não alteram\*\* o modelo, o banco nem os relatórios gerados pelo pipeline.

# 

# \---

# 

# \## 10. Decisões técnicas e justificativas

# 

# | Decisão | Motivo | Trade-off |

# |---|---|---|

# | \*\*Random Forest\*\* | Lida bem com relações não lineares entre sensores, é robusto a escalas diferentes, compensa falhas raras com `class\_weight="balanced"` e fornece a \*\*importância das variáveis\*\*, que explica cada alerta | Pode ser superado por modelos mais complexos; precisa ser recalibrado com dados reais |

# | \*\*Feature engineering\*\* | Variáveis como `thermal\_stress` e `maintenance\_overdue` codificam conhecimento do domínio de manutenção | Limiares (90 dias, 80% de umidade) devem ser validados com especialistas |

# | \*\*Dados simulados com ruído injetado\*\* | Permitem demonstrar o pipeline e a validação de forma reprodutível (semente fixa) | Não representam falhas reais |

# | \*\*Imputação pela mediana da máquina\*\* | Preserva o comportamento individual de cada equipamento e é robusta a outliers | Pode suavizar variações reais em períodos longos sem leitura |

# | \*\*SQLite\*\* | Zero configuração no MVP; o acesso está isolado em `database.py` | Não atende muitos acessos simultâneos; migração para PostgreSQL troca só essa camada |

# | \*\*Streamlit + Plotly\*\* | Dashboard interativo em Python puro, com desenvolvimento rápido | Menos customizável que um front-end dedicado |

# | \*\*PDF com Matplotlib\*\* | Sem dependências pesadas de renderização | Layout mais simples |

# | \*\*RBAC + criptografia + auditoria desde o início\*\* | Dados de risco são sensíveis e exigem rastreabilidade | Usuários de demonstração; em produção, usar SSO corporativo |

# | \*\*Arquitetura em camadas e código modular\*\* | Cada responsabilidade em uma pasta facilita testes e evolução | Mais arquivos para um MVP pequeno |

# | \*\*Testes automatizados e semente fixa\*\* | Garantem reprodutibilidade e detectam regressões | — |

# 

# \---

# 

# \## 11. Evolução ao longo das quatro Sprints

# 

# | Sprint | Foco | Entregas |

# |---|---|---|

# | \*\*Sprint 1\*\* | \[preencher] | \[preencher] |

# | \*\*Sprint 2\*\* | \[preencher] | \[preencher] |

# | \*\*Sprint 3\*\* | \[preencher] | \[preencher] |

# | \*\*Sprint 4\*\* | Consolidação do MVP | Pipeline integrado ponta a ponta, modelo preditivo com score de risco, alertas com recomendações, dashboard com controle de acesso, relatórios em CSV/PDF, segurança e auditoria, testes automatizados e documentação final |

# 

# \---

# 

# \## 12. Limitações e próximos passos

# 

# \*\*Limitações atuais\*\*

# 

# \- Os dados são \*\*simulados\*\*; o modelo não foi validado com histórico real de sinistros.

# \- O SQLite e os usuários de demonstração servem ao MVP, não à produção.

# \- A ingestão é por arquivo, não em tempo real.

# \- O limiar de decisão do modelo é fixo em 0,5.

# 

# \*\*Próximos passos\*\*

# 

# 1\. Treinar e validar o modelo com \*\*histórico real\*\* de falhas e sinistros.

# 2\. Conectar \*\*sensores em tempo real\*\* (ingestão contínua).

# 3\. Migrar para \*\*PostgreSQL\*\* e adotar \*\*login unificado (SSO)\*\*.

# 4\. Ajustar limiares de alerta e o critério de decisão do modelo com especialistas de manutenção.

# 5\. Monitorar o desempenho do modelo ao longo do tempo (\*drift\*) e automatizar o retreino.

# 

# \---

# 

\*\*Challenge FIAP × Sompo Seguros\*\* — Douglas Felicio · Gabriel Kaique · Richard Wrobel dos Santos


Vídeo: https://youtu.be/esoPa7ceaXM
===

