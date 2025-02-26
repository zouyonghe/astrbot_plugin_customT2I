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

    @command("test1")
    async def test1(self, event: AstrMessageEvent):
        yield event.plain_result("《哈利·波特与魔法石》： 　　一岁的哈利·波特失去父母后，神秘地出现在姨父姨妈家的门前。哈利在姨父家饱受欺凌，度过十年极其痛苦的日子。姨父和姨妈好似凶神恶煞，他们那混世魔王儿子达力——一个肥胖、娇惯、欺负人的大块头，更是经济对哈利拳脚相加。哈利的“房间”是位于楼梯口的一个又暗又小的碗橱。十年来，从来没有人为他过过生日。 　　《哈利·波特与密室》： 　　哈利·波特在霍格沃茨魔法学校学习一年之后，暑假开始了。他在姨父姨妈家熬过痛苦的假期。正当他准备打点行装去学校时，小精灵多比前来发出警告：如果哈利返回霍格沃茨，灾难将会临头。 　　《哈利·波特与凤凰社》： 　　神奇小子哈利.波特再掀狂潮，这次带领全球“哈利迷”去到的是一个更为神秘诡异的世界：身怀绝技的小哈利在更为强大的敌人面前大展身手，魔法与信心一体，机智共勇气并存，而更值得关注的是，我们的小哈利长大了，一群天真可爱的小女孩出现在他身边…… 哈利意外遭到摄魂怪袭击，邓布利多校长被赶下台，魔法部新官员打伤了麦格教授，一切都糟糕得不能再糟糕了，而这些，都还只是开头，哈利与凤凰社成员们担负起对抗日益强大的伏地魔的重任…… 　　《哈利·波特与混血王子》： 　　本书是“哈利·波特”系列的第六集，据说开篇情节罗琳已经酝酿了13年，讲的是哈利·波特在霍格沃茨魔法学校第六年的生活。承接前五集的精彩情节，哈利·波特将再次经历一场惊心动魄、险象环生的魔法旅途。这一生中，邪恶之王沃尔德莫德的“力量和鲜花都在日益增长”，伏地魔的力量日益增加，正义与邪恶之战一触即发…… 　　罗琳的小说“继承了最好的惊险小说传统，从来不让任何场景拉长到让人沉闷的地步，而且基本场景很适合天马行空的魔法世界”。可以说，罗琳创造的幻想世界令人为之疯狂，并以幽默的方式玩着智慧的游戏。 　　《哈利·波特与火焰杯》： 　　6月1日对孩子们而言无疑是一个重大的日子，而2001年的6月1日，更是非同凡响，因为这一天，孩子们翘首以待多日的儿童故事书《哈里·波特》第四集面市了！哈利注定永远都不可能平平常常，即使拿魔法界的标准来衡量。黑魔的阴影始终挥之不去，种种暗藏杀机的神秘事件将他一步步推向了伏地魔的魔爪。他渴望在百年不遇的三强争霸赛中战胜自我，完成三个惊险艰巨的魔法项目，谁知整个竞赛竟是一个天大的阴谋…… 　　《哈利·波特与阿兹卡班的囚徒》： 　　哈利·波特在霍格沃茨魔法学校已经度过了不平凡的两年，而且早已听说魔法世界中有一座守备森严的阿兹卡班监狱，里面关押着一个臭名昭著的囚徒，名字叫小天狼星布莱克。传言布莱克是“黑魔法”高手伏地魔——杀害哈利父母的凶手——的忠实信徒，曾经用一句魔咒接连结束了十三条性命…… 　　《哈利·波特与死亡圣器》： 　　哈利·波特十年历程完美谢幕，死亡圣器终揭神秘面纱——哈利·波特与死亡圣器，全球哈迷最后的狂欢。 　　《哈利·波特与死亡圣器》是“哈利·波特”系列的第七集，也是最后一集。十年前，J.K.罗琳创造了一个令人为之疯狂的幻想世界，并以幽默的方式玩着智慧的游戏；十年后，这列奇幻列车终于开到最后一站，许多有关哈利·波特的谜团正在一一解开，每个人静静迎接着自己的宿命。")

    @command("test2")
    async def test2(self, event: AstrMessageEvent):
        yield event.image_result("")