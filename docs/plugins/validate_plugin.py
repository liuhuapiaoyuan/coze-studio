#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coze Studio 插件配置验证工具

此脚本用于验证插件配置文件的正确性，包括：
- YAML 语法检查
- 必需字段验证
- ID 唯一性检查
- OpenAPI 规范验证
- 文件存在性检查

使用方法:
    python validate_plugin.py [plugin_openapi.yaml] [plugin_meta.yaml]
"""

import sys
import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class PluginValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_yaml_syntax(self, file_path: str) -> Optional[Dict]:
        """验证 YAML 文件语法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data
        except yaml.YAMLError as e:
            self.errors.append(f"YAML 语法错误 in {file_path}: {str(e)}")
            return None
        except FileNotFoundError:
            self.errors.append(f"文件不存在: {file_path}")
            return None
        except Exception as e:
            self.errors.append(f"读取文件失败 {file_path}: {str(e)}")
            return None
    
    def validate_openapi_spec(self, openapi_data: Dict, file_path: str) -> bool:
        """验证 OpenAPI 规范"""
        if not openapi_data:
            return False
            
        # 检查必需字段
        required_fields = ['openapi', 'info', 'paths']
        for field in required_fields:
            if field not in openapi_data:
                self.errors.append(f"OpenAPI 缺少必需字段 '{field}' in {file_path}")
        
        # 检查 OpenAPI 版本
        if 'openapi' in openapi_data:
            version = openapi_data['openapi']
            if not version.startswith('3.0'):
                self.warnings.append(f"建议使用 OpenAPI 3.0.x 版本，当前: {version}")
        
        # 检查 info 部分
        if 'info' in openapi_data:
            info = openapi_data['info']
            info_required = ['title', 'version', 'description']
            for field in info_required:
                if field not in info:
                    self.errors.append(f"OpenAPI info 缺少必需字段 '{field}' in {file_path}")
        
        # 检查 paths 部分
        if 'paths' in openapi_data:
            paths = openapi_data['paths']
            if not paths:
                self.warnings.append(f"OpenAPI paths 为空 in {file_path}")
            
            for path, methods in paths.items():
                if not isinstance(methods, dict):
                    continue
                    
                for method, operation in methods.items():
                    if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                        continue
                    
                    # 检查 operationId
                    if 'operationId' not in operation:
                        self.errors.append(f"缺少 operationId in {path} {method}")
                    
                    # 检查响应定义
                    if 'responses' not in operation:
                        self.errors.append(f"缺少 responses in {path} {method}")
                    else:
                        responses = operation['responses']
                        if '200' not in responses and 'default' not in responses:
                            self.warnings.append(f"建议定义 200 响应 in {path} {method}")
        
        # 检查 servers 部分
        if 'servers' not in openapi_data or not openapi_data['servers']:
            self.errors.append(f"OpenAPI 缺少 servers 配置 in {file_path}")
        
        return len(self.errors) == 0
    
    def validate_plugin_meta(self, meta_data: List[Dict], file_path: str) -> bool:
        """验证插件元数据配置"""
        if not meta_data or not isinstance(meta_data, list):
            self.errors.append(f"插件元数据必须是数组格式 in {file_path}")
            return False
        
        plugin_ids = set()
        tool_ids = set()
        
        for i, plugin in enumerate(meta_data):
            plugin_prefix = f"插件 #{i} in {file_path}"
            
            # 检查必需字段
            required_fields = [
                'plugin_id', 'product_id', 'version', 'openapi_doc_file',
                'plugin_type', 'manifest', 'tools'
            ]
            
            for field in required_fields:
                if field not in plugin:
                    self.errors.append(f"{plugin_prefix}: 缺少必需字段 '{field}'")
            
            # 检查 plugin_id 唯一性
            if 'plugin_id' in plugin:
                plugin_id = plugin['plugin_id']
                if plugin_id in plugin_ids:
                    self.errors.append(f"{plugin_prefix}: plugin_id {plugin_id} 重复")
                else:
                    plugin_ids.add(plugin_id)
            
            # 检查 manifest 结构
            if 'manifest' in plugin:
                manifest = plugin['manifest']
                manifest_required = [
                    'schema_version', 'name_for_model', 'name_for_human',
                    'description_for_model', 'description_for_human',
                    'auth', 'logo_url', 'api'
                ]
                
                for field in manifest_required:
                    if field not in manifest:
                        self.errors.append(f"{plugin_prefix}: manifest 缺少必需字段 '{field}'")
                
                # 检查认证配置
                if 'auth' in manifest and 'type' not in manifest['auth']:
                    self.errors.append(f"{plugin_prefix}: auth 缺少 type 字段")
            
            # 检查工具配置
            if 'tools' in plugin:
                tools = plugin['tools']
                if not tools or not isinstance(tools, list):
                    self.warnings.append(f"{plugin_prefix}: 没有定义任何工具")
                else:
                    for j, tool in enumerate(tools):
                        tool_prefix = f"{plugin_prefix}, 工具 #{j}"
                        
                        # 检查工具必需字段
                        tool_required = ['tool_id', 'method', 'sub_url']
                        for field in tool_required:
                            if field not in tool:
                                self.errors.append(f"{tool_prefix}: 缺少必需字段 '{field}'")
                        
                        # 检查 tool_id 唯一性
                        if 'tool_id' in tool:
                            tool_id = tool['tool_id']
                            if tool_id in tool_ids:
                                self.errors.append(f"{tool_prefix}: tool_id {tool_id} 重复")
                            else:
                                tool_ids.add(tool_id)
                        
                        # 检查 HTTP 方法
                        if 'method' in tool:
                            method = tool['method'].lower()
                            if method not in ['get', 'post', 'put', 'delete', 'patch']:
                                self.errors.append(f"{tool_prefix}: 不支持的 HTTP 方法 '{method}'")
        
        return True
    
    def validate_file_references(self, meta_data: List[Dict], base_dir: str) -> bool:
        """验证文件引用是否存在"""
        base_path = Path(base_dir)
        
        for i, plugin in enumerate(meta_data):
            plugin_prefix = f"插件 #{i}"
            
            # 检查 OpenAPI 文件
            if 'openapi_doc_file' in plugin:
                openapi_file = base_path / plugin['openapi_doc_file']
                if not openapi_file.exists():
                    self.errors.append(f"{plugin_prefix}: OpenAPI 文件不存在: {openapi_file}")
            
            # 检查图标文件
            if 'manifest' in plugin and 'logo_url' in plugin['manifest']:
                logo_path = base_path / plugin['manifest']['logo_url']
                if not logo_path.exists():
                    self.warnings.append(f"{plugin_prefix}: 图标文件不存在: {logo_path}")
        
        return True
    
    def validate_consistency(self, openapi_data: Dict, meta_data: List[Dict]) -> bool:
        """验证 OpenAPI 和元数据的一致性"""
        if not openapi_data or not meta_data:
            return True
        
        # 提取 OpenAPI 中的路径
        openapi_paths = set()
        if 'paths' in openapi_data:
            for path, methods in openapi_data['paths'].items():
                for method in methods.keys():
                    if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                        openapi_paths.add((method.lower(), path))
        
        # 检查元数据中的工具是否在 OpenAPI 中定义
        for plugin in meta_data:
            if 'tools' in plugin:
                for tool in plugin['tools']:
                    if 'method' in tool and 'sub_url' in tool:
                        method = tool['method'].lower()
                        sub_url = tool['sub_url']
                        
                        if (method, sub_url) not in openapi_paths:
                            self.warnings.append(
                                f"工具 {method.upper()} {sub_url} 在元数据中定义但在 OpenAPI 中未找到"
                            )
        
        return True
    
    def validate_plugin(self, openapi_file: str, meta_file: str) -> bool:
        """验证完整的插件配置"""
        print(f"🔍 验证插件配置...")
        print(f"   OpenAPI 文件: {openapi_file}")
        print(f"   元数据文件: {meta_file}")
        print()
        
        # 验证 OpenAPI 文件
        openapi_data = self.validate_yaml_syntax(openapi_file)
        if openapi_data:
            self.validate_openapi_spec(openapi_data, openapi_file)
        
        # 验证元数据文件
        meta_data = self.validate_yaml_syntax(meta_file)
        if meta_data:
            self.validate_plugin_meta(meta_data, meta_file)
            
            # 验证文件引用
            base_dir = os.path.dirname(meta_file)
            self.validate_file_references(meta_data, base_dir)
        
        # 验证一致性
        if openapi_data and meta_data:
            self.validate_consistency(openapi_data, meta_data)
        
        return len(self.errors) == 0
    
    def print_results(self) -> bool:
        """打印验证结果"""
        if self.errors:
            print("❌ 验证失败，发现以下错误:")
            for error in self.errors:
                print(f"   • {error}")
            print()
        
        if self.warnings:
            print("⚠️  警告信息:")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ 插件配置验证通过！")
            return True
        elif not self.errors:
            print("✅ 插件配置基本正确，但有一些警告需要注意。")
            return True
        else:
            print(f"❌ 发现 {len(self.errors)} 个错误，请修复后重新验证。")
            return False

def main():
    if len(sys.argv) < 3:
        print("用法: python validate_plugin.py <openapi_file.yaml> <plugin_meta.yaml>")
        print()
        print("示例:")
        print("  python validate_plugin.py document_converter.yaml plugin_meta.yaml")
        sys.exit(1)
    
    openapi_file = sys.argv[1]
    meta_file = sys.argv[2]
    
    validator = PluginValidator()
    success = validator.validate_plugin(openapi_file, meta_file)
    validator.print_results()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()