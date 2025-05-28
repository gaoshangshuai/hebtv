import time
import hashlib

current_t = int(time.time())
salt = "hebtv"
data = f"{current_t}{salt}".encode()
k = hashlib.md5(data).hexdigest()

url = f"https://tv.pull.hebtv.com/jishi/weishipindao.m3u8?t={current_t}&k={k}"

with open("hebtv.m3u", "w") as f:
    f.write("#EXTM3U\n#EXTINF:-1,河北卫视\n" + url)
