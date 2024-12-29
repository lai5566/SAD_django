# sad_django

## 專案介紹
此專案基於 Django 開發，專注於 **sad_django** 的應用，提供完整的後端服務。

---

## 1. 環境準備
### 安裝 Miniconda
1. 下載 Miniconda：
   - 前往 [Miniconda 官方網站](https://docs.conda.io/en/latest/miniconda.html)。
   - 根據您的操作系統下載對應版本。

2. 安裝 Miniconda：
   - 按照安裝向導完成安裝。

3. 確認安裝是否成功：
   ```bash
   conda --version
   ```

### 安裝 VS Code
1. 下載並安裝 [VS Code](https://code.visualstudio.com/)。
2. 安裝 Python 擴展：
   - 打開 VS Code，進入擴展市場（Extensions Market）。
   - 搜索並安裝 **"Python"** 擴展。

---

## 2. 專案環境設置
### 克隆專案
使用以下命令將專案克隆到本地：
```bash
git clone https://github.com/lai5566/SAD_django.git
cd SAD_django
```

### 創建 Conda 環境
1. 使用專案內的 `environment.yaml` 文件創建環境：
   ```bash
   conda env create -f environment.yaml
   ```

2. 激活環境：
   ```bash
   conda activate djangoProject
   ```

3. 確認環境中安裝的依賴：
   ```bash
   conda list
   ```

### 確保資料庫遷移
1. 運行以下命令以進行資料庫遷移：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. 創建管理員帳戶（可選）：
   ```bash
   python manage.py createsuperuser
   ```

---

## 3. 在 VS Code 中運行專案
1. 打開 VS Code 並選擇專案目錄：
   ```bash
   code .
   ```

2. 選擇正確的 Python 解釋器：
   - 按 `Ctrl+Shift+P` （macOS 使用 `Cmd+Shift+P`）。
   - 輸入並選擇 **"Python: Select Interpreter"**。
   - 從列表中選擇 `sad_django` 的 Conda 環境。

3. 打開終端，激活環境：
   ```bash
   conda activate sad_django
   ```

4. 啟動開發伺服器：
   ```bash
   python manage.py runserver
   ```

5. 在瀏覽器中訪問 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)。

---

## 4. 常見問題
### 更新依賴
如果 `environment.yaml` 更新，可運行以下命令更新環境：
```bash
conda env update -f environment.yaml --prune
```

### 刪除環境
如需重新創建環境，可刪除舊環境：
```bash
conda remove --name sad_django --all
```

---

## 5. 聯絡方式
若有任何問題，請聯絡：[lai5566](mailto:lai5566@gmail.com)
