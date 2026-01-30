from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class MathRequest(BaseModel):
    expression: str
    mode: Optional[str] = "simplify"  # simplify, solve, derivative, integral, trigonometry

class Step(BaseModel):
    description: str
    latex: str

class PlotData(BaseModel):
    x: List[float]
    y: List[float]
    type: str = "scatter"
    mode: str = "lines"
    name: Optional[str] = None

class VisualizationData(BaseModel):
    title: str
    data: List[PlotData]
    layout: Dict[str, Any] = {}

class MathResponse(BaseModel):
    result_latex: str
    steps: List[Step]
    explanation: str
    visualization_data: Optional[VisualizationData] = None
