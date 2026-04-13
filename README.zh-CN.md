# llm-wiki-skill

**语言:** [English](README.md) | [한국어](README.ko.md) | [简体中文](README.zh-CN.md)

**教程:** [English](docs/TUTORIAL.md) | [한국어](docs/TUTORIAL.ko.md) | [简体中文](docs/TUTORIAL.zh-CN.md)

**运营指南:** [English](docs/OPERATIONS.md) | [한국어](docs/OPERATIONS.ko.md) | [简体中文](docs/OPERATIONS.zh-CN.md)

这是一个独立的、与运行时无关的 skill，用来构建和维护可持续累积的
Markdown 知识库，基于
[Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

兼容 GitHub Copilot CLI、Claude Code、Codex CLI、Gemini CLI，以及任何
[agentskills.io](https://agentskills.io) 兼容运行时。

---

## 为什么会有这个仓库

`llm-wiki-skill` 把
[`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent)
中已经验证过的思路，整理成一个可在多种运行时复用的通用 skill 包。

在 Hermes Agent 里，`llm-wiki` 是更大代理系统中的一个内置 skill；而在这个仓库里，
它被拆分成一个独立包，并附带：

- 核心工作流 `SKILL.md`
- 面向不同领域的 `templates/`
- 零依赖检查脚本 `scripts/wiki-lint.py`
- 快速查看整体状态的 `scripts/wiki-stats.py`
- 参考示例 `examples/`
- 可选扩展 `extensions/`，如 arXiv、GitHub 和 Obsidian

这样就能在不引入 Hermes 专属配置和运行时假设的情况下，复用同样的知识管理模式。

---

## 它解决什么问题

大多数 AI 会话都会从零开始。你需要反复解释同一个领域，代理反复读取相同来源，
再次发现相同关系，工作无法累积。

**llm-wiki** 反过来做这件事：代理把知识整理成互相链接的 Markdown 文件。
下一次会话只要先阅读 SCHEMA、index 和最近的 log，就能在已有成果上继续推进。
交叉引用已经存在，矛盾已经标记，综合结论也会持续沉淀。

---

## 从这里开始

- 阅读上手教程：[docs/TUTORIAL.zh-CN.md](docs/TUTORIAL.zh-CN.md)
- 参考运营指南：[docs/OPERATIONS.zh-CN.md](docs/OPERATIONS.zh-CN.md)
- 把 skill 安装到你使用的运行时
- 选择一个真实领域初始化 wiki
- 先导入几份资料，再评价这套工作流

---

## 安装

### GitHub Copilot CLI

```bash
# 项目级安装
cp SKILL.md .github/skills/llm-wiki/SKILL.md

# 用户级安装
cp SKILL.md ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
# 项目级
New-Item -ItemType Directory -Force .github\skills\llm-wiki | Out-Null
Copy-Item SKILL.md .github\skills\llm-wiki\SKILL.md

# 用户级
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

## 快速开始

```powershell
# 1. 设置 wiki 路径
$env:LLM_WIKI_PATH = "$HOME/wiki"

# 2. 如果你在本地使用这个仓库，可以先生成 wiki 骨架
python3 scripts/wiki-init.py $env:LLM_WIKI_PATH --template tech-stack --domain "AI coding tools"

# 3. 导入第一份资料
# > Ingest this article into the wiki: [URL or paste text]

# 4. 查询 wiki
# > What do we know about agentic coding patterns?

# 5. 运行 lint
python3 scripts/wiki-lint.py
```

如果你想看完整场景，包括如何集成到项目、如何在 Copilot 中确认已安装、
wiki 会如何逐步长出来，以及如何更好地使用，请阅读
[docs/TUTORIAL.zh-CN.md](docs/TUTORIAL.zh-CN.md)。

---

## 三个核心操作

| 操作 | 触发方式 | 发生什么 |
|-----------|---------|-------------|
| **Ingest** | “Add this to the wiki” 或提供 URL/文本 | 保存 raw 来源 -> 检查重复 -> 创建/更新页面 -> 更新 index 与 log |
| **Query** | “What does the wiki say about X?” | 读取 index -> 找到相关页面 -> 综合回答 -> 必要时存档结果 |
| **Lint** | “Check the wiki” 或 `python3 scripts/wiki-lint.py` | 检查孤儿页、坏链、index 缺失、frontmatter 问题、过期内容 |

---

## 仓库结构

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

## `$LLM_WIKI_PATH` 中生成的 wiki 结构

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

## 扩展

核心 `SKILL.md` 没有外部依赖，扩展是可选的。

| 扩展 | 作用 |
|-----------|-------------|
| [`extensions/arxiv`](extensions/arxiv/SKILL.md) | 在 ingest 时搜索 arXiv |
| [`extensions/github`](extensions/github/SKILL.md) | ingest GitHub issues、PR、release 和 README 材料 |
| [`extensions/obsidian`](extensions/obsidian/SKILL.md) | 使用 Obsidian vault 并支持无界面同步 |

---

## Lint 脚本

```bash
python3 scripts/wiki-init.py ~/wiki/ai-coding-tools --template tech-stack --domain "AI coding tools"
python3 scripts/wiki-lint.py
python3 scripts/wiki-lint.py ~/my-project-wiki
python3 scripts/wiki-lint.py --strict ~/my-project-wiki
python3 scripts/wiki-lint.py --json ~/my-project-wiki
python3 scripts/wiki-lint.py --fix ~/my-project-wiki
python3 scripts/wiki-stats.py ~/my-project-wiki
```

检查内容包括：坏的 wikilink、source 文件缺失、孤儿页、index 缺失、
frontmatter 缺失、未知标签、最少 outbound link、contradiction 目标、
index header 元数据、页面过大、内容过旧、log 轮转。

`wiki-stats.py` 可快速汇总页面数量、链接密度、raw source 数量和最近活动。

---

## 与 Hermes Agent 及 everything-copilot-cli 的关系

这个仓库起点是
[`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent)
中的 `llm-wiki` skill，随后被扩展成一个面向多运行时的独立包。

它也被有意与
[everything-copilot-cli](https://github.com/drvoss/everything-copilot-cli)
分开维护，因为 `llm-wiki-skill` 不只是单个 `SKILL.md`，还包含模板、lint 工具、
教程、示例和扩展。

---

## License

MIT
