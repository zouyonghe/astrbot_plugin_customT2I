# CustomT2I 插件

## 简介

`CustomT2I` 插件用于在 `astrbot` 中切换和管理自定义模板。通过该插件，用户可以轻松地切换到自定义的 T2I 模板，或者恢复到默认模板，提供了更高的灵活性与可配置性。

## 功能

- **切换到自定义模板**：通过 `enable` 命令，切换到预设的自定义模板。
- **恢复默认模板**：通过 `disable` 命令，恢复到默认的 T2I 模板。
- **查看当前模板**：通过 `status` 命令，查看当前使用的模板。

## 安装

1. 将 `CustomT2I` 插件文件添加到 `astrbot` 的插件目录下。
2. 确保插件的模板文件路径正确（`custom_base.html` 和 `base.html`）。
3. 配置插件参数和文件路径。

## 配置

- `enable_ct2i`: 配置是否启用自定义模板。

## 命令

- **`enable`**: 切换到自定义模板。
    - 示例：`!ct2i enable`
    - 成功后返回：`✅ 已切换到自定义模板`
- **`disable`**: 恢复默认模板。
    - 示例：`!ct2i disable`
    - 成功后返回：`✅ 已恢复默认模板`
- **`status`**: 查看当前使用的模板。
    - 示例：`!ct2i status`
    - 返回：`当前使用的模板: 自定义模板`
