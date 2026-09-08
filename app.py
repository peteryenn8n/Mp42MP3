import streamlit as st
import os
import subprocess
import imageio_ffmpeg

# 設定頁面資訊
st.set_page_config(page_title="M4A轉MP3神器", page_icon="🎵")

st.title("🎵 M4A 轉 MP3 線上轉換器")
st.markdown("### 簡單、隱私、無需安裝")
st.write("直接上傳手機錄音檔 (.m4a)，系統將自動轉換為 MP3 供您下載。")

# --- 檔案上傳區 ---
uploaded_file = st.file_uploader("請拖曳或點擊上傳檔案", type=["m4a"])

if uploaded_file is not None:
    # 顯示檔案資訊
    st.info(f"📄 檔案名稱: {uploaded_file.name} | 📦 大小: {uploaded_file.size / 1024 / 1024:.2f} MB")

    # 轉檔按鈕
    if st.button("🚀 開始轉檔"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("正在準備檔案...")
            progress_bar.progress(10)

            # 定義暫存路徑
            temp_input = "temp_input.m4a"
            temp_output = "output.mp3"

            # 1. 寫入暫存檔
            with open(temp_input, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            status_text.text("正在啟動轉檔引擎 (FFmpeg)...")
            progress_bar.progress(30)

            # --- 關鍵補上這行：取得內建的 ffmpeg 執行檔路徑 ---
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

            # 2. 執行 FFmpeg 指令
            cmd = [
                ffmpeg_path,
                '-i', temp_input,
                '-vn',            # 不處理影像
                '-ab', '192k',    # 設定音質 192kbps
                '-y',             # 強制覆蓋
                temp_output
            ]

            # 執行轉檔
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            progress_bar.progress(100)
            status_text.text("✅ 轉換完成！")
            st.success("成功！您的檔案已準備好。")

            # 3. 提供下載
            with open(temp_output, "rb") as f:
                mp3_bytes = f.read()
                
            st.download_button(
                label="📥 下載 MP3 檔案",
                data=mp3_bytes,
                file_name=os.path.splitext(uploaded_file.name)[0] + ".mp3",
                mime="audio/mpeg"
            )

        except Exception as e:
            st.error(f"❌ 發生錯誤: {e}")
        
        finally:
            # 清理暫存檔
            if os.path.exists(temp_input):
                os.remove(temp_input)
            if os.path.exists(temp_output):
                os.remove(temp_output)
