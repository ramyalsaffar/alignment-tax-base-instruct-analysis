# Class ModelManager
#-------------------
# This class will:
    # load the LLM models that are locally-stored,
    # get the LLM responses after feeding it the prompts. 
# Please note that there is no need to reload the models everytime we feed it a
# prompt, because it is already stateless and do not save the conversation.
# This is important for this alignment tax project to make the analysis and 
# conclusions fair.
# Re-loading the models for every prompt will not add any benefits, and it will
# slow down the processing speed.
###############################################################################


# Class ModelManager
#-------------------
class ModelManager:
    
    def __init__(self, model_config=None):
        self.models = {}
        self.config = model_config or {}

        # Context tracking
        self.context_usage = {}


    def _ensure_model_exists(self, model_path):
        """
        Ensure model file exists. If in AWS mode and model doesn't exist,
        try to download from S3.

        Args:
            model_path: Path to model file

        Returns:
            True if model exists or was downloaded successfully
        """
        if Path(model_path).exists():
            return True

        # If not in AWS mode, can't do anything
        if os.getenv('ENVIRONMENT') != 'aws':
            return False

        # Try to download from S3
        try:
            print(f"📥 Model not found locally, attempting S3 download...")
            from S3Handler import S3Handler

            # Extract filename from path
            filename = os.path.basename(model_path)
            s3_key = f"models/{filename}"

            # Create directory if needed
            os.makedirs(os.path.dirname(model_path), exist_ok=True)

            s3_handler = S3Handler()
            s3_handler.download_file(s3_key, str(model_path))
            print(f"✅ Model downloaded from S3")
            return True

        except Exception as e:
            print(f"❌ Model download failed: {e}")
            return False


    def load_model(self, model_path, model_name):

        """Load model with error handling and S3 download support"""
        if model_name not in self.models:
            try:
                print(f"Loading {model_name}...")

                # Ensure model exists (downloads from S3 if needed in AWS mode)
                if not self._ensure_model_exists(model_path):
                    raise FileNotFoundError(f"Model file not found: {model_path}")
                
                self.models[model_name] = Llama(
                    model_path=str(model_path),
                    n_ctx=self.config.get('n_ctx', 2048),
                    n_threads=self.config.get('n_threads', 4),
                    n_gpu_layers=self.config.get('n_gpu_layers', 32),
                    n_batch=self.config.get('n_batch', 512),
                    use_mlock=self.config.get('use_mlock', False), # Prevent memory locking issues
                    seed=self.config.get('seed', -1),
                    verbose=self.config.get('verbose', False)
                    )
                print(f"✓ {model_name} loaded successfully")
                
            except Exception as e:
                print(f"✗ Failed to load {model_name}: {str(e)}")
                raise
    
    
    def get_response(self, model_name, prompt, max_retries=None):
        
        """Get response with retry logic and error handling"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not loaded")
            
        if max_retries is None:
            max_retries = self.config.get('max_retries', 3)
            
        # Reset context if getting too full
        prompt_tokens = len(prompt.split())  # Rough estimate
        if prompt_tokens > 1500:  # Leave buffer in 2048 context
            prompt = prompt[:6000]  # Truncate prompt if too long
        
        for attempt in range(max_retries):
            try:
                
                # Clear KV cache periodically to prevent decode errors
                # Clear KV cache before retry
                if hasattr(self.models[model_name], 'reset'):
                    self.models[model_name].reset()
                    
                elif hasattr(self.models[model_name], 'llama_kv_cache_clear'):
                    self.models[model_name].llama_kv_cache_clear()
                
                response = self.models[model_name](
                    prompt,
                    max_tokens=self.config.get('max_tokens', 512),
                    temperature=self.config.get('temperature', 0.7),
                    top_p=self.config.get('top_p', 1.0),
                    repeat_penalty=self.config.get('repeat_penalty', 1.1),
                    stop=self.config.get('stop', ["</s>", "\n\n"]),
                    echo=self.config.get('echo', False)
                    )
                
                # Validate response
                text = response.get("choices", [{}])[0].get("text", "").strip()
                if not text:
                    raise ValueError("Empty response received")
                
                return text
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed after {max_retries} attempts: {str(e)}")
                    return "[ERROR: Failed to generate response]"
                time.sleep(2 * attempt)  # Brief incremental pause before retry


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""
