# IPL Cricket Analytics — Streamlit Web App

**BDA Lab Project | Section C | Apache Hadoop + Streamlit**

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
Open → http://localhost:8501

---

## Deploy FREE on Streamlit Community Cloud

1. Push this folder to a **GitHub repo** (public or private)
2. Go to → **https://share.streamlit.io**
3. Click **"New app"**
4. Select your repo, branch `main`, file `app.py`
5. Click **Deploy** — live URL in ~60 seconds!

---

## Project Structure

```
ipl_streamlit_app/
├── app.py                    ← Main Streamlit application
├── requirements.txt          ← Python dependencies
├── .streamlit/
│   └── config.toml           ← Dark theme config
├── data/
│   ├── generate_dataset.py   ← Generates IPL CSV data
│   ├── matches.csv           ← 240 match records
│   └── deliveries.csv        ← 24,000 delivery records
└── README.md
```

## App Features

| Tab | Contents |
|-----|----------|
| Overview | BDA architecture, project summary, season snapshot |
| MapReduce Jobs | Simulated Hadoop Streaming jobs with live terminal output |
| Hive Analytics | 10 Hive query results with interactive Plotly charts |
| Dashboard | Unified multi-chart analytics view |
| Dataset | Interactive HDFS data explorer with filters |
