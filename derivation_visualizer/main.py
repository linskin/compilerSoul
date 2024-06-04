import threading

from compress_grammar import GrammarCleaner
from extract_grammar import GrammaticalQuadrupleExtraction
from grammar_derivation_visualizer_window import GrammarDerivationVisualizer
from output_window import MyOutputWindow
from tools.banner import banner_str, banner_str_welcome
from data.grammar import grammar_str6, grammar_str9, grammar_str8, grammar_str1


def solve():
    print(banner_str, '\n', banner_str_welcome)
    # 数据初始化
    grammar_string = grammar_str1

    extractor = GrammaticalQuadrupleExtraction()
    terminators, non_terminators, production, start = extractor.extract_grammar_components(grammar_string)
    cleaner = GrammarCleaner()
    cleaned_production = cleaner.auto_clean(production, start, terminators)
    # 实例化两个窗口类
    window1 = MyOutputWindow(grammar_string=grammar_string)
    window2 = GrammarDerivationVisualizer(cleaned_production, start)

    # 创建并启动线程
    thread1 = threading.Thread(target=window1.run())
    thread2 = threading.Thread(target=window2.run())
    thread1.start()
    thread2.start()


if __name__ == '__main__':
    solve()

# 这个错误通常意味着在运行某个程序时，它试图加载一个名为 `icudtl1.dat` 的数据文件，但是该文件在指定的路径下不存在。
#
# 这个文件通常是与国际化（International Components for Unicode，ICU）相关的，用于 Unicode
# 字符处理。大多数情况下，这个文件应该是在安装或配置过程中被正确地安装和设置的。但有时可能会出现文件丢失或路径配置错误的情况。
#
# 要解决这个问题，你可以尝试以下几个步骤：
#
# 1. **检查文件路径和权限：** 确保 `C:\Users\lenovo\.conda\envs\env\icudtl1.dat` 这个路径是正确的，并且你有权限访问该文件。
#
# 2. **重新安装或更新程序：** 如果可能的话，尝试重新安装或更新程序，以确保所有依赖文件都正确安装和配置。
#
# 3. **检查环境变量和配置：** 确保程序的配置正确，特别是与文件路径相关的配置，例如环境变量或配置文件。
#
# 4. **尝试手动安装：** 如果可能的话，尝试手动安装缺失的文件。你可以从官方源或其他可信赖的来源获取该文件，并将其放置到正确的路径下。
#
# 如果以上方法都没有解决问题，可能需要进一步的调查和诊断。你可能需要查看程序的文档或与开发者或社区寻求帮助，以获得更多指导和支持。
