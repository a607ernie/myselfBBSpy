import os
import requests
import m3u8
import subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from dotenv import dotenv_values
import shutil
from tqdm import tqdm

class AnimeDownloader:
    def __init__(self,cfg,tmp_path,m3u8_url,output_file):
        self.tmp_path = tmp_path
        self.AnimeName = cfg.get("AnimeName")
        self.m3u8_url = m3u8_url
        self.output_file = output_file
        self.max_workers = cfg.get("max_workers")
        self.m3u8_obj = m3u8.load(m3u8_url)  # 下載 M3U8
        self.base_url = m3u8_url.rsplit("/", 1)[0]  # 取得 base URL

    # 下載 ts 檔案的函數
    def download_ts(self,i, segment, pbar):
        ts_url = segment.uri if segment.uri.startswith("http") else f"{self.base_url}/{segment.uri}"
        ts_filename = f"{self.tmp_path}/{i}.ts"

        response = requests.get(ts_url, stream=True)
        with open(ts_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        pbar.update(1)  # 更新進度條
        # print(f"下載完成：{ts_filename}")
        return ts_filename

    def parallel_downloads(self):
        # 使用 ThreadPoolExecutor 進行並行下載
        ts_files = [None] * len(self.m3u8_obj.segments)
        total_segments = len(self.m3u8_obj.segments)

        with tqdm(total=total_segments, desc=f"下載進度", unit="ts") as pbar:
            with ThreadPoolExecutor(max_workers=int(self.max_workers)) as executor:  # 設定 N 個並行執行緒
                futures = {
                    executor.submit(self.download_ts, i, segment, pbar): i
                    for i, segment in enumerate(self.m3u8_obj.segments)
                }

                for future in as_completed(futures):
                    index = futures[future]
                    ts_files[index] = future.result()  # 確保檔案順序正確
        return ts_files

    def merge_ts(self,ts_files):
        concat_file_path = os.path.join(self.tmp_path,"concat_list.txt")

        # 合併 TS 檔案
        with open(concat_file_path, "w") as f:
            for ts in ts_files:
                ts_name = os.path.basename(ts)  # 只取得檔名，避免路徑錯誤
                f.write(f"file '{ts_name}'\n")
                # f.write(f"file '{ts}'\n")

        # 使用 ffmpeg 合併成 MP4
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file_path,
            "-c", "copy", "-reset_timestamps", "1", self.output_file
        ])

        print("影片合併完成：", self.output_file)

    def run(self):
        ts_files = self.parallel_downloads()
        self.merge_ts(ts_files)
        

if __name__ == '__main__':

    cfg = dotenv_values(".env")
    animeID = cfg.get("AnimeID")
    animeName = cfg.get("AnimeName")
    episodes = int(cfg.get("episodes"))
    ts_path = cfg.get("ts_path")

    output_path = os.path.join(os.getcwd(),"output")
    os.makedirs(output_path, exist_ok=True) # 建立output輸出資料夾
    
    for episode in range(1,episodes+1):
        
        tmp_path = os.path.abspath(os.path.join(os.getcwd(), ts_path, animeName, str(episode)))
        os.makedirs(tmp_path, exist_ok=True) # 建立暫存資料夾
        os.makedirs(os.path.join(output_path,animeName), exist_ok=True) # 建立影片輸出資料夾
        
        output_file = os.path.join(output_path,animeName,f"{animeName}[{episode}].mp4")
        epiNum = str(episode).zfill(3) # 設定集數
        try:
            m3u8_url = f"https://vpx05.myself-bbs.com/vpx/{animeID}/{epiNum}/720p.m3u8" # 設定 m3u8 網址
            animedl = AnimeDownloader(cfg,tmp_path,m3u8_url,output_file)
            animedl.run()
        except:
            epiNum += '_v01'
            m3u8_url = f"https://vpx05.myself-bbs.com/vpx/{animeID}/{epiNum}/720p.m3u8" # 設定 m3u8 網址
            animedl = AnimeDownloader(cfg,tmp_path,m3u8_url,output_file)
            animedl.run()

        # 安全刪除暫存資料夾
        if tmp_path.startswith(os.getcwd()) and animeName in tmp_path:
            shutil.rmtree(tmp_path)
            print(f"已刪除暫存資料夾: {tmp_path}")
        else:
            print(f"⚠️ 安全檢查未通過，未刪除 {tmp_path}")
        
        