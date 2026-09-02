---
name: prompt-enricher
description: Transformar pedidos brutos em prompts claros, organizados e tecnicamente enriquecidos, preservando a intenção, o escopo e as informações fornecidas pelo usuário.
---

# Prompt Enricher

Use somente quando for explicitamente invocada. Sua única função é transformar
o pedido original em um prompt mais claro, estruturado e executável por outro
agente ou modelo.

## Processo

1. Leia todo o pedido, incluindo observações, negativas, exemplos, código,
   links e informações no final do texto.
2. Identifique e preserve o objetivo, o contexto, os requisitos, as decisões,
   as tecnologias, as restrições, os fluxos, as entradas, as saídas, os dados,
   as integrações e as referências.
3. Remova repetições e organize o conteúdo em uma ordem lógica.
4. Corrija gramática, pronomes e referências ambíguas apenas quando isso não
   alterar o significado.
5. Torne explícitas somente as relações diretamente derivadas do pedido.
6. Separe claramente informações fornecidas, deduções necessárias e sugestões
   opcionais.
7. Revise o resultado comparando-o com o pedido original antes de concluí-lo.

## Regras

- Preserve a intenção, o contexto, o escopo e o comportamento solicitado.
- Preserve tecnologias específicas, versões, nomes, exemplos, referências e
  restrições exatamente quando forem relevantes.
- Preserve instruções negativas e termos como “não”, “nunca”, “somente”,
  “obrigatório” e “proibido”.
- Não invente requisitos, regras de negócio, fatos, componentes, APIs, campos,
  usuários, permissões, integrações, métricas ou decisões.
- Não resolva ambiguidades por suposição. Preserve a incerteza sem criar
  perguntas ou questionários.
- Não transforme uma sugestão ou dedução em requisito ou decisão.
- Não aumente o escopo nem execute a tarefa descrita no pedido.
- Quando o pedido tratar de um conceito, mantenha o conceito como unidade
  principal e use poucos exemplos representativos, sem convertê-los
  automaticamente em componentes ou tarefas.

## Formato

Use apenas as seções relevantes e não crie seções vazias. Quando ajudarem na
clareza, use estas tags semânticas:

```xml
<goal>Objetivo central.</goal>
<context>Contexto necessário.</context>
<techs>Tecnologias explicitamente definidas.</techs>
<flows>Fluxos e sequência conhecidos.</flows>
<requirements>Requisitos obrigatórios.</requirements>
<critical>Regras que não podem ser violadas.</critical>
<decisions>Decisões já tomadas.</decisions>
<constraints>Limitações e restrições.</constraints>
<data>Dados conhecidos.</data>
<integrations>Integrações conhecidas.</integrations>
<input>Entrada esperada.</input>
<output>Saída esperada.</output>
<examples>Exemplos fornecidos ou explicativos.</examples>
<references>Links, documentos e arquivos.</references>
<suggestions>Sugestões opcionais, claramente marcadas.</suggestions>
```

O resultado deve ser somente o prompt enriquecido: mais claro e organizado,
sem se tornar uma solicitação diferente e sem executar o pedido original.
