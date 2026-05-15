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
