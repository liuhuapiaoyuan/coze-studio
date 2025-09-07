# Coze Studio 插件开发文档

欢迎来到 Coze Studio 插件开发文档！本文档集合提供了从入门到精通的完整插件开发指导。

## 📚 文档目录

### 🚀 快速开始
- **[快速入门指南](QUICK_START.md)** - 5分钟创建你的第一个插件
- **[插件开发指南](PLUGIN_DEVELOPMENT_GUIDE.md)** - 完整的插件开发教程

### 📋 模板文件
- **[OpenAPI 规范模板](templates/plugin_template.yaml)** - 标准的 OpenAPI 3.0.1 模板
- **[插件元数据模板](templates/plugin_meta_template.yaml)** - 插件配置模板

### 🛠️ 开发工具
- **[插件验证脚本](validate_plugin.py)** - 配置文件验证工具

### 💡 示例插件
在 `backend/conf/plugin/pluginproduct/` 目录中可以找到以下示例：
- **[文档转换器](../../backend/conf/plugin/pluginproduct/document_converter.yaml)** - PDF/Word 转 Markdown
- **[图片压缩](../../backend/conf/plugin/pluginproduct/image_compression.yaml)** - 图片处理示例
- **[搜索插件](../../backend/conf/plugin/pluginproduct/bocha_search.yaml)** - 网络搜索示例
- **[飞书云文档](../../backend/conf/plugin/pluginproduct/lark_docx.yaml)** - 第三方服务集成示例

---

## 🏗️ 插件架构概览

Coze Studio 插件系统基于以下核心组件：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Coze Studio   │────│   Plugin API    │────│  External API   │
│    Frontend     │    │    Gateway      │    │    Service      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
    用户交互界面            插件管理和调用          具体业务逻辑实现
```

### 插件类型
- **云端插件**: 调用外部 HTTP API 服务（推荐）
- **本地插件**: 在 Coze Studio 内部执行逻辑

### 核心特性
- ✅ 基于 OpenAPI 3.0.1 规范
- ✅ 支持多种认证方式（无认证、API Token、OAuth）
- ✅ 自动参数验证和错误处理
- ✅ 高并发和无状态设计
- ✅ 可视化配置界面

---

## 📖 开发流程

### 1. 准备阶段
1. 📋 确定插件功能需求
2. 🔧 准备外部 API 服务
3. 🖼️ 准备插件图标（64x64 或 128x128 PNG）

### 2. 开发阶段
1. 📝 编写 OpenAPI 规范文件
2. ⚙️ 配置插件元数据
3. 🧪 验证配置文件
4. 🔍 测试插件功能

### 3. 部署阶段
1. 📦 部署到开发环境
2. 🧪 完整功能测试
3. 🚀 生产环境发布
4. 📊 监控和维护

---

## 🛠️ 开发工具使用

### 配置验证
```bash
# 验证插件配置
python docs/plugins/validate_plugin.py your_plugin.yaml plugin_meta.yaml

# 检查 YAML 语法
python -c "import yaml; yaml.safe_load(open('your_plugin.yaml'))"
```

### API 测试
```bash
# 测试外部 API
curl -X POST "https://your-api.com/endpoint" \
     -H "Content-Type: application/json" \
     -H "User-Agent: Coze/1.0" \
     -d '{"param": "value"}'
```

### 开发环境启动
```bash
# 启动后端服务
make server

# 启动前端开发服务器
cd frontend/apps/coze-studio && npm run dev
```

---

## 🌟 最佳实践

### ✅ 设计原则
- **简单易用**: 最小化用户配置，提供合理默认值
- **错误友好**: 提供清晰的错误信息和处理建议
- **性能优化**: 支持并发访问，合理设置超时时间
- **安全考虑**: 验证所有输入，保护敏感信息

### ✅ API 设计
- **RESTful**: 遵循 REST API 设计原则
- **一致性**: 保持请求/响应格式一致
- **文档化**: 提供详细的参数说明和示例
- **版本控制**: 使用语义化版本号

### ✅ 配置管理
- **唯一性**: 确保 plugin_id 和 tool_id 全局唯一
- **可读性**: 使用有意义的名称和描述
- **可维护**: 定期更新和优化配置

---

## 🔧 常见问题解决

### Q: 插件无法加载？
**A:** 检查以下项目：
- YAML 语法是否正确
- plugin_id 是否唯一
- OpenAPI 文件路径是否正确
- 必需字段是否完整

### Q: API 调用失败？
**A:** 验证以下内容：
- 外部 API 服务是否可访问
- 请求格式是否符合 OpenAPI 规范
- 认证配置是否正确
- 超时设置是否合理

### Q: 响应格式错误？
**A:** 确保：
- JSON 格式符合定义
- 必需字段存在
- 数据类型匹配
- 错误处理完整

---

## 📞 获取帮助

### 社区支持
- **GitHub Issues**: [提交问题和建议](https://github.com/coze-dev/coze-studio/issues)
- **讨论区**: 参与社区讨论和经验分享

### 开发资源
- **OpenAPI 规范**: [OpenAPI 3.0 官方文档](https://spec.openapis.org/oas/v3.0.1)
- **YAML 语法**: [YAML 官方文档](https://yaml.org/spec/1.2.2/)
- **HTTP 状态码**: [MDN HTTP 状态码参考](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

### 在线工具
- **Swagger Editor**: [在线 OpenAPI 编辑器](https://editor.swagger.io/)
- **YAML Validator**: [在线 YAML 验证器](https://yamlchecker.com/)
- **JSON Formatter**: [JSON 格式化工具](https://jsonformatter.org/)

---

## 🚀 开始开发

准备好开始了吗？选择适合你的起点：

- 🆕 **初次开发**: 从 [快速入门指南](QUICK_START.md) 开始
- 📚 **深入学习**: 阅读 [完整开发指南](PLUGIN_DEVELOPMENT_GUIDE.md)
- 📋 **使用模板**: 复制 [插件模板](templates/) 快速开始
- 🔍 **参考示例**: 查看现有插件的实现方式

让我们一起构建强大的 Coze Studio 插件生态系统！ 🎉

---

## 📄 许可证

本文档和示例代码遵循与 Coze Studio 项目相同的 [Apache 2.0 许可证](../../LICENSE)。

---

*最后更新时间: 2024年1月*