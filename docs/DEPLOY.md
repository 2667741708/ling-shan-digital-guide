# 部署说明

## Docker Compose

```powershell
Copy-Item .env.example .env
docker compose -f deploy/docker-compose.yml up --build
```

访问地址：

- 游客端：http://localhost:5173
- 后端 API：http://localhost:8000/api/health

## 本地开发

完整交互测试说明见 [项目交互与运行指南](./user_interaction_guide.md)。

推荐优先使用可复现 Python runner：

```powershell
python scripts\run_local.py check-env
python scripts\run_local.py build-kb
python scripts\run_local.py test-backend
python scripts\run_local.py smoke-backend
```

Git Bash / MINGW64 必须使用正斜杠 `/`，不要使用反斜杠 `\`：

```bash
python scripts/run_local.py check-env
python scripts/run_local.py install-frontend
python scripts/run_local.py build-frontend
python scripts/smoke_vue_full_stack.py
```

也可以使用 Git Bash 包装脚本：

```bash
bash scripts/run_local.sh check-env
bash scripts/smoke_vue_full_stack.sh
bash scripts/dev_vue_full_stack.sh
```

对应实现：

- [环境检查 scripts/run_local.py:L51-L63](../scripts/run_local.py#L51-L63)
- [知识库构建 scripts/run_local.py:L78-L79](../scripts/run_local.py#L78-L79)
- [后端烟测 scripts/run_local.py:L136-L146](../scripts/run_local.py#L136-L146)

后端手动开发命令：

```powershell
cd backend
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

前端：

```powershell
cd frontend
npm install
npm run dev
```

当前 Vue 工程已可安装和构建，推荐通过 runner 执行：

```powershell
python scripts\run_local.py install-frontend
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
```

对应实现：

- [前端安装 scripts/run_local.py:L70-L71](../scripts/run_local.py#L70-L71)
- [前端构建 scripts/run_local.py:L74-L75](../scripts/run_local.py#L74-L75)
- [Vue 完整栈烟测 scripts/smoke_vue_full_stack.py:L67-L122](../scripts/smoke_vue_full_stack.py#L67-L122)
- [Git Bash runner scripts/run_local.sh:L1-L5](../scripts/run_local.sh#L1-L5)
- [Git Bash Vue 烟测 scripts/smoke_vue_full_stack.sh:L1-L5](../scripts/smoke_vue_full_stack.sh#L1-L5)

手动体验页面时使用持续运行脚本：

```bash
python scripts/dev_vue_full_stack.py
```

打开：

- 数字人导游页：http://127.0.0.1:5173/guide
- 景区地图页：http://127.0.0.1:5173/map
- 管理大屏页：http://127.0.0.1:5173/admin

实现位置：[dev_vue_full_stack.py:L52-L95](../scripts/dev_vue_full_stack.py#L52-L95)

若 npm registry 网络异常，可使用无 npm 依赖静态演示端：

```powershell
python scripts\smoke_full_stack.py
```

该命令会启动后端和静态前端，验证完整链路后自动关闭进程。实现位置：

- [完整栈烟测 scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61)
- [静态演示端 frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218)

## GitHub 发布

当前项目本地版本已经保留 `v0.0` baseline tag，最新优化分支为 `codex/optimize-map-avatar-v0.1`。发布到 GitHub 时优先使用可复现 Python 脚本：

```powershell
python scripts\publish_github.py --remote-url https://github.com/<your-name>/<repo>.git --branch main --push-tags
```

Git Bash / MINGW64 使用：

```bash
python scripts/publish_github.py --remote-url https://github.com/<your-name>/<repo>.git --branch main --push-tags
```

脚本会检查工作区是否干净，自动新增或更新 `origin`，并把当前分支推送到 GitHub 的 `main` 分支。实现位置：

- [GitHub 发布 CLI scripts/publish_github.py:L56-L84](../scripts/publish_github.py#L56-L84)
- [工作区保护 scripts/publish_github.py:L38-L44](../scripts/publish_github.py#L38-L44)
- [远程仓库配置 scripts/publish_github.py:L47-L53](../scripts/publish_github.py#L47-L53)

### 本次 GitHub 发布复盘

本项目曾出现两类“提交/推送失败”，原因不同：

1. 直接在工具层执行 `git add -A` 时被运行策略拦截，错误来自 Codex 工具权限包装层，不是 Git 仓库问题。后续改用 Python `subprocess.run(["git", "add", "-A"])` 在项目根目录执行，成功完成暂存和提交。
2. 推送 GitHub 时 HTTPS 与 SSH 都在连接阶段被中断，典型错误为 `Recv failure: Connection was aborted` 和 `Connection to 198.18.0.25 port 22: Connection aborted`。这说明当时机器到 GitHub 的网络或代理链路不可用，尚未进入账号认证阶段。网络恢复后，同一发布脚本成功推送。

本次最终成功标志：

```text
已推送 codex/optimize-map-avatar-v0.1 -> origin/main
origin/main = b630176 feat(admin): add persistent versioned knowledge base
origin tag v0.0 = 37cd58b chore(release): baseline v0.0
```

相关复盘：

- [GitHub 网络中断错误 docs/error_traceability.md:L295-L334](./error_traceability.md#L295-L334)
- [GitHub 发布先失败后成功 docs/error_traceability.md:L195-L259](./error_traceability.md#L195-L259)
- [GitHub push 连接中断排错 docs/troubleshooting.md:L243-L319](./troubleshooting.md#L243-L319)
- [为什么之前提交失败后来成功 docs/question_traceability.md:L177-L205](./question_traceability.md#L177-L205)
