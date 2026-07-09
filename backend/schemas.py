from pydantic import BaseModel, Field
from typing import List, Literal

class EmployeeFeatures(BaseModel):
    # Categorical Features
    BusinessTravel: Literal["Travel_Rarely", "Travel_Frequently", "Non-Travel"] = Field(
        default="Travel_Rarely", 
        description="Frequency of business travel"
    )
    Department: Literal["Sales", "Research & Development", "Human Resources"] = Field(
        default="Research & Development", 
        description="Employee department"
    )
    EducationField: Literal["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other", "Human Resources"] = Field(
        default="Life Sciences", 
        description="Field of education"
    )
    Gender: Literal["Female", "Male"] = Field(
        default="Male", 
        description="Gender of employee"
    )
    JobRole: Literal[
        "Sales Executive", "Research Scientist", "Laboratory Technician", 
        "Manufacturing Director", "Healthcare Representative", "Manager", 
        "Sales Representative", "Research Director", "Human Resources"
    ] = Field(
        default="Research Scientist", 
        description="Job role in the company"
    )
    MaritalStatus: Literal["Single", "Married", "Divorced"] = Field(
        default="Single", 
        description="Marital status"
    )
    OverTime: Literal["Yes", "No"] = Field(
        default="No", 
        description="Does the employee work overtime?"
    )

    # Numerical Features
    Age: int = Field(default=35, ge=18, le=100, description="Age of employee")
    DailyRate: int = Field(default=800, ge=100, le=2000, description="Daily billing rate")
    DistanceFromHome: int = Field(default=5, ge=1, le=50, description="Distance from home to work in km")
    Education: int = Field(default=3, ge=1, le=5, description="Education level (1: Below College, 5: Doctor)")
    EnvironmentSatisfaction: int = Field(default=3, ge=1, le=4, description="Workspace environment satisfaction (1-4)")
    HourlyRate: int = Field(default=65, ge=30, le=100, description="Hourly billing rate")
    JobInvolvement: int = Field(default=3, ge=1, le=4, description="Level of job involvement (1-4)")
    JobLevel: int = Field(default=2, ge=1, le=5, description="Job responsibility level (1-5)")
    JobSatisfaction: int = Field(default=3, ge=1, le=4, description="Job satisfaction rating (1-4)")
    MonthlyIncome: int = Field(default=5000, ge=1000, le=30000, description="Monthly income in USD")
    MonthlyRate: int = Field(default=15000, ge=2000, le=30000, description="Monthly rate in USD")
    NumCompaniesWorked: int = Field(default=2, ge=0, le=15, description="Number of prior companies worked at")
    PercentSalaryHike: int = Field(default=12, ge=10, le=30, description="Percent salary hike last year")
    PerformanceRating: int = Field(default=3, ge=1, le=4, description="Performance rating (1-4)")
    RelationshipSatisfaction: int = Field(default=3, ge=1, le=4, description="Relationship satisfaction with peers (1-4)")
    StockOptionLevel: int = Field(default=0, ge=0, le=3, description="Stock option benefits level (0-3)")
    TotalWorkingYears: int = Field(default=10, ge=0, le=50, description="Total career working years")
    TrainingTimesLastYear: int = Field(default=2, ge=0, le=6, description="Number of training sessions attended last year")
    WorkLifeBalance: int = Field(default=3, ge=1, le=4, description="Work-life balance rating (1-4)")
    YearsAtCompany: int = Field(default=5, ge=0, le=50, description="Years spent at the current company")
    YearsInCurrentRole: int = Field(default=3, ge=0, le=30, description="Years in current job role")
    YearsSinceLastPromotion: int = Field(default=1, ge=0, le=30, description="Years elapsed since last promotion")
    YearsWithCurrManager: int = Field(default=3, ge=0, le=30, description="Years spent under current manager")

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 for Stay, 1 for Leave")
    probability: float = Field(..., description="Attrition probability (0.0 to 1.0)")
    risk_level: Literal["Low", "High"] = Field(..., description="Risk categorization based on threshold 0.5")
    risk_factors: List[str] = Field(default=[], description="List of primary reasons driving high risk")
