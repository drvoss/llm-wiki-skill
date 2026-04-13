# llm-wiki-skill 튜토리얼

**언어:** [English](TUTORIAL.md) | [한국어](TUTORIAL.ko.md) | [简体中文](TUTORIAL.zh-CN.md)

이 튜토리얼은 실제 사용 흐름을 기준으로 설명합니다.

1. `llm-wiki-skill` 설치
2. 프로젝트에 반영
3. Copilot에서 설치 확인
4. 사용하면서 위키가 어떻게 자라는지 확인
5. 더 잘 사용하는 운영 습관 익히기

---

## 시나리오

플랫폼 팀이 AI 코딩 도구를 평가한다고 가정해 봅시다. 단순한 채팅 기록이 아니라,
다음이 남는 지식 베이스가 필요합니다.

- 원문 소스 보관
- 요약과 비교 정리
- 무엇이 언제 바뀌었는지에 대한 기록
- 위키가 실제로 자라고 있는지 보는 빠른 현황 요약

이 역할을 `llm-wiki-skill`이 맡습니다.

이 튜토리얼은 이 워크플로가 원래 Hermes Agent 안에서 검증되었고, 이후 Hermes
전용 설정 없이 Copilot, Codex, Claude Code, Gemini 등에서 재사용할 수 있도록
독립 저장소로 분리되었다는 맥락 위에서 작성되었습니다.

---

## 1. 스킬 설치

### Copilot CLI 프로젝트 단위 설치

저장소 루트에서:

```bash
mkdir -p .github/skills/llm-wiki
cp SKILL.md .github/skills/llm-wiki/SKILL.md
```

```powershell
New-Item -ItemType Directory -Force .github\skills\llm-wiki | Out-Null
Copy-Item SKILL.md .github\skills\llm-wiki\SKILL.md
```

이 방식은 스킬 설정을 프로젝트와 함께 배포하고 싶을 때 적합합니다.

### Copilot CLI 사용자 단위 설치

```bash
mkdir -p ~/.copilot/skills/llm-wiki
cp SKILL.md ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
New-Item -ItemType Directory -Force $HOME\.copilot\skills\llm-wiki | Out-Null
Copy-Item SKILL.md $HOME\.copilot\skills\llm-wiki\SKILL.md
```

모든 세션에서 공통으로 쓰고 싶다면 이 방식이 편합니다.

### 다른 런타임

```bash
# Claude Code
cp SKILL.md ~/.claude/skills/llm-wiki/SKILL.md

# Codex CLI
cp SKILL.md ~/.codex/skills/llm-wiki/SKILL.md

# Gemini CLI
gemini skills install github:drvoss/llm-wiki-skill
```

---

## 2. 프로젝트에 반영

프로젝트에서 사용할 위키 경로를 정합니다.

```powershell
$env:LLM_WIKI_PATH = "$HOME\wiki\ai-coding-tools"
```

자주 쓰는 패턴:

- **저장소별 위키**: 코드베이스 지식 축적에 적합
- **도메인별 위키**: 장기 리서치나 시장 조사에 적합
- **팀 공용 위키**: 여러 프로젝트에서 같은 주제를 반복 탐구할 때 적합

반복 사용한다면 쉘 프로필이나 프로젝트 부트스트랩 스크립트에
`LLM_WIKI_PATH`를 넣어두는 편이 좋습니다.

---

## 3. Copilot에서 설치 확인

이 저장소가 별도의 "설치된 스킬 목록" 화면을 제공하는 것은 아니므로,
실제로 스킬을 호출해 확인하는 방식이 가장 확실합니다.

1. 프로젝트 루트에서 Copilot CLI를 시작합니다.
2. 아래처럼 직접 스킬 사용을 유도하는 프롬프트를 보냅니다.

```text
Initialize a new llm-wiki at $env:LLM_WIKI_PATH about AI coding tools.
```

또는:

```text
What is the llm-wiki workflow you have available in this session?
```

스킬이 정상 로드되었다면 Copilot은 일반적인 임의 응답보다,
SCHEMA/index/log, ingest/query/lint, 마크다운 위키 운영 흐름 중심으로 반응합니다.

파일 자체도 확인해 두면 좋습니다.

```bash
ls .github/skills/llm-wiki/SKILL.md
```

```powershell
Get-Item .github\skills\llm-wiki\SKILL.md
```

사용자 단위 설치라면:

```bash
ls ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
Get-Item $HOME\.copilot\skills\llm-wiki\SKILL.md
```

간단한 체크리스트:

- Copilot 응답이 **SCHEMA / index / log** 중심인지
- Copilot이 일반 메모가 아니라 **ingest / query / lint** 워크플로로 설명하는지
- 설치된 skill 파일이 예상 경로에 실제로 존재하는지

---

## 4. 위키 초기화

이 저장소를 로컬 clone으로 사용 중이라면, 먼저 helper 스크립트로 디렉터리
골격을 만든 뒤 Copilot에게 이어서 작업하게 할 수 있습니다.

```bash
python3 scripts/wiki-init.py ~/wiki/ai-coding-tools --template tech-stack --domain "AI coding tools used by our platform team"
```

그 다음 Copilot에게 이어서 정리하게 하거나, 처음부터 Copilot에게 초기화를
맡겨도 됩니다.

Copilot에게 이렇게 요청합니다.

```text
Initialize a new llm-wiki at $env:LLM_WIKI_PATH about AI coding tools used by our platform team.
```

초기화 후에는 대략 이런 구조가 생깁니다.

```text
ai-coding-tools/
|- SCHEMA.md
|- index.md
|- log.md
|- raw/
|  |- articles/
|  |- papers/
|  |- transcripts/
|  \- assets/
|- entities/
|- concepts/
|- comparisons/
\- queries/
```

각 파일의 역할:

| 파일 | 역할 |
|------|------|
| `SCHEMA.md` | 도메인 범위, 규칙, 태그 taxonomy |
| `index.md` | 페이지 목록과 한 줄 요약 |
| `log.md` | ingest/query/lint 이력 |
| `raw/` | 변경하지 않는 원문 보관 |
| `entities/`, `concepts/`, `comparisons/`, `queries/` | 에이전트가 관리하는 지식 페이지 |

---

## 5. 첫 소스 ingest

이제 실제 자료를 넣습니다.

```text
Ingest this article into the wiki: https://example.com/article-about-coding-agents
```

또는 텍스트를 직접 붙여넣을 수 있습니다.

```text
Ingest this transcript into the wiki and focus on agent orchestration trade-offs:
[paste text here]
```

한 번의 제대로 된 ingest 후에는 보통 이런 변화가 생깁니다.

```text
ai-coding-tools/
|- raw/
|  \- articles/
|     \- article-about-coding-agents-2026-04.md
|- entities/
|  \- github-copilot.md
|- concepts/
|  |- agentic-coding.md
|  \- tool-orchestration.md
|- index.md
\- log.md
```

보통 일어나는 일:

- 원문이 `raw/` 아래 저장됨
- entity/concept 페이지가 새로 생기거나 업데이트됨
- `index.md`에 새 항목이 추가됨
- `log.md`에 변경 이력이 기록됨

중요한 점은 **원문과 해석이 분리되어 남는다**는 것입니다.

---

## 5A. 위키 현황 빠르게 보기

문제 목록을 보고 싶으면 `wiki-lint.py`, 현재 상태를 빠르게 보고 싶으면
`wiki-stats.py`를 사용하세요.

```bash
python3 scripts/wiki-stats.py ~/wiki/ai-coding-tools
python3 scripts/wiki-stats.py --json ~/wiki/ai-coding-tools
```

페이지 타입 분포, raw source 증가, 최근 활동을 빠르게 확인할 때 유용합니다.

---

## 6. 위키에 질문하기

소스가 몇 개 쌓이면 질문합니다.

```text
What does the wiki say about the difference between Copilot CLI and Codex CLI?
```

좋은 동작은 대체로 이렇습니다.

- Copilot이 먼저 `index.md`를 읽음
- 관련 entity/concept 페이지를 찾음
- 원문 전체를 다시 훑기보다 이미 정리된 위키를 기준으로 합성함
- 답변 가치가 높으면 `queries/`나 `comparisons/`에 저장함

예를 들어:

```text
ai-coding-tools/
|- comparisons/
|  \- copilot-cli-vs-codex-cli.md
\- queries/
   \- when-to-use-agentic-cli-tools.md
```

---

## 7. lint로 위키 건강 점검

포함된 스크립트를 사용합니다.

```bash
python3 scripts/wiki-lint.py
```

특정 위키를 지정할 수도 있습니다.

```bash
python3 scripts/wiki-lint.py ~/wiki/ai-coding-tools
```

유용한 플래그:

- `--strict` : warning도 실패로 처리
- `--json` : 기계 판독용 출력
- `--fix` : `index.md` header 같은 안전한 메타데이터 자동 수정

다음 상황에서 lint를 돌리면 좋습니다.

- 큰 ingest로 여러 페이지가 바뀐 뒤
- 링크가 어색해지기 시작할 때
- 태그가 흔들리기 시작할 때
- 위키가 점점 탐색하기 어려워질 때

---

## 8. 시간이 지나며 위키가 어떻게 바뀌는가

### 첫날

- raw 소스 몇 개
- concept/entity 페이지 몇 개
- 작지만 유용한 index

### 몇 세션 후

- 반복 주제는 처음부터 다시 설명할 필요가 줄어듦
- 비교 문서를 유지하기 쉬워짐
- 모순이 사라지지 않고 기록됨
- 에이전트가 0부터 시작하지 않고 누적 지식을 출발점으로 삼음

### 더 오래 쓰면

- `queries/`는 재활용 가능한 해답 라이브러리가 되고
- `comparisons/`는 의사결정 기록이 되며
- `SCHEMA.md`는 위키 일관성을 지키는 계약이 됩니다

---

## 9. 더 잘 쓰는 방법

### 처음에는 좁은 도메인으로 시작

좋은 예:

- "플랫폼 팀이 쓰는 AI 코딩 도구"
- "이 코드베이스의 ingestion pipeline"
- "agent memory 패턴 연구"

나쁜 예:

- "모든 소프트웨어"
- "AI 전부"

### raw 소스는 불변으로 유지

`raw/`는 ingest 후 수정하지 않는 편이 좋습니다. 이해가 바뀌면 위키 페이지를
고치고, 원문 사본은 그대로 두세요.

### schema를 구체적으로 작성

모호한 `SCHEMA.md`는 모호한 페이지를 낳습니다. 도메인과 태그 taxonomy가
구체적일수록 결과가 좋아집니다.

### 관련 소스는 배치로 ingest

서로 관련된 글 5개를 각각 처리하는 것보다, 한 번에 묶어서 ingest하면
entity/concept 구조가 더 잘 잡힙니다.

### 오래 쓸 답만 저장

사소한 응답은 굳이 파일로 남기지 말고, 다시 만들기 힘든 답만 `queries/`나
`comparisons/`에 저장하세요.

### lint를 자주 실행

링크, 태그, 탐색성이 망가지면 위키 가치도 같이 떨어집니다.

### 확장은 필요할 때만 추가

- 논문 중심 리서치면 `extensions/arxiv`
- 시각적 graph view와 vault가 필요하면 `extensions/obsidian`

---

## 10. 추천 첫 워크플로

1. Copilot CLI에 스킬 설치
2. 범위를 좁힌 위키 하나 초기화
3. 의미 있는 소스 3-5개 ingest
4. 실제 질문 2-3개 수행
5. lint 실행
6. 실제로 필요했던 태그와 페이지 타입을 기준으로 `SCHEMA.md` 조정

이 정도면 이 패턴이 팀이나 프로젝트에 맞는지 판단하기 충분합니다.

초기 설정 이후의 운영 흐름은 [docs/OPERATIONS.ko.md](OPERATIONS.ko.md)를 보세요.
