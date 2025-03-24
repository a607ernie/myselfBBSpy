# MySelfBBS Downloader

這是一個用於下載 Myself-BBS 動畫的 Python 腳本，透過多執行緒並行下載 `.ts` 檔案，並使用 `ffmpeg` 進行合併，最終輸出 `.mp4` 影片。

## 功能特色
- **多執行緒並行下載** (`ThreadPoolExecutor`)
- **使用 `tqdm` 顯示下載進度條**
- **自動合併 TS 檔案為 MP4** (`ffmpeg`)
- **下載後自動清理暫存資料夾**

## 需求安裝
請確保您的環境已安裝以下套件：

```bash
pip install requests m3u8 python-dotenv tqdm
```

或是

```bash
pip install  -r requirements.txt
```

此外，請安裝 `ffmpeg`，若尚未安裝，可依據作業系統使用以下指令：
- **Ubuntu / Debian**:
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```
- **MacOS (Homebrew)**:
  ```bash
  brew install ffmpeg
  ```
- **Windows**:
  下載對應版本的 ffmpeg，並設定環境變數。

## 設定 `.env`
在專案目錄下建立 `.env` 檔案，填入動畫下載設定，例如：

```
AnimeID=12345
AnimeName="無頭騎士異聞錄 DuRaRaRa!!"
episodes=25
max_workers=16
ts_path="video_ts"
```

## 使用方式
1. 編輯 `.env` 檔案，確保 `AnimeID`、`AnimeName`、`episodes` 等參數正確。
2. 執行下載腳本：
   ```bash
   python main.py
   ```
3. 完成後，影片將存放於 `output/AnimeName/` 資料夾內。

## 目錄結構
```
.
├── main.py             # 主要的下載腳本
├── .env                # 設定檔 (需手動建立)
├── output/             # 下載的 MP4 影片存放處(會自動產生)
├── video_ts/           # 暫存 TS 檔案的目錄 (下載完成後自動刪除)
└── README.md           # 本文件
```

## 版權聲明
此腳本僅供學術研究與個人使用，請勿用於任何侵犯版權的行為。請遵守當地法律，使用本程式請自行承擔風險。

