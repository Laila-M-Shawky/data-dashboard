# 📊 Data Dashboard — Streamlit App

داشبورد تحليل بيانات تفاعلي مبني بـ Streamlit + Plotly.

## المميزات
- رفع ملفات CSV وتحليلها فوراً
- KPI cards تلقائية لكل الأعمدة الرقمية
- Line chart، Bar chart، Histogram، Pie chart، Heatmap
- تصدير البيانات CSV
- ثيم داكن احترافي

## تشغيل محلياً

```bash
pip install -r requirements.txt
streamlit run app.py
```

## الرفع على Streamlit Community Cloud

### الخطوات:

1. **ارفع المشروع على GitHub**
   ```bash
   git init
   git add .
   git commit -m "first commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPO_NAME.git
   git push -u origin main
   ```

2. **اعمل حساب على Streamlit Cloud**
   - روح على: https://share.streamlit.io
   - سجّل دخول بحساب GitHub

3. **انشر الـ app**
   - اضغط "New app"
   - اختر الـ repository والـ branch
   - حط `app.py` في خانة Main file path
   - اضغط "Deploy!"

4. **بعد دقيقتين** — الـ app هيكون live على رابط مجاني زي:
   `https://username-appname.streamlit.app`

## هيكل الملفات

```
streamlit_app/
├── app.py                  # الكود الرئيسي
├── requirements.txt        # المكتبات
└── .streamlit/
    └── config.toml         # إعدادات الثيم والـ server
```
