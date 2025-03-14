# **Projek Analisis Data dengan Python**  
## 1. Setup Environment 
### A. Menggunakan Anaconda
Jalankan perintah berikut di terminal atau Anaconda Prompt:  
```
conda create --name main-ds python=3.13.2
conda activate main-ds
pip install -r requirements.txt
```

### B. Menggunakan Shell/Terminal (Tanpa Anaconda) 
Jalankan perintah berikut di terminal:  
```
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 2. Menjalankan Aplikasi Streamlit  

### Langkah-langkah: 
1. Buka IDE (misalnya Visual Studio Code)  
2. Navigasi ke folder proyek  
   ```
   cd Dashboard
   ```
3. Jalankan aplikasi Streamlit
   ```
   streamlit run Dashboard.py
   ```
