# ThingsBoard Gateway for RK3588 with USB Camera

本项目基于 Python 开发，旨在将 临滴LPB3588 Box打造成一个边缘智能网关，具备以下核心功能：

- 连接 USB 摄像头，采集视频图像
- 实时图像推流（MJPEG / HLS）
- 将摄像头图像在 ThingsBoard Dashboard 中展示
- 支持通过 MQTT / HTTP 与 ThingsBoard 平台通信
- 标准化代码管理与 CI/CD 流程

## 🔧 项目结构

```
thingsboard-gateway-rk3588/
├── gateway/           # 网关主逻辑
│   ├── camera/        # 摄像头处理模块
│   └── tb_client/     # ThingsBoard 通信模块
├── tb-plugins/        # 自定义插件/Widget源码
├── tb-deploy/         # ThingsBoard 部署相关（Docker）
├── scripts/           # 工具与脚本
├── docs/              # 项目文档
└── README.md
```

## 🚀 快速开始

1. **安装依赖（RK3588 网关端）**

```bash
sudo apt update
sudo apt install python3-opencv python3-pip v4l-utils ffmpeg
pip3 install paho-mqtt flask
```

2. **运行 MJPEG 摄像头采集模块**

```bash
python3 gateway/main.py
```

3. **运行 ThingsBoard（本地）**

```bash
cd tb-deploy
docker-compose up -d
```

4. **打开浏览器访问**

默认地址：[http://localhost:8080](http://localhost:8080)

默认账号：`tenant@thingsboard.org` / `tenant`

## 📦 依赖组件

- Python 3.7+
- OpenCV / FFmpeg
- Flask（用于视频推流）
- ThingsBoard CE 3.5+
- MQTT broker（可使用 ThingsBoard 内置）

## 📈 项目目标（阶段性）

- [x] 摄像头图像采集与 MJPEG 推流
- [x] ThingsBoard 仪表盘集成图像展示
- [ ] 视频流控制（开/关）
- [ ] 多摄像头管理
- [ ] 视频图像识别与边缘推理（AI 模型集成）

## 👨‍💻 开发与维护

本项目由 RK3588 爱好者主导开发，采用现代化工程管理方式：

- Git + 分支管理
- Markdown 文档规范
- CI/CD 自动构建（GitHub Actions 规划中）
- 模块化开发 + 插件化集成

---

欢迎学习、复刻、共建！Let’s make edge AI visible 🌟
