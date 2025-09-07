# 开发环境配置指南

本文档将指导您从零开始配置 Coze Studio 插件开发环境。

## 前置要求

### 系统要求

- **操作系统**: Linux (推荐) / macOS / Windows 10+
- **内存**: 最少 4GB RAM，推荐 8GB+
- **磁盘**: 最少 10GB 可用空间
- **网络**: 能够访问外网进行依赖下载

### 必需软件

#### 1. Go 开发环境

```bash
# Linux/macOS
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz

# 配置环境变量
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export GO111MODULE=on' >> ~/.bashrc
source ~/.bashrc

# 验证安装
go version
```

#### 2. Node.js 环境

```bash
# 使用 nvm 安装 Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# 验证安装
node -v
npm -v
```

#### 3. Docker 环境

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 验证安装
docker --version
docker-compose --version
```

#### 4. Git

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# CentOS/RHEL
sudo yum install git

# 配置 Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 项目环境搭建

### 1. 克隆项目

```bash
# 克隆主仓库
git clone https://github.com/coze-dev/coze-studio.git
cd coze-studio

# 查看项目结构
ls -la
```

### 2. 前端环境配置

```bash
# 安装 Rush.js
npm install -g @microsoft/rush

# 安装前端依赖
rush update

# 验证前端构建
cd frontend/apps/coze-studio
npm run build
```

### 3. 后端环境配置

```bash
# 进入后端目录
cd backend

# 下载 Go 依赖
go mod download
go mod verify

# 验证后端构建
go build ./...
```

### 4. 数据库环境

#### 方式一：Docker Compose（推荐）

```bash
# 复制环境变量文件
cd docker
cp .env.example .env

# 编辑环境变量（可选）
vim .env

# 启动所有中间件服务
docker compose up -d

# 检查服务状态
docker compose ps
```

服务包括：
- **MySQL 8.4.5**: 主数据库
- **Redis 8.0**: 缓存服务
- **Elasticsearch 8.18.0**: 搜索引擎
- **Milvus v2.5.10**: 向量数据库
- **MinIO**: 对象存储
- **NSQ**: 消息队列
- **etcd 3.5**: 配置中心

#### 方式二：本地安装

```bash
# MySQL
sudo apt-get install mysql-server
sudo mysql_secure_installation

# Redis
sudo apt-get install redis-server
sudo systemctl enable redis-server

# 其他服务请参考官方文档安装
```

### 5. 初始化数据库

```bash
# 同步数据库结构
make sync_db

# 初始化基础数据
make sql_init

# 验证数据库连接
make test_db
```

## 开发工具配置

### 1. IDE 配置

#### VS Code（推荐）

```bash
# 安装 VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code
```

**推荐插件**:
```json
{
  "recommendations": [
    "golang.go",
    "ms-vscode.vscode-typescript-next", 
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "42Crunch.vscode-openapi"
  ]
}
```

#### GoLand

```bash
# 下载并安装 JetBrains GoLand
wget https://download.jetbrains.com/go/goland-2023.3.tar.gz
tar -xzf goland-2023.3.tar.gz
cd GoLand-2023.3/bin
./goland.sh
```

### 2. 命令行工具

#### HTTP 客户端

```bash
# 安装 curl（通常已预装）
sudo apt-get install curl

# 安装 HTTPie
pip3 install httpie

# 安装 Postman CLI
npm install -g newman
```

#### YAML 工具

```bash
# 安装 yq
sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/local/bin/yq

# 验证安装
yq --version
```

#### JSON 工具

```bash
# 安装 jq
sudo apt-get install jq

# 验证安装
echo '{"name": "test"}' | jq .
```

## 插件开发环境

### 1. 插件目录结构

```bash
# 创建插件开发目录
mkdir -p ~/plugin-dev
cd ~/plugin-dev

# 创建标准目录结构
mkdir -p {configs,services,tests,docs}

# 目录结构
tree
```

```
plugin-dev/
├── configs/          # 插件配置文件
│   ├── openapi.yaml
│   └── plugin.yaml
├── services/         # 外部服务实现
│   └── api-server/
├── tests/           # 测试文件
│   ├── unit/
│   └── integration/
└── docs/           # 文档
    └── README.md
```

### 2. 开发辅助脚本

#### 插件验证脚本

```bash
#!/bin/bash
# validate-plugin.sh

# 验证 YAML 语法
echo "🔍 验证 YAML 配置文件..."
for file in configs/*.yaml; do
    if [ -f "$file" ]; then
        yq eval '.' "$file" > /dev/null
        if [ $? -eq 0 ]; then
            echo "✅ $file 语法正确"
        else
            echo "❌ $file 语法错误"
            exit 1
        fi
    fi
done

# 验证 OpenAPI 规范
echo "🔍 验证 OpenAPI 规范..."
if command -v swagger &> /dev/null; then
    swagger validate configs/openapi.yaml
    if [ $? -eq 0 ]; then
        echo "✅ OpenAPI 规范验证通过"
    else
        echo "❌ OpenAPI 规范验证失败"
        exit 1
    fi
fi

echo "✅ 所有验证通过！"
```

#### 测试脚本

```bash
#!/bin/bash
# test-plugin.sh

# 启动测试服务
echo "🚀 启动测试服务..."
cd services/api-server && go run main.go &
SERVER_PID=$!

# 等待服务启动
sleep 3

# 运行集成测试
echo "🧪 运行插件测试..."
cd tests/integration

# 测试基本功能
curl -X POST http://localhost:8080/api/test \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}' \
     | jq .

# 清理
kill $SERVER_PID
echo "✅ 测试完成！"
```

## 环境变量配置

### 1. 系统环境变量

```bash
# ~/.bashrc 或 ~/.zshrc
export COZE_ENV=development
export COZE_LOG_LEVEL=debug
export COZE_CONFIG_PATH=/path/to/coze-studio/backend/conf

# 数据库连接
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=coze_studio

# Redis 连接
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_PASSWORD=

# 重载环境变量
source ~/.bashrc
```

### 2. 插件开发环境变量

```bash
# .env.plugin
PLUGIN_DEV_MODE=true
PLUGIN_HOT_RELOAD=true
PLUGIN_CONFIG_PATH=./configs
PLUGIN_SERVICE_HOST=localhost
PLUGIN_SERVICE_PORT=8080

# API 密钥（测试用）
TEST_API_KEY=your_test_api_key
OAUTH_CLIENT_ID=your_client_id
OAUTH_CLIENT_SECRET=your_client_secret
```

## 开发流程工具

### 1. Makefile 配置

```makefile
# Makefile for plugin development

.PHONY: dev test build clean validate deploy

# 开发模式
dev:
	@echo "🚀 启动开发环境..."
	docker-compose up -d
	go run cmd/server/main.go

# 验证配置
validate:
	@echo "🔍 验证插件配置..."
	./scripts/validate-plugin.sh

# 测试
test:
	@echo "🧪 运行测试..."
	go test ./...
	./scripts/test-plugin.sh

# 构建
build:
	@echo "🔨 构建项目..."
	go build -o bin/server cmd/server/main.go

# 清理
clean:
	@echo "🧹 清理资源..."
	docker-compose down
	rm -rf bin/

# 部署
deploy:
	@echo "🚀 部署插件..."
	docker build -t plugin-service .
	kubectl apply -f k8s/
```

### 2. Git Hooks

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "🔍 运行预提交检查..."

# 验证 YAML 文件
make validate

# 运行测试
make test

# 代码格式化
go fmt ./...
goimports -w .

# 提交信息规范检查
# (可选) conventional commits 检查

echo "✅ 预提交检查通过！"
```

## 常用开发命令

### 项目管理

```bash
# 启动完整开发环境
make debug

# 启动中间件服务
make middleware

# 启动后端服务
make server

# 启动前端开发服务器
cd frontend/apps/coze-studio && npm run dev

# 构建前端
make fe

# 构建后端
make build_server
```

### 插件开发

```bash
# 验证插件配置
yq eval configs/plugin.yaml

# 测试 OpenAPI 规范
swagger validate configs/openapi.yaml

# 热重载插件配置
# (需要实现热重载功能)
curl -X POST http://localhost:8080/admin/reload-plugins

# 查看插件状态
curl http://localhost:8080/admin/plugins
```

### 数据库管理

```bash
# 同步数据库结构
make sync_db

# 数据库迁移
make atlas-hash

# 备份数据库
make dump_db

# 重置数据库
make reset_db
```

## 故障排查

### 常见问题

#### 1. Go 模块下载失败

```bash
# 设置 Go 代理
export GOPROXY=https://goproxy.cn,direct

# 清理模块缓存
go clean -modcache
go mod download
```

#### 2. Node.js 依赖安装失败

```bash
# 切换 npm 源
npm config set registry https://registry.npmmirror.com

# 清理缓存
npm cache clean --force
rush purge
rush update
```

#### 3. Docker 服务启动失败

```bash
# 检查端口占用
sudo netstat -tlnp | grep :3306

# 清理 Docker 资源
docker system prune -a

# 重新启动服务
docker-compose down && docker-compose up -d
```

#### 4. 数据库连接失败

```bash
# 检查 MySQL 服务状态
sudo systemctl status mysql

# 测试数据库连接
mysql -h localhost -u root -p

# 检查用户权限
SHOW GRANTS FOR 'root'@'localhost';
```

## 性能优化

### 开发环境优化

```bash
# 增加文件监听限制
echo 'fs.inotify.max_user_watches=524288' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# 优化 Go 编译缓存
export GOCACHE=$HOME/.cache/go-build
export GOTMPDIR=$HOME/.cache/go-tmp

# Node.js 内存限制调整
export NODE_OPTIONS="--max-old-space-size=4096"
```

### Docker 优化

```bash
# Docker 镜像加速器
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://mirror.baidubce.com"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 下一步

环境配置完成后，您可以：

1. 📖 阅读 [插件配置文件规范](./plugin-configuration.md)
2. 🔧 学习 [OpenAPI 规范指南](./openapi-specification.md)  
3. 🚀 开始 [部署和测试](./deployment-testing.md)

---

如遇到任何环境配置问题，请参考 [常见问题解答](./best-practices.md#常见问题) 或在社区中寻求帮助。