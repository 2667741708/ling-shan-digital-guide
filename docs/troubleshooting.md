# 通用排错经验

## TRB-001 前端 npm install 超时或 ECONNRESET

### 错误现象

`npm install` 长时间无输出，日志中出现 `ECONNRESET`。

### 常见原因

本机到 npm registry 或镜像源的网络连接不稳定。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| npm 配置 | 已切换 registry 并关闭 audit/fund/progress | [frontend/.npmrc:L1-L4](../frontend/.npmrc#L1-L4) |
| 前端安装入口 | Python subprocess 调用 npm | [install_frontend_deps scripts/run_local.py:L70-L71](../scripts/run_local.py#L70-L71) |
| 静态兜底 | 无 npm 依赖演示前端 | [frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218) |

### 修复方式

优先重试：

```powershell
python scripts\run_local.py install-frontend
```

当前网络恢复后已验证 `npm install` 成功，安装入口仍为 [install_frontend_deps scripts/run_local.py:L70-L71](../scripts/run_local.py#L70-L71)。

如果持续失败，使用静态前端兜底：

```powershell
python scripts\smoke_full_stack.py
```

## TRB-002 端口占用

### 错误现象

后端或前端启动失败，提示端口已被占用。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 端口检查 | 检查 8000/5173 是否忙 | [port_is_busy scripts/run_local.py:L45-L48](../scripts/run_local.py#L45-L48) |
| 环境检查 | 输出端口占用状态 | [check_env scripts/run_local.py:L51-L63](../scripts/run_local.py#L51-L63) |
| Vue 烟测复用 | 如果 8000/5173 已有健康服务则复用，否则再启动 | [is_url_ready scripts/smoke_vue_full_stack.py:L43-L50](../scripts/smoke_vue_full_stack.py#L43-L50), [main scripts/smoke_vue_full_stack.py:L67-L122](../scripts/smoke_vue_full_stack.py#L67-L122) |

### 验证命令

```powershell
python scripts\run_local.py check-env
python scripts\smoke_vue_full_stack.py
```

## TRB-003 DeepSeek API Key 缺失或调用失败

### 错误现象

游客问答返回 `model_used = mock-fallback`。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 配置 | DeepSeek Key、模型和超时配置 | [.env.example:L25-L28](../.env.example#L25-L28) |
| 客户端 | 判断 Key 是否存在、设置超时并调用 API | [DeepSeekClient backend/app/services/deepseek_service.py:L9-L50](../backend/app/services/deepseek_service.py#L9-L50) |
| 降级逻辑 | API 异常时回退到本地回答 | [chat_with_text backend/app/services/chat_service.py:L53-L69](../backend/app/services/chat_service.py#L53-L69) |

### 验证命令

```powershell
python scripts\run_local.py smoke-backend
```

## TRB-004 知识库检索不到内容

### 常见原因

知识库文件未生成、资料文件缺失或查询词与资料差距过大。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 构建入口 | 生成 JSON 向量库 | [build_knowledge_base backend/app/services/vector_store.py:L223-L243](../backend/app/services/vector_store.py#L223-L243) |
| 检索入口 | 计算查询向量并排序 | [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) |
| 数据源 | 示范景区导览资料 | [data/raw_documents/demo_scenic_guide.md:L1-L25](../data/raw_documents/demo_scenic_guide.md#L1-L25) |

### 验证命令

```powershell
python scripts\run_local.py build-kb
python scripts\run_local.py test-backend
```

## TRB-005 真实 xlsx 资料过大导致知识库构建超时

### 错误现象

构建真实资料包时长时间无输出，进程卡在 xlsx 解析或向量化阶段。

### 原因分析

真实资料包中的行为分析表工作表 XML 体积较大，全量解析会生成大量低价值数字行为数据。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| xlsx 抽取 | 仅抽取文本/含中文内容并限制单元格数量 | [extract_xlsx_text backend/app/services/vector_store.py:L151-L188](../backend/app/services/vector_store.py#L151-L188) |
| 资料包读取 | xlsx 标记为 `behavior_data`，路线问答默认排除 | [load_scenic_pack_entries backend/app/services/vector_store.py:L191-L216](../backend/app/services/vector_store.py#L191-L216) |
| 路线上下文过滤 | 路线问题排除 xlsx 行为数据，避免回答其他景区 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |

### 验证命令

```powershell
python scripts\run_local.py build-kb
python scripts\run_local.py smoke-backend
```

## TRB-006 Element Plus 类型声明导致 Vue 构建失败

### 错误现象

```text
node_modules/element-plus/... Type 'GlobalComponents' does not satisfy the constraint ...
```

### 原因分析

当前页面没有使用 Element Plus 组件，但入口文件全局注册了 Element Plus，`vue-tsc` 会检查其声明文件并触发第三方类型兼容问题。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 修复位置 | 移除未使用的 Element Plus 全局注册和样式导入 | [frontend/src/main.ts:L1-L9](../frontend/src/main.ts#L1-L9) |
| 构建入口 | Vue production build | [build_frontend scripts/run_local.py:L74-L75](../scripts/run_local.py#L74-L75) |

### 验证命令

```powershell
python scripts\run_local.py build-frontend
```

## TRB-007 Vue 烟测后 Vite 子进程残留

### 错误现象

Vue 完整栈烟测结束后，`5173` 端口仍被 Vite 子进程占用。

### 原因分析

Windows 下 `npm run dev` 会启动子进程，直接 `terminate()` 父进程不一定清理完整进程树。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 修复位置 | Windows 下使用 `taskkill /T /F` 清理进程树 | [terminate_tree scripts/smoke_vue_full_stack.py:L52-L62](../scripts/smoke_vue_full_stack.py#L52-L62) |
| 烟测入口 | 复用健康服务或启动 FastAPI 与 Vite 并最终清理 | [main scripts/smoke_vue_full_stack.py:L67-L122](../scripts/smoke_vue_full_stack.py#L67-L122) |

### 验证命令

```powershell
python scripts\smoke_vue_full_stack.py
python scripts\run_local.py check-env
```

## TRB-008 Git Bash 中使用反斜杠导致 Python 找不到脚本

### 错误现象

```text
python.exe: can't open file '...\\scriptsrun_local.py': [Errno 2] No such file or directory
```

### 原因分析

Git Bash / MINGW64 中反斜杠 `\` 是转义字符，不是可靠的路径分隔符。`scripts\run_local.py` 会被解析成 `scriptsrun_local.py`。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| Git Bash 命令说明 | 使用 `/` 路径或 `.sh` 包装脚本 | [docs/DEPLOY.md:L19-L37](./DEPLOY.md#L19-L37) |
| Git Bash runner | 转到项目根目录并调用 Python runner | [scripts/run_local.sh:L1-L5](../scripts/run_local.sh#L1-L5) |
| Git Bash Vue 烟测 | 转到项目根目录并调用 Vue 烟测 | [scripts/smoke_vue_full_stack.sh:L1-L5](../scripts/smoke_vue_full_stack.sh#L1-L5) |

### 修复方式

在 Git Bash 中使用：

```bash
python scripts/run_local.py install-frontend
python scripts/run_local.py build-frontend
python scripts/smoke_vue_full_stack.py
```

或：

```bash
bash scripts/run_local.sh install-frontend
bash scripts/run_local.sh build-frontend
bash scripts/smoke_vue_full_stack.sh
```

## TRB-009 Playwright CLI 包下载失败

### 错误现象

```text
npm error network request to https://registry.npmmirror.com/@playwright%2fcli failed, reason: read ECONNRESET
```

### 原因分析

Playwright skill 的 wrapper 依赖 `npx --package @playwright/cli`。当前 `npx` 存在，但下载 `@playwright/cli` / `playwright` 包时 registry 连接重置。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| Playwright 脚本 | 启动后端/Vite 后调用 Playwright wrapper | [scripts/playwright_smoke_vue.py:L56-L115](../scripts/playwright_smoke_vue.py#L56-L115) |
| 根 npm 配置 | Playwright wrapper 在仓库根目录读取此配置 | [.npmrc:L1-L4](../.npmrc#L1-L4) |

### 验证命令

```bash
command -v npx
python scripts/playwright_smoke_vue.py
```

如果 registry 仍然 `ECONNRESET`，先使用已通过的 Vue 完整栈烟测：

```bash
python scripts/smoke_vue_full_stack.py
```

## TRB-010 GitHub push 连接中断

### 错误现象

```text
fatal: unable to access 'https://github.com/2667741708/ling-shan-digital-guide.git/': Recv failure: Connection was aborted
```

SSH 检查也可能出现：

```text
kex_exchange_identification: read: Connection aborted
banner exchange: Connection to 198.18.0.25 port 22: Connection aborted
```

### 常见原因

1. 当前网络或代理阻断 GitHub HTTPS/SSH。
2. GitHub 域名被解析到代理虚拟网段，连接在认证前被中断。
3. 本机 Git 凭据并未进入认证流程，因此不是代码或仓库内容问题。

### 定位位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 发布脚本 | 推送当前分支和 tag 到 GitHub | [publish_github main scripts/publish_github.py:L56-L84](../scripts/publish_github.py#L56-L84) |
| 远程配置 | 新增或更新 `origin` | [configure_remote scripts/publish_github.py:L47-L53](../scripts/publish_github.py#L47-L53) |
| 发布文档 | 可复现发布命令 | [docs/DEPLOY.md:L110-L128](./DEPLOY.md#L110-L128) |
| 错误记录 | 本次连接中断记录 | [ERR-0009 docs/error_traceability.md:L228-L268](./error_traceability.md#L228-L268) |

### 排查命令

```powershell
git remote -v
git status --short --branch
ssh -T git@github.com
python scripts\publish_github.py --help
```

### 修复方式

先恢复可访问 GitHub 的网络或代理，再执行：

```powershell
python scripts\publish_github.py --remote-url https://github.com/2667741708/ling-shan-digital-guide.git --branch main --push-tags
```

如果 HTTPS 仍失败，可以先确认 SSH 可用，再切换 remote：

```powershell
git remote set-url origin git@github.com:2667741708/ling-shan-digital-guide.git
git push -u origin codex/optimize-map-avatar-v0.1:main
git push origin --tags
```
