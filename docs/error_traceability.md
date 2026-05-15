# 错误追踪

## ERR-0001 Windows subprocess 找不到 npm

### 错误现象

```text
FileNotFoundError: [WinError 2] 系统找不到指定的文件。
```

### 触发命令

```powershell
python scripts\run_local.py install-frontend
```

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 原始问题 | `subprocess.run(["npm", "install"])` 在 Windows 下不一定能解析 PowerShell 命令 | [install_frontend_deps scripts/run_local.py:L70-L71](../scripts/run_local.py#L70-L71) |
| 修复位置 | 使用 `shutil.which` 解析 `npm.cmd` / `npm.exe` / `npm.ps1` | [resolve_command scripts/run_local.py:L23-L31](../scripts/run_local.py#L23-L31) |
| 调用位置 | 所有 subprocess 命令统一走解析后的可执行文件 | [run scripts/run_local.py:L34-L37](../scripts/run_local.py#L34-L37) |

### 修复方案

在 runner 中新增 `resolve_command()`，所有命令通过 `run()` 统一解析可执行文件。

### 验证命令

```powershell
python scripts\run_local.py check-env
```

## ERR-0002 npm registry 连接超时

### 错误现象

```text
http fetch GET https://registry.npmjs.org/... attempt 1 failed with ECONNRESET
```

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| npm 配置 | 切换镜像并关闭非必要网络请求 | [frontend/.npmrc:L1-L4](../frontend/.npmrc#L1-L4) |
| 静态兜底 | 无 npm 依赖前端可继续演示 | [frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218) |
| 完整栈烟测 | 验证静态前端 + 后端可运行 | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |

### 当前状态

已确认后端和静态前端完整栈可运行；Vue 前端构建受本机 npm 网络影响，后续可在网络稳定时重试。

### 验证命令

```powershell
python scripts\smoke_full_stack.py
```

## ERR-0003 Element Plus 类型声明导致 Vue 构建失败

### 错误现象

```text
Type 'GlobalComponents' does not satisfy the constraint ...
Cannot find namespace 'JSX'.
```

### 触发命令

```powershell
python scripts\run_local.py build-frontend
```

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 入口文件 | 原先全局注册了未使用的 Element Plus | [frontend/src/main.ts:L1-L9](../frontend/src/main.ts#L1-L9) |
| 构建入口 | Vue production build | [build_frontend scripts/run_local.py:L74-L75](../scripts/run_local.py#L74-L75) |

### 修复方案

移除入口文件中未使用的 Element Plus 注册和样式导入，避免 `vue-tsc` 检查 Element Plus 第三方声明文件。

### 验证命令

```powershell
python scripts\run_local.py build-frontend
```

## ERR-0004 Vue 烟测后 Vite 子进程残留

### 错误现象

```text
frontend_port_busy: true
```

### 触发命令

```powershell
python scripts\smoke_vue_full_stack.py
python scripts\run_local.py check-env
```

## ERR-0005 Git Bash 反斜杠路径被转义

### 错误现象

```text
D:\ProgramData\anaconda3\python.exe: can't open file 'C:\\Users\\hmw20\\Documents\\New project 3\\scriptsrun_local.py': [Errno 2] No such file or directory
```

### 触发命令

```bash
python scripts\run_local.py install-frontend
```

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 文档修复 | Git Bash 使用 `/` 路径 | [docs/DEPLOY.md:L19-L37](./DEPLOY.md#L19-L37) |
| 包装脚本 | Git Bash runner | [scripts/run_local.sh:L1-L5](../scripts/run_local.sh#L1-L5) |
| 包装脚本 | Git Bash Vue 烟测 | [scripts/smoke_vue_full_stack.sh:L1-L5](../scripts/smoke_vue_full_stack.sh#L1-L5) |

### 修复方案

Git Bash 中使用：

```bash
python scripts/run_local.py install-frontend
python scripts/run_local.py build-frontend
python scripts/smoke_vue_full_stack.py
```

## ERR-0006 Playwright CLI npx 下载失败

### 错误现象

```text
npm error code ECONNRESET
npm error network request to https://registry.npmmirror.com/@playwright%2fcli failed
```

### 触发命令

```bash
python scripts/playwright_smoke_vue.py
```

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| Playwright 调用 | 通过技能 wrapper 调用 Playwright CLI | [scripts/playwright_smoke_vue.py:L56-L115](../scripts/playwright_smoke_vue.py#L56-L115) |
| npm 配置 | 根目录 registry 配置 | [.npmrc:L1-L4](../.npmrc#L1-L4) |

### 当前状态

`npx` 已存在，但 registry 下载 `@playwright/cli` 失败。Vue 完整栈烟测已通过，可先作为页面级运行验证。

### 错误定位

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 修复位置 | 通过 `taskkill /T /F` 清理 Windows 进程树 | [terminate_tree scripts/smoke_vue_full_stack.py:L43-L53](../scripts/smoke_vue_full_stack.py#L43-L53) |
| 烟测入口 | `finally` 中清理前后端进程 | [main scripts/smoke_vue_full_stack.py:L56-L94](../scripts/smoke_vue_full_stack.py#L56-L94) |

### 验证命令

```powershell
python scripts\smoke_vue_full_stack.py
python scripts\run_local.py check-env
```
