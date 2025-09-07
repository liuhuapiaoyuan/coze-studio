# 插件配置文件规范

本文档详细介绍 Coze Studio 插件配置文件的结构、字段定义和配置规范。

## 配置文件概览

Coze Studio 插件系统使用两种主要配置文件：

1. **OpenAPI 规范文件** (`*.yaml`): 定义插件的 API 接口
2. **插件元数据文件** (`plugin_meta.yaml`): 定义插件的基本信息和配置

## 文件结构

```
backend/conf/plugin/pluginproduct/
├── plugin_meta.yaml              # 插件元数据总配置
├── document_converter.yaml       # 文档转换器 OpenAPI 定义
├── image_compression.yaml        # 图片压缩 OpenAPI 定义
├── worth_buying.yaml             # 什么值得买 OpenAPI 定义
└── official_plugin_icon/         # 插件图标目录
    ├── plugin_document_converter.png
    └── plugin_image_compression.jpeg
```

## OpenAPI 规范文件

### 基本结构

```yaml
info:
  description: 插件功能描述
  title: 插件标题
  version: v1
openapi: 3.0.1
paths:
  /api/endpoint:
    post:
      # API 端点定义
servers:
  - url: https://api.example.com
```

### 完整示例 (document_converter.yaml)

```yaml
info:
  description: 文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式。通过输入文档链接，调用转换服务，返回格式化的 Markdown 内容，便于 AI 处理和分析。
  title: 文档转换器
  version: v1
openapi: 3.0.1

paths:
  /api/convert:
    post:
      operationId: convert_document
      summary: 将文档转换为 Markdown 格式
      description: |
        接收文档文件链接，调用转换服务将 PDF、Word 文档转换为 Markdown 格式。
        
        **支持的文件格式：**
        - PDF (.pdf)
        - Microsoft Word (.doc, .docx)
        
        **功能特性：**
        - 保留文档结构和格式
        - 自动识别标题层级
        - 转换表格为 Markdown 表格格式
        - 提取文档元数据信息
        - 支持中英文文档

      requestBody:
        description: 文档转换请求参数
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - fileUrl
              properties:
                fileUrl:
                  type: string
                  format: uri
                  description: 要转换的文档文件链接，支持 PDF、Word (.doc, .docx) 格式。文件需要可公开访问。
                  example: "https://example.com/document.pdf"
                outputFormat:
                  type: string
                  enum: ["markdown"]
                  default: "markdown"
                  description: 输出格式，当前仅支持 markdown
                preserveFormatting:
                  type: boolean
                  default: true
                  description: 是否保留原文档格式信息（如标题层级、表格结构等）

      responses:
        "200":
          description: 转换成功响应
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    description: 转换是否成功
                  markdown:
                    type: string
                    description: 转换后的 Markdown 内容
                  metadata:
                    type: object
                    description: 文档元数据信息
                    properties:
                      originalFileName:
                        type: string
                        description: 原文件名
                      fileSize:
                        type: integer
                        description: 文件大小（字节）
                      pageCount:
                        type: integer
                        description: 页数（仅 PDF）
                      wordCount:
                        type: integer
                        description: 字数统计
                      convertedAt:
                        type: string
                        format: date-time
                        description: 转换时间戳
                  error:
                    type: string
                    description: 错误信息（转换失败时）

        "400":
          description: 请求参数错误
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: false
                  error:
                    type: string
                    example: "无效的文件链接或不支持的文件格式"

        "422":
          description: 文件处理错误
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: false
                  error:
                    type: string
                    example: "文件无法访问或下载失败"

        "500":
          description: 服务器内部错误
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: false
                  error:
                    type: string
                    example: "服务器内部错误，请稍后重试"

servers:
  - url: https://pdf.ggss.club
    description: 文档转换服务
```

### 字段说明

#### info 对象

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 插件显示名称 |
| `description` | string | ✅ | 插件功能描述 |
| `version` | string | ✅ | API 版本号 |

#### paths 对象

定义 API 端点和操作：

```yaml
paths:
  /api/endpoint:           # API 路径
    post:                  # HTTP 方法 (get, post, put, delete, patch)
      operationId: string  # 操作唯一标识符
      summary: string      # 简短描述
      description: string  # 详细描述
      requestBody:         # 请求体定义
      responses:          # 响应定义
      parameters:         # 路径/查询参数
```

#### requestBody 对象

```yaml
requestBody:
  description: string    # 请求体描述
  required: boolean     # 是否必需
  content:
    application/json:   # 媒体类型
      schema:          # JSON Schema 定义
        type: object
        required: [field1, field2]
        properties:
          field1:
            type: string
            description: string
```

#### responses 对象

```yaml
responses:
  "200":                # HTTP 状态码
    description: string # 响应描述
    content:
      application/json:
        schema:         # 响应数据结构
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
```

#### servers 对象

```yaml
servers:
  - url: https://api.example.com    # 服务器 URL
    description: 生产环境服务器      # 服务器描述
  - url: https://test-api.example.com
    description: 测试环境服务器
```

## 插件元数据文件 (plugin_meta.yaml)

### 基本结构

```yaml
- plugin_id: 1                    # 插件唯一 ID
  product_id: 7500000000000000001 # 产品 ID
  deprecated: false               # 是否已废弃
  version: v1.0.0                # 版本号
  openapi_doc_file: plugin.yaml  # OpenAPI 文件名
  plugin_type: 1                 # 插件类型
  manifest:                      # 插件清单
    # 插件元信息
  tools:                         # 工具列表
    # 工具定义
```

### 完整示例

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
    description_for_model: 文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式。通过输入文档链接，调用转换服务，返回格式化的 Markdown 内容，便于 AI 处理和分析。
    description_for_human: 文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式。通过输入文档链接，调用转换服务，返回格式化的 Markdown 内容。
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

### 字段详解

#### 顶层字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `plugin_id` | integer | ✅ | 插件唯一标识符 |
| `product_id` | integer | ✅ | 插件商店产品 ID |
| `deprecated` | boolean | ✅ | 是否已废弃 |
| `version` | string | ✅ | 插件版本号 |
| `openapi_doc_file` | string | ✅ | OpenAPI 文档文件名 |
| `plugin_type` | integer | ✅ | 插件类型 (1=普通插件) |

#### manifest 对象

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `schema_version` | string | ✅ | Manifest 版本 (固定为 "v1") |
| `name_for_model` | string | ✅ | AI 模型使用的插件名 |
| `name_for_human` | string | ✅ | 用户界面显示的插件名 |
| `description_for_model` | string | ✅ | AI 模型使用的描述 |
| `description_for_human` | string | ✅ | 用户界面显示的描述 |
| `auth` | object | ✅ | 认证配置 |
| `logo_url` | string | ✅ | 插件图标路径 |
| `api` | object | ✅ | API 类型配置 |
| `common_params` | object | ✅ | 通用参数配置 |

#### auth 对象

**无认证插件**:
```yaml
auth:
  type: none
```

**API Key 认证插件**:
```yaml
auth:
  type: service_http
  key: Authorization           # 认证参数名
  sub_type: token/api_key     # 认证子类型
  payload: '{"key": "Authorization", "service_token": "", "location": "Header"}'
```

**OAuth 认证插件**:
```yaml
auth:
  type: oauth
  sub_type: authorization_code
  payload: '{"client_id":"","client_secret":"","client_url":"https://accounts.example.com/oauth/authorize","scope":"read write","authorization_url":"https://api.example.com/oauth/token","authorization_content_type":"application/json"}'
```

#### common_params 对象

定义插件调用时的通用参数：

```yaml
common_params:
  body: []                    # 请求体通用参数
  header:                     # 请求头通用参数
    - name: User-Agent
      value: Coze/1.0
    - name: Content-Type
      value: application/json
  path: []                    # 路径参数
  query: []                   # 查询参数
```

#### tools 数组

定义插件包含的工具：

```yaml
tools:
  - tool_id: 10001           # 工具唯一 ID
    deprecated: false        # 是否已废弃
    method: post            # HTTP 方法
    sub_url: /api/convert   # API 子路径
```

## 认证配置详解

### 1. 无认证 (none)

适用于公开 API，无需任何认证信息：

```yaml
auth:
  type: none
```

### 2. 服务端认证 (service_http)

适用于需要 API Key 的服务：

#### Header 认证

```yaml
auth:
  type: service_http
  key: Authorization
  sub_type: token/api_key
  payload: '{"key": "Authorization", "service_token": "Bearer YOUR_API_KEY", "location": "Header"}'
```

#### Query 参数认证

```yaml
auth:
  type: service_http
  key: api_key
  sub_type: token/api_key
  payload: '{"key": "api_key", "service_token": "YOUR_API_KEY", "location": "Query"}'
```

#### Body 认证

```yaml
auth:
  type: service_http
  key: token
  sub_type: token/api_key
  payload: '{"key": "token", "service_token": "YOUR_API_KEY", "location": "Body"}'
```

### 3. OAuth 认证 (oauth)

适用于需要用户授权的第三方服务：

#### Authorization Code 流程

```yaml
auth:
  type: oauth
  sub_type: authorization_code
  payload: '{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret", 
    "client_url": "https://accounts.example.com/oauth/authorize",
    "scope": "read write offline_access",
    "authorization_url": "https://api.example.com/oauth/token",
    "authorization_content_type": "application/json"
  }'
```

#### Client Credentials 流程

```yaml
auth:
  type: oauth
  sub_type: client_credentials
  payload: '{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "authorization_url": "https://api.example.com/oauth/token",
    "scope": "api_access"
  }'
```

## 配置最佳实践

### 1. 命名规范

#### 插件命名

- **name_for_model**: 使用英文小写，下划线分隔
  ```yaml
  name_for_model: document_converter
  name_for_model: image_processor
  name_for_model: data_analyzer
  ```

- **name_for_human**: 使用中文，简洁明了
  ```yaml
  name_for_human: 文档转换器
  name_for_human: 图片处理器
  name_for_human: 数据分析器
  ```

#### 文件命名

- OpenAPI 文件: `{功能}_plugin.yaml`
- 图标文件: `plugin_{功能}_{格式}`

### 2. 描述规范

#### AI 模型描述 (description_for_model)

应该详细描述插件的功能、用途和限制：

```yaml
description_for_model: |
  文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式。
  功能特性：
  1. 支持 PDF (.pdf) 和 Word (.doc, .docx) 格式
  2. 保留文档结构和格式信息
  3. 自动识别标题层级
  4. 转换表格为 Markdown 表格格式
  5. 提取文档元数据信息
  使用场景：文档内容分析、知识库整理、AI 辅助编辑
```

#### 用户描述 (description_for_human)

应该简洁明了，突出核心价值：

```yaml
description_for_human: 将 PDF、Word 文档转换为 Markdown 格式，便于 AI 处理和分析。
```

### 3. 错误处理规范

#### 标准错误响应

```yaml
responses:
  "400":
    description: 请求参数错误
    content:
      application/json:
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "参数验证失败"
            code:
              type: string
              example: "INVALID_PARAMS"
```

#### 错误码定义

| HTTP 状态码 | 错误类型 | 说明 |
|------------|----------|------|
| 400 | 请求错误 | 参数验证失败、格式错误 |
| 401 | 认证错误 | API Key 无效、Token 过期 |
| 403 | 权限错误 | 无权限访问该资源 |
| 422 | 处理错误 | 业务逻辑错误、文件处理失败 |
| 429 | 限流错误 | 请求频率超限 |
| 500 | 服务错误 | 服务器内部错误 |

### 4. 版本管理

#### 语义化版本

使用 [Semantic Versioning](https://semver.org/) 规范：

```yaml
version: v1.0.0   # 主版本.次版本.修订版本
```

- **主版本**: 不兼容的 API 修改
- **次版本**: 向后兼容的功能性新增
- **修订版本**: 向后兼容的问题修复

#### 版本迁移

```yaml
# 旧版本
- plugin_id: 1
  version: v1.0.0
  deprecated: false

# 新版本
- plugin_id: 1
  version: v1.1.0
  deprecated: false
  
# 废弃旧版本
- plugin_id: 1
  version: v1.0.0
  deprecated: true
```

## 验证和测试

### 配置文件验证

```bash
# YAML 语法验证
yq eval plugin_meta.yaml > /dev/null

# OpenAPI 规范验证
swagger validate document_converter.yaml

# JSON Schema 验证
jsonschema -i plugin_meta.yaml plugin_schema.json
```

### 自动化验证脚本

```python
#!/usr/bin/env python3
# validate_plugin_config.py

import yaml
import jsonschema
from pathlib import Path

def validate_plugin_config(config_path):
    """验证插件配置文件"""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # 基础字段验证
    required_fields = ['plugin_id', 'product_id', 'version', 'manifest']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"缺少必需字段: {field}")
    
    # Manifest 验证
    manifest = config['manifest']
    manifest_fields = ['name_for_model', 'name_for_human', 'auth', 'api']
    for field in manifest_fields:
        if field not in manifest:
            raise ValueError(f"Manifest 缺少必需字段: {field}")
    
    print("✅ 配置文件验证通过")

if __name__ == "__main__":
    validate_plugin_config("plugin_meta.yaml")
```

## 下一步

配置文件编写完成后，您可以：

1. 📚 学习 [OpenAPI 规范指南](./openapi-specification.md) 深入了解 API 定义
2. 🚀 参考 [部署和测试指南](./deployment-testing.md) 部署您的插件
3. 💡 查看 [最佳实践](./best-practices.md) 了解更多开发技巧

---

如果您在配置过程中遇到问题，请参考示例配置文件或在开发者社区寻求帮助。