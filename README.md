<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://github.com/Misty02600/nonebot-plugin-template/releases/download/assets/NoneBotPlugin.png" width="310" alt="logo"></a>

## ✨ nonebot-plugin-template ✨

[![python](https://img.shields.io/badge/python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-black?logo=uv)](https://github.com/astral-sh/uv)
[![ruff](https://img.shields.io/badge/code%20style-ruff-black?logo=ruff)](https://github.com/astral-sh/ruff)

</div>

从模板新建仓库，先到 Settings -> Actions -> General 打开 Workflow permissions 的 Read and write，再创建 LICENSE（会触发初始化工作流）。

---

## 目录

- [快速开始](#快速开始)
- [工具链概览](#工具链概览)
- [本地命令（just）](#本地命令just)
- [预提交钩子系统](#预提交钩子系统)
- [代码质量工具](#代码质量工具)
- [测试框架](#测试框架)
- [版本管理与变更日志](#版本管理与变更日志)
- [CI/CD 工作流](#cicd-工作流)
- [项目配置参考](#项目配置参考)

---

## 快速开始

```bash
# 建议使用 Python 3.12+，uv 会自动创建虚拟环境
uv sync --all-groups

# 安装 git 钩子（推荐用 prek）
just hooks
```

---

## 工具链概览

本模板采用现代化 Python 开发工具链，各工具职责明确：


| 类别                | 工具                                                         | 作用                           | 配置位置                           |
| ------------------- | ------------------------------------------------------------ | ------------------------------ | ---------------------------------- |
| **包管理与构建**    | [uv](https://github.com/astral-sh/uv)                        | 虚拟环境、依赖安装、构建、发布 | `pyproject.toml`                   |
| **任务编排**        | [just](https://github.com/casey/just)                        | 命令行任务运行器               | `justfile`                         |
| **代码检查/格式化** | [Ruff](https://github.com/astral-sh/ruff)                    | Lint + Format 一站式检查       | `pyproject.toml [tool.ruff]`       |
| **类型检查**        | [BasedPyright](https://github.com/DetachHead/basedpyright)   | 严格静态类型检查               | `pyproject.toml [tool.pyright]`    |
| **测试**            | [pytest](https://pytest.org/)                                | 单元测试框架                   | `pyproject.toml [tool.pytest]`     |
| **预提交钩子**      | [prek](https://github.com/j178/prek)                         | Git 钩子管理                   | `.pre-commit-config.yaml`          |
| **提交规范**        | [commitizen](https://github.com/commitizen-tools/commitizen) | 约定式提交校验与版本管理       | `pyproject.toml [tool.commitizen]` |
| **变更日志**        | [git-cliff](https://github.com/orhun/git-cliff)              | 自动生成 CHANGELOG             | `cliff.toml`                       |

---

## 本地命令（just）

`justfile` 封装了常用开发任务，简化命令行操作：

```bash
just           # 列出所有可用命令
just test      # 运行测试（pytest -n auto 并行，输出 coverage.xml 和 junit.xml）
just lint      # 代码检查与格式化（ruff check --fix + ruff format）
just check     # 类型检查（basedpyright）
just hooks     # 安装预提交钩子（uv run prek install）
just update    # 更新预提交钩子版本（uv run prek autoupdate）
just changelog # 生成最新变更日志（uv run git-cliff --latest）
just bump      # 版本升级（cz bump + uv lock，生成 tag）
```

### 命令详解


| 命令         | 等价于                                                                    | 说明                                       |
| ------------ | ------------------------------------------------------------------------- | ------------------------------------------ |
| `just test`  | `uv run pytest --cov=src --cov-report xml --junitxml=./junit.xml -n auto` | 并行运行测试，生成覆盖率和 JUnit 报告      |
| `just lint`  | `uv run ruff check . --fix && uv run ruff format .`                       | 自动修复 lint 问题并格式化代码             |
| `just check` | `uv run basedpyright`                                                     | 运行静态类型检查                           |
| `just bump`  | `uv run cz bump && uv lock`                                               | 根据提交历史自动升级版本号，更新 lock 文件 |

---

## 预提交钩子系统

### 钩子运行器：prek

本项目**必须使用 [prek](https://github.com/j178/prek)** 作为预提交钩子运行器，**不能使用 pre-commit**。

> ⚠️ **注意**：配置文件使用了 `repo: builtin` 语法，这是 prek 特有的功能，pre-commit 不支持。

prek 是 pre-commit 的高性能替代品，具有以下优势：

- ⚡ **更快的执行速度**：基于 Python 包缓存，避免重复创建虚拟环境
- 🔧 **内置常用钩子**：通过 `repo: builtin` 直接使用，无需指定远程仓库
- 📦 **轻量级**：无需全局安装，通过 `uv run prek` 直接使用

#### 安装 prek

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://github.com/j178/prek/releases/download/v0.2.13/prek-installer.ps1 | iex"
```

**Linux / macOS:**

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/j178/prek/releases/download/v0.2.13/prek-installer.sh | sh
```

**或通过 uv 安装（推荐）：**

```bash
uv tool install prek
```

#### 安装/更新钩子

```bash
# 安装钩子
just hooks          # 或 uv run prek install

# 更新钩子版本
just update         # 或 uv run prek autoupdate
```

### 钩子配置详解

配置文件：`.pre-commit-config.yaml`

```yaml
default_install_hook_types: [pre-commit, commit-msg]
```

本项目安装两种类型的钩子：

- **pre-commit**: 在 `git commit` 前运行，检查代码质量
- **commit-msg**: 在提交信息写入后运行，校验提交信息格式

### 已配置的钩子清单

#### 1. builtin 内置钩子（prek 特有）


| 钩子 ID                   | 作用                 | 触发阶段   |
| ------------------------- | -------------------- | ---------- |
| `trailing-whitespace`     | 移除行尾空白字符     | pre-commit |
| `end-of-file-fixer`       | 确保文件以换行符结尾 | pre-commit |
| `check-yaml`              | 检查 YAML 文件语法   | pre-commit |
| `check-added-large-files` | 阻止提交大文件       | pre-commit |

#### 2. Ruff（`astral-sh/ruff-pre-commit@v0.14.13`）


| 钩子 ID       | 作用                 | 参数                | 触发阶段   |
| ------------- | -------------------- | ------------------- | ---------- |
| `ruff-check`  | 代码静态分析（lint） | `--fix`（自动修复） | pre-commit |
| `ruff-format` | 代码格式化           | -                   | pre-commit |

#### 3. Commitizen（`commitizen-tools/commitizen@v4.12.0`）


| 钩子 ID      | 作用                                                                                  | 触发阶段   |
| ------------ | ------------------------------------------------------------------------------------- | ---------- |
| `commitizen` | 校验提交信息是否符合[Conventional Commits](https://www.conventionalcommits.org/) 规范 | commit-msg |

### 钩子执行流程

```bash
git add <files>
       ↓
git commit -m "feat: ..."
       ↓
┌─────────────────────────────────────────────────────────┐
│                    pre-commit 阶段                       │
│  1. trailing-whitespace  → 清理行尾空白                  │
│  2. end-of-file-fixer    → 修复文件末尾换行              │
│  3. check-yaml           → 检查 YAML 语法                │
│  4. check-added-large-files → 检查大文件                 │
│  5. ruff-check --fix     → Lint 并自动修复               │
│  6. ruff-format          → 格式化代码                    │
└─────────────────────────────────────────────────────────┘
       ↓ (通过)
┌─────────────────────────────────────────────────────────┐
│                   commit-msg 阶段                       │
│  commitizen → 校验提交信息格式                          │
│  有效格式示例：                                         │
│    feat: 添加新功能                                     │
│    fix: 修复某个 bug                                    │
│    docs: 更新文档                                       │
└─────────────────────────────────────────────────────────┘
       ↓ (通过)
     提交成功
```

---

## 代码质量工具

### Ruff

[Ruff](https://github.com/astral-sh/ruff) 是一个极速的 Python linter 和 formatter，集成了多个传统工具的功能。

**配置位置**：`pyproject.toml [tool.ruff]`

#### 启用的规则集


| 规则集  | 说明                                   |
| ------- | -------------------------------------- |
| `F`     | Pyflakes 基础检查                      |
| `W`     | pycodestyle 警告                       |
| `E`     | pycodestyle 错误                       |
| `I`     | isort 导入排序                         |
| `B`     | flake8-bugbear（潜在 bug 检测）        |
| `UP`    | pyupgrade（Python 版本升级语法）       |
| `ASYNC` | flake8-async（异步代码检查）           |
| `C4`    | flake8-comprehensions（推导式优化）    |
| `T10`   | flake8-debugger（调试器检查）          |
| `T20`   | flake8-print（print 语句检查）         |
| `PYI`   | flake8-pyi（类型存根文件检查）         |
| `PT`    | flake8-pytest-style（pytest 风格检查） |
| `Q`     | flake8-quotes（引号风格检查）          |
| `TID`   | flake8-tidy-imports（导入整理）        |
| `RUF`   | Ruff 特定规则                          |

#### 忽略的规则


| 规则             | 原因                     |
| ---------------- | ------------------------ |
| `E402`           | 允许模块导入不在文件顶部 |
| `UP037`          | 允许引号类型注解         |
| `RUF001/002/003` | 允许中文等 Unicode 字符  |
| `W191`           | 允许使用制表符缩进       |
| `TID252`         | 允许相对导入             |

#### 使用方式

```bash
# 检查并自动修复 + 格式化
just lint

# 仅检查（不修复）
uv run ruff check .

# 仅格式化
uv run ruff format .
```

### BasedPyright

[BasedPyright](https://github.com/DetachHead/basedpyright) 是 Pyright 的增强分支，提供更严格的类型检查。

**配置位置**：`pyproject.toml [tool.pyright]`

```toml
[tool.pyright]
include = ["src", "tests"]
pythonVersion = "3.11"
pythonPlatform = "All"
typeCheckingMode = "standard"
```

#### 测试目录特殊配置

```toml
[[tool.pyright.executionEnvironments]]
root = "tests"
reportPrivateUsage = "none"      # 允许测试访问私有属性
reportUnknownMemberType = "none" # 允许 Mock 对象等动态类型
```

#### 使用方式

```bash
just check    # 或 uv run basedpyright
```

---

## 测试框架

### pytest 配置

**配置位置**：`pyproject.toml [tool.pytest]`

**测试依赖**（`[dependency-groups] test`）：

- `nonebug` - NoneBot 测试框架
- `pytest-asyncio` - 异步测试支持
- `pytest-cov` - 覆盖率报告
- `pytest-xdist` - 并行测试

#### pytest 选项

```toml
[tool.pytest]
addopts = [
  "--import-mode=importlib",  # 使用 importlib 导入模式
  "--strict-markers",         # 严格标记模式
  "--tb=short",               # 简短的错误回溯
  "-ra",                      # 显示所有测试结果摘要
]
pythonpath = ["src", "tests"]
asyncio_mode = "auto"         # 自动检测异步测试
```

#### 使用方式

```bash
just test     # 并行运行，生成覆盖率报告

# 或手动运行
uv run pytest                           # 运行所有测试
uv run pytest -n auto                   # 并行运行
uv run pytest --cov=src --cov-report html  # 生成 HTML 覆盖率报告
```

---

## 版本管理与变更日志

### Commitizen

[Commitizen](https://github.com/commitizen-tools/commitizen) 用于管理版本号和校验提交信息。

**配置位置**：`pyproject.toml [tool.commitizen]`

```toml
[tool.commitizen]
name = "cz_conventional_commits"   # 使用约定式提交
version = "0.1.0"                  # 当前版本
tag_format = "v$version"           # tag 格式：v0.1.0
version_files = ["pyproject.toml:^version"]  # 版本号同步到的文件
major_version_zero = true          # 允许 0.x.x 版本
```

#### 提交信息格式（Conventional Commits）

```
<type>(<scope>): <subject>

<body>

<footer>
```

**常用 type：**

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档变更
- `style`: 代码格式（不影响逻辑）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具变更

**示例：**

```bash
git commit -m "feat(auth): 添加用户登录功能"
git commit -m "fix: 修复消息发送失败的问题"
```

#### 版本升级流程

```bash
just bump     # 自动分析提交历史，升级版本号

# 或指定升级类型
uv run cz bump --increment patch   # 0.1.0 → 0.1.1
uv run cz bump --increment minor   # 0.1.0 → 0.2.0
uv run cz bump --increment major   # 0.1.0 → 1.0.0
```

`just bump` 执行以下操作：

1. 解析提交历史确定新版本号
2. 更新 `pyproject.toml` 中的版本号
3. 运行 `uv lock` 更新锁文件
4. 创建 git tag（如 `v0.2.0`）

### git-cliff

[git-cliff](https://github.com/orhun/git-cliff) 根据提交历史自动生成变更日志。

**配置位置**：`cliff.toml`

#### 提交分组规则


| 提交前缀 | 分组标题   |
| -------- | ---------- |
| `feat`   | ✨ Features |
| `fix`    | 🐛 Fixes    |
| `revert` | ◀️ Revert   |

#### 使用方式

```bash
just changelog              # 生成最新版本的变更日志
uv run git-cliff            # 生成完整变更日志
uv run git-cliff --latest   # 仅最新版本
```

---

## CI/CD 工作流

所有工作流位于 `.github/workflows/` 目录。

### 1. CI 工作流（`ci.yml`）

**触发条件**：

- push 到 `main` 分支
- PR 修改 `src/`、`tests/`、`pyproject.toml` 或 `.github/workflows/`

#### Jobs 概览


| Job              | 作用                 | Python 版本         |
| ---------------- | -------------------- | ------------------- |
| **Ruff**         | 代码检查与格式化验证 | 3.11                |
| **BasedPyright** | 静态类型检查         | 3.11                |
| **Coverage**     | 测试与覆盖率上报     | 3.11 - 3.14（矩阵） |

#### Ruff Job

```yaml
- uvx ruff check --output-format=github .   # 检查，GitHub 格式输出
- uvx ruff format --check .                 # 格式验证（不修改）
```

#### BasedPyright Job

```yaml
- uv sync                 # 安装依赖
- uvx basedpyright        # 类型检查
```

#### Coverage Job

```yaml
- uv sync
- uv run pytest --cov=src --cov-report xml --junitxml=./junit.xml -n auto
- codecov/codecov-action@v5   # 上传覆盖率（OIDC 认证）
```

### 2. Release 工作流（`release.yml`）

**触发条件**：push tag `v*`（如 `v0.2.0`）

#### 执行流程

```
推送 tag v0.2.0
       ↓
┌──────────────────────────────────────┐
│ 1. 版本校验                          │
│    比对 tag 版本与 pyproject.toml    │
│    不一致则失败退出                  │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ 2. 生成变更日志                      │
│    git-cliff --latest --strip header │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ 3. 构建与发布                        │
│    uv build → uv publish (PyPI)      │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ 4. 创建 GitHub Release               │
│    附带变更日志和构建产物            │
└──────────────────────────────────────┘
```

### 3. 初始化工作流（`rename.yml`）

**触发条件**：

- 手动触发（`workflow_dispatch`）
- push 修改 `LICENSE` 文件

**作用**：从模板创建仓库后，自动替换所有占位符：

- README.md 中的仓库名和所有者
- pyproject.toml 中的包名和链接
- 插件目录重命名（`nonebot_plugin_template` → 实际包名）
- 测试文件中的导入路径

### 4. 模板同步工作流（`template-sync.yml`）

**触发条件**：

- 定时：每周一 UTC 03:00
- 手动触发

**作用**：从上游模板仓库 `Misty02600/nonebot-plugin-template` 同步更新，以 squash 方式合并，保持历史整洁。

### 分支策略说明

如果您采用 `main` + `dev` 分支策略进行开发：

```
dev (开发分支) ──PR──▶ main (稳定分支) ──tag──▶ release (发布)
                              ▲
                              │
                    template-sync PR (模板同步)
```

- **release.yml**：仅由 tag 触发，不会修改任何分支
- **template-sync.yml**：仅向 `main` 分支创建 PR
- **dev 分支完全独立**，不受上述工作流影响，是您的开发空间

---

## 项目配置参考

### 文件结构

```
.
├── .github/
│   ├── ISSUE_TEMPLATE/     # Issue 模板
│   └── workflows/          # GitHub Actions 工作流
│       ├── ci.yml          # CI：lint, type check, test
│       ├── release.yml     # 发布到 PyPI
│       ├── rename.yml      # 模板初始化
│       └── template-sync.yml # 上游同步
├── src/
│   └── nonebot_plugin_template/  # 插件源码
├── tests/                  # 测试代码
├── .pre-commit-config.yaml # 预提交钩子配置
├── cliff.toml              # git-cliff 配置
├── justfile                # just 任务定义
└── pyproject.toml          # 项目元数据、依赖、工具配置
```

### 依赖分组

在 `pyproject.toml` 中：

```toml
[dependency-groups]
dev = [
  "basedpyright>=1.16.0",   # 类型检查
  "commitizen>=4.1.0",       # 提交规范
  "git-cliff>=2.11.0",       # 变更日志
  "prek>=0.2.0",             # 预提交钩子
  "ruff>=0.14.13,<1.0.0",    # Lint + Format
  { include-group = "test" },
]
test = [
  "nonebug>=0.4.3",          # NoneBot 测试框架
  "pytest-asyncio>=1.3.0",   # 异步测试
  "pytest-cov>=7.0.0",       # 覆盖率
  "pytest-xdist>=3.8.0",     # 并行测试
]
```

---

## 快速参考

### 日常开发命令

```bash
# 安装依赖
uv sync --all-groups

# 开发前安装钩子
just hooks

# 提交前检查
just lint && just check

# 运行测试
just test

# 准备发布
just bump                    # 自动升级版本
git push origin --tags       # 推送 tag 触发发布
```
