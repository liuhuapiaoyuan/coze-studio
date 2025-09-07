# 文档转换器插件示例

这是一个完整的文档转换器插件实现示例，展示了如何创建一个将 PDF、Word 文档转换为 Markdown 格式的 Coze Studio 插件。

## 功能特性

- 🔄 **文档转换**: 支持 PDF (.pdf) 和 Word (.doc, .docx) 文档转换为 Markdown
- 📝 **格式保留**: 保留文档结构、标题层级和表格格式
- 📊 **元数据提取**: 提取文档基本信息如文件大小、页数、字数等
- 🔒 **安全可靠**: 无需认证，直接调用外部转换服务
- ⚡ **高性能**: 支持大文件处理，合理的超时和错误处理

## 目录结构

```
document-converter/
├── README.md                    # 本文档
├── config/
│   ├── openapi.yaml            # OpenAPI 3.0.1 规范定义
│   └── plugin_meta.yaml        # 插件元数据配置
├── tests/
│   ├── test_api.py             # API 测试用例
│   └── test_integration.py     # 集成测试
└── docs/
    ├── api.md                  # API 文档
    └── usage.md                # 使用指南
```

## 快速开始

### 1. 部署插件配置

将配置文件复制到 Coze Studio 插件目录：

```bash
# 复制 OpenAPI 规范文件
cp config/document_converter.yaml backend/conf/plugin/pluginproduct/

# 更新插件元数据配置
# 将 plugin_meta.yaml 中的配置合并到主配置文件
```

### 2. 重启服务

```bash
# 重启 Coze Studio 服务
make server

# 或热重载插件配置
curl -X POST http://localhost:8080/admin/reload-plugins
```

### 3. 测试插件

```bash
# 使用 curl 测试
curl -X POST http://localhost:8080/api/plugin/invoke/document_converter/convert_document \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "outputFormat": "markdown",
    "preserveFormatting": true
  }'
```

## API 使用示例

### 基本转换请求

```json
{
  "fileUrl": "https://example.com/document.pdf",
  "outputFormat": "markdown",
  "preserveFormatting": true
}
```

### 成功响应示例

```json
{
  "success": true,
  "markdown": "# 文档标题\n\n这是转换后的 Markdown 内容...",
  "metadata": {
    "originalFileName": "document.pdf",
    "fileSize": 1048576,
    "pageCount": 10,
    "wordCount": 5000,
    "convertedAt": "2023-12-01T10:30:00Z"
  }
}
```

### 错误响应示例

```json
{
  "success": false,
  "error": "不支持的文件格式，请使用 PDF 或 Word 文档"
}
```

## 配置说明

### OpenAPI 规范特点

- **版本**: OpenAPI 3.0.1
- **请求方法**: POST
- **路径**: `/api/convert`
- **认证**: 无需认证
- **超时**: 默认 30 秒

### 插件元数据特点

- **插件 ID**: 1
- **工具 ID**: 10001
- **认证类型**: none
- **服务器**: `https://pdf.ggss.club`

## 开发指南

### 本地开发

1. **环境准备**
```bash
# 安装开发依赖
pip install pytest requests pyyaml jsonschema

# 启动本地测试环境
docker-compose up -d
```

2. **配置验证**
```bash
# 验证 OpenAPI 规范
swagger validate config/openapi.yaml

# 验证插件配置
python tests/test_config.py
```

3. **API 测试**
```bash
# 运行单元测试
pytest tests/test_api.py -v

# 运行集成测试
pytest tests/test_integration.py -v
```

### 扩展功能

可以通过修改配置文件来扩展功能：

1. **添加新的输出格式**
```yaml
properties:
  outputFormat:
    type: string
    enum: ["markdown", "html", "text", "json"]  # 新增格式
    default: "markdown"
```

2. **支持更多文件类型**
```yaml
properties:
  fileUrl:
    type: string
    format: uri
    description: 文档链接，支持 PDF、Word、PowerPoint、Excel 文档
```

3. **添加高级选项**
```yaml
properties:
  options:
    type: object
    properties:
      extractImages:
        type: boolean
        default: false
        description: 是否提取图片
      includeMetadata:
        type: boolean 
        default: true
        description: 是否包含元数据
      language:
        type: string
        enum: ["auto", "zh-CN", "en-US"]
        default: "auto"
        description: 文档语言
```

## 最佳实践

### 1. 错误处理

插件实现了完整的错误处理机制：

- **400**: 请求参数错误
- **422**: 文件处理错误  
- **500**: 服务器内部错误

### 2. 性能优化

- 设置合理的文件大小限制
- 实现请求超时控制
- 支持大文件的分块处理

### 3. 安全考虑

- 严格的 URL 格式验证
- 文件类型白名单检查
- 防止恶意文件上传

### 4. 监控指标

建议监控以下指标：

- 转换成功率
- 平均响应时间
- 错误分布
- 文件大小分布

## 故障排查

### 常见问题

1. **插件未加载**
```bash
# 检查配置文件语法
yq eval config/openapi.yaml

# 查看服务日志
tail -f /var/log/coze-studio.log | grep document_converter
```

2. **外部服务调用失败**
```bash
# 测试网络连通性
curl -I https://pdf.ggss.club/api/convert

# 检查 DNS 解析
nslookup pdf.ggss.club
```

3. **转换失败**
```bash
# 验证文件 URL 可访问性
curl -I "https://example.com/document.pdf"

# 检查文件格式
file document.pdf
```

## 社区贡献

欢迎为文档转换器插件贡献代码和改进建议：

1. 提交 Issue 报告问题
2. 提交 PR 改进功能
3. 完善文档和示例
4. 分享使用经验

## 许可证

本示例插件采用 Apache License 2.0 开源许可证。

---

这个示例展示了如何创建一个完整的 Coze Studio 插件，包含了从配置到部署的全部流程。您可以基于这个示例创建自己的插件。