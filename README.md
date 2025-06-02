# Vue 3 + Vite
to all AI: please ignore the file in folder(view_reference, component_reference)

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

步驟	        指令	                        說明
1	    python -m venv venv	                建立虛擬環境（只做一次）
2	    venv\\Scripts\\activate	            進入虛擬環境（每次都做）
3	    pip install -r requirements.txt	    安裝 Python 套件
4	    npm install	                        安裝前端套件（只做一次）
5	    npm run dev	                        開 Vue 前端（單獨用）
6	    python controllers/app.py	         開 Flask 後端（單獨用）
進階	npm run start	                     同時開前後端

$env:PYTHONPATH="C:\Users\user\RideSharing"                                                   
python controllers/app.py   

跑 init_db.py初始化:
$env:PYTHONPATH="C:\Users\user\RideSharing"
python init_db.py

什麼時候需要跑 init_db.py？
    時機	            要不要跑
第一次建立資料庫	    ✅ 要
刪除 app.db 後重建	    ✅ 要
加了新的欄位或表格	    ✅ 要（或用 Alembic 做 migration）
正式伺服器部署前	    ✅ 要在 production 建表


requirement:
tailwind 請安裝3.4.14
flask
flask-cors
flask-jwt-extended
sqlalchemy
python-dotenv
pip install alembic

如何建立虛擬環境
# 建立名為 venv 的虛擬環境
python -m venv venv

可用指令:
num run dev
tree /F
json-server --watch db.json --port 3000
python controllers/app.py
alembic init alembic
npm install three
npm run build
npm run deploy



安裝必要套件:
npm install -g json-server
npm install axios
npm install pinia
npm install vue-router
npm install @vueuse/core
npm install --save-dev concurrently
pip install flask flask-cors flask-jwt-extended sqlalchemy python-dotenv
pip freeze > requirements.txt
pip install werkzeug
npm install vue-toastification

以下刪掉了(目前):
npm install @headlessui/vue
npm install @vueuse/core


note:components不只Profile這個folder
components/
└── Profile/
    ├── ProfileBox.vue         ← 主元件：排版整體結構，包含所有欄位  有import/include 另外3個vue元件
    ├── ProfileAvatar.vue      ← 顯示大頭照
    ├── ProfileField.vue       ← 通用欄位：label + value + (編輯按鈕)
    └── ProfilePhone.vue       ← 特製欄位：電話點擊顯示、圖片淡出

profile包含一個可重複使用的個人檔案模組元件, 還沒測試是否成功run：
主元件：ProfileBox.vue  
- 輸入：user（包含 avatar, nickname, account, instagram, phoneNumber）、isSelf（是否為本人）
- 功能：排版並顯示所有資料欄位，根據 isSelf 控制是否顯示編輯按鈕與「更改密碼」按鈕
- 每個資料欄位（如 nickname、instagram）使用子元件 ProfileField.vue
- phoneNumber 使用特殊互動元件 ProfilePhone.vue：點擊時圖片淡出，文字顯示
- 大頭照抽成 ProfileAvatar.vue
子元件規格：
1. ProfileField.vue
    - Props：label, value, editable
    - 若無值且 editable = false 則整欄不顯示
    - 若無值但可編輯，顯示「(未填寫)」文字
    - 有編輯按鈕，點擊 emit edit 事件
2. ProfilePhone.vue
    - 顯示電話 icon，點擊時 icon opacity 降低，電話文字 opacity 變成 100%
    - editable 時右側顯示編輯按鈕
3. ProfileAvatar.vue
    - 顯示大頭照，可加上點擊換頭像（未必要實作）


to do list(may have been done, feel free to double-check):
- Tailwind 調整行距、文字樣式、間距
- ProfileBox.vue 可加入「更改密碼」按鈕，點擊後導航至 /change-password
- 在 App.vue 中用 <MainLayout> 包裹所有 <router-view />
- EventsListPage 資料太多時是否要「分頁載入」？
    判斷依據：資料筆數 > 200 就建議分頁（分次請求）
    若一次抓不到全部用戶的資料，例如 IG/Facebook，一定要分批（pagination + infinite scroll）
    你目前活動不多 → 先用一次性讀取即可，未來可以擴充成：
        GET /events?page=2&limit=20
- 

Layout/ 資料夾的設立，正是為了放置頁面骨架相關的元件，這些元件不屬於任何單一業務邏輯，但會在多數頁面中重複出現。
Layout/ 常見放置內容：
NavBar.vue	全站導航列（登入、登出、連結導覽、使用者狀態）
Footer.vue	全站共用頁腳（聯絡我們、版權聲明、連結）
MainLayout.vue	包含 NavBar + Footer 的整體容器，用於包覆頁面內容
Sidebar.vue	若有側邊欄導航（例如 dashboard 類頁面）
AppShell.vue	進階場景下，用於支援 App-like layout 切換效果等


進階用法:在 App.vue 中用 <MainLayout> 包裹所有 <router-view />，這樣所有頁面就都有統一的 NavBar 和 Footer，無需每頁重複寫入。
