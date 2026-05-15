# 配置字段说明

| 字段 | 类型 | 默认值 | 是否必填 | 业务含义 | 使用位置 | 修改风险 |
|---|---|---|---|---|---|---|
| `BACKEND_PORT` | int | `8000` | 否 | 后端本地监听端口 | [run_local.py:L19-L20](../scripts/run_local.py#L19-L20), [smoke_vue_full_stack.py:L15-L16](../scripts/smoke_vue_full_stack.py#L15-L16) | 改动后需同步前端 API 地址和烟测脚本 |
| `FRONTEND_PORT` | int | `5173` | 否 | 前端本地监听端口 | [run_local.py:L19-L20](../scripts/run_local.py#L19-L20), [smoke_vue_full_stack.py:L15-L16](../scripts/smoke_vue_full_stack.py#L15-L16) | 改动后需同步访问地址 |
| `VECTOR_DB_TYPE` | string | `local_json` | 否 | 当前向量库实现类型 | [.env.example:L14-L15](../.env.example#L14-L15) | P1 切 Chroma 时需要同步依赖与构建脚本 |
| `VECTOR_DB_PATH` | string | `data/vector_db/scenic_vector_store.json` | 否 | 本地 JSON 向量库文件位置 | [.env.example:L14-L15](../.env.example#L14-L15), [VECTOR_STORE_PATH backend/app/services/vector_store.py:L13-L16](../backend/app/services/vector_store.py#L13-L16) | 文件缺失时会懒构建，路径错误会导致检索失败 |
| `ADMIN_KNOWLEDGE_DIR` | path | `data/admin_knowledge` | 否 | 后台上传知识文档保存目录，构建向量库时会读取该目录中的 `.md/.txt/.csv/.json/.docx/.xlsx` | [ADMIN_KNOWLEDGE_DIR backend/app/services/vector_store.py:L15-L19](../backend/app/services/vector_store.py#L15-L19), [load_admin_document_entries backend/app/services/vector_store.py:L150-L170](../backend/app/services/vector_store.py#L150-L170) | 删除该目录会移除后台上传资料；修改后需同步知识库管理服务和文档 |
| `DEEPSEEK_BASE_URL` | string | `https://api.deepseek.com` | 否 | DeepSeek OpenAI 兼容 API 地址 | [.env.example:L25-L28](../.env.example#L25-L28), [DeepSeekClient backend/app/services/deepseek_service.py:L11-L14](../backend/app/services/deepseek_service.py#L11-L14) | 错误会触发降级 mock |
| `DEEPSEEK_MODEL` | string | `deepseek-v4-flash` | 否 | DeepSeek 文本模型 | [.env.example:L25-L28](../.env.example#L25-L28), [DeepSeekClient backend/app/services/deepseek_service.py:L11-L14](../backend/app/services/deepseek_service.py#L11-L14) | 模型不可用会触发降级 mock |
| `DEEPSEEK_API_KEY` | string | `replace_me` | 本地必填 | 真实 DeepSeek 调用凭据 | [.env.example:L25-L28](../.env.example#L25-L28), [DeepSeekClient backend/app/services/deepseek_service.py:L11-L14](../backend/app/services/deepseek_service.py#L11-L14) | 不应提交真实 Key；缺失时只走 mock |
| `DEEPSEEK_TIMEOUT_SECONDS` | float | `4.5` | 否 | DeepSeek 请求最大等待时间，超时后使用 RAG 降级回答，控制演示响应时延 | [.env.example:L25-L28](../.env.example#L25-L28), [DeepSeekClient backend/app/services/deepseek_service.py:L11-L14](../backend/app/services/deepseek_service.py#L11-L14) | 过低会更频繁降级，过高可能超过 5 秒演示目标 |
| `frontend/.npmrc registry` | string | `https://registry.npmmirror.com` | 否 | 前端依赖安装镜像 | [frontend/.npmrc:L1-L4](../frontend/.npmrc#L1-L4) | 本机网络仍可能 ECONNRESET，可用静态前端兜底 |

## 验证命令

```powershell
python scripts\run_local.py check-env
```
