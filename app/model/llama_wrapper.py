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
            
            # Create a dedicated models directory in your application folder
            models_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models"))
            os.makedirs(models_dir, exist_ok=True)
            
            # Load tokenizer with explicit cache directory
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                local_files_only=False,
                cache_dir=models_dir
            )
            
            # Try to load without quantization
            if self.device == "cpu":
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
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
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
            
            # Decode response
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Try various methods to extract just the assistant's response
            
            # Method 1: Look for assistant header in the format used by Llama models
            if "<|start_header_id|>assistant<|end_header_id|>" in response_text:
                assistant_response = response_text.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
            
            # Method 2: Look for "Assistant:" format
            elif "Assistant:" in response_text:
                assistant_response = response_text.split("Assistant:", 1)[1].strip()
            
            # Method 3: Try to find the section after prompt in the response
            elif prompt in response_text:
                assistant_response = response_text.split(prompt, 1)[1].strip()
            
            # Method 4: Look for common section headers
            elif any(header in response_text for header in ["SUMMARY:", "Summary:", "Abnormal Values:", "ABNORMAL VALUES:"]):
                assistant_response = response_text
            
            # Fallback: Just use the entire response
            else:
                assistant_response = response_text
            
            # Process and structure the response
            structured_response = self._process_response(assistant_response)
            
            return structured_response
            
        except Exception as e:
            self.logger.error(f"Error during inference: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": f"Analysis failed: {str(e)}"}

    def _extract_assistant_response(self, full_response: str, original_prompt: str) -> str:
        """
        Extract just the assistant's response from the full model output.
        
        Args:
            full_response: The complete response from the model
            original_prompt: The original prompt sent to the model
            
        Returns:
            Just the assistant's portion of the response
        """
        # Try to find common patterns in model responses
        # 1. Look for "<|start_header_id|>assistant<|end_header_id|>" format
        if "<|start_header_id|>assistant<|end_header_id|>" in full_response:
            return full_response.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
        
        # 2. Look for "Assistant:" format (common in many LLM outputs)
        if "Assistant:" in full_response:
            return full_response.split("Assistant:", 1)[1].strip()
        
        # 3. Try to strip the original prompt from the beginning
        # This is less reliable but can work as a fallback
        if full_response.startswith(original_prompt):
            return full_response[len(original_prompt):].strip()
        
        # If we can't identify the assistant's response specifically,
        # return the full response minus any common prefixes
        for prefix in ["User:", "Human:", "<s>"]:
            if prefix in full_response:
                parts = full_response.split(prefix)
                if len(parts) > 1:
                    # Return everything after the last user/human prefix
                    return parts[-1].strip()
        
        return full_response
    
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
        
        # Try to extract each section using regular expressions
        # Summary section
        summary_patterns = [
            r'(?:Summary:?|SUMMARY:?)(.*?)(?:Abnormal Values|ABNORMAL VALUES|$)',
            r'(?:SUMMARY|Summary)(.*?)(?:ABNORMAL VALUES|Abnormal Values|$)'
        ]
        
        for pattern in summary_patterns:
            summary_match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if summary_match:
                structured_response["summary"] = summary_match.group(1).strip()
                break
        
        # Abnormal values section
        abnormal_patterns = [
            r'(?:Abnormal Values(?:\s+Analysis)?:?|ABNORMAL VALUES(?:\s+ANALYSIS)?:?)(.*?)(?:Health Implications|HEALTH IMPLICATIONS|Implications|IMPLICATIONS|$)',
            r'(?:ABNORMAL VALUES|Abnormal Values)(.*?)(?:HEALTH IMPLICATIONS|Health Implications|IMPLICATIONS|Implications|$)'
        ]
        
        for pattern in abnormal_patterns:
            abnormal_match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if abnormal_match:
                section_text = abnormal_match.group(1).strip()
                structured_response["abnormal_values"] = self._extract_bullet_points(section_text)
                break
        
        # Health implications section
        implications_patterns = [
            r'(?:Health Implications:?|HEALTH IMPLICATIONS:?|Implications:?|IMPLICATIONS:?)(.*?)(?:Recommendations|RECOMMENDATIONS|$)',
            r'(?:HEALTH IMPLICATIONS|Health Implications|IMPLICATIONS|Implications)(.*?)(?:RECOMMENDATIONS|Recommendations|$)'
        ]
        
        for pattern in implications_patterns:
            implications_match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if implications_match:
                section_text = implications_match.group(1).strip()
                structured_response["implications"] = self._extract_bullet_points(section_text)
                break
        
        # Recommendations section
        recommendations_patterns = [
            r'(?:Recommendations:?|RECOMMENDATIONS:?)(.*?)(?:Follow-up Tests|FOLLOW-UP TESTS|Followup Tests|FOLLOWUP TESTS|$)',
            r'(?:RECOMMENDATIONS|Recommendations)(.*?)(?:FOLLOW-UP TESTS|Follow-up Tests|FOLLOWUP TESTS|Followup Tests|$)'
        ]
        
        for pattern in recommendations_patterns:
            recommendations_match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if recommendations_match:
                section_text = recommendations_match.group(1).strip()
                structured_response["recommendations"] = self._extract_bullet_points(section_text)
                break
        
        # Follow-up tests section
        followup_patterns = [
            r'(?:Follow-up Tests:?|FOLLOW-UP TESTS:?|Followup Tests:?|FOLLOWUP TESTS:?)(.*?)$',
            r'(?:FOLLOW-UP TESTS|Follow-up Tests|FOLLOWUP TESTS|Followup Tests)(.*?)$'
        ]
        
        for pattern in followup_patterns:
            followup_match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if followup_match:
                section_text = followup_match.group(1).strip()
                structured_response["followup_tests"] = self._extract_bullet_points(section_text)
                break
        
        # If we couldn't extract any meaningful sections, add the raw response
        if (not structured_response["summary"] and 
            len(structured_response["abnormal_values"]) == 0 and 
            len(structured_response["implications"]) == 0 and
            len(structured_response["recommendations"]) == 0 and
            len(structured_response["followup_tests"]) == 0):
            
            structured_response["summary"] = "Could not properly structure the model's response. Please see the raw output below."
            structured_response["raw_response"] = response_text
        
        # Additional fallback: If we at least got a summary but no sections, try to extract sections
        # by looking for numbered lines or bullet points
        if structured_response["summary"] and not any([
            structured_response["abnormal_values"],
            structured_response["implications"],
            structured_response["recommendations"],
            structured_response["followup_tests"]
        ]):
            # Try to find all bullet points or numbered items in the response
            all_bullets = re.findall(r'\n\s*(?:\d+[\.\)\-]|\-|\•)\s*(.*?)(?=\n\s*(?:\d+[\.\)\-]|\-|\•)|\Z)', 
                                    '\n' + response_text, re.DOTALL)
            
            if all_bullets:
                # Simply distribute these among the sections
                structured_response["abnormal_values"] = all_bullets
        
        return structured_response

    def _extract_bullet_points(self, text: str) -> List[str]:
        """
        Extract bullet points from a section of text.
        
        Args:
            text: Text section to process
            
        Returns:
            List of extracted bullet points
        """
        # First, filter out any "Content is blocked" text
        text = text.replace("Content is blocked", "")
        
        # Split by newlines and clean up
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        bullet_points = []
        current_point = ""
        
        for i, line in enumerate(lines):
            # Skip lines that only contain "blocked content" text
            if "is blocked" in line.lower() and len(line.split()) <= 5:
                continue
                
            # Check if this line starts a new bullet point
            if (re.match(r'^\d+[\.\)\-]', line) or  # Numbered bullet (1. or 1) or 1-)
                line.startswith('- ') or 
                line.startswith('• ')):
                
                # Save the previous point if it exists
                if current_point:
                    # Only add the point if it doesn't contain blocked content phrases
                    if not any(phrase in current_point.lower() for phrase in ["content is blocked", "is blocked content"]):
                        bullet_points.append(current_point)
                
                # Start a new point, removing the bullet marker
                if re.match(r'^\d+[\.\)\-]', line):
                    current_point = re.sub(r'^\d+[\.\)\-]\s*', '', line)
                else:
                    current_point = line[2:].strip()  # Remove "- " or "• "
            else:
                # If no bullet point, either add to the current point or start a new one
                if current_point:
                    current_point += " " + line
                else:
                    current_point = line
        
        # Add the last point if it exists and doesn't contain blocked content
        if current_point and not any(phrase in current_point.lower() for phrase in ["content is blocked", "is blocked content"]):
            bullet_points.append(current_point)
        
        # If no bullet points were extracted but we have text, use the whole text
        # after filtering any blocked content
        if not bullet_points and text.strip():
            filtered_text = text.strip()
            if not any(phrase in filtered_text.lower() for phrase in ["content is blocked", "is blocked content"]):
                bullet_points = [filtered_text]
        
        # Final cleanup to remove any remaining blocked content references
        bullet_points = [
            point.replace("Content is blocked", "").replace("content is blocked", "")
            .replace("is blocked Content", "").replace("is blocked content", "")
            .strip() for point in bullet_points
        ]
        
        # Remove any points that became empty after cleanup
        bullet_points = [point for point in bullet_points if point.strip()]
        
        return bullet_points
    
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