#!/bin/bash
python3 -m venv myenv  # 创建虚拟环境
source myenv/bin/activate  # 激活虚拟环境

pip install -r requirements.txt # 安装依赖

playwright install # 安装 Playwright 所需的浏览器
playwright install-deps # 安装 Playwright 所需的依赖

python3 -m main # 运行主程序