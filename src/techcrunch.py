from crawl4ai import AsyncWebCrawler
from typing import List, Dict, Any
import json
import asyncio
from datetime import datetime

class TechCrunchCrawler:
    def __init__(self, verbose=True):
        self.verbose = verbose

    async def fetch_content(self, url, css_selector):
        """抓取单个页面内容"""
        async with AsyncWebCrawler(verbose=self.verbose) as crawler:
            result = await crawler.arun(
                url=url,
                css_selector=css_selector,
                magic=True,  # 启用所有反检测特性
                bypass_cache=True  # 绕过缓存获取最新内容
            )
            if result.success:
                print(f"成功抓取: {url}") if self.verbose else None
                return result
            else:
                print(f"抓取失败: {url}, 错误: {result.error_message}") if self.verbose else None
                return None
        
    async def crawl_list(self) -> List[Dict[str, Any]]:
        """返回符合API格式的文章列表"""
        url = "https://techcrunch.com/latest"
        results = []
        
        async with AsyncWebCrawler(verbose=self.verbose) as crawler:
            result = await crawler.arun(
                css_selector="ul.wp-block-post-template",
                url=url,
                magic=True,
                bypass_cache=True
            )
            
            if result.success:
                print(f"成功抓取: {url}") if self.verbose else None
                content = json.loads(result.extracted_content)
                
                for i in range(len(content)):
                    item = content[i]
                    # 查找包含标题的项（以###开头）
                    if item['content'].startswith('### '):
                        title_with_url = item['content'].replace('### ', '')
                        # 提取标题和URL
                        title = title_with_url[:title_with_url.find('(')].strip('[]')
                        url_start = title_with_url.find('(') + 1
                        url_end = title_with_url.find(')')
                        article_url = title_with_url[url_start:url_end]
                        
                        # 检查下一项是否包含时间信息
                        if i + 1 < len(content):
                            time_text = content[i + 1]['content']
                            # 检查是否包含min或hour
                            if 'min' in time_text or 'hour' in time_text:
                                results.append({
                                    "title": title.strip()[1:],
                                    "url": article_url
                                })
                
                return results
            else:
                print(f"抓取失败: {url}, 错误: {result.error_message}") if self.verbose else None
                return []

    async def crawl(self):
        article_list = await self.crawl_list()
        print(article_list)
        results = []
        
        # 并发抓取所有文章
        tasks = [self.fetch_content(article['url'], "div.entry-content") 
                for article in article_list]
        article_results = await asyncio.gather(*tasks)
        
        # 处理抓取结果
        for article, result in zip(article_list, article_results):
            try:
                if result and result.success:
                    article_data = json.loads(result.extracted_content)
                    # 过滤并拼接内容
                    content = "\n".join(
                        item["content"] for item in article_data 
                        if not item["content"].startswith("![") and  # 排除图片
                        not "Image Credits:" in item["content"] and  # 排除图片说明
                        not item["content"].strip().startswith("##") and  # 排除二级标题
                        item["content"].strip()  # 确保内容不为空
                    )
                    
                    results.append({
                        "title": article['title'],
                        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),  # 使用当前时间
                        "content": content.strip()
                    })
                else:
                    print(f"抓取文章失败: {article['url']}") if self.verbose else None
            except Exception as e:
                print(f"处理文章时出错 {article['url']}: {str(e)}") if self.verbose else None

        return results