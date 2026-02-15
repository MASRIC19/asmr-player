# ASMR Player

一个基于 [Flet](https://flet.dev/) 开发的跨平台 ASMR 音频播放器应用。支持浏览作品列表、搜索、以及在线音频播放。

## 功能特性

- **发现**：浏览最新、下载最多、评分最高的 ASMR 作品。
- **搜索**：支持通过关键词搜索作品。
- **播放**：内置音频播放器，支持播放/暂停、进度拖拽、后台播放（Android）。
- **跨平台**：支持 Android 和 Windows。

## 开发指南

### 环境要求

- Python 3.12+
- Git

### 本地运行 (Windows)

为了在本地 Windows 电脑上正常调试音频功能，建议使用 **Flet 0.25.2** 版本（原生支持音频组件）。

1.  **克隆仓库**
    ```bash
    git clone https://github.com/MASRIC19/asmr-player.git
    cd asmr-player
    ```

2.  **创建虚拟环境**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **安装依赖 (本地调试版)**
    *注意：本地调试建议手动安装旧版 Flet，否则可能会遇到 `Unknown control: audio` 错误。*
    ```bash
    pip install flet==0.25.2 httpx
    ```

4.  **运行应用**
    ```bash
    flet run main.py
    ```

### Android 打包

本项目配置了 GitHub Actions 自动构建 Android APK。

1.  **配置**：
    为了保证 Android 端音频组件正常工作，`requirements.txt` 中使用的是 **Flet 0.80.5** + `flet-audio`。
    *注意：这个版本组合在本地 Windows `flet run` 时可能会报错，但在 Android 构建中是正常的。*

2.  **触发构建**：
    只需将代码推送到 GitHub 的 `main` 分支：
    ```bash
    git push origin main
    ```

3.  **下载 APK**：
    构建完成后，在 GitHub 仓库的 **Actions** 页面找到对应的工作流运行记录，在底部的 **Artifacts** 区域下载 `app-release` 压缩包。

## 依赖说明

- `requirements.txt`: 默认配置为 **Android 构建环境** (Flet 0.80.5)。
- 本地开发建议临时修改为 `flet==0.25.2`。

## 许可证

MIT License
