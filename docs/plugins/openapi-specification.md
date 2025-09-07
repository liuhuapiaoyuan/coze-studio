# OpenAPI 规范指南

本文档详细介绍如何在 Coze Studio 插件开发中使用 OpenAPI 3.0.1 规范定义 API 接口。

## 什么是 OpenAPI

OpenAPI 规范（原 Swagger 规范）是一种用于描述 REST API 的标准化格式。Coze Studio 使用 OpenAPI 3.0.1 规范来：

- 定义插件 API 接口
- 自动生成 HTTP 客户端
- 验证请求和响应数据
- 生成 API 文档

## 基础结构

### 最简 OpenAPI 文档

```yaml
openapi: 3.0.1
info:
  title: 示例插件
  description: 一个简单的示例插件
  version: v1
paths:
  /api/hello:
    get:
      operationId: hello
      summary: 问候接口
      responses:
        '200':
          description: 成功响应
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
servers:
  - url: https://api.example.com
```

### 完整结构概览

```yaml
openapi: 3.0.1          # OpenAPI 版本
info:                   # API 基本信息
  title: string
  description: string
  version: string
  
servers:               # 服务器列表
  - url: string
    description: string
    
paths:                 # API 路径定义
  /path:
    method:           # HTTP 方法
      operationId: string
      summary: string
      description: string
      parameters: []   # 参数定义
      requestBody:     # 请求体
      responses:       # 响应定义
      
components:            # 可复用组件
  schemas:            # 数据模型
  parameters:         # 参数模板
  responses:          # 响应模板
```

## Info 对象详解

Info 对象包含 API 的基本元信息：

```yaml
info:
  title: 文档转换器              # API 名称（必需）
  description: |               # API 描述（必需）
    文档转换器，支持将 PDF、Word 文档转换为 Markdown 格式。
    
    **主要功能：**
    - 支持 PDF (.pdf) 和 Word (.doc, .docx) 格式
    - 保留文档结构和格式
    - 自动识别标题层级
    - 提取文档元数据
    
  version: v1                  # API 版本（必需）
  termsOfService: https://example.com/terms  # 服务条款
  contact:                     # 联系信息
    name: API 支持团队
    url: https://example.com/support
    email: support@example.com
  license:                     # 许可证信息
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html
```

## Servers 对象详解

Servers 定义 API 的服务器地址：

```yaml
servers:
  - url: https://api.example.com           # 生产环境
    description: 生产环境服务器
  - url: https://test-api.example.com      # 测试环境
    description: 测试环境服务器
  - url: https://dev-api.example.com       # 开发环境
    description: 开发环境服务器
```

### 动态服务器地址

```yaml
servers:
  - url: https://{environment}.example.com/api/{version}
    description: 多环境服务器
    variables:
      environment:
        default: api
        enum:
          - api      # 生产环境
          - test     # 测试环境
          - dev      # 开发环境
      version:
        default: v1
        enum: [v1, v2]
```

## Paths 对象详解

Paths 是 OpenAPI 文档的核心，定义所有 API 端点：

### 基本路径定义

```yaml
paths:
  /api/convert:                    # API 路径
    post:                          # HTTP 方法
      operationId: convert_document # 操作 ID（必需，全局唯一）
      summary: 转换文档              # 简短描述
      description: |               # 详细描述
        将文档转换为 Markdown 格式
      tags:                       # 标签分组
        - 文档处理
      deprecated: false           # 是否已弃用
```

### 支持的 HTTP 方法

```yaml
paths:
  /api/resource:
    get:        # 获取资源
    post:       # 创建资源
    put:        # 更新资源（完整更新）
    patch:      # 更新资源（部分更新）
    delete:     # 删除资源
    head:       # 获取资源头信息
    options:    # 获取支持的方法
```

## Parameters 参数定义

### 参数位置

OpenAPI 支持四种参数位置：

1. **path**: 路径参数
2. **query**: 查询参数
3. **header**: 请求头参数
4. **cookie**: Cookie 参数

### 路径参数 (Path Parameters)

```yaml
paths:
  /api/documents/{documentId}:
    get:
      parameters:
        - name: documentId
          in: path              # 参数位置
          required: true        # 路径参数总是必需的
          schema:
            type: string
            pattern: '^[a-zA-Z0-9-]+$'
          description: 文档唯一标识符
          example: "doc-123"
```

### 查询参数 (Query Parameters)

```yaml
paths:
  /api/documents:
    get:
      parameters:
        - name: page
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
          description: 页码
        - name: size
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
          description: 每页数量
        - name: format
          in: query
          required: false
          schema:
            type: string
            enum: ["pdf", "docx", "markdown"]
          description: 文档格式筛选
```

### 请求头参数 (Header Parameters)

```yaml
paths:
  /api/convert:
    post:
      parameters:
        - name: X-Request-ID
          in: header
          required: false
          schema:
            type: string
            format: uuid
          description: 请求追踪 ID
        - name: Accept-Language
          in: header
          required: false
          schema:
            type: string
            default: "zh-CN"
          description: 客户端语言偏好
```

## Request Body 请求体定义

### 基本请求体

```yaml
paths:
  /api/convert:
    post:
      requestBody:
        description: 文档转换请求
        required: true              # 是否必需
        content:
          application/json:         # 媒体类型
            schema:
              type: object
              required:
                - fileUrl
              properties:
                fileUrl:
                  type: string
                  format: uri
                  description: 文档文件链接
                  example: "https://example.com/doc.pdf"
```

### 多媒体类型请求体

```yaml
requestBody:
  description: 上传文件或URL
  required: true
  content:
    application/json:              # JSON 格式
      schema:
        type: object
        properties:
          fileUrl:
            type: string
            format: uri
    multipart/form-data:           # 文件上传
      schema:
        type: object
        properties:
          file:
            type: string
            format: binary
          metadata:
            type: string
    application/x-www-form-urlencoded:  # 表单数据
      schema:
        type: object
        properties:
          url:
            type: string
```

### 请求体示例

```yaml
requestBody:
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/ConvertRequest'
      examples:
        pdf_conversion:
          summary: PDF 转换示例
          description: 转换 PDF 文档为 Markdown
          value:
            fileUrl: "https://example.com/sample.pdf"
            outputFormat: "markdown"
            preserveFormatting: true
        word_conversion:
          summary: Word 转换示例
          description: 转换 Word 文档为 Markdown
          value:
            fileUrl: "https://example.com/sample.docx"
            outputFormat: "markdown"
            preserveFormatting: false
```

## Responses 响应定义

### 基本响应结构

```yaml
responses:
  '200':                           # HTTP 状态码
    description: 转换成功           # 响应描述
    content:
      application/json:            # 响应媒体类型
        schema:                    # 响应数据结构
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
        examples:                  # 响应示例
          success:
            summary: 成功响应
            value:
              success: true
              data:
                markdown: "# 标题\n\n内容..."
```

### 完整响应定义

```yaml
responses:
  '200':
    description: 转换成功
    headers:                      # 响应头
      X-Request-ID:
        schema:
          type: string
        description: 请求追踪 ID
      X-Rate-Limit-Remaining:
        schema:
          type: integer
        description: 剩余请求次数
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ConvertResponse'
  '400':
    description: 请求参数错误
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ErrorResponse'
  '422':
    description: 文件处理失败
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ErrorResponse'
  '500':
    description: 服务器内部错误
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ErrorResponse'
```

## Schemas 数据模型

### 基本数据类型

```yaml
components:
  schemas:
    # 字符串类型
    StringField:
      type: string
      minLength: 1
      maxLength: 255
      pattern: '^[a-zA-Z0-9-_]+$'
      
    # 数值类型
    NumberField:
      type: number
      minimum: 0
      maximum: 1000
      multipleOf: 0.01
      
    # 整数类型
    IntegerField:
      type: integer
      minimum: 1
      maximum: 100
      
    # 布尔类型
    BooleanField:
      type: boolean
      default: false
      
    # 日期时间类型
    DateTimeField:
      type: string
      format: date-time
      example: "2023-12-01T10:00:00Z"
```

### 对象类型

```yaml
components:
  schemas:
    ConvertRequest:
      type: object
      required:
        - fileUrl
      properties:
        fileUrl:
          type: string
          format: uri
          description: 要转换的文档链接
          example: "https://example.com/doc.pdf"
        outputFormat:
          type: string
          enum: ["markdown", "html", "text"]
          default: "markdown"
          description: 输出格式
        options:
          type: object
          properties:
            preserveFormatting:
              type: boolean
              default: true
            extractImages:
              type: boolean
              default: false
```

### 数组类型

```yaml
components:
  schemas:
    DocumentList:
      type: array
      items:
        $ref: '#/components/schemas/Document'
      minItems: 0
      maxItems: 100
      
    TagList:
      type: array
      items:
        type: string
      uniqueItems: true
      example: ["pdf", "document", "conversion"]
```

### 继承和组合

```yaml
components:
  schemas:
    # 基础响应
    BaseResponse:
      type: object
      required:
        - success
        - timestamp
      properties:
        success:
          type: boolean
        timestamp:
          type: string
          format: date-time
        requestId:
          type: string
          format: uuid
    
    # 成功响应（继承）
    SuccessResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
    
    # 错误响应（继承）
    ErrorResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            error:
              type: object
              properties:
                code:
                  type: string
                message:
                  type: string
```

## 数据验证

### 字符串验证

```yaml
properties:
  email:
    type: string
    format: email                # 邮箱格式
    example: "user@example.com"
  
  url:
    type: string
    format: uri                  # URI 格式
    example: "https://example.com"
  
  phone:
    type: string
    pattern: '^1[3-9]\d{9}$'    # 正则表达式
    example: "13800138000"
  
  password:
    type: string
    minLength: 8                 # 最小长度
    maxLength: 32               # 最大长度
    format: password            # 密码格式（UI 提示）
```

### 数值验证

```yaml
properties:
  age:
    type: integer
    minimum: 0                  # 最小值
    maximum: 150               # 最大值
    example: 25
  
  price:
    type: number
    minimum: 0.01             # 最小值（包含）
    maximum: 9999.99         # 最大值（包含）
    exclusiveMinimum: 0      # 最小值（不包含）
    multipleOf: 0.01         # 倍数验证
    example: 99.99
  
  rating:
    type: number
    minimum: 1
    maximum: 5
    enum: [1, 2, 3, 4, 5]    # 枚举值
```

### 数组验证

```yaml
properties:
  tags:
    type: array
    items:
      type: string
      minLength: 1
    minItems: 1               # 最少元素数
    maxItems: 10             # 最多元素数
    uniqueItems: true        # 元素唯一性
  
  coordinates:
    type: array
    items:
      type: number
    minItems: 2
    maxItems: 2
    example: [121.473701, 31.230416]
```

## 高级特性

### 条件验证 (OneOf, AnyOf, AllOf)

```yaml
components:
  schemas:
    PaymentMethod:
      oneOf:                    # 只能匹配一个
        - $ref: '#/components/schemas/CreditCard'
        - $ref: '#/components/schemas/BankTransfer'
        - $ref: '#/components/schemas/DigitalWallet'
      discriminator:            # 判别器
        propertyName: type
        mapping:
          credit_card: '#/components/schemas/CreditCard'
          bank_transfer: '#/components/schemas/BankTransfer'
          digital_wallet: '#/components/schemas/DigitalWallet'
    
    SearchQuery:
      anyOf:                    # 可以匹配多个
        - type: object
          properties:
            keyword:
              type: string
        - type: object
          properties:
            category:
              type: string
```

### 动态属性

```yaml
components:
  schemas:
    DynamicObject:
      type: object
      properties:
        name:
          type: string
      additionalProperties:     # 允许额外属性
        type: string
      
    StrictObject:
      type: object
      properties:
        name:
          type: string
      additionalProperties: false  # 禁止额外属性
```

### 可为空值

```yaml
components:
  schemas:
    OptionalField:
      type: object
      properties:
        name:
          type: string
        description:
          type: string
          nullable: true        # 可为 null
        tags:
          type: array
          items:
            type: string
          default: []           # 默认空数组
```

## 安全配置

虽然 Coze Studio 插件的认证主要通过插件元数据配置，但了解 OpenAPI 的安全配置有助于理解整个认证流程：

### API Key 认证

```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header                # 位置：header, query, cookie
      name: X-API-Key          # 参数名

security:                     # 全局安全要求
  - ApiKeyAuth: []
  
paths:
  /api/convert:
    post:
      security:                # 路径级安全要求
        - ApiKeyAuth: []
```

### Bearer Token 认证

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT       # 可选，提示 token 格式

security:
  - BearerAuth: []
```

### OAuth 2.0 认证

```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          scopes:
            read: 读取权限
            write: 写入权限
            admin: 管理员权限

security:
  - OAuth2: [read, write]
```

## 文档化最佳实践

### 1. 详细的描述

```yaml
info:
  description: |
    # 文档转换 API
    
    这个 API 提供文档格式转换服务，支持将各种格式的文档转换为 Markdown。
    
    ## 支持的格式
    
    | 输入格式 | 文件扩展名 | 说明 |
    |---------|-----------|------|
    | PDF | .pdf | Adobe PDF 文档 |
    | Word | .doc, .docx | Microsoft Word 文档 |
    
    ## 使用限制
    
    - 文件大小不超过 10MB
    - 每分钟最多 60 次请求
    - 支持的语言：中文、英文
```

### 2. 丰富的示例

```yaml
components:
  schemas:
    ConvertRequest:
      type: object
      properties:
        fileUrl:
          type: string
          format: uri
          description: 文档下载链接
          example: "https://example.com/sample.pdf"
      example:                  # 完整对象示例
        fileUrl: "https://example.com/document.pdf"
        outputFormat: "markdown"
        preserveFormatting: true
        
  examples:                    # 可复用示例
    PdfConversion:
      summary: PDF 转换示例
      description: 一个典型的 PDF 转换请求
      value:
        fileUrl: "https://example.com/report.pdf"
        outputFormat: "markdown"
        options:
          preserveFormatting: true
          extractImages: false
```

### 3. 标签和分组

```yaml
tags:
  - name: 文档转换
    description: 文档格式转换相关接口
  - name: 文档管理
    description: 文档上传、下载、管理接口

paths:
  /api/convert:
    post:
      tags:
        - 文档转换              # 分配到标签组
      summary: 转换文档格式
```

## 常见模式和模板

### 分页响应模式

```yaml
components:
  schemas:
    PaginatedResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Document'
        pagination:
          type: object
          properties:
            page:
              type: integer
              minimum: 1
            size:
              type: integer
              minimum: 1
              maximum: 100
            total:
              type: integer
              minimum: 0
            hasNext:
              type: boolean
```

### 错误响应模式

```yaml
components:
  schemas:
    ErrorResponse:
      type: object
      required:
        - success
        - error
      properties:
        success:
          type: boolean
          example: false
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              description: 错误代码
              example: "INVALID_FILE_FORMAT"
            message:
              type: string
              description: 错误描述
              example: "不支持的文件格式"
            details:
              type: object
              description: 详细错误信息
        requestId:
          type: string
          format: uuid
          description: 请求追踪 ID
```

### 异步任务模式

```yaml
components:
  schemas:
    TaskResponse:
      type: object
      properties:
        taskId:
          type: string
          format: uuid
          description: 任务 ID
        status:
          type: string
          enum: ["pending", "processing", "completed", "failed"]
          description: 任务状态
        progress:
          type: integer
          minimum: 0
          maximum: 100
          description: 完成进度（百分比）
        result:
          type: object
          description: 任务结果（完成时）
          nullable: true
        error:
          type: string
          description: 错误信息（失败时）
          nullable: true
        createdAt:
          type: string
          format: date-time
        completedAt:
          type: string
          format: date-time
          nullable: true
```

## 验证和测试

### 使用 Swagger Editor 验证

```bash
# 在线验证器
https://editor.swagger.io/

# 本地验证
npm install -g swagger-editor
swagger-editor
```

### 使用命令行工具验证

```bash
# Swagger Codegen CLI
swagger-codegen validate -i openapi.yaml

# OpenAPI Generator CLI
openapi-generator validate -i openapi.yaml

# Spectral (OpenAPI Linter)
npm install -g @stoplight/spectral-cli
spectral lint openapi.yaml
```

### 自动化测试

```javascript
// 使用 Jest 和 OpenAPI Schema Validator
const OpenAPISchemaValidator = require('openapi-schema-validator').default;
const yaml = require('js-yaml');
const fs = require('fs');

test('OpenAPI 规范验证', () => {
  const spec = yaml.load(fs.readFileSync('openapi.yaml', 'utf8'));
  const validator = new OpenAPISchemaValidator({ version: 3 });
  const result = validator.validate(spec);
  
  expect(result.errors).toHaveLength(0);
});
```

## 下一步

OpenAPI 规范编写完成后，您可以：

1. 🚀 参考 [部署和测试指南](./deployment-testing.md) 部署您的插件
2. 💡 查看 [最佳实践](./best-practices.md) 了解更多开发技巧
3. 🔍 浏览 [示例插件](./examples/) 学习具体实现

---

掌握 OpenAPI 规范是插件开发的基础，良好的 API 设计将使您的插件更容易使用和维护。