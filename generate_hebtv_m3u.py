import requests
import re
import json

def get_m3u8_url():
    url = "https://www.hebtv.com/19/19js/st/xdszb/index.shtml?index=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # 方法1：正则匹配m3u8链接
        m3u8_patterns = [
            r'(https?://[^\s<>"\']+\.m3u8[^\s<>"\']*)',
            r'src\s*:\s*["\']([^"\']+\.m3u8)["\']',
            r'url\s*["\']?([^"\'\s]+\.m3u8)'
        ]
        
        for pattern in m3u8_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        # 方法2：查找JSON配置
        json_pattern = r'var\s+config\s*=\s*(\{.*?\});'
        json_match = re.search(json_pattern, response.text, re.DOTALL)
        if json_match:
            try:
                config = json.loads(json_match.group(1))
                # 根据实际JSON结构提取
                if 'url' in config or 'm3u8' in config:
                    return config.get('url') or config.get('m3u8')
            except:
                pass
        
        # 方法3：检查iframe或脚本
        iframe_pattern = r'<iframe[^>]+src=["\']([^"\']+)["\']'
        iframe_match = re.search(iframe_pattern, response.text)
        if iframe_match:
            return iframe_match.group(1)
            
    except Exception as e:
        print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    m3u8_url = get_m3u8_url()
    if m3u8_url:
        print(f"Found m3u8: {m3u8_url}")
        # 保存到文件
        with open('playlist.m3u8', 'w') as f:
            f.write('#EXTM3U\n')
            f.write(f'#EXTINF:-1,河北卫视\n')
            f.write(f'{m3u8_url}\n')
    else:
        print("No m3u8 found")
