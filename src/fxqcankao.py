from crawl4ai import AsyncWebCrawler
from typing import List, Dict, Any
import json
from datetime import datetime
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

class FxqCankaoCrawler:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.url = "https://rss.icloudnative.io/telegram/channel/xhqcankao"

    async def get_strategy(self):
        schema = {
            "name": "fxq参考消息",
            "baseSelector": "item",
            "isList": True,
            "fields": [
                {
                    "name": "title",
                    "selector": "title",
                    "type": "text",
                },
                {
                    "name": "date",
                    "selector": "pubDate",
                    "type": "text",
                },
                {
                    "name": "content",
                    "selector": "description",
                    "type": "text",  
                },
            ],
        }
        return JsonCssExtractionStrategy(schema, verbose=True)
        
    async def crawl(self) -> List[Dict[str, Any]]:
        """抓取参考消息内容"""
        results = []
        
        async with AsyncWebCrawler(verbose=self.verbose) as crawler:
            result = await crawler.arun(
                url=self.url,
                magic=True,
                bypass_cache=True,
                extraction_strategy=await self.get_strategy()
            )
            
            if result.success:
                print(f"成功抓取: {self.url}") if self.verbose else None
                content = json.loads(result.extracted_content)
                
                print(content)
                for item in content:
                    try:
                        # 确保内容不为空且不是图片
                        if (item['content'].strip() and 
                            not item['content'].startswith('![') and
                            not item['content'].startswith('#')):
                            
                            results.append({
                                "title": item['title'].strip(),
                                "date": item['date'].strip(),
                                "content": item['content'].strip()
                            })
                    except Exception as e:
                        print(f"处理内容时出错: {str(e)}") if self.verbose else None
                
                return results
            else:
                print(f"抓取失败: {self.url}, 错误: {result.error_message}") if self.verbose else None
                return []