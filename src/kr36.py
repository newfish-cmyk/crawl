from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import json
import asyncio

class Kr36Crawler:
    def __init__(self, verbose=True):
        self.verbose = verbose

    async def get_strategy(self):
        schema = {
            "name": "36Kr News Article",
            "baseSelector": "div.article-wrapper",
            "fields": [
                {
                    "name": "title",
                    "selector": "h1",
                    "type": "text",
                },
                {
                    "name": "date",
                    "selector": "div.article-title-icon > span.item-time",
                    "type": "text",
                },
                {
                    "name": "content",
                    "selector": "div.articleDetailContent",
                    "type": "text",  
                },
            ],
        }
        return JsonCssExtractionStrategy(schema, verbose=True)
        

    async def crawl_list(self):
        url = "https://www.36kr.com/information/technology/"
        all_articles = []
        
        # 点击加载更多按钮的JS
        js_load_more = """
        (async () => {
            for(let i=0; i<1; i++) {
                const button = document.querySelector('div.kr-loading-more-button');
                if(button) {
                    button.click();
                    await new Promise(r => setTimeout(r, 2000)); // 等待加载
                }
            }
        })();
        """
        
        async with AsyncWebCrawler(verbose=self.verbose) as crawler:
            # 修复lambda函数,添加参数
            crawler.crawler_strategy.set_hook('on_execution_started', lambda _: print("开始抓取页面"))
            
            # 先执行加载更多,然后一次性抓取所有内容
            result = await crawler.arun(
                url=url,
                css_selector="div.kr-information-flow",
                js=js_load_more,
                magic=True,  
                bypass_cache=True
            )
            
            if not result.success:
                print("抓取页面失败")
                return []

            content = json.loads(result.extracted_content)
            article_list = []
            
            i = 0
            while i < len(content):
                item = content[i]
                item_content = item.get('content', '')
                
                # 检查是否是标题格式 (包含[...]和/p/...)
                if item_content.startswith('[') and '/p/' in item_content:
                    title = item_content[1:item_content.find('](/p/')]
                    url_part = item_content[item_content.find('/p/'):-1]
                    full_url = f"https://www.36kr.com{url_part}"
                    
                    # 寻找时间信息
                    time_found = False
                    for j in range(i + 1, min(i + 4, len(content))):  # 向后最多查找3条
                        time_content = content[j].get('content', '')
                        if '前' in time_content:
                            time_found = True
                            if i % 4 == 1:
                                article_list.append({
                                    'title': title,
                                    'url': full_url
                                })
                            break
                i += 1        
        print(article_list)
        return article_list

    async def crawl(self):
        strategy = await self.get_strategy()
        article_list = await self.crawl_list()
        results = []
        
        # 并发抓取所有文章
        async with AsyncWebCrawler(verbose=self.verbose) as crawler:
            tasks = [crawler.arun(
                url=article['url'],
                extraction_strategy=strategy,
                bypass_cache=True
            # ) for article in [{"url": "https://www.36kr.com/p/3020867926877702"}]]
            ) for article in article_list]
            
            article_results = await asyncio.gather(*tasks)
            
            # 处理抓取结果
            for article, result in zip(article_list, article_results):
            # for article, result in zip([{"url": "https://www.36kr.com/p/3020867926877702"}], article_results):
                if result and result.success:
                    article_data = json.loads(result.extracted_content)
                    # article_data 是一个列表,取第一个元素
                    if article_data and len(article_data) > 0:
                        article_item = article_data[0]
                        results.append({
                            "title": article_item.get("title", ""),
                            "date": article_item.get("date", ""), 
                            "content": article_item.get("content", "")
                        })
                else:
                    print(f"抓取文章失败: {article['url']}") if self.verbose else None

        return results
        
