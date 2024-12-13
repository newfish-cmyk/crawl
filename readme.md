## 🤖 简介

AI 日报机器人的数据源部分代码，需结合 Sealos Devbox 使用

详情可见 https://mp.weixin.qq.com/s/C3edt0mrQ6Ql1ggNltVa9w

## 🚀 运行

1. 创建 Devbox python 项目并连接
![open_devbox](https://oss.laf.dev/lk63dw-crawl/open_devbox.jpg)

2. git clone https://github.com/newfish-cmyk/crawl.git 或 连不上 GitHub 可以使用 wget https://oss.laf.dev/lk63dw-crawl/crawl-0.0.1.tar.gz
![wget](https://oss.laf.dev/lk63dw-crawl/commond.jpg)

3. 将 crawl 中的文件拖到根目录进行替换
![directory](https://oss.laf.dev/lk63dw-crawl/directory.jpg)

4. 执行 ./entrypoint.sh，等待依赖安装完成并启动
![entrypoint](https://oss.laf.dev/lk63dw-crawl/entrypoint.jpg)

5. 使用 Devbox 的公网地址进行测试，将 {{Devbox 公网地址}}/api/test 填入 http 节点，使用 get 方法
![link](https://oss.laf.dev/lk63dw-crawl/link.png)
![result](https://oss.laf.dev/lk63dw-crawl/result.jpg)
