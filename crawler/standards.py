import time
from duckduckgo_search import DDGS
from utils.filter import match, STANDARD_PATTERNS

def _fetch_patterns_from_ddg():
    results = []
    
    # 每次搜尋 3 個標籤，避免搜尋字串過長影響精準度
    chunk_size = 3
    
    with DDGS() as ddgs:
        for i in range(0, len(STANDARD_PATTERNS), chunk_size):
            chunk = STANDARD_PATTERNS[i:i + chunk_size]
            
            # 建構搜尋語句: "Pattern 1" OR "Pattern 2"
            quoted_terms = [f'"{term}"' for term in chunk]
            query = " OR ".join(quoted_terms)
            
            print(f"Fetching DuckDuckGo for tags: {chunk}")
            
            try:
                # timelimit="y" 代表搜尋過去一年內的結果，剛好涵蓋你想要的歷史範圍
                # max_results=15 代表我們只看這組搜尋結果的前 15 筆（最相關的）
                ddgs_results = ddgs.text(query, timelimit="y", max_results=15)
                
                if not ddgs_results:
                    continue
                    
                for r in ddgs_results:
                    title = r.get('title', '')
                    url = r.get('href', '')
                    body = r.get('body', '')
                    
                    # 將標題與摘要合併，交給你的過濾器判斷是否真的有命中標籤
                    text = f"{title} {body}"
                    matched = match(text)
                    
                    if not matched:
                        continue
                        
                    results.append({
                        "title": title,
                        "url": url,
                        "source": "DuckDuckGo Web Search",
                        "summary": body,
                        "matched": matched,
                        "force_send": False,
                        "is_official": False,
                    })
            except Exception as e:
                print(f"Error fetching {query}: {e}")
                
            # 每次搜尋後暫停 2 秒，避免被 DuckDuckGo 當作惡意攻擊而封鎖
            time.sleep(2)
            
    return results

def fetch_standards():
    """Fetch recent standard updates using global search engine."""
    print("Fetching standards updates from DuckDuckGo...")
    return _fetch_patterns_from_ddg()
