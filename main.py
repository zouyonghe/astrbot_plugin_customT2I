import logging
import shutil

from astrbot.api.all import *

logger = logging.getLogger("astrbot")
current_directory = os.getcwd()

PLUGIN_CONFIG_PATH = "data/config/astrbot_plugin_customt2i_config.json"

@register("Custom_T2I", "buding", "自定义T2I模板插件", "0.0.2")
class CustomT2I(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.base_path = f"{current_directory}/astrbot/core/utils/t2i/template/base.html"
        self.custom_path = f"{current_directory}/data/plugins/astrbot_plugin_customt2i/custom_base.html"
        self.base_bak_path = f"{current_directory}/data/plugins/astrbot_plugin_customt2i/base.html"

    def save_plugin_config(self, file_path=PLUGIN_CONFIG_PATH):
        """
        保存插件配置到文件
        Args:
            file_path: 保存的配置文件路径
        """
        if not file_path:
            logger.error("插件配置文件路径不存在，保存失败。")
            return
        try:
            with open(file_path, "w", encoding="utf-8") as config_file:
                json.dump(self.config, config_file, indent=2, ensure_ascii=False)
            logger.info(f"插件配置已保存到文件: {file_path}")
        except Exception as e:
            logger.error(f"保存插件配置失败: {e}")

    def _replace_template(self, source_path: str, target_path: str, success_msg: str, error_msg: str) -> bool:
        """通用的模板替换方法"""
        if os.path.exists(source_path):
            shutil.copy(source_path, target_path)
            logger.info(success_msg)
            return True
        else:
            logger.error(error_msg)
            return False

    def _switch_to_custom_template(self):
        """切换到自定义模板"""
        return self._replace_template(self.custom_path, self.base_path, "已切换到自定义模板!",
                                      f"自定义模板文件不存在: {self.custom_path}")

    def _restore_default_template(self):
        """恢复默认模板"""
        return self._replace_template(self.base_bak_path, self.base_path, "已恢复默认模板!",
                                      f"备份模板文件不存在: {self.base_bak_path}")

    def _get_current_template(self) -> str:
        """查看当前使用的模板"""
        if self.config.get("enable_ct2i", False):
            return "自定义模版"
        else:
            return "默认模板"

    @command_group("ct2i")
    def ct2i(self):
        pass

    @ct2i.command("enable")
    async def enable_custom_T2I(self, event: AstrMessageEvent):
        """使用自定义模板"""
        try:
            if self._switch_to_custom_template():
                self.config["enable_ct2i"] = True
                self.save_plugin_config()
                yield event.plain_result("✅ 已切换到自定义模板")
            else:
                yield event.plain_result("❌ 切换自定义模板失败")
        except FileNotFoundError as e:
            logger.error(f"文件未找到: {e}")
            yield event.plain_result("❌ 文件未找到，请检查模板文件路径")
        except Exception as e:
            logger.error(f"未知错误: {e}")
            yield event.plain_result("❌ 切换自定义模板失败，请检查配置")

    @ct2i.command("disable")
    async def disable_custom_T2I(self, event: AstrMessageEvent):
        """恢复默认模板"""
        try:
            if self._restore_default_template():
                self.config["enable_ct2i"] = False
                self.save_plugin_config()
                yield event.plain_result("✅ 已恢复原始模板")
            else:
                yield event.plain_result("❌ 恢复原始模板失败")
        except FileNotFoundError as e:
            logger.error(f"文件未找到: {e}")
            yield event.plain_result("❌ 文件未找到，请检查模板文件路径")
        except Exception as e:
            logger.error(f"未知错误: {e}")
            yield event.plain_result("❌ 恢复原始模板失败，请检查配置")

    @ct2i.command("status")
    async def get_current_status(self, event: AstrMessageEvent):

        """查看当前使用的模板"""
        try:
            current_template = self._get_current_template()
            yield event.plain_result(f"当前使用的模板: {current_template}")
        except Exception as e:
            logger.error(f"获取当前模板失败: {e}")
            yield event.plain_result("❌ 获取当前模板失败")

    @ct2i.command("help")
    async def ct2i_help(self, event: AstrMessageEvent):
        """显示 ct2i 插件的帮助信息"""
        help_message = (
            "🚀 **自定义模板插件帮助**\n"
            "1. `/ct2i enable` - 切换到自定义模板。\n"
            "2. `/ct2i disable` - 恢复默认模板。\n"
            "3. `/ct2i status` - 查看当前使用的模板。"
        )
        try:
            yield event.plain_result(help_message)
        except Exception as e:
            logger.error(f"获取帮助信息失败: {e}")
            yield event.plain_result("❌ 获取帮助信息失败")