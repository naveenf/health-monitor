# app/utils/analysis_service.py

from ..model.llama_wrapper import LlamaWrapper
from typing import Dict, Any, List
import logging
import time

class AnalysisService:
    def __init__(self, model_path: str = None, lazy_loading: bool = True):
        """
        Initialize the analysis service.
        
        Args:
            model_path: Path to the model or model identifier
            lazy_loading: If True, model will only be loaded when needed
        """
        self.logger = logging.getLogger(__name__)
        self.model = LlamaWrapper(model_path=model_path)
        self.model_loaded = False
        
        # If not lazy loading, load the model right away
        if not lazy_loading:
            self.load_model()
    
    def load_model(self) -> bool:
        """
        Load the AI model.
        
        Returns:
            bool: Success status
        """
        if self.model_loaded:
            return True
            
        try:
            success = self.model.load_model()
            self.model_loaded = success
            return success
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            return False
    
    def get_basic_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform only basic analysis (fast, no AI required).
        
        Args:
            data: Dictionary containing patient info and blood parameters
            
        Returns:
            Dictionary with basic analysis results
        """
        # Perform basic analysis
        basic_analysis = self._perform_basic_analysis(data['blood_parameters'])
        
        # Return result with basic analysis
        return {
            "patient": data['patient'],
            "test": data['test'],
            "blood_parameters": data['blood_parameters'],
            "basic_analysis": basic_analysis,
            # No AI analysis yet
        }
    
    def get_ai_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform AI analysis.
        
        Args:
            data: Dictionary containing patient info and blood parameters
            
        Returns:
            Dictionary with AI analysis results
        """
        try:
            # Try to get AI analysis
            ai_analysis = self.model.analyze_blood_parameters(
                data['blood_parameters'],
                data['patient']
            )
            
            # Add medical disclaimer
            ai_analysis["disclaimer"] = (
                "This analysis is generated by an AI model and should be reviewed "
                "by a healthcare professional. It is not a substitute for "
                "professional medical advice, diagnosis, or treatment."
            )
            
            return ai_analysis
        except Exception as e:
            self.logger.error(f"AI analysis failed: {str(e)}")
            return {
                "error": str(e),
                "summary": "AI analysis failed. The basic analysis is still available above.",
                "disclaimer": "AI analysis unavailable. Please consult a healthcare professional."
            }
    
    def analyze_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze blood test results with both basic and AI analysis.
        
        Args:
            data: Dictionary containing patient info and blood parameters
            
        Returns:
            Dictionary with all analysis results
        """
        # Get basic analysis
        result = self.get_basic_analysis(data)
        
        # Add AI analysis if requested
        if data.get('preferences', {}).get('use_ai_analysis', False):
            ai_analysis = self.get_ai_analysis(data)
            result["ai_analysis"] = ai_analysis
        
        return result
    
    def _perform_basic_analysis(self, blood_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform basic analysis on blood parameters without using AI.
        
        Args:
            blood_parameters: Dictionary of blood parameters and their values
            
        Returns:
            Dictionary with basic analysis results
        """
        abnormal_parameters = []
        
        for name, data in blood_parameters.items():
            value = data.get('value')
            range_vals = data.get('range', [None, None])
            
            if range_vals and len(range_vals) == 2 and range_vals[0] and range_vals[1]:
                min_val = float(range_vals[0])
                max_val = float(range_vals[1])
                
                if value < min_val:
                    abnormal_parameters.append({
                        "name": name,
                        "value": value,
                        "status": "low",
                        "deviation": ((min_val - value) / min_val) * 100
                    })
                elif value > max_val:
                    abnormal_parameters.append({
                        "name": name,
                        "value": value,
                        "status": "high",
                        "deviation": ((value - max_val) / max_val) * 100
                    })
        
        return {
            "abnormal_count": len(abnormal_parameters),
            "abnormal_parameters": abnormal_parameters,
            "critical_count": sum(1 for p in abnormal_parameters if p["deviation"] > 20)
        }