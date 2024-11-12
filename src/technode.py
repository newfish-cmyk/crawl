from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import json
import asyncio
from datetime import datetime, timedelta

class TechNodeCrawler:
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

    async def crawl_list(self):
        url_array = [
            "https://cn.technode.com/latest/",
            "https://cn.technode.com/latest/page/2/"
        ]
        results = []
        
        # 并发抓取列表页
        tasks = [self.fetch_content(url, "div.row-container") for url in url_array]
        list_results = await asyncio.gather(*tasks)
        
        for result in list_results:
            if not result or not result.success:
                continue
                
            content = json.loads(result.extracted_content)
            
            # 从内容中提取文章信息
            for i in range(len(content)):
                item = content[i]
                if '###' not in item['content']:
                    continue
                    
                # 提取标题和URL
                title_with_url = item['content'].replace('### ', '')
                title = title_with_url[:title_with_url.find('(')].strip('[]') if '(' in title_with_url else title_with_url.strip('[]')
                title = title.strip()
                
                # 提取URL
                start = item['content'].find('(') + 1
                end = item['content'].find(')')
                if start <= 0 or end <= start:
                    continue
                    
                article_url = item['content'][start:end]
                
                # 提取日期
                if i + 1 >= len(content):
                    continue
                    
                date_item = content[i + 1]['content']
                date_start = date_item.find('[') + 1
                date_end = date_item.find(']')
                if date_start <= 0 or date_end <= date_start:
                    continue
                    
                date = date_item[date_start:date_end]
                
                # 判断日期是否在24小时内
                try:
                    article_date = datetime.strptime(date, '%Y/%m/%d %H:%M')
                    now = datetime.now()
                    if now - article_date <= timedelta(hours=16):
                        results.append({
                            'title': title,
                            'url': article_url,
                            'date': date
                        })
                except ValueError:
                    print(f"日期格式错误: {date}") if self.verbose else None
                    
        print(results)
        return results
        
    async def crawl(self):
        # 获取文章URL列表
        article_list = await self.crawl_list()
        results = []
        
        # 并发抓取所有文章
        tasks = [self.fetch_content(article['url'], "div.col-lg-8") 
                for article in article_list]
        article_results = await asyncio.gather(*tasks)
        
        # 处理抓取结果
        for article, result in zip(article_list, article_results):
            try:
                if result and result.success:
                    article_data = json.loads(result.extracted_content)
                    # 将数组中的内容连接成一个字符串，去掉最后一个元素
                    content = "\n".join(item["content"] for item in article_data[:-1])
                    results.append({
                        "title": article['title'],
                        "date": article['date'],
                        "content": content.strip()
                    })
                else:
                    print(f"抓取文章失败: {article['url']}") if self.verbose else None
            except Exception as e:
                print(f"处理文章时出错 {article['url']}: {str(e)}") if self.verbose else None

        return results