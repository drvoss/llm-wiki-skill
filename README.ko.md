# llm-wiki-skill

**언어:** [English](README.md) | [한국어](README.ko.md) | [简体中文](README.zh-CN.md)

**튜토리얼:** [English](docs/TUTORIAL.md) | [한국어](docs/TUTORIAL.ko.md) | [简体中文](docs/TUTORIAL.zh-CN.md)

**운영 가이드:** [English](docs/OPERATIONS.md) | [한국어](docs/OPERATIONS.ko.md) | [简体中文](docs/OPERATIONS.zh-CN.md)

지속적으로 누적되는 마크다운 지식 베이스를 구축하고 관리하기 위한 독립형,
런타임 비종속 스킬입니다. [Andrej Karpathy의 LLM Wiki 패턴](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)을
바탕으로 합니다.

GitHub Copilot CLI, Claude Code, Codex CLI, Gemini CLI, 그리고
[agentskills.io](https://agentskills.io) 호환 런타임에서 사용할 수 있습니다.

---

## 이 저장소가 존재하는 이유

`llm-wiki-skill`은
[`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent) 안에서
검증된 아이디어를 꺼내, 여러 런타임에서 재사용할 수 있는 범용 skill 패키지로
정리한 저장소입니다.

Hermes Agent에서는 `llm-wiki`가 큰 에이전트 시스템 안에 포함된 번들 스킬이지만,
이 저장소는 그 아이디어를 다음 구성요소와 함께 독립 패키지로 분리합니다.

- 코어 워크플로를 담은 `SKILL.md`
- 도메인별 스키마 템플릿 `templates/`
- 의존성 없는 점검 스크립트 `scripts/wiki-lint.py`
- 빠른 현황 요약 스크립트 `scripts/wiki-stats.py`
- 참조용 예시 위키 `examples/`
- arXiv, GitHub, Obsidian 같은 선택형 확장 `extensions/`

즉 Hermes 전용 설정과 런타임 가정은 덜어내고, 패턴 자체를 더 쉽게 도입할 수
있도록 만든 저장소입니다.

---

## 해결하려는 문제

AI 세션은 보통 매번 0에서 시작합니다. 같은 도메인을 다시 설명하고, 에이전트는
같은 소스를 다시 읽고, 같은 관계를 다시 찾아냅니다. 작업이 누적되지 않습니다.

**llm-wiki**는 이 흐름을 뒤집습니다. 에이전트가 지식을 한 번 인터링크된
마크다운 파일로 정리해두고, 다음 세션에는 SCHEMA + index + 최근 log만 읽고
이어서 작업합니다. 교차 참조가 남고, 모순이 표시되고, 합성 결과가 축적됩니다.

---

## 여기서 시작하세요

- 실전 튜토리얼 읽기: [docs/TUTORIAL.ko.md](docs/TUTORIAL.ko.md)
- 운영 습관 정리: [docs/OPERATIONS.ko.md](docs/OPERATIONS.ko.md)
- 사용하는 런타임에 스킬 설치
- 실제 도메인 하나로 위키 초기화
- 최소 몇 개의 소스를 넣어본 뒤 워크플로 평가

---

## 설치

### GitHub Copilot CLI

```bash
# 프로젝트 단위 설치: .github/skills/ 아래에 복사
cp SKILL.md .github/skills/llm-wiki/SKILL.md

# 사용자 단위 설치: 모든 세션에서 사용 가능
cp SKILL.md ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
# 프로젝트 단위
New-Item -ItemType Directory -Force .github\skills\llm-wiki | Out-Null
Copy-Item SKILL.md .github\skills\llm-wiki\SKILL.md

# 사용자 단위
New-Item -ItemType Directory -Force $HOME\.copilot\skills\llm-wiki | Out-Null
Copy-Item SKILL.md $HOME\.copilot\skills\llm-wiki\SKILL.md
```

### Claude Code

```bash
cp SKILL.md ~/.claude/skills/llm-wiki/SKILL.md
```

### Codex CLI

```bash
cp SKILL.md ~/.codex/skills/llm-wiki/SKILL.md
```

### Gemini CLI

```bash
gemini skills install github:drvoss/llm-wiki-skill
```

---

## 빠른 시작

```powershell
# 1. 위키 경로 지정
$env:LLM_WIKI_PATH = "$HOME/wiki"

# 2. 이 저장소를 로컬에서 쓰고 있다면 위키 골격 생성
python3 scripts/wiki-init.py $env:LLM_WIKI_PATH --template tech-stack --domain "AI coding tools"

# 3. 첫 소스 ingest
# > Ingest this article into the wiki: [URL or paste text]

# 4. 위키 질의
# > What do we know about agentic coding patterns?

# 5. lint 실행
python3 scripts/wiki-lint.py
```

프로젝트 반영, Copilot에서 설치 확인, 위키가 자라나는 모습, 더 잘 쓰는 요령까지
한 번에 보려면 [docs/TUTORIAL.ko.md](docs/TUTORIAL.ko.md)를 보세요.

---

## 세 가지 핵심 작업

| 작업 | 트리거 | 수행 내용 |
|-----------|---------|-------------|
| **Ingest** | "Add this to the wiki", URL/텍스트 제공 | raw 저장 -> 중복 확인 -> 페이지 생성/수정 -> index + log 갱신 |
| **Query** | "What does the wiki say about X?" | index 읽기 -> 관련 페이지 찾기 -> 합성 -> 필요하면 결과 파일링 |
| **Lint** | "Check the wiki" 또는 `python3 scripts/wiki-lint.py` | orphan, broken link, index 누락, frontmatter 문제, stale content 점검 |

---

## 구조

```
llm-wiki-skill/
|- SKILL.md
|- scripts/
|  |- wiki-init.py
|  |- wiki-lint.py
|  \- wiki-stats.py
|- templates/
|  |- SCHEMA-tech-stack.md
|  |- SCHEMA-codebase.md
|  |- SCHEMA-product-intelligence.md
|  |- SCHEMA-research.md
|  \- pages/
|- docs/
|- examples/
|  \- sample-wiki/
\- extensions/
   |- arxiv/SKILL.md
   |- github/SKILL.md
   \- obsidian/SKILL.md
```

---

## `$LLM_WIKI_PATH` 아래 생성되는 위키 구조

```
~/wiki/
|- SCHEMA.md
|- index.md
|- log.md
|- raw/
|- entities/
|- concepts/
|- comparisons/
\- queries/
```

---

## 확장

기본 `SKILL.md`는 외부 의존성이 없습니다. 확장은 선택형입니다.

| 확장 | 기능 |
|-----------|-------------|
| [`extensions/arxiv`](extensions/arxiv/SKILL.md) | ingest 중 arXiv 검색 |
| [`extensions/github`](extensions/github/SKILL.md) | GitHub issues, PR, release, README 자료 ingest |
| [`extensions/obsidian`](extensions/obsidian/SKILL.md) | Obsidian vault + headless sync |

---

## Lint 스크립트

```bash
python3 scripts/wiki-init.py ~/wiki/ai-coding-tools --template tech-stack --domain "AI coding tools"
python3 scripts/wiki-lint.py
python3 scripts/wiki-lint.py ~/my-project-wiki
python3 scripts/wiki-lint.py --strict ~/my-project-wiki
python3 scripts/wiki-lint.py --json ~/my-project-wiki
python3 scripts/wiki-lint.py --fix ~/my-project-wiki
python3 scripts/wiki-stats.py ~/my-project-wiki
```

점검 항목: broken wikilink, source 파일 누락, orphan page, index 누락, frontmatter 누락,
알 수 없는 태그, 최소 outbound link, contradiction 대상, index header 메타데이터,
과도하게 긴 페이지, stale content, log rotation.

`wiki-stats.py`는 페이지 수, 링크 밀도, raw source 수, 최근 활동을 빠르게 요약하는
보조 스크립트입니다.

---

## Hermes Agent 및 everything-copilot-cli 와의 관계

이 저장소는
[`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent)의
`llm-wiki` 스킬에서 출발해, 여러 런타임에서 쓸 수 있는 독립 패키지로 확장한 것입니다.

또한
[everything-copilot-cli](https://github.com/drvoss/everything-copilot-cli)와도
의도적으로 분리해 두었습니다. `llm-wiki-skill`은 단일 `SKILL.md`를 넘어
템플릿, lint 도구, 튜토리얼, 예시, 확장을 함께 제공하는 저장소이기 때문입니다.

---

## 라이선스

MIT
