# IPL Cricket Analytics — Streamlit Web App
**Shri Ramdeobaba University, Nagpur**  
*Department of Computer Science & Engineering | Final Year B.Tech Capstone Framework*  
**Academic Track:** Big Data Analytics (BDA) Lab Project — Section C  
**Core Stack:** Apache Hadoop Distributed File System (HDFS), MapReduce, Hive Analytics, Streamlit Cloud

---

## 🔬 Project Overview & Ecosystem Impact
This repository serves as an open-source academic blueprint designed to simulate and evaluate distributed data pipelines. Built as a core component of the 4th-year B.Tech CSE curriculum at Ramdeobaba University, it bridges heavy data infrastructure with interactive visualization layers. 

### 🤖 Claude & LLM Benchmarking Integration
This codebase functions as a standardized testing framework for evaluating Large Language Model performance in data engineering tasks. It is actively used to benchmark LLM capabilities in:
* **Code Translation:** Evaluating model accuracy when transforming complex Apache Hive HQL schemas into modern Pandas query structures.
* **MapReduce Synthesising:** Testing automated code generation for Java/Python Hadoop Streaming jobs against edge-case transactional sports data.

---

## 🏗️ Architecture & App Features

| Module / Tab | Technical Implementation & Infrastructure Scope |
|:---|:---|
| **📊 Overview** | BDA system architecture topology, HDFS block distribution simulation, and season metadata. |
| **⚙️ MapReduce Jobs** | Emulated Hadoop Streaming jobs running Python Mappers/Reducers with live standard output streaming. |
| **🗃️ Hive Analytics** | 10 high-concurrency Hive Query Language (HQL) OLAP operations visualised via interactive Plotly engines. |
| **📈 Dashboard** | Multi-dimensional analytical dashboard for aggregate computation processing. |
| **💾 Dataset Explorer** | Interactive HDFS data explorer mirroring distributed directory navigation with tabular filtration. |

---

## 📂 Project Directory Structure

```text
ipl_streamlit_app/
├── app.py                    ← Main Streamlit visualization engine
├── requirements.txt          ← Production python dependencies
├── .streamlit/
│   └── config.toml           ← UI presentation configuration
├── data/
│   ├── generate_dataset.py   ← Automated pipeline for synthetic HDFS generation
│   ├── matches.csv           ← High-level match transactional records (240 rows)
│   └── deliveries.csv        ← Granular delivery logs (24,000 distributed records)
└── README.md                 ← Project manifest & deployment guide
```

---

## 🚀 Execution & Local Deployment

To spinning up the visualization cluster on a local node, ensure you have Python 3.10+ initialized:

```bash
# Clone the repository
git clone https://github.com
cd ipl-hadoop-analytics

# Install production requirements
pip install -r requirements.txt

# Launch the framework application
streamlit run app.py
```
Open your browser and navigate to: **`http://localhost:8501`**

---

## ☁️ Cloud Orchestration (Streamlit Community Cloud)

1. Push this absolute folder structure to a public branch on your **GitHub repository**.
2. Authenticate into the cloud orchestration console at: [share.streamlit.io](https://streamlit.io)
3. Click on **"New App"** within your workspace.
4. Link this specific repository (`ipl-hadoop-analytics`), set the production branch to `main`, and declare the entry point as `app.py`.
5. Click **Deploy**. Your scalable big data visualization node will map to a live URL within ~60 seconds.
