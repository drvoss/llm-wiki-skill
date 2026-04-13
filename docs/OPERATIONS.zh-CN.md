# llm-wiki 运营指南

**语言:** [English](OPERATIONS.md) | [한국어](OPERATIONS.ko.md) | [简体中文](OPERATIONS.zh-CN.md)

这份文档关注首次上手之后的 day-2 工作：去重、批量 ingest、lint 纪律、
归档标准以及长期维护方式。

---

## 1. 运营模型

- `raw/` 是不可变原始资料层
- `entities/`, `concepts/`, `comparisons/`, `queries/` 是整理后的知识层
- `SCHEMA.md` 是规则契约
- `index.md` 和 `log.md` 是导航骨架

推荐节奏：

1. ingest 一批相关资料
2. 一次性更新相关页面
3. 运行 `wiki-lint.py`
4. 立即修正 taxonomy 或导航漂移

---

## 2. 重复页面清理

建议规则：

- 覆盖同一实体/概念时 **合并**
- 范围不同则 **保留分离**
- 完全被替代时 **归档**

推荐步骤：

1. 选定保留页
2. 合并有效内容
3. 修正重要链接
4. 从 `index.md` 中移除旧页
5. 在 `log.md` 中记录

---

## 3. 处理 Schema Drift

常见表现：

- 相近标签越来越多
- 页面范围开始混杂
- 文件命名规则变得不一致

处理顺序：

1. 先收紧 `SCHEMA.md` 的 taxonomy
2. 再批量调整页面标签
3. 检查标题和文件名
4. 运行 `wiki-lint.py --strict`

---

## 4. Batch Ingest 策略

如果多份资料讨论的是同一主题，不要一篇篇独立处理。

建议顺序：

1. 先读完所有相关资料
2. 列出重复出现的 entity / concept
3. 一次性搜索已有 wiki
4. 一次性创建或更新页面
5. 只更新一次 `index.md`
6. 只写一条 `log.md`

---

## 5. Query 存档规则

`queries/` 里应只保留那些重新推导会很痛苦的答案。

适合存档的：

- 综合多个页面的答案
- 以后大概率还会再问的问题
- 支撑重复决策的问题

不适合存档的：

- 简单查找
- 一句话事实答案
- 很容易重新得到的回答

---

## 6. Stale 页面审查

stale 页面不一定是坏页面。

- 仍然准确且有用：保留
- 部分过时但仍相关：更新
- 已完全被取代：归档

重点应该是提高质量，而不是为了“更新”而更新。

---

## 7. 归档流程

推荐步骤：

1. 把页面移到 `_archive/`
2. 从 `index.md` 中移除
3. 修正关键 wikilink
4. 在 `log.md` 中写清由什么替代

不要归档 raw source。raw 是你的 provenance 层。

---

## 8. Lint 工作流

```bash
python3 scripts/wiki-lint.py ~/wiki/my-domain
python3 scripts/wiki-lint.py --strict ~/wiki/my-domain
python3 scripts/wiki-lint.py --json ~/wiki/my-domain
python3 scripts/wiki-lint.py --fix ~/wiki/my-domain
```

- 日常维护：普通 lint
- CI / 共享仓库：`--strict`
- 自动化：`--json`
- 安全元数据修复：`--fix`

---

## 9. Stats 工作流

当你想快速看整体状态而不是错误列表时，使用 `wiki-stats.py`。

```bash
python3 scripts/wiki-stats.py ~/wiki/my-domain
python3 scripts/wiki-stats.py --json ~/wiki/my-domain
```

适合用于：

- 检查 wiki 是否真的在增长
- 查看不同页面类型的分布
- 判断 raw source 和整理后页面是否同步增长

---

## 10. 维护节奏建议

### 每次有意义的 ingest 之后

- 更新相关页面
- 更新 index/log
- 运行 lint

### 一批资料处理完成后

- 做一次命名和标签整理
- 如有必要，存入 1-2 个高价值 query

### 定期

- 审查 stale 页面
- 清理标签膨胀
- 归档过时页面

这样就足以在不过度流程化的前提下保持 wiki 健康。
