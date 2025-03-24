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

- AnimeID：動畫的 ID，會用於組成 m3u8 下載連結

- AnimeName：動畫名稱，會作為輸出影片的資料夾名稱

- episodes：下載目標的總集數

- ts_path：暫存 .ts 片段的存放目錄

- max_workers：下載 .ts 片段時的最大併發數

## 使用方式
1. 編輯 `.env` 檔案，確保 `AnimeID`、`AnimeName`、`episodes` 等參數正確。
2. 執行下載腳本：
   ```bash
   python main.py
   ```
3. 完成後，影片將存放於 `output/AnimeName/` 資料夾內。
  ```
  output/
    ├── 動畫名稱/
    │   ├── 動畫名稱[1].mp4
    │   ├── 動畫名稱[2].mp4
    │   ├── ...
    │   └── 動畫名稱[集數].mp4
    └── ...
  ```



## 目錄結構
```
.
├── main.py             # 主要的下載腳本
├── .env                # 設定檔 (需手動建立)
├── output/             # 下載的 MP4 影片存放處(會自動產生)
├── video_ts/           # 暫存 TS 檔案的目錄 (下載完成後自動刪除)
└── README.md           # 本文件
```

## TODO
- [ ] 增加錯誤處理機制，確保下載失敗時能夠重新嘗試
- [ ] 增加下載暫停與續傳功能，避免中途斷線導致下載失敗
- [x] 優化 `ffmpeg` 合併 `.ts` 檔案時的時間戳問題，解決 `Non-monotonous DTS` 錯誤
- [ ] 提供 CLI 參數支援，例如讓使用者指定 `AnimeID`、集數範圍、畫質等
- [ ] 增加日誌記錄 (`logging`)，記錄下載與合併的過程，方便除錯
- [ ] 使用 `aria2c` 下載 `.ts` 片段，提高下載效率
- [ ] 增加下載速度限制，避免影響其他網路應用
- [ ] 增加 Telegram/Discord 通知，下載完成時自動發送提醒
- [ ] 整合 Docker，讓使用者能夠更輕鬆部署


## 版權聲明
此腳本僅供學術研究與個人使用，請勿用於任何侵犯版權的行為。請遵守當地法律，使用本程式請自行承擔風險。

