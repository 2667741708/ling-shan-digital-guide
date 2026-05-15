# 测试方式和验证命令

## TEST-001 健康检查

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-003 |
| 测试函数 | [test_health backend/tests/test_health.py:L6-L10](../backend/tests/test_health.py#L6-L10) |
| 被测接口 | [health backend/app/main.py:L21-L23](../backend/app/main.py#L21-L23) |
| 运行命令 | `python scripts\run_local.py test-backend` |

## TEST-002 知识库构建

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-002 |
| 测试函数 | [test_build_knowledge_base_creates_entries backend/tests/test_vector_store.py:L4-L6](../backend/tests/test_vector_store.py#L4-L6) |
| 被测函数 | [build_knowledge_base backend/app/services/vector_store.py:L223-L243](../backend/app/services/vector_store.py#L223-L243) |
| 运行命令 | `python scripts\run_local.py build-kb` |

## TEST-003 知识库检索命中

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-002 |
| 测试函数 | [test_retrieve_context_finds_facility_answer backend/tests/test_vector_store.py:L9-L12](../backend/tests/test_vector_store.py#L9-L12) |
| 被测函数 | [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) |
| 预期结果 | 查询“附近哪里有洗手间”可命中包含“洗手间”的知识片段 |

## TEST-004 问答服务单元测试

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-001 |
| 测试函数 | [test_chat_with_text_uses_references_and_latency backend/tests/test_chat_service.py:L5-L12](../backend/tests/test_chat_service.py#L5-L12) |
| 被测函数 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 预期结果 | 返回答案、引用来源、模型标记和真实延迟 |

## TEST-005 后端烟测

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-001、REQ-002、REQ-003 |
| 烟测脚本 | [smoke_test scripts/smoke_test.py:L41-L57](../scripts/smoke_test.py#L41-L57) |
| 启动脚本 | [smoke_backend scripts/run_local.py:L136-L146](../scripts/run_local.py#L136-L146) |
| 运行命令 | `python scripts\run_local.py smoke-backend` |

## TEST-006 完整栈烟测

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-003 |
| 烟测脚本 | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |
| 静态前端 | [frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218) |
| 运行命令 | `python scripts\smoke_full_stack.py` |

## TEST-007 Vue 前端安装与构建

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-003 |
| 安装入口 | [install_frontend_deps scripts/run_local.py:L70-L71](../scripts/run_local.py#L70-L71) |
| 构建入口 | [build_frontend scripts/run_local.py:L74-L75](../scripts/run_local.py#L74-L75) |
| Vue 入口 | [frontend/src/main.ts:L1-L9](../frontend/src/main.ts#L1-L9) |
| 运行命令 | `python scripts\run_local.py install-frontend` 和 `python scripts\run_local.py build-frontend` |
| 预期结果 | `npm install` 成功，`vite build` 输出 `dist/` |

## TEST-008 Vue 完整栈烟测

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-003 |
| 烟测脚本 | [main scripts/smoke_vue_full_stack.py:L67-L122](../scripts/smoke_vue_full_stack.py#L67-L122) |
| 进程清理 | [terminate_tree scripts/smoke_vue_full_stack.py:L52-L62](../scripts/smoke_vue_full_stack.py#L52-L62) |
| 运行命令 | `python scripts\smoke_vue_full_stack.py` |
| 预期结果 | 输出 `vue full stack ok: http://127.0.0.1:5173` |

## TEST-009 Git Bash 命令兼容性

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-003 |
| Git Bash runner | [scripts/run_local.sh:L1-L5](../scripts/run_local.sh#L1-L5) |
| Git Bash Vue 烟测 | [scripts/smoke_vue_full_stack.sh:L1-L5](../scripts/smoke_vue_full_stack.sh#L1-L5) |
| Git Bash 手动体验 | [scripts/dev_vue_full_stack.sh:L1-L5](../scripts/dev_vue_full_stack.sh#L1-L5) |
| 运行命令 | `python scripts/smoke_vue_full_stack.py` |
| 预期结果 | 在 Git Bash 中使用 `/` 路径可运行，不能使用 `\` |

## TEST-010 Playwright CLI 页面验证

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-003 |
| Playwright 脚本 | [scripts/playwright_smoke_vue.py:L56-L115](../scripts/playwright_smoke_vue.py#L56-L115) |
| 运行命令 | `python scripts/playwright_smoke_vue.py` |
| 当前状态 | `npx` 存在，但 `@playwright/cli` 下载出现 registry `ECONNRESET` |

## TEST-011 手动测试数字人导游

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-001、REQ-003、REQ-006 |
| 启动脚本 | [dev_vue_full_stack main scripts/dev_vue_full_stack.py:L52-L95](../scripts/dev_vue_full_stack.py#L52-L95) |
| 前端路由 | [frontend/src/router/index.ts:L10-L20](../frontend/src/router/index.ts#L10-L20) |
| 问答页面 | [ChatGuide frontend/src/pages/visitor/ChatGuide.vue:L1-L147](../frontend/src/pages/visitor/ChatGuide.vue#L1-L147) |
| 数字人组件 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L64](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L64) |
| 后端问答 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 运行命令 | `python scripts/dev_vue_full_stack.py` |
| 测试页面 | `http://127.0.0.1:5173/guide` |

## TEST-012 灵山地图和路线推荐

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-005 |
| 测试函数 | [test_route_service backend/tests/test_route_service.py:L6-L26](../backend/tests/test_route_service.py#L6-L26) |
| 景点数据 | [SCENIC_SPOTS backend/app/services/scenic_service.py:L14-L225](../backend/app/services/scenic_service.py#L14-L225) |
| 路线算法 | [recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116) |
| 地图组件 | [ScenicMapView frontend/src/components/ScenicMapView.vue:L1-L101](../frontend/src/components/ScenicMapView.vue#L1-L101) |
| 运行命令 | `python scripts\run_local.py test-backend` 和 `python scripts\run_local.py build-frontend` |
| 预期结果 | 后端返回真实灵山点位，2 小时历史拍照路线包含灵山核心景点，前端构建通过 |

## 本次验证记录

```text
python scripts\run_local.py build-kb
结果：entry_count = 3377

python scripts\run_local.py test-backend
结果：6 passed

python scripts\run_local.py smoke-backend
结果：DeepSeek 模型 deepseek-v4-flash 返回问答，知识库命中 faq_3

python scripts\smoke_full_stack.py
结果：后端和静态前端均可访问，完整栈烟测通过

python scripts\run_local.py install-frontend
结果：added 105 packages

python scripts\run_local.py build-frontend
结果：Vue/Vite production build 通过

python scripts\smoke_vue_full_stack.py
结果：Vue dev server + FastAPI + DeepSeek 问答完整栈通过
```

## TEST-013 GitHub 发布脚本帮助命令

| 项目 | 内容 |
|---|---|
| 对应需求 | REQ-009 |
| 测试命令 | `python scripts\publish_github.py --help` |
| 被测入口 | [main scripts/publish_github.py:L56-L84](../scripts/publish_github.py#L56-L84) |
| 远程配置逻辑 | [configure_remote scripts/publish_github.py:L47-L53](../scripts/publish_github.py#L47-L53) |
| 工作区保护 | [ensure_clean_worktree scripts/publish_github.py:L38-L44](../scripts/publish_github.py#L38-L44) |
| 预期结果 | 输出 `--remote-url`、`--branch`、`--push-tags` 等参数说明，不修改远程仓库 |
