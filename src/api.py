from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import asyncio
from src.technode import TechNodeCrawler
from src.techcrunch import TechCrunchCrawler
from src.kr36 import Kr36Crawler
from src.fxqcankao import FxqCankaoCrawler

app = FastAPI(
    title="Tech News API",
    description="API for crawling tech news",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """健康检查接口"""
    return {"status": "ok"}

@app.get("/api/technode", response_model=List[Dict[str, Any]])
async def get_technode():
    try:
        crawler = TechNodeCrawler(verbose=True)
        results = await asyncio.wait_for(crawler.crawl(), timeout=600.0)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/techcrunch", response_model=List[Dict[str, Any]])
async def get_techcrunch():
    try:
        crawler = TechCrunchCrawler(verbose=True)
        results = await asyncio.wait_for(crawler.crawl(), timeout=600.0)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kr36", response_model=List[Dict[str, Any]])
async def get_kr36():
    try:
        crawler = Kr36Crawler(verbose=True)
        results = await asyncio.wait_for(crawler.crawl(), timeout=600.0)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/fxqcankao", response_model=List[Dict[str, Any]])
async def get_fxqcankao():
    try:
        crawler = FxqCankaoCrawler(verbose=True)
        results = await asyncio.wait_for(crawler.crawl(), timeout=600.0)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))