# app/model/llama_wrapper.py

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, List, Any, Optional
import logging
import re

class LlamaWrapper:
    # Class variable for caching
    _model_cache = None
    _tokenizer_cache = None
    
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
        
        # Check for cached model
        if LlamaWrapper._model_cache is not None:
            self.logger.info("Using cached model")
            self.model = LlamaWrapper._model_cache
            self.tokenizer = LlamaWrapper._tokenizer_cache
            
    def load_model(self) -> bool:
        """
        Load the Llama-3-8B-UltraMedical model and tokenizer.
        
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        # If already loaded, return True
        if self.model is not None:
            return True
            
        # If cached model exists, use it
        if LlamaWrapper._model_cache is not None:
            self.model = LlamaWrapper._model_cache
            self.tokenizer = LlamaWrapper._tokenizer_cache
            return True
            
        try:
            self.logger.info(f"Loading Medical model from {self.model_path}")
            self.logger.info(f"Using device: {self.device}")
            
            print(f"Downloading/loading model from {self.model_path}. This may take a few minutes on first run...")
            
            # Create a dedicated models directory in your application folder
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
            
            # Cache the model for future use
            LlamaWrapper._model_cache = self.model
            LlamaWrapper._tokenizer_cache = self.tokenizer
            
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
        # Extract generated content from response
        try:
            response_content = response_text.split("Assistant:", 1)[1].strip()
        except IndexError:
            # If splitting fails, just use everything after the prompt
            response_parts = response_text.split("follow-up tests if necessary", 1)
            if len(response_parts) > 1:
                response_content = response_parts[1].strip()
            else:
                response_content = response_text  # Fallback to using the whole text
        
        # Basic structure for the response
        structured_response = {
            "summary": "",
            "abnormal_values": [],
            "implications": [],
            "recommendations": [],
            "followup_tests": []
        }
        
        # Enhanced parsing logic with section headers
        lines = response_content.split('\n')
        current_section = "summary"
        section_buffer = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Check for section headers
            if "SUMMARY:" in line.upper():
                current_section = "summary"
                continue
            elif "ABNORMAL VALUES:" in line.upper():
                current_section = "abnormal_values"
                continue
            elif "HEALTH IMPLICATIONS:" in line.upper() or "IMPLICATIONS:" in line.upper():
                current_section = "implications"
                continue
            elif "RECOMMENDATIONS:" in line.upper():
                current_section = "recommendations"
                continue
            elif "FOLLOW-UP TESTS:" in line.upper() or "FOLLOWUP TESTS:" in line.upper():
                current_section = "followup_tests"
                continue
            
            # Process the line based on the current section
            if current_section == "summary":
                if structured_response["summary"]:
                    structured_response["summary"] += " " + line
                else:
                    structured_response["summary"] = line
            else:
                # For list sections, check for numbered bullets or other markers
                if line[0].isdigit() and line[1:3] in ['. ', '- ', ') '] and line[3:].strip():
                    # This is a new item in a numbered list
                    structured_response[current_section].append(line[3:].strip())
                elif line.startswith('- ') or line.startswith('• '):
                    # This is a new item in a bulleted list
                    structured_response[current_section].append(line[2:].strip())
                elif structured_response[current_section] and line:
                    # This is a continuation of the previous item
                    idx = len(structured_response[current_section]) - 1
                    if idx >= 0:
                        structured_response[current_section][idx] += " " + line
                elif line:
                    # This is a new item without a bullet or number
                    structured_response[current_section].append(line)
        
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