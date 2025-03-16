import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, List, Any, Optional
import logging
import re

class LlamaWrapper:
    def __init__(self, model_path: str = None, device: str = None):
        """
        Initialize the Llama model wrapper.
        
        Args:
            model_path: Path to the model or model identifier from huggingface.co/models
            device: Device to use ('cpu', 'cuda', or 'auto')
        """
        self.logger = logging.getLogger(__name__)
        
        # Default to the TsinghuaC3I/Llama-3-8B-UltraMedical model
        if model_path is None:
            model_path = "TsinghuaC3I/Llama-3-8B-UltraMedical"
        
        self.model_path = model_path
        
        # Auto-detect device if not specified
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize components to None
        self.model = None
        self.tokenizer = None
        
    def load_model(self) -> bool:
        """
        Load the Llama-3-8B-UltraMedical model and tokenizer.
        
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        try:
            self.logger.info(f"Loading Medical model from {self.model_path}")
            self.logger.info(f"Using device: {self.device}")
            
            print(f"Downloading/loading model from {self.model_path}. This may take a few minutes on first run...")
            
            # Create a dedicated models directory in your application folder
            import os
            models_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models"))
            os.makedirs(models_dir, exist_ok=True)
            print(f"Using models directory: {models_dir}")
            
            # Load tokenizer with explicit cache directory
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                local_files_only=False,
                cache_dir=models_dir
            )
            
            # Try to load without quantization
            if self.device == "cpu":
                print("Loading model for CPU without quantization (this may use more memory)...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.float16, 
                    device_map="auto",
                    trust_remote_code=True,
                    cache_dir=models_dir,
                    low_cpu_mem_usage=True
                )
            else:
                # Use 16-bit for GPU
                print("Loading model with float16 for GPU...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True,
                    cache_dir=models_dir
                )
            
            self.logger.info("Model loaded successfully")
            print("Model loaded successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            print(f"Error loading model: {str(e)}")
            return False
    
    def analyze_blood_parameters(self, blood_parameters: Dict[str, Any], 
                           patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze blood parameters and generate insights using Llama-3-8B-UltraMedical.
        
        Args:
            blood_parameters: Dictionary of blood parameters and their values
            patient_info: Dictionary of patient information
            
        Returns:
            Dictionary with insights and recommendations
        """
        if not self.model or not self.tokenizer:
            if not self.load_model():
                return {"error": "Model could not be loaded"}
        
        # Construct prompt from blood parameters and patient info
        prompt = self._construct_prompt(blood_parameters, patient_info)
        
        # Generate response
        try:
            # Format as messages for the model's chat template
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            # Apply chat template
            formatted_prompt = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False,
                add_generation_prompt=True
            )
            
            # Tokenize with explicit attention mask
            inputs = self.tokenizer(
                formatted_prompt, 
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Create attention mask if not present
            if 'attention_mask' not in inputs:
                inputs['attention_mask'] = torch.ones_like(inputs['input_ids'])
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs['input_ids'],
                    attention_mask=inputs['attention_mask'],
                    max_new_tokens=1024,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    repetition_penalty=1.2,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response and extract assistant's reply
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the assistant's response
            assistant_response = response_text.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
            
            # Process and structure the response
            return self._process_response(assistant_response)
            
        except Exception as e:
            self.logger.error(f"Error during inference: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _construct_prompt(self, blood_parameters: Dict[str, Any], 
                     patient_info: Dict[str, Any]) -> str:
        """
        Construct a prompt for Llama-3-8B-UltraMedical from blood parameters and patient info.
        
        Args:
            blood_parameters: Dictionary of blood parameters and their values
            patient_info: Dictionary of patient information
            
        Returns:
            Formatted prompt string
        """
        gender = patient_info.get('gender', 'Unknown')
        age = patient_info.get('age', 'Unknown')
        
        # Format prompt as a medical query with clear sections
        prompt = f"""I have blood test results for a {age}-year-old {gender}. Please analyze these values and provide a detailed medical assessment.

    Blood Test Results:
    {self._format_blood_parameters(blood_parameters)}

    Please provide a comprehensive analysis with the following clear sections:

    1. Summary: A clear summary of the overall health status based on these results.

    2. Abnormal Values Analysis: Detailed analysis of any abnormal values and their significance.

    3. Health Implications: Potential health conditions or concerns suggested by these results.

    4. Recommendations: Specific lifestyle or dietary adjustments that would be beneficial.

    5. Follow-up Tests: Any suggested additional tests that would provide more insights.

    For each section, please be specific, detailed, and focus on clinical implications. Format each section with clear bullet points where appropriate."""
        
        return prompt

    
    def _format_blood_parameters(self, blood_parameters: Dict[str, Any]) -> str:
        """Format blood parameters for the prompt in a clean, readable format"""
        formatted_params = ""
        
        for name, data in blood_parameters.items():
            value = data.get('value')
            unit = data.get('unit', '')
            range_vals = data.get('range', [None, None])
            
            if range_vals and len(range_vals) == 2 and range_vals[0] is not None and range_vals[1] is not None:
                range_str = f"(Normal range: {range_vals[0]}-{range_vals[1]} {unit})"
            else:
                range_str = ""
                
            formatted_params += f"- {name}: {value} {unit} {range_str}\n"
        
        return formatted_params
    
    def _process_response(self, response_text: str) -> Dict[str, Any]:
        """
        Process the raw model response into structured data.
        
        Args:
            response_text: Raw text response from the model
            
        Returns:
            Dictionary with structured insights and recommendations
        """
        # Basic structure for the response
        structured_response = {
            "summary": "",
            "abnormal_values": [],
            "implications": [],
            "recommendations": [],
            "followup_tests": []
        }
        
        # Try to find sections in the response
        # Summary section
        summary_match = re.search(r'(?:1\..*?summary|summary|overall health status)(?:\s*?:?\s*)(.*?)(?:(?:2\.)|$)', 
                                response_text, re.DOTALL | re.IGNORECASE)
        if summary_match:
            summary_text = summary_match.group(1).strip()
            # If summary text is too short, try to find a more complete section
            if len(summary_text) < 30:
                # Look for more text that might be part of the summary
                extended_summary = re.search(r'(?:health status|assessment|summary).*?(.*?)(?:abnormal|analysis|section 2)', 
                                        response_text, re.DOTALL | re.IGNORECASE)
                if extended_summary:
                    summary_text = extended_summary.group(1).strip()
            
            structured_response["summary"] = summary_text
        
        # Abnormal values section
        abnormal_match = re.search(r'(?:2\..*?abnormal|abnormal values|analysis of abnormal)(?:\s*?:?\s*)(.*?)(?:(?:3\.)|(?:health implications)|$)', 
                                response_text, re.DOTALL | re.IGNORECASE)
        if abnormal_match:
            abnormal_text = abnormal_match.group(1).strip()
            # Extract bullet points or list items
            abnormal_items = re.findall(r'(?:•|-|\*|\d+\.)\s*(.*?)(?=(?:•|-|\*|\d+\.)|$)', 
                                    abnormal_text, re.DOTALL)
            if abnormal_items and len(abnormal_items[0]) > 10:  # If we found meaningful bullet points
                structured_response["abnormal_values"] = [item.strip() for item in abnormal_items if item.strip()]
            else:
                # If no bullet points or they're too short, use sentences
                sentences = re.findall(r'([^.!?]+[.!?])', abnormal_text)
                if sentences:
                    structured_response["abnormal_values"] = [s.strip() for s in sentences if len(s.strip()) > 10]
                else:
                    # If no sentences, use the whole text
                    structured_response["abnormal_values"] = [abnormal_text] if len(abnormal_text) > 10 else ["No specific abnormal values analysis provided."]
        
        # Health implications section (similar pattern for all remaining sections)
        implications_match = re.search(r'(?:3\..*?implications|potential health|health implications)(?:\s*?:?\s*)(.*?)(?:(?:4\.)|(?:recommendations)|$)', 
                                    response_text, re.DOTALL | re.IGNORECASE)
        if implications_match:
            implications_text = implications_match.group(1).strip()
            implications_items = re.findall(r'(?:•|-|\*|\d+\.)\s*(.*?)(?=(?:•|-|\*|\d+\.)|$)', 
                                        implications_text, re.DOTALL)
            if implications_items and len(implications_items[0]) > 10:
                structured_response["implications"] = [item.strip() for item in implications_items if item.strip()]
            else:
                sentences = re.findall(r'([^.!?]+[.!?])', implications_text)
                if sentences:
                    structured_response["implications"] = [s.strip() for s in sentences if len(s.strip()) > 10]
                else:
                    structured_response["implications"] = [implications_text] if len(implications_text) > 10 else ["No specific health implications provided."]
        
        # Recommendations section
        recommendations_match = re.search(r'(?:4\..*?recommend|lifestyle|dietary)(?:\s*?:?\s*)(.*?)(?:(?:5\.)|(?:follow)|(?:suggested)|$)', 
                                        response_text, re.DOTALL | re.IGNORECASE)
        if recommendations_match:
            recommendations_text = recommendations_match.group(1).strip()
            recommendations_items = re.findall(r'(?:•|-|\*|\d+\.)\s*(.*?)(?=(?:•|-|\*|\d+\.)|$)', 
                                            recommendations_text, re.DOTALL)
            if recommendations_items and len(recommendations_items[0]) > 10:
                structured_response["recommendations"] = [item.strip() for item in recommendations_items if item.strip()]
            else:
                sentences = re.findall(r'([^.!?]+[.!?])', recommendations_text)
                if sentences:
                    structured_response["recommendations"] = [s.strip() for s in sentences if len(s.strip()) > 10]
                else:
                    structured_response["recommendations"] = [recommendations_text] if len(recommendations_text) > 10 else ["No specific recommendations provided."]
        
        # Follow-up tests section
        followup_match = re.search(r'(?:5\..*?follow|suggested tests|additional tests|follow.*?up)(?:\s*?:?\s*)(.*?)(?:$|disclaimer)', 
                                response_text, re.DOTALL | re.IGNORECASE)
        if followup_match:
            followup_text = followup_match.group(1).strip()
            followup_items = re.findall(r'(?:•|-|\*|\d+\.)\s*(.*?)(?=(?:•|-|\*|\d+\.)|$)', 
                                    followup_text, re.DOTALL)
            if followup_items and len(followup_items[0]) > 10:
                structured_response["followup_tests"] = [item.strip() for item in followup_items if item.strip()]
            else:
                sentences = re.findall(r'([^.!?]+[.!?])', followup_text)
                if sentences:
                    structured_response["followup_tests"] = [s.strip() for s in sentences if len(s.strip()) > 10]
                else:
                    structured_response["followup_tests"] = [followup_text] if len(followup_text) > 10 else ["No specific follow-up tests suggested."]
        
        # Clean up any "blockedContent" mentions that might appear
        for key in structured_response:
            if isinstance(structured_response[key], list):
                structured_response[key] = [
                    item.replace("blockedContent", "").strip() 
                    for item in structured_response[key] 
                    if "blockedContent" not in item or len(item.replace("blockedContent", "").strip()) > 10
                ]
                # If we filtered everything out, add a default message
                if not structured_response[key]:
                    structured_response[key] = ["No specific information provided."]
            elif isinstance(structured_response[key], str):
                if "blockedContent" in structured_response[key]:
                    structured_response[key] = "No specific information provided."
        
        # Ensure each section has at least one entry
        for key, value in structured_response.items():
            if not value and key != "summary":
                structured_response[key] = ["No specific information provided."]
            elif key == "summary" and not value:
                structured_response[key] = "No summary provided."
        
        return structured_response
    
    def unload_model(self) -> None:
        """
        Unload the model from memory to free up resources.
        """
        if self.model:
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            
            # Force garbage collection
            import gc
            gc.collect()
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            self.logger.info("Model unloaded from memory")