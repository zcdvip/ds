import time
import os
import requests
import re
import threading
from queue import Queue
import eventlet


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

urls = [
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hpamlhemh1YW5nIg%3D%3D",  #shijiazhuang 石家庄
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGFuZGFuIg%3D%3D",  # handan 邯郸
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYmFvZGluZyI%3D",  # baoding 保定
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0idGFuZ3NoYW4i",  # tangshan 唐山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGVuZ3NodWki",  # henghsui 衡水
   # "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieGluZ3RhaSI%3D",  # xingtai 邢台
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhhbmdqaWFrb3Ui",  # zhangjiakou 张家口
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2FuZ3pob3Ui",  # cangzhou 沧州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibGFuZ2Zhbmci",  # langfang 廊坊

]

results = []

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=15)
        page_content = response.text
        # 查找所有符合指定格式的网址
        pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
        urls_all = re.findall(pattern, page_content)
        # urls = list(set(urls_all))  # 去重得到唯一的URL列表
        urls = set(urls_all)  # 去重得到唯一的URL列表
        # 遍历网址列表，获取JSON文件并解析
        for url in urls:
            try:
                # 发送GET请求获取JSON文件，设置超时时间为0.5秒
                json_url = f'{url}/ZHGXTV/Public/json/live_interface.txt'
                response = requests.get(json_url, timeout=1)
                json_data = response.content.decode('utf-8')
                try:
                    # 按行分割数据
                    lines = json_data.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            name, channel_url = line.split(',',1)
                            urls = channel_url.split('/', 3)
                            url_data = json_url.split('/', 3)
                            if len(urls) >= 4:
                                urld = (f"{urls[0]}//{url_data[2]}/{urls[3]}")
                            else:
                                urld = (f"{urls[0]}//{url_data[2]}")
                            if name and urld:
                                # 删除特定文字
                                name = name.replace("cctv", "CCTV")
                                name = name.replace("中央", "CCTV")
                                name = name.replace("央视", "CCTV")
                                name = name.replace("高清", "")
                                name = name.replace("超高", "")
                                name = name.replace("HD", "")
                                name = name.replace("标清", "")
                                name = name.replace("频道", "")
                                name = name.replace("-", "")
                                name = name.replace(" ", "")
                                name = name.replace("PLUS", "+")
                                name = name.replace("＋", "+")
                                name = name.replace("(", "")
                                name = name.replace(")", "")
                                name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                                name = name.replace("CCTV1综合", "CCTV1")
                                name = name.replace("CCTV2财经", "CCTV2")
                                name = name.replace("CCTV3综艺", "CCTV3")
                                name = name.replace("CCTV4国际", "CCTV4")
                                name = name.replace("CCTV4中文国际", "CCTV4")
                                name = name.replace("CCTV4欧洲", "CCTV4")
                                name = name.replace("CCTV5体育", "CCTV5")
                                name = name.replace("CCTV6电影", "CCTV6")
                                name = name.replace("CCTV7军事", "CCTV7")
                                name = name.replace("CCTV7军农", "CCTV7")
                                name = name.replace("CCTV7农业", "CCTV7")
                                name = name.replace("CCTV7国防军事", "CCTV7")
                                name = name.replace("CCTV8电视剧", "CCTV8")
                                name = name.replace("CCTV9记录", "CCTV9")
                                name = name.replace("CCTV9纪录", "CCTV9")
                                name = name.replace("CCTV10科教", "CCTV10")
                                name = name.replace("CCTV11戏曲", "CCTV11")
                                name = name.replace("CCTV12社会与法", "CCTV12")
                                name = name.replace("CCTV12法制", "CCTV12")
                                name = name.replace("CCTV13新闻", "CCTV13")
                                name = name.replace("CCTV新闻", "CCTV13")
                                name = name.replace("CCTV14少儿", "CCTV14")
                                name = name.replace("CCTV15音乐", "CCTV15")
                                name = name.replace("CCTV16奥林匹克", "CCTV16")
                                name = name.replace("CCTV17农业农村", "CCTV17")
                                name = name.replace("CCTV17农业", "CCTV17")
                                name = name.replace("CCTV5+体育赛视", "CCTV5+")
                                name = name.replace("CCTV5+体育赛事", "CCTV5+")
                                name = name.replace("CCTV5+体育", "CCTV5+")
                                name = name.replace("河北少儿科教", "河北少儿")
                                if "udp://" not in urld:
                                    results.append(f"{name},{urld}")
                except:
                    continue
            except:
                continue
    except:
        continue

results = set(results)   # 去重得到唯一的URL列表
results = sorted(results)
with open("itv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")

channels = []

for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',',1)
        channels.append((channel_name, channel_url))


eventlet.monkey_patch()

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []
error_channels = []

# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            response = requests.get(channel_url, timeout=1)
            if response.status_code == 200:
                channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
                lines = requests.get(channel_url,timeout=1).text.strip().split('\n')  # 获取m3u8文件内容
                ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
                file_size = 0
                start_time = time.time()
                # 多获取的视频数据进行20秒钟限制
                with eventlet.Timeout(10, False):
                    for i in range(len(ts_lists)):
                        ts_url = channel_url_t + ts_lists[i]  # 拼接单个视频片段下载链接
                        response = requests.get(ts_url, stream=True, timeout=1)
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file_size += len(chunk)
                        response.close()
                end_time = time.time()
                response_time = end_time - start_time
                download_speed = file_size / response_time / 1024
                normalized_speed =download_speed / 1024  # 将速率从kB/s转换为MB/s
                ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接
                if normalized_speed >= 0.1:
                    result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                    results.append(result)
                    numberx = (len(results) + len(error_channels)) / len(channels) * 100
                    #print(f"可用频道：{len(results)} , 网速：{normalized_speed:.3f} MB/s , 分辨率：{width}X{height}, 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
                    print(f"可用频道：{len(results)} , 网速：{normalized_speed:.3f} MB/s ,不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
                else:
                    error_channel = channel_name, channel_url
                    error_channels.append(error_channel)
                    numberx = (len(results) + len(error_channels)) / len(channels) * 100
                    print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} , 网速：{normalized_speed:.3f} MB/s , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channel = channel_name, channel_url
                error_channels.append(error_channel)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(
                    f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 10
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)  # 将工作线程设置为守护线程
    t.start()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))

# 将结果写入文件
with open("itv_results.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url},{speed}\n")

result_counter = 8  # 每个频道需要的个数

with open("ds.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('河北频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '河北' in channel_name or '石家庄' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

    channel_counters = {}
    file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name and '河北' not in channel_name and '石家庄' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
