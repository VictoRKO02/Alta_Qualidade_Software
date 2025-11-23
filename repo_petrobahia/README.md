# PetroBahia S.A.

A **PetroBahia S.A.** é uma empresa fictícia do setor de óleo e gás. Seu sistema interno calcula preços de combustíveis, valida clientes e gera relatórios. 
O código está **mal estruturado** e **difícil de manter**. O objetivo é **refatorar** aplicando **PEP8**, **Clean Code** e **princípios SOLID** (SRP e OCP).

## Objetivos
- Melhorar legibilidade e clareza do código
- Extrair funções e classes coesas
- Eliminar duplicações e efeitos colaterais
- Melhorar nomes e modularidade

## Estrutura
```
src/
├── main.py
└── legacy/
    ├── clientes.py
    ├── pedido_service.py
    └── preco_calculadora.py
```

## Instruções
1. Leia o código legado.
2. Liste os problemas encontrados.
3. Refatore sem mudar o comportamento principal.
4. Documente suas **decisões de design** neste README.

---

## DECISÕES DE DESIGN
Abaixo estão as principais decisões tomadas durante a refatoração, os problemas identificados no código antigo e recomendações para manter a qualidade no futuro.

### Problemas encontrados
- Funções e módulos com múltiplas responsabilidades (viola SRP).
- Nomes pouco descritivos que dificultam leitura e manutenção.
- Lógica de negócio misturada com I/O (leitura/ escrita de arquivos e prints).
- Baixa testabilidade em algumas partes (dependências acopladas e efeitos colaterais globais).

### Principais mudanças aplicadas
- **Separação de responsabilidades:** Extração de serviços (`cliente_service`, `pedido_service`, `preco_calculadora`) para isolar validação, processamento e cálculo de preços.
- **Melhores nomes:** Renomeei funções e variáveis para refletirem sua responsabilidade, melhorando a leitura do código.
- **Remoção de efeitos colaterais:** Isolamento do I/O (leitura de `clientes.txt` e geração de relatórios) para que a lógica possa ser testada sem tocar no sistema de arquivos.
- **Injeção de dependências:** Onde apropriado, usei injeção simples para permitir mocks nos testes e reduzir acoplamento.
- **Cobertura de testes:** Mantive e adaptei os testes existentes em `src/tests/` para garantir que o comportamento principal não foi alterado.
- **PEP8 e formatação:** Ajustes de estilo para seguir PEP8 e facilitar aplicação de linters/formatadores (`flake8`, `black`).

### Racional das decisões
- Mudanças que reduzem acoplamento e aumentam coesão para seguir SRP e OCP foram priorizadas — isso facilita adições futuras (ex.: novas regras de preço) sem modificar código existente.
- Foi evitado o uso de frameworks ou reescritas completas: a intenção foi refatorar com o mínimo de mudanças comportamentais.

### Como rodar os testes
No diretório do projeto, execute:

```bash
python -m pytest -q
```
