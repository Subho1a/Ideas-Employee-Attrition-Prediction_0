import streamlit as st
import requests
import json
import os
import sys

# Add project root to path for local imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Custom premium styling
st.set_page_config(
    page_title="Employee Attrition Prediction Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)
BACKEND_URL = "https://employee-attrition-prediction-aabn.onrender.com"
# Deep dark mode and glassmorphism styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #FF4B4B, #FF8F6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #A0AEC0;
        margin-bottom: 2rem;
    }
    
    /* Custom Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }
    
    /* Metrics block */
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
        margin-top: 10px;
    }
    
    .metric-risk-high {
        color: #FF5A5A;
        background: linear-gradient(135deg, #FF4B4B, #E53E3E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-risk-low {
        color: #38A169;
        background: linear-gradient(135deg, #48BB78, #38A169);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .factor-item {
        background: rgba(255, 90, 90, 0.07);
        border-left: 4px solid #FF5A5A;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    
    .factor-item-ok {
        background: rgba(72, 187, 120, 0.07);
        border-left: 4px solid #48BB78;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }

    .recommendation-card {
        background: rgba(66, 153, 225, 0.08);
        border: 1px solid rgba(66, 153, 225, 0.2);
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
    }
    
    .recommendation-title {
        color: #4299E1;
        font-weight: 600;
        margin-bottom: 5px;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("<div class='main-title'>HR Attrition Intellect</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Predictive analytics to evaluate employee retention risks and identify retention strategies.</div>", unsafe_allow_html=True)

# Setup layout
col_input, col_display = st.columns([3, 2], gap="large")

with col_input:
    st.markdown("<h3 style='margin-bottom:15px;'>Employee Parameters</h3>", unsafe_allow_html=True)
    
    # Form layout with tabs/expanders
    with st.expander("🏢 Job Description & Financials", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Age", 18, 65, 34)
            gender = st.selectbox("Gender", ["Male", "Female"])
            marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
            dept = st.selectbox("Department", ["Research & Development", "Sales", "Human Resources"])
            role = st.selectbox("Job Role", [
                "Sales Executive", "Research Scientist", "Laboratory Technician", 
                "Manufacturing Director", "Healthcare Representative", "Manager", 
                "Sales Representative", "Research Director", "Human Resources"
            ])
            distance = st.slider("Distance From Home (km)", 1, 40, 9)
        with col2:
            monthly_income = st.number_input("Monthly Income (USD)", 1000, 25000, 5000, step=500)
            percent_hike = st.slider("Percent Salary Hike (%)", 10, 25, 12)
            stock_level = st.slider("Stock Option Level", 0, 3, 1)
            daily_rate = st.number_input("Daily Billing Rate", 100, 1500, 800, step=50)
            hourly_rate = st.number_input("Hourly Billing Rate", 30, 100, 65, step=5)
            monthly_rate = st.number_input("Monthly Billing Rate", 2000, 30000, 14000, step=1000)
            
    with st.expander("📝 Tenure & Experience"):
        col3, col4 = st.columns(2)
        with col3:
            total_years = st.slider("Total Working Years", 0, 40, 10)
            years_at_company = st.slider("Years At Company", 0, 40, 5)
            years_in_role = st.slider("Years In Current Role", 0, 20, 3)
        with col4:
            years_since_promo = st.slider("Years Since Last Promotion", 0, 15, 1)
            years_with_manager = st.slider("Years With Current Manager", 0, 20, 3)
            num_companies = st.slider("Number of Companies Worked At", 0, 10, 2)
            
    with st.expander("📊 Workplace Experience & Sentiment"):
        col5, col6 = st.columns(2)
        with col5:
            job_satisfaction = st.slider("Job Satisfaction Rating (1: Low, 4: High)", 1, 4, 3)
            env_satisfaction = st.slider("Environment Satisfaction Rating (1: Low, 4: High)", 1, 4, 3)
            rel_satisfaction = st.slider("Relationship Satisfaction Rating (1: Low, 4: High)", 1, 4, 3)
        with col6:
            work_life_balance = st.slider("Work Life Balance Rating (1: Bad, 4: Good)", 1, 4, 3)
            job_involvement = st.slider("Job Involvement Rating (1: Low, 4: High)", 1, 4, 3)
            overtime = st.selectbox("Works Overtime?", ["No", "Yes"])
            travel = st.selectbox("Business Travel Frequency", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
            
    with st.expander("🎓 Education & Performance"):
        col7, col8 = st.columns(2)
        with col7:
            edu_level = st.slider("Education Level (1: Below College, 5: Doctor)", 1, 5, 3)
            edu_field = st.selectbox("Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"])
        with col8:
            performance = st.slider("Performance Rating (3: Good, 4: Outstanding)", 3, 4, 3)
            training_times = st.slider("Training Sessions Last Year", 0, 6, 2)

    # Prediction Action
    payload = {
        "Age": age,
        "BusinessTravel": travel,
        "DailyRate": daily_rate,
        "Department": dept,
        "DistanceFromHome": distance,
        "Education": edu_level,
        "EducationField": edu_field,
        "EnvironmentSatisfaction": env_satisfaction,
        "Gender": gender,
        "HourlyRate": hourly_rate,
        "JobInvolvement": job_involvement,
        "JobLevel": int(age // 15), # simple heuristic mapping to mimic job level bounds if not inputs
        "JobRole": role,
        "JobSatisfaction": job_satisfaction,
        "MaritalStatus": marital,
        "MonthlyIncome": monthly_income,
        "MonthlyRate": monthly_rate,
        "NumCompaniesWorked": num_companies,
        "OverTime": overtime,
        "PercentSalaryHike": percent_hike,
        "PerformanceRating": performance,
        "RelationshipSatisfaction": rel_satisfaction,
        "StockOptionLevel": stock_level,
        "TotalWorkingYears": total_years,
        "TrainingTimesLastYear": training_times,
        "WorkLifeBalance": work_life_balance,
        "YearsAtCompany": years_at_company,
        "YearsInCurrentRole": years_in_role,
        "YearsSinceLastPromotion": years_since_promo,
        "YearsWithCurrManager": years_with_manager
    }
    
    # Overwrite JobLevel with actual slider inputs if they belong
    payload["JobLevel"] = int(max(1, min(5, int(total_years // 4) + 1))) 

with col_display:
    st.markdown("<h3 style='margin-bottom:15px;'>Prediction Results</h3>", unsafe_allow_html=True)
    
    # Trigger Prediction
    result = None
    is_fallback = False
    
    try:
        # Call Backend REST API
        # api_url = "http://localhost:8000/predict"
        api_url = f"{BACKEND_URL}/predict"
        response = requests.post(api_url, json=payload, timeout=2)
        if response.status_code == 200:
            result = response.json()
        else:
            is_fallback = True
    except Exception:
        is_fallback = True
        
    if is_fallback:
        # Fallback to local prediction model if Backend API is down or not started
        try:
            from src.predict import InferenceEngine
            engine = InferenceEngine()
            result = engine.predict(payload)
        except Exception as e:
            st.error("Inference Engine Offline.")
            st.info("The ML models have not been trained yet. Please run the training pipeline first using: \n`python run.py train`")
            result = None

    if result:
        prob = result["probability"]
        risk_level = result["risk_level"]
        risk_class = "metric-risk-high" if risk_level == "High" else "metric-risk-low"
        
        # Display probability and risk inside custom glassmorphism card
        st.markdown(f"""
<div class="glass-card">
    <div style="font-size: 0.9rem; color: #A0AEC0; text-transform: uppercase; letter-spacing: 1px;">Attrition Probability</div>
    <div class="metric-value {risk_class}">{prob * 100:.1f}%</div>
    <div style="margin-top: 15px; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 1rem; color: #E2E8F0;">Risk Classification:</span>
        <span class="{risk_class}" style="font-weight: 700; font-size: 1.1rem;">{risk_level} Risk</span>
    </div>
</div>
""", unsafe_allow_html=True)
        
        # Display warnings or stable signals
        st.markdown("<h4>Retention & Risk Analysis</h4>", unsafe_allow_html=True)
        
        if risk_level == "High":
            st.markdown("<p style='color: #A0AEC0; font-size:0.9rem;'>The following attributes are contributing heavily to the attrition risk score:</p>", unsafe_allow_html=True)
            for factor in result["risk_factors"]:
                st.markdown(f'<div class="factor-item">{factor}</div>', unsafe_allow_html=True)
                
            # HR Retention Action Plan recommendation card
            st.markdown(f"""
<div class="recommendation-card">
    <div class="recommendation-title">💡 Actionable Retention Recommendation</div>
    <div style="font-size:0.95rem; color:#E2E8F0; line-height: 1.6;">
        {"• Offer overtime compensation, adjust shift schedules, or assign project support to distribute workload." if overtime == "Yes" else ""}
        {"• Conduct a 1-on-1 check-in to discuss compensation alignments, role expectations, or career growth." if monthly_income < 4000 or percent_hike < 13 else ""}
        {"• Provide career progression visibility or transition to a new project/role to resolve promotion delay." if years_since_promo >= 4 else ""}
        {"• Encourage a shift-based flexible routine, remote days, or workload reductions to recover work-life balance. "if work_life_balance <= 2 or env_satisfaction <= 2 else ""}
        {"• Coordinate manager alignment feedback or transition the employee under a new leadership lead.<br>" if years_with_manager >= 5 and job_satisfaction <= 2 else ""}
        • Review active opportunities to improve their role alignment within 30 days.
    
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="factor-item-ok">✅ Retention Risk is low. The employee is satisfied and shows strong retention attributes.</div>', unsafe_allow_html=True)
            st.markdown(f"""
<div class="recommendation-card" style="background: rgba(72, 187, 120, 0.05); border: 1px solid rgba(72, 187, 120, 0.15);">
    <div class="recommendation-title" style="color: #48BB78;">📈 Growth Strategy</div>
    <div style="font-size:0.95rem; color:#E2E8F0; line-height: 1.4;">
        Continue providing growth pathways and training sessions. Key indicators suggest this employee is well-integrated and satisfied with their current management and work balance.
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar metadata
st.sidebar.markdown("<h2 style='text-align: center; color: #FF8F6B;'>System Hub</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Service status indicators
try:
    # health_resp = requests.get("http://localhost:8000/health", timeout=1).json()
    health_resp = requests.get(f"{BACKEND_URL}/health", timeout=5).json()
    api_status = "🟢 Online" if health_resp.get("status") == "healthy" else "🟡 Missing Models"
except Exception:
    api_status = "🔴 Offline"
    
st.sidebar.markdown(f"**FastAPI Backend:** {api_status}")
if is_fallback and api_status == "🔴 Offline":
    st.sidebar.info("Dashboard is running in **Local Fallback Mode** (direct import of InferenceEngine).")
else:
    st.sidebar.success("Dashboard is connected to **FastAPI REST Server**.")

