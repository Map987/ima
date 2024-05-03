import os
import re
import requests
from urllib.parse import urljoin

# 网站主页URL
base_url = 'https://www.mappa.co.jp'
# 存储图片的目录
image_dir = 'downloaded_image'

# 如果目录不存在，则创建它
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# 获取网页内容
response = requests.get(base_url + '/works/')
web_content = response.text

# 使用正则表达式查找图片链接
# 匹配格式如 "https://www.mappa.co.jp/wp-content/uploads/2023/12/bkb_b2_kv_re6-814x1150.jpg"
image_pattern = re.compile(r'"thumb":"(https://www.mappa.co.jp/wp-content/uploads/[^\s"]+)"')

image_links = re.findall(image_pattern, web_content)

# 去重并处理链接
unique_image_links = set()
for link in image_links:
    # 移除链接中的分辨率部分
    clean_link = re.sub(r'(-\d+x\d+)\.jpg$', '.jpg', link)
    unique_image_links.add(clean_link)

# 下载图片
for link in unique_image_links:
    print(f"{link}")
    # 构建图片的本地文件路径
    file_name = os.path.join(image_dir, link.split('/')[-1])
    
    # 如果文件已经存在，则跳过下载
    if os.path.exists(file_name):
        continue
    
    # 下载图片
    with requests.get(link, stream=True) as r:
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
