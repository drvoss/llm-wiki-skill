# llm-wiki-skill 教程

**语言:** [English](TUTORIAL.md) | [한국어](TUTORIAL.ko.md) | [简体中文](TUTORIAL.zh-CN.md)

本教程按一个真实使用场景来走：

1. 安装 `llm-wiki-skill`
2. 集成到项目中
3. 在 Copilot 中确认已经可用
4. 观察 wiki 如何随着使用逐步长出来
5. 学会更高效的使用方式

---

## 场景

假设你的团队正在评估 AI 编码工具。你需要的不只是聊天记录，而是一个能持续积累的知识库，用来保存：

- 原始资料
- 摘要与比较
- 每次变化的记录
- 一个能快速判断 wiki 是否在持续成长的状态视图

这正是 `llm-wiki-skill` 的用途。

本教程也有一个背景前提：这套工作流最早在 Hermes Agent 中得到验证，后来被
拆分成这个独立仓库，以便在 Copilot、Codex、Claude Code、Gemini 等运行时中
复用，而不需要带上 Hermes 专属配置。

---

## 1. 安装 skill

### Copilot CLI 项目级安装

在仓库根目录执行：

```bash
mkdir -p .github/skills/llm-wiki
cp SKILL.md .github/skills/llm-wiki/SKILL.md
```

```powershell
New-Item -ItemType Directory -Force .github\skills\llm-wiki | Out-Null
Copy-Item SKILL.md .github\skills\llm-wiki\SKILL.md
```

当你希望 skill 随项目一起分发时，使用这种方式。

### Copilot CLI 用户级安装

```bash
mkdir -p ~/.copilot/skills/llm-wiki
cp SKILL.md ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
New-Item -ItemType Directory -Force $HOME\.copilot\skills\llm-wiki | Out-Null
Copy-Item SKILL.md $HOME\.copilot\skills\llm-wiki\SKILL.md
```

当你希望所有会话都可用时，使用这种方式。

### 其他运行时

```bash
# Claude Code
cp SKILL.md ~/.claude/skills/llm-wiki/SKILL.md

# Codex CLI
cp SKILL.md ~/.codex/skills/llm-wiki/SKILL.md

# Gemini CLI
gemini skills install github:drvoss/llm-wiki-skill
```

---

## 2. 反映到你的项目中

先为项目决定一个 wiki 路径：

```powershell
$env:LLM_WIKI_PATH = "$HOME\wiki\ai-coding-tools"
```

常见模式：

- **每个仓库一个 wiki**：适合代码库知识
- **每个领域一个 wiki**：适合长期研究或市场分析
- **团队共享 wiki**：适合同一主题跨项目反复使用

如果你希望它自动生效，可以把 `LLM_WIKI_PATH` 写入 shell profile
或项目的启动脚本。

---

## 3. 确认 Copilot 能看到这个 skill

这里没有专门的“已安装 skill 列表”界面，所以最实用的确认方式是直接调用它。

1. 在项目目录中启动 Copilot CLI。
2. 直接给它一个明显会触发该 skill 的提示。

例如：

```text
Initialize a new llm-wiki at $env:LLM_WIKI_PATH about AI coding tools.
```

或者：

```text
What is the llm-wiki workflow you have available in this session?
```

如果 skill 已正确加载，Copilot 的回答通常会围绕：

- SCHEMA / index / log
- ingest / query / lint
- Markdown wiki 结构

你也可以顺手确认文件确实在位：

```bash
ls .github/skills/llm-wiki/SKILL.md
```

```powershell
Get-Item .github\skills\llm-wiki\SKILL.md
```

若是用户级安装：

```bash
ls ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
Get-Item $HOME\.copilot\skills\llm-wiki\SKILL.md
```

可用下面的快速检查清单：

- Copilot 的回答是否围绕 **SCHEMA / index / log**
- Copilot 是否以 **ingest / query / lint** 的工作流来描述，而不是泛泛的记笔记
- skill 文件是否确实存在于预期路径

---

## 4. 初始化 wiki

如果你是在本地 clone 这个仓库，可以先用 helper 脚本生成目录骨架，再让
Copilot 接着往下做：

```bash
python3 scripts/wiki-init.py ~/wiki/ai-coding-tools --template tech-stack --domain "AI coding tools used by our platform team"
```

之后你可以让 Copilot 接着完善，也可以直接让它从头初始化。

向 Copilot 发送：

```text
Initialize a new llm-wiki at $env:LLM_WIKI_PATH about AI coding tools used by our platform team.
```

初始化后，目录大致会变成这样：

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

各部分含义：

| 文件 | 作用 |
|------|------|
| `SCHEMA.md` | 定义领域边界、规则和标签体系 |
| `index.md` | 页面目录与一行摘要 |
| `log.md` | ingest/query/lint 的追加式记录 |
| `raw/` | 不可变的原始资料 |
| `entities/`, `concepts/`, `comparisons/`, `queries/` | 由代理维护的知识页面 |

---

## 5. 导入第一份资料

现在给代理一份真实资料：

```text
Ingest this article into the wiki: https://example.com/article-about-coding-agents
```

也可以直接粘贴文本：

```text
Ingest this transcript into the wiki and focus on agent orchestration trade-offs:
[paste text here]
```

一次高质量的 ingest 之后，通常会出现这样的变化：

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

典型变化包括：

- 原始资料保存在 `raw/`
- 一个或多个 entity/concept 页面被创建或更新
- `index.md` 增加新条目
- `log.md` 记录这次变化

关键点是：**原始资料和综合后的知识是分开的。**

---

## 5A. 快速看 wiki 状态

想找问题时用 `wiki-lint.py`，想快速看整体状态时用 `wiki-stats.py`。

```bash
python3 scripts/wiki-stats.py ~/wiki/ai-coding-tools
python3 scripts/wiki-stats.py --json ~/wiki/ai-coding-tools
```

它适合用来快速查看页面分布、raw source 增长和最近活动。

---

## 6. 查询 wiki

导入几份资料后，就可以提问：

```text
What does the wiki say about the difference between Copilot CLI and Codex CLI?
```

理想表现通常是：

- Copilot 先读取 `index.md`
- 找到相关的 entity 与 concept 页面
- 基于已经整理好的 wiki 综合回答，而不是从零重读所有资料
- 如果答案很有价值，会存入 `queries/` 或 `comparisons/`

例如：

```text
ai-coding-tools/
|- comparisons/
|  \- copilot-cli-vs-codex-cli.md
\- queries/
   \- when-to-use-agentic-cli-tools.md
```

---

## 7. 运行 lint 保持 wiki 健康

使用内置脚本：

```bash
python3 scripts/wiki-lint.py
```

也可以指定某个 wiki：

```bash
python3 scripts/wiki-lint.py ~/wiki/ai-coding-tools
```

有用的参数：

- `--strict`：把 warning 也视为失败
- `--json`：输出机器可读结果
- `--fix`：自动修正 `index.md` header 之类的安全元数据

以下情况尤其建议运行 lint：

- 一次 ingest 改动了很多页面之后
- 链接开始变乱
- 标签体系开始漂移
- wiki 越来越难导航

---

## 8. 随着时间推移，wiki 会变成什么样

### 第一天

- 少量 raw 来源
- 几个 concept/entity 页面
- 一个还小但有用的 index

### 几次会话后

- 重复主题不再需要每次从头解释
- 对比文档更容易维护
- 矛盾会被记录，而不是被遗忘
- 代理的起点变成已整理的 wiki，而不是零

### 长期使用后

- `queries/` 会变成高价值答案库
- `comparisons/` 会变成决策记录
- `SCHEMA.md` 会成为维持整体一致性的契约

---

## 9. 如何得到更好的结果

### 先从窄领域开始

好的范围：

- “平台团队使用的 AI 编码工具”
- “这个代码库的 ingestion pipeline”
- “agent memory 模式研究”

不好的范围：

- “所有软件”
- “AI 的一切”

### 保持 raw 来源不可变

不要在 ingest 之后修改 `raw/`。理解变化应该写进 wiki 页面，而不是回头改原文副本。

### 把 schema 写具体

模糊的 `SCHEMA.md` 会得到模糊的页面。领域越明确、标签体系越清晰，效果越好。

### 相关来源尽量批量 ingest

如果你有 5 篇相关资料，批量处理通常比一篇篇单独处理更容易形成稳定的
entity/concept 结构。

### 只保存有长期价值的答案

不要把每个琐碎回答都写进文件。只保存那些重新推导会很痛苦的答案。

### 定期运行 lint

一旦链接、标签和导航变差，wiki 的价值也会随之下降。

### 只在有帮助时再启用扩展

- 论文研究较多时用 `extensions/arxiv`
- 想要 vault 和图谱视图时用 `extensions/obsidian`

---

## 10. 推荐的第一轮工作流

1. 在 Copilot CLI 中安装 skill
2. 初始化一个范围明确的 wiki
3. 导入 3-5 份有意义的资料
4. 基于 wiki 提 2-3 个真实问题
5. 运行 lint
6. 根据实际需要的标签和页面类型回头调整 `SCHEMA.md`

通常做到这里，就足以判断这套模式是否适合你的团队或项目。

如果你想看初始化之后的长期维护方式，请继续阅读 [docs/OPERATIONS.zh-CN.md](OPERATIONS.zh-CN.md)。
