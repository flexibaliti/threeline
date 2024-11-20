import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
import time

def fetch_baidu_results():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 搜索关键词
    keywords = ['三线工程 历史', '三线工程 影响', '三线工程 建设']
    results = []
    
    for keyword in keywords:
        encoded_keyword = quote(keyword)
        url = f'https://www.baidu.com/s?wd={encoded_keyword}'
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取搜索结果
            search_results = soup.find_all('div', class_='result')
            
            for result in search_results:
                title = result.find('h3')
                link = title.find('a')['href'] if title and title.find('a') else ''
                snippet = result.find('div', class_='c-abstract')
                
                if title and snippet:
                    results.append({
                        'title': title.get_text(),
                        'url': link,
                        'snippet': snippet.get_text()
                    })
            
            # 避免请求过于频繁
            time.sleep(2)
            
        except Exception as e:
            print(f"Error fetching results for {keyword}: {str(e)}")
    
    # 保存结果到文件
    with open('search_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

if __name__ == "__main__":
    results = fetch_baidu_results()
    print(f"获取到 {len(results)} 条搜索结果") 