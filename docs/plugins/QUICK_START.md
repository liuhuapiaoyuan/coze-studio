# Coze Studio 插件开发快速入门

本文档提供插件开发的快速入门指南，帮助开发者快速创建第一个插件。

## 5分钟创建你的第一个插件

### 步骤 1: 准备外部 API 服务

确保你有一个可访问的 HTTP API 服务。示例：

```bash
# 测试你的 API 是否可用
curl -X POST "https://your-api.com/endpoint" \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
```

### 步骤 2: 创建 OpenAPI 规范文件

在 `backend/conf/plugin/pluginproduct/` 目录下创建 `your_plugin.yaml`：

```yaml
info:
  description: 你的插件描述
  title: 你的插件名称
  version: v1
openapi: 3.0.1
paths:
  /your-endpoint:
    post:
      operationId: your_operation_id
      requestBody:
        content:
          application/json:
            schema:
              properties:
                input:
                  description: 输入参数
                  type: string
              required:
                - input
              type: object
        required: true
      responses:
        "200":
          content:
            application/json:
              schema:
                properties:
                  success:
                    type: boolean
                  data:
                    type: string
                type: object
          description: 成功响应
      summary: 你的 API 功能描述
servers:
  - url: https://your-api.com
```

### 步骤 3: 更新插件元数据

编辑 `backend/conf/plugin/pluginproduct/plugin_meta.yaml`，在文件开头添加：

```yaml
- plugin_id: 999  # 使用唯一的 ID
  product_id: 7999999999999999999
  deprecated: false
  version: v1.0.0
  openapi_doc_file: your_plugin.yaml
  plugin_type: 1
  manifest:
    schema_version: v1
    name_for_model: your_plugin_name
    name_for_human: 你的插件名称
    description_for_model: 给AI看的功能描述
    description_for_human: 给用户看的功能描述
    auth:
      type: none  # 或者配置你需要的认证方式
    logo_url: official_plugin_icon/plugin_your_plugin.png
    api:
      type: openapi
    common_params:
      body: []
      header:
        - name: User-Agent
          value: Coze/1.0
      path: []
      query: []
  tools:
    - tool_id: 99001  # 使用唯一的工具 ID
      deprecated: false
      method: post
      sub_url: /your-endpoint
```

### 步骤 4: 添加插件图标

创建或放置插件图标：

```bash
# 创建图标目录
mkdir -p backend/conf/plugin/pluginproduct/official_plugin_icon/

# 复制你的图标文件 (PNG 格式)
cp your-icon.png backend/conf/plugin/pluginproduct/official_plugin_icon/plugin_your_plugin.png
```

### 步骤 5: 测试插件

重启服务并测试：

```bash
# 重新构建并启动服务
make build_server
make server

# 或使用开发模式
make debug
```

## 常用插件模板

### 1. 简单数据查询插件

```yaml
# simple_query_plugin.yaml
info:
  description: 简单数据查询插件
  title: 数据查询
  version: v1
openapi: 3.0.1
paths:
  /query:
    get:
      operationId: query_data
      parameters:
        - description: 查询关键词
          in: query
          name: keyword
          required: true
          schema:
            type: string
      responses:
        "200":
          content:
            application/json:
              schema:
                properties:
                  results:
                    type: array
                    items:
                      type: object
                type: object
          description: 查询结果
      summary: 根据关键词查询数据
servers:
  - url: https://your-query-api.com
```

### 2. 数据处理插件

```yaml
# data_processor_plugin.yaml
info:
  description: 数据处理插件
  title: 数据处理器
  version: v1
openapi: 3.0.1
paths:
  /process:
    post:
      operationId: process_data
      requestBody:
        content:
          application/json:
            schema:
              properties:
                data:
                  description: 要处理的数据
                  type: array
                  items:
                    type: object
                options:
                  description: 处理选项
                  type: object
              required:
                - data
              type: object
      responses:
        "200":
          content:
            application/json:
              schema:
                properties:
                  processed_data:
                    type: array
                    items:
                      type: object
                  metadata:
                    type: object
                type: object
      summary: 处理输入数据
servers:
  - url: https://your-processor-api.com
```

### 3. 需要认证的插件

```yaml
# authenticated_plugin.yaml
info:
  description: 需要API密钥认证的插件
  title: 认证插件
  version: v1
openapi: 3.0.1
paths:
  /protected:
    post:
      operationId: protected_operation
      requestBody:
        content:
          application/json:
            schema:
              properties:
                message:
                  type: string
              required:
                - message
              type: object
      responses:
        "200":
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: string
                type: object
        "401":
          description: 认证失败
      summary: 受保护的操作
servers:
  - url: https://your-secure-api.com
```

对应的元数据配置：

```yaml
auth:
  type: service_http
  key: Authorization
  sub_type: token/api_key
  payload: '{"key": "Authorization", "service_token": "your-api-key", "location": "Header"}'
```

## 快速调试技巧

### 1. 验证配置文件

```bash
# 检查 YAML 语法
python3 -c "import yaml; print('Valid') if yaml.safe_load(open('your_plugin.yaml')) else print('Invalid')"

# 检查 JSON 格式
echo '{"test": "json"}' | jq .
```

### 2. 测试外部 API

```bash
# 模拟插件调用
curl -X POST "https://your-api.com/endpoint" \
     -H "Content-Type: application/json" \
     -H "User-Agent: Coze/1.0" \
     -d '{"input": "test"}'
```

### 3. 查看服务日志

```bash
# 实时查看插件日志
tail -f backend/logs/plugin.log | grep "your_plugin_id"

# 查看错误日志
tail -f backend/logs/error.log
```

## 常见错误及解决方案

### 错误 1: 插件 ID 冲突

```
Error: plugin_id already exists
```

**解决方案**: 使用唯一的 plugin_id 和 tool_id

### 错误 2: OpenAPI 文件找不到

```
Error: openapi_doc_file not found
```

**解决方案**: 检查文件路径和文件名是否正确

### 错误 3: 外部 API 调用失败

```
Error: failed to call external API
```

**解决方案**: 
1. 检查网络连接
2. 验证 API 端点 URL
3. 确认认证配置正确

## 下一步

完成第一个插件后，建议：

1. 阅读完整的 [插件开发指南](PLUGIN_DEVELOPMENT_GUIDE.md)
2. 研究现有插件的实现方式
3. 添加错误处理和边界情况
4. 优化性能和用户体验
5. 编写详细的插件文档

## 插件示例库

查看更多插件示例：

- [文档转换插件](../backend/conf/plugin/pluginproduct/document_converter.yaml) - 文档格式转换
- [图片压缩插件](../backend/conf/plugin/pluginproduct/image_compression.yaml) - 图片处理
- [搜索插件](../backend/conf/plugin/pluginproduct/bocha_search.yaml) - 网络搜索
- [飞书插件](../backend/conf/plugin/pluginproduct/lark_docx.yaml) - 第三方服务集成

通过学习这些示例，你可以更好地理解插件开发的最佳实践。