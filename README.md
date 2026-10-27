# nuCases — Staff Lab

Portal de estudo em português para entrevistas de Staff Software Engineer, com foco no Nubank: fundamentos, coding, sistemas distribuídos, arquitetura e decisões de engenharia. Inclui um dojo para praticar sintaxe, imports e reconstrução de código sem consultar a resposta.

**Portal no GitHub Pages:** [wesleyvieira99.github.io/nuCases](https://wesleyvieira99.github.io/nuCases/).

## Conteúdo

- 20 módulos e 60 lições, dos fundamentos às decisões de nível Staff.
- 60 simulações autorais, com 240 rodadas e aproximadamente 120 horas de prática sugerida.
- 14 laboratórios de código, com testes e explicações.
- Dojo de sintaxe com 36 exercícios, 108 lacunas e 12 receitas de código.
- 256 flashcards, revisão espaçada, cronômetro, rubricas e rascunhos.
- **Java de cabeça:** 56 cartões de sintaxe, classes, métodos e imports, com rascunho, referência oculta, autoavaliação e exemplos completos para Java 17.
- 32 fontes públicas, com pesquisa consolidada em **26/10/2026** e distinção entre fontes oficiais e relatos de candidatos.

## Como usar

Abra `index.html` diretamente no navegador para estudar offline ou sirva a pasta do projeto:

```sh
python3 -m http.server 8000
```

Acesse [localhost:8000](http://localhost:8000). Comece pelo dojo: tente resolver sem olhar, confira a solução e depois reconstrua o exemplo em um arquivo vazio. Use as simulações com tempo marcado e registre os pontos a revisar.

O progresso e os rascunhos ficam no armazenamento local do navegador. Use a exportação e a importação do portal para fazer backup ou transferir seus dados. **Não há conta nem sincronização automática** entre dispositivos, navegadores ou a versão local e a versão online. Limpar os dados do navegador pode apagar o progresso.

## Estrutura e atualização

```text
index.html                      # Portal completo, com conteúdo incorporado
src/{shell.html,style.css,app.js,java.js} # Interface e comportamento
data/                           # curriculum, research, simulations, syntax e java.json
scripts/build.py                # Gera o index.html
downloads/codigos-e-receitas.zip  # Códigos e receitas para prática
.nojekyll                       # Publicação estática no GitHub Pages
```

Após editar os arquivos de `src/` ou `data/`, gere novamente o portal:

```sh
python3 scripts/build.py
```

O HTML final funciona sem servidor de aplicação. A hospedagem pública disponibiliza os materiais de estudo; o progresso de cada pessoa continua armazenado no próprio navegador.

## Escopo e validação

Este é um material independente, **não oficial e sem vínculo com o Nubank**. Os casos são autorais, inspirados em competências e informações públicas; não representam um banco de perguntas reais nem cobrem todos os processos possíveis. Etapas e requisitos podem variar por vaga e mudar com o tempo. O material não garante aprovação.

Na preparação desta versão, 12 dos 14 laboratórios foram executados; os dois de Clojure passaram por revisão manual estática. A validação do dojo incluiu 23 exemplos. Esses resultados descrevem o que foi verificado e não garantem a execução de todos os exemplos em qualquer ambiente ou versão de linguagem/framework.

A seção [Java de cabeça](https://wesleyvieira99.github.io/nuCases/#java) também inclui um mapa de imports e um ritual de recuperação de memória. Todos os 56 programas Java foram compilados e executados com Java 17 e assertions habilitadas. Cada cartão permite baixar seu próprio `Main.java`; rode-os em pastas separadas. O editor no portal salva rascunhos, mas não executa nem corrige código automaticamente.
