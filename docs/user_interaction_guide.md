# 项目交互与运行指南

## 1. 推荐启动方式

### 方式 A：Git Bash 手动体验，推荐

```bash
bash scripts/dev_vue_full_stack.sh
```

启动后打开：

| 页面 | 地址 | 用途 |
|---|---|---|
| 数字人导游 | http://127.0.0.1:5173/guide | 测试游客问答、数字人状态、DeepSeek RAG |
| 景区地图 | http://127.0.0.1:5173/map | 查看景点点位 |
| 管理大屏 | http://127.0.0.1:5173/admin | 查看运营指标 |
| 知识库管理 | http://127.0.0.1:5173/admin/knowledge | 查看知识文档 |
| 数字人配置 | http://127.0.0.1:5173/admin/avatar | 查看数字人配置 |

对应实现：

- [Git Bash 启动脚本 scripts/dev_vue_full_stack.sh:L1-L5](../scripts/dev_vue_full_stack.sh#L1-L5)
- [持续运行入口 scripts/dev_vue_full_stack.py:L56-L100](../scripts/dev_vue_full_stack.py#L56-L100)
- [前端路由 frontend/src/router/index.ts:L10-L20](../frontend/src/router/index.ts#L10-L20)

停止方式：在终端按 `Ctrl+C`。

### 方式 B：Git Bash 自动烟测

```bash
bash scripts/smoke_vue_full_stack.sh
```

用途：自动启动后端和 Vue，检查页面和 API 后自动退出。

- [Git Bash 烟测脚本 scripts/smoke_vue_full_stack.sh:L1-L5](../scripts/smoke_vue_full_stack.sh#L1-L5)
- [Vue 完整栈烟测 scripts/smoke_vue_full_stack.py:L56-L94](../scripts/smoke_vue_full_stack.py#L56-L94)

### 方式 C：PowerShell / CMD 手动体验

```powershell
python scripts\dev_vue_full_stack.py
```

### 方式 D：PowerShell / CMD 自动烟测

```powershell
python scripts\smoke_vue_full_stack.py
```

### 方式 E：只跑后端

```powershell
python scripts\run_local.py serve-backend
```

后端健康检查：

```text
http://127.0.0.1:8000/api/health
```

实现位置：

- [后端启动 scripts/run_local.py:L89-L105](../scripts/run_local.py#L89-L105)
- [后端健康检查 backend/app/main.py:L21-L23](../backend/app/main.py#L21-L23)

### 方式 F：Vue 前端单独运行

需要后端已运行。

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

### 方式 G：静态兜底演示

如果 npm/Vue 临时不可用：

```powershell
python scripts\smoke_full_stack.py
```

该方式启动后端和无依赖静态演示端，适合演示兜底。

- [静态演示端 frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218)
- [静态完整栈烟测 scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61)

### 方式 H：Docker Compose

```powershell
Copy-Item .env.example .env
docker compose -f deploy/docker-compose.yml up --build
```

注意：当前主要验证路径是 Python runner。Docker Compose 适合后续统一部署复现。

## 2. 数字人导游测试流程

1. 启动：

   ```bash
   bash scripts/dev_vue_full_stack.sh
   ```

2. 打开：

   ```text
   http://127.0.0.1:5173/guide
   ```

3. 输入测试问题：

   ```text
   我只有两个小时，喜欢历史和拍照，怎么逛？
   古建筑群有什么特色？
   附近哪里有洗手间？
   下雨天怎么玩？
   ```

4. 预期表现：

   - 左侧显示数字人形象。
   - 提交问题后，数字人状态先显示“思考中”，回答后进入“讲解中”。
   - 回答由后端 [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) 生成。
   - 有 DeepSeek Key 时，响应中 `model_used` 应为 `deepseek-v4-flash`。
   - 回答应引用本地知识库片段。

## 3. 后端 API 直接测试

### 文本问答

```bash
python scripts/smoke_vue_full_stack.py
```

或者只测后端：

```bash
python scripts/run_local.py smoke-backend
```

对应 API：

- [游客文本问答 API docs/api_reference.md](./api_reference.md#api-002-游客文本问答)
- [text_chat backend/app/api/visitor.py:L20-L21](../backend/app/api/visitor.py#L20-L21)

### 知识库检索测试

后台接口：

```text
POST /api/admin/knowledge/search-test
```

实现位置：

- [knowledge_search_test backend/app/api/admin.py:L27-L28](../backend/app/api/admin.py#L27-L28)
- [search_test backend/app/services/knowledge_service.py:L38-L39](../backend/app/services/knowledge_service.py#L38-L39)

## 4. Git Bash 路径规则

Git Bash / MINGW64 中必须使用 `/`：

```bash
python scripts/run_local.py check-env
```

不要使用 `\`：

```bash
python scripts\run_local.py check-env
```

原因和修复记录见 [TRB-008 Git Bash 中使用反斜杠导致 Python 找不到脚本](./troubleshooting.md#trb-008-git-bash-中使用反斜杠导致-python-找不到脚本)。

