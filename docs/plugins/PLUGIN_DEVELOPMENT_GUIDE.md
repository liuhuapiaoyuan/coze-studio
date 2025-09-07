# Coze Studio 插件开发指南

本指南将详细介绍如何为 Coze Studio 开发插件，包括环境准备、架构设计、配置文件编写、测试调试和部署发布等各个环节。

## 目录

1. [开发环境准备](#开发环境准备)
2. [插件架构设计](#插件架构设计)
3. [OpenAPI 规范编写](#openapi-规范编写)
4. [插件配置文件编写](#插件配置文件编写)
5. [插件测试和调试](#插件测试和调试)
6. [插件部署和发布](#插件部署和发布)
7. [最佳实践和常见问题](#最佳实践和常见问题)

---

## 开发环境准备

### 1. 系统要求

- **操作系统**: Linux/macOS/Windows
- **Node.js**: >= 18.0.0
- **Go**: >= 1.21.0
- **Docker**: >= 20.10.0 (可选)
- **Git**: 用于版本控制

### 2. 克隆项目仓库

```bash
git clone https://github.com/coze-dev/coze-studio.git
cd coze-studio
```

### 3. 安装依赖

#### 前端依赖安装
```bash
# 使用 Rush.js 管理前端依赖
rush update
```

#### 后端依赖安装
```bash
cd backend
go mod tidy
```

### 4. 启动开发环境

#### 启动中间件服务
```bash
make middleware
```

#### 启动后端服务
```bash
make server
```

#### 启动前端开发服务器
```bash
cd frontend/apps/coze-studio
npm run dev
```

### 5. 开发工具推荐

- **代码编辑器**: VS Code, GoLand, WebStorm
- **API 测试工具**: Postman, Insomnia, curl
- **YAML 编辑器**: YAML Language Server 插件
- **OpenAPI 工具**: Swagger Editor, OpenAPI Generator

---

## 插件架构设计

### 1. 插件系统概述

Coze Studio 的插件系统基于以下核心概念：

- **外部服务调用**: 插件通过 HTTP API 调用外部服务
- **OpenAPI 规范**: 使用 OpenAPI 3.0.1 定义接口规范
- **配置驱动**: 通过 YAML 配置文件定义插件行为
- **无状态设计**: 插件调用是无状态的，支持高并发

### 2. 插件架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Coze Studio   │────│   Plugin API    │────│  External API   │
│    Frontend     │    │    Gateway      │    │    Service      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   Bot/Workflow  │    │  Plugin Config  │    │  Business Logic │
    │   Integration   │    │   Management    │    │  Implementation │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 3. 插件类型

#### A. 云端插件 (Cloud Plugin)
- 调用外部 HTTP API 服务
- 适用于大多数业务场景
- 无需在 Coze Studio 部署额外代码

#### B. 本地插件 (Local Plugin)
- 在 Coze Studio 内部执行逻辑
- 适用于数据处理、格式转换等场景
- 需要实现对应的 Go 处理逻辑

### 4. 数据流设计

```
用户请求 → Coze Studio → 插件网关 → 外部 API → 响应处理 → 返回结果
    ↓            ↓            ↓           ↓           ↓         ↓
  参数验证    权限检查    请求转换    业务处理    数据清洗    格式化输出
```

---

## OpenAPI 规范编写

### 1. 基本结构

每个插件都需要一个 OpenAPI 3.0.1 规范文件，位于 `backend/conf/plugin/pluginproduct/` 目录下。

#### 基本模板

```yaml
info:
  description: 插件功能描述
  title: 插件名称
  version: v1
openapi: 3.0.1
paths:
  /api/endpoint:
    post:
      operationId: unique_operation_id
      # 接口定义...
servers:
  - url: https://your-api-server.com
    description: API 服务器描述
```

### 2. 请求参数定义

#### 查询参数 (Query Parameters)
```yaml
parameters:
  - description: 参数描述
    in: query
    name: param_name
    required: true
    schema:
      type: string
      example: "示例值"
```

#### 请求体 (Request Body)
```yaml
requestBody:
  content:
    application/json:
      schema:
        properties:
          param1:
            description: 参数1描述
            type: string
            format: uri  # 特定格式
            example: "https://example.com/file.pdf"
          param2:
            description: 参数2描述
            type: boolean
            default: true
          param3:
            description: 参数3描述
            type: integer
            minimum: 1
            maximum: 100
        required:
          - param1
        type: object
  description: 请求体描述
  required: true
```

### 3. 响应定义

#### 成功响应
```yaml
responses:
  "200":
    content:
      application/json:
        schema:
          properties:
            success:
              description: 操作是否成功
              type: boolean
            data:
              description: 返回的数据
              type: object
              properties:
                result:
                  description: 处理结果
                  type: string
                metadata:
                  description: 元数据信息
                  type: object
            error:
              description: 错误信息
              type: string
          type: object
    description: 成功响应
```

#### 错误响应
```yaml
"400":
  content:
    application/json:
      schema:
        properties:
          success:
            type: boolean
            example: false
          error:
            type: string
            example: "参数错误"
        type: object
  description: 请求参数错误

"500":
  content:
    application/json:
      schema:
        properties:
          success:
            type: boolean
            example: false
          error:
            type: string
            example: "服务器内部错误"
        type: object
  description: 服务器内部错误
```

### 4. 数据类型和格式

#### 基本数据类型
- `string`: 字符串
- `integer`: 整数
- `number`: 数值
- `boolean`: 布尔值
- `array`: 数组
- `object`: 对象

#### 特殊格式
- `format: uri`: URL 格式
- `format: email`: 邮箱格式
- `format: date-time`: 时间格式
- `format: image_url`: 图片链接格式

#### 示例：文档转换插件 OpenAPI
```yaml
info:
  description: 文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式
  title: 文档转换器
  version: v1
openapi: 3.0.1
paths:
  /api/convert:
    post:
      operationId: convert_document
      requestBody:
        content:
          application/json:
            schema:
              properties:
                fileUrl:
                  description: 要转换的文档文件链接
                  type: string
                  format: uri
                outputFormat:
                  description: 输出格式
                  type: string
                  enum: ["markdown"]
                  default: "markdown"
              required:
                - fileUrl
              type: object
      responses:
        "200":
          content:
            application/json:
              schema:
                properties:
                  success:
                    type: boolean
                  markdown:
                    type: string
                  metadata:
                    type: object
                type: object
          description: 转换成功
      summary: 将文档转换为 Markdown 格式
servers:
  - url: https://pdf.ggss.club
```

---

## 插件配置文件编写

### 1. 插件元数据配置

插件元数据配置文件位于 `backend/conf/plugin/pluginproduct/plugin_meta.yaml`，用于注册和管理插件。

#### 配置结构
```yaml
- plugin_id: 唯一插件ID (整数)
  product_id: 产品ID (长整数)
  deprecated: 是否废弃 (布尔值)
  version: 版本号 (字符串)
  openapi_doc_file: OpenAPI文件名 (字符串)
  plugin_type: 插件类型 (整数，1=云端插件)
  manifest: 插件清单配置
  tools: 工具列表配置
```

#### 插件清单 (Manifest) 配置
```yaml
manifest:
  schema_version: v1                    # 固定值
  name_for_model: plugin_internal_name  # 内部标识名
  name_for_human: 插件显示名称           # 用户可见名称
  description_for_model: 给AI模型看的描述  # AI理解用描述
  description_for_human: 给用户看的描述   # 用户可读描述
  auth: 认证配置                        # 认证方式配置
  logo_url: 图标路径                    # 插件图标
  api: API配置                         # API类型配置
  common_params: 通用参数配置           # 公共参数
```

### 2. 认证配置

#### A. 无认证 (None)
```yaml
auth:
  type: none
```

#### B. API Token 认证
```yaml
auth:
  type: service_http
  key: Authorization                    # 认证头名称
  sub_type: token/api_key              # 子类型
  payload: >                           # 认证配置
    {
      "key": "Authorization",
      "service_token": "",
      "location": "Header"
    }
```

#### C. OAuth 认证
```yaml
auth:
  type: oauth
  sub_type: authorization_code
  payload: >
    {
      "client_id": "",
      "client_secret": "",
      "client_url": "https://auth.example.com/oauth/authorize",
      "scope": "read write",
      "authorization_url": "https://auth.example.com/oauth/token",
      "authorization_content_type": "application/json"
    }
```

### 3. 通用参数配置

```yaml
common_params:
  body: []                             # 请求体通用参数
  header:                             # 请求头通用参数
    - name: User-Agent
      value: Coze/1.0
    - name: Content-Type
      value: application/json
  path: []                            # 路径通用参数
  query: []                           # 查询通用参数
```

### 4. 工具配置

```yaml
tools:
  - tool_id: 工具唯一ID (整数)
    deprecated: 是否废弃 (布尔值)
    method: HTTP方法 (get/post/put/delete)
    sub_url: API子路径 (字符串)
```

### 5. 完整配置示例

```yaml
- plugin_id: 1
  product_id: 7500000000000000001
  deprecated: false
  version: v1.0.0
  openapi_doc_file: document_converter.yaml
  plugin_type: 1
  manifest:
    schema_version: v1
    name_for_model: document_converter
    name_for_human: 文档转换器
    description_for_model: 文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式
    description_for_human: 文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式
    auth:
      type: none
    logo_url: official_plugin_icon/plugin_document_converter.png
    api:
      type: openapi
    common_params:
      body: []
      header:
        - name: User-Agent
          value: Coze/1.0
        - name: Content-Type
          value: application/json
      path: []
      query: []
  tools:
    - tool_id: 10001
      deprecated: false
      method: post
      sub_url: /api/convert
```

---

## 插件测试和调试

### 1. 配置验证

#### YAML 语法验证
```bash
# 使用 Python 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('your_plugin.yaml').read()); print('YAML is valid')"

# 使用 yq 工具验证
yq eval '.' your_plugin.yaml > /dev/null && echo "YAML is valid"
```

#### OpenAPI 规范验证
```bash
# 使用 swagger-codegen 验证
swagger-codegen validate -i your_openapi.yaml

# 使用在线工具
# 访问 https://editor.swagger.io/ 粘贴你的 YAML 内容
```

### 2. API 服务测试

#### 使用 curl 测试
```bash
# GET 请求测试
curl -X GET "https://your-api.com/endpoint?param=value" \
     -H "User-Agent: Coze/1.0" \
     -H "Authorization: Bearer your-token"

# POST 请求测试
curl -X POST "https://your-api.com/endpoint" \
     -H "Content-Type: application/json" \
     -H "User-Agent: Coze/1.0" \
     -d '{
       "param1": "value1",
       "param2": "value2"
     }'
```

#### 使用 Postman 测试
1. 创建新的 Collection
2. 添加请求，设置 URL 和方法
3. 配置 Headers 和 Body
4. 发送请求验证响应格式

### 3. 本地调试

#### 启动 Coze Studio 开发环境
```bash
# 启动后端服务 (调试模式)
make debug

# 启动前端开发服务器
cd frontend/apps/coze-studio
npm run dev
```

#### 查看插件日志
```bash
# 查看插件相关日志
tail -f backend/logs/plugin.log

# 查看 HTTP 请求日志
tail -f backend/logs/http.log
```

### 4. 插件调试 API

Coze Studio 提供了插件调试接口：

```bash
# 调试插件 API
curl -X POST "http://localhost:8080/api/plugin_api/debug_api" \
     -H "Content-Type: application/json" \
     -d '{
       "plugin_id": "your_plugin_id",
       "api_id": "your_api_id",
       "parameters": "{\"param1\":\"value1\"}",
       "operation": 1
     }'
```

### 5. 常见调试问题

#### A. 插件无法加载
- 检查 YAML 语法是否正确
- 验证 plugin_id 和 tool_id 是否唯一
- 确认 openapi_doc_file 路径正确

#### B. API 调用失败
- 验证外部 API 服务是否可访问
- 检查请求参数格式是否符合 OpenAPI 规范
- 确认认证配置是否正确

#### C. 响应格式错误
- 检查响应 JSON 格式是否符合定义
- 验证必需字段是否存在
- 确认数据类型是否匹配

---

## 插件部署和发布

### 1. 文件组织

插件需要包含以下文件：

```
backend/conf/plugin/pluginproduct/
├── your_plugin.yaml                 # OpenAPI 规范文件
├── plugin_meta.yaml                 # 插件元数据 (更新)
└── official_plugin_icon/
    └── plugin_your_plugin.png       # 插件图标
```

### 2. 版本管理

#### 版本号规范
遵循语义化版本控制 (SemVer)：
- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能新增
- **修订号**: 向下兼容的问题修正

```yaml
version: v1.2.3
```

#### 版本更新流程
1. 更新 OpenAPI 规范文件
2. 更新 plugin_meta.yaml 中的版本号
3. 添加版本更新说明
4. 进行充分测试
5. 提交代码变更

### 3. 部署检查清单

#### 部署前检查
- [ ] YAML 文件语法正确
- [ ] OpenAPI 规范验证通过
- [ ] 外部 API 服务稳定运行
- [ ] 认证配置测试通过
- [ ] 插件图标文件存在
- [ ] 版本号符合规范
- [ ] 插件功能完整测试

#### 部署配置
```bash
# 重新构建服务
make build_server

# 重启服务 (生产环境)
systemctl restart coze-studio

# 验证插件加载
curl -X POST "http://localhost:8080/api/plugin_api/get_dev_plugin_list" \
     -H "Content-Type: application/json" \
     -d '{"dev_id": "your_dev_id", "space_id": "your_space_id"}'
```

### 4. 发布流程

#### A. 内部测试发布
1. 在测试环境部署插件
2. 执行完整的功能测试
3. 验证性能和稳定性
4. 收集测试反馈

#### B. 生产环境发布
1. 代码审查和安全检查
2. 准备回滚方案
3. 生产环境部署
4. 监控插件运行状态
5. 用户培训和文档更新

### 5. 监控和维护

#### 监控指标
- API 调用成功率
- 响应时间
- 错误率统计
- 用户使用情况

#### 日志监控
```bash
# 监控插件调用日志
grep "plugin_id=your_plugin_id" backend/logs/plugin.log

# 监控错误日志
grep "ERROR" backend/logs/plugin.log | grep "your_plugin"
```

#### 维护任务
- 定期检查外部 API 服务状态
- 监控插件性能指标
- 及时响应用户反馈
- 定期更新插件版本

---

## 最佳实践和常见问题

### 1. 设计最佳实践

#### A. API 设计原则
- **RESTful 设计**: 遵循 REST API 设计原则
- **统一响应格式**: 保持响应结构一致性
- **错误处理**: 提供详细的错误信息
- **参数验证**: 严格验证输入参数
- **幂等性**: GET 和 PUT 操作应保持幂等

#### B. 性能优化
- **并发处理**: 设计支持高并发的 API
- **缓存策略**: 合理使用缓存减少延迟
- **超时设置**: 设置合理的超时时间
- **资源限制**: 避免资源滥用

#### C. 安全考虑
- **数据验证**: 严格验证所有输入数据
- **权限控制**: 实现细粒度的权限管理
- **敏感信息**: 避免在日志中记录敏感数据
- **HTTPS**: 强制使用 HTTPS 通信

### 2. 常见问题解决

#### A. 插件无法加载

**问题**: 插件在系统中不显示或无法使用

**可能原因和解决方案**:
```yaml
# 1. 检查插件 ID 是否唯一
- plugin_id: 确保在所有插件中唯一

# 2. 检查 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"

# 3. 检查文件路径
openapi_doc_file: 确保文件存在且路径正确

# 4. 检查工具 ID 唯一性
tools:
  - tool_id: 确保在所有工具中唯一
```

#### B. API 调用超时

**问题**: 插件调用外部 API 时频繁超时

**解决方案**:
```yaml
# 在 OpenAPI 规范中添加超时处理
responses:
  "408":
    description: 请求超时
    content:
      application/json:
        schema:
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "请求超时，请稍后重试"
```

```go
// 外部 API 实现超时控制
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

client := &http.Client{Timeout: 30 * time.Second}
```

#### C. 认证失败

**问题**: 插件调用外部 API 时认证失败

**解决方案**:
```yaml
# 检查认证配置格式
auth:
  type: service_http
  key: Authorization
  sub_type: token/api_key
  payload: '{"key": "Authorization", "service_token": "valid_token", "location": "Header"}'

# 或 OAuth 配置
auth:
  type: oauth
  sub_type: authorization_code
  payload: '{"client_id": "valid_id", "client_secret": "valid_secret", ...}'
```

#### D. 响应格式不匹配

**问题**: 外部 API 返回的数据格式与 OpenAPI 规范不符

**解决方案**:
```yaml
# 1. 更新 OpenAPI 规范以匹配实际响应
responses:
  "200":
    content:
      application/json:
        schema:
          # 根据实际响应更新 schema
          
# 2. 在外部 API 中添加数据格式转换
def format_response(raw_data):
    return {
        "success": True,
        "data": raw_data,
        "timestamp": datetime.now().isoformat()
    }
```

### 3. 性能优化建议

#### A. 请求优化
- 使用连接池减少建连开销
- 实现请求重试机制
- 合理设置超时时间
- 压缩请求和响应数据

#### B. 缓存策略
```go
// 示例：Redis 缓存实现
func getCachedResult(key string) (string, error) {
    result, err := redisClient.Get(key).Result()
    if err == redis.Nil {
        // 缓存不存在，调用 API
        apiResult := callExternalAPI()
        redisClient.Set(key, apiResult, 5*time.Minute)
        return apiResult, nil
    }
    return result, err
}
```

#### C. 监控指标
- API 调用响应时间
- 成功率和错误率
- 并发请求数量
- 资源使用情况

### 4. 调试技巧

#### A. 日志记录
```go
// 结构化日志记录
log.WithFields(log.Fields{
    "plugin_id": pluginID,
    "tool_id":   toolID,
    "user_id":   userID,
    "duration":  duration,
}).Info("Plugin API called successfully")
```

#### B. 错误追踪
```yaml
# 在响应中包含请求 ID 便于追踪
responses:
  "200":
    content:
      application/json:
        schema:
          properties:
            request_id:
              type: string
              description: 请求追踪 ID
```

#### C. 开发工具
- **Swagger Editor**: 编辑和验证 OpenAPI 规范
- **Postman**: API 测试和调试
- **curl**: 命令行 API 测试
- **jq**: JSON 数据处理

### 5. 文档和维护

#### A. 文档要求
- 完整的 API 文档
- 使用示例和代码片段
- 错误代码说明
- 版本更新记录

#### B. 版本控制
```yaml
# 版本更新示例
version: v1.1.0
# 更新说明:
# - 新增批量处理功能
# - 优化响应性能
# - 修复认证问题
```

#### C. 用户支持
- 提供详细的使用文档
- 建立问题反馈渠道
- 定期收集用户反馈
- 及时修复发现的问题

---

## 总结

本指南详细介绍了 Coze Studio 插件开发的完整流程，从环境准备到部署发布，涵盖了开发过程中的各个关键环节。通过遵循本指南的最佳实践，你可以开发出高质量、稳定可靠的插件，为 Coze Studio 生态系统贡献力量。

在开发过程中如遇到问题，建议：
1. 仔细阅读相关章节的说明
2. 参考现有插件的实现方式
3. 使用提供的调试工具进行问题定位
4. 在社区或 GitHub 仓库中寻求帮助

持续学习和改进是插件开发的重要组成部分，随着 Coze Studio 平台的发展，插件开发的最佳实践也会不断演进。