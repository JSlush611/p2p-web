<h1 align="center"> 🎯 P2P-Web: Swim Data Visualization 🏊📊 </h1> 
<p align="center"> Welcome to the <strong>P2P-Web</strong> project! This full-stack web application is designed to scrape, process, and visualize over 15 years of open-water swim data. The goal is to provide interactive and insightful visualizations for swimmers, enabling them to analyze trends, track performance, and explore historical race data. 🌊📈 </p>

## 📁 Project Structure
Here's how the project is organized:

```
p2p-web/
├── 📂 p2p-backend/
│   ├── 📂 app/
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Core business logic
│   │   ├── graph_building/ # Data processing & visualization logic
│   │   ├── app.py        # Flask entry point
│   │   ├── __init__.py   # App initialization
│   ├── Dockerfile        # Backend containerization
│   ├── run.py            # Backend application entry script
│   ├── requirements.txt  # Python dependencies
│
├── 📂 p2p-frontend/
│   ├── 📂 src/           # React frontend source files
│   ├── public/          # Static assets
│   ├── package.json     # Frontend dependencies
│   ├── Dockerfile       # Frontend containerization
│   ├── nginx.conf       # NGINX config for serving frontend
│
├── docker-compose.yaml  # Container orchestration for local development
├── .github/workflows/   # CI/CD pipelines
├── .gitignore           # Ignored files like `.env` and pycache
├── README.md            # Project overview (You're here!)
```
<h2>💻 What It Does</h2>

<h3>1️⃣ Full-Stack Swim Data Visualization</h3>
<ul>
  <li><strong>Data Collection</strong> → Scrapes and processes <b>15+ years</b> of open-water swim race results.</li>
  <li><strong>Visualization</strong> → Displays <b>interactive graphs</b> of participation, performance trends, and historical rankings.</li>
  <li><strong>User Customization</strong> → Allows users to <b>explore swim statistics</b> and filter data.</li>
</ul>

<h3>2️⃣ Modern Cloud-Based Architecture</h3>
<ul>
  <li><strong>Flask API (Backend)</strong> → Processes data and serves JSON responses for visualization.</li>
  <li><strong>React Frontend</strong> → Provides an interactive UI for users to explore swim data.</li>
  <li><strong>Cloud Run Deployment</strong> → Automatically scales with usage for cost efficiency.</li>
</ul>

<h3>3️⃣ CI/CD & Automation</h3>
<ul>
  <li><strong>GitHub Actions</strong> → Automates <b>building, testing, and deploying</b> Docker images.</li>
  <li><strong>Dockerized Services</strong> → Ensures smooth local and cloud-based execution.</li>
</ul>

<hr>

<h2>🚀 Features</h2>

<h3>📊 Data Processing & Visualization</h3>
<ul>
  <li><strong>Race Participation Over Time</strong> → Track how participation numbers have changed over the years.</li>
  <li><strong>Average & Fastest Swim Times</strong> → Analyze trends in race times.</li>
  <li><strong>Performance Comparisons</strong> → Compare swimmers based on age, gender, or other criteria.</li>
</ul>

<h3>🏗️ Scalable & Cloud-Based</h3>
<ul>
  <li><strong>Stateless Microservice Architecture</strong> → Designed to run efficiently on <b>Google Cloud Run</b>.</li>
  <li><strong>Containerized Deployment</strong> → Backend and frontend are <b>Dockerized</b> for smooth deployment.</li>
</ul>

<h3>🏃 Automated Workflows</h3>
<ul>
  <li><strong>CI/CD Pipeline</strong> → Uses <b>GitHub Actions</b> to <b>build, push, and deploy</b> the backend and frontend.</li>
  <li><strong>Automated Cloud Run Deployment</strong> → Seamlessly updates live service.</li>
</ul>

<hr>

<h2>📜 Acknowledgments</h2>
<ul>
  <li>🏊 <strong>Swim Community</strong> → For inspiring this project.</li>
  <li>📊 <strong>Plotly & Pandas</strong> → For enabling advanced visualizations.</li>
  <li>☁️ <strong>Google Cloud</strong> → For scalable deployment options.</li>
</ul>

<p align="center"><strong>Feel free to contribute, report bugs, or suggest new features! 🚀</strong></p>
