# Class GPTAPI
#-------------
# This class will:
    # call the GPT API,
    # ask it to provide prompts for the eval axes,
    # then evaluate the responses received from the LLM we trying to asses 
    # their behavior.
###############################################################################


# Class
#------
class RateLimiter:
    """Rate limiter to prevent API throttling"""
    
    
    def __init__(self, max_calls=20, time_window=60):
        """
        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove old calls outside the time window
        while self.calls and self.calls[0] <= now - self.time_window:
            self.calls.popleft()
        
        # If at limit, wait
        if len(self.calls) >= self.max_calls:
            sleep_time = self.time_window - (now - self.calls[0]) + 1
            if sleep_time > 0:
                print(f"â³ Rate limit reached. Waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
        
        # Record this call
        self.calls.append(now)


# Class GPTAPI
#-------------
class GPTAPI:

    # Method: Constructor
    def __init__(self, api_key, rate_limit: Optional[RateLimiter] = None, api_config=None):
        openai.api_key = api_key
        config = api_config or {}
        self.rate_limiter = rate_limit or RateLimiter(
            max_calls=config.get('rate_limit_calls', 20),
            time_window=config.get('rate_limit_window', 60)
        )
        self.api_config = config        
        
        self.call_count = 0
        self.error_count = 0
    

    # Method: Call ChatGPT API
    # temperature=0.7 is the default
    def call_gpt(self, prompt, temperature=None, max_tokens=None):
        if temperature is None:
            temperature = self.api_config.get('temperature_evaluate', 0.7)
        if max_tokens is None:
            max_tokens = self.api_config.get('max_tokens_evaluate', 200)
        
        """Call with rate limiting and tracking"""
        self.rate_limiter.wait_if_needed()
        self.call_count += 1
        
        try:
            response = openai.chat.completions.create(
                model=self.api_config.get('model', 'gpt-4o'),
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
            
        except openai.RateLimitError:
            self.error_count += 1
            print(f"âš ï¸ Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
            return self.call_gpt(prompt, temperature, max_tokens)
            
        except Exception as e:
            self.error_count += 1
            print(f"âŒ API Error: {str(e)}")
            raise
    

    # Generate the needed prompts that will be evaluated
    # temperature=0.8 to make prompt generation more creative
    def generate_prompts(self, prompt):
        response = self.call_gpt(
            prompt, 
            temperature=self.api_config.get('temperature_generate', 0.8),
            max_tokens=self.api_config.get('max_tokens_generate', 200)
        )
        
        #print(f"RAW RESPONSE LENGTH: {len(response)}")  # DEBUG
        #print(f"FIRST 200 CHARS: {response[:200]}")  # DEBUG
        
        prompts = response.split('\n')
        
        prompts = [p.strip() for p in prompts if p.strip()]
    
        # If suspiciously few prompts, check for refusal
        if len(prompts) < 5:  # Threshold for suspicion
            refusal_phrases = ["I'm sorry", "I can't", "I cannot", "I apologize", "I'm unable"]
            if any(phrase in response for phrase in refusal_phrases):
                print(f"⚠️ GPT REFUSED! Only got {len(prompts)} prompts")
                print(f"   Response: {response[:100]}...")
        
        return prompts

    
    # Evaluate the base and instruct responses to ChatGPT prompts
    # temperature=0.1 to be more consistent eval
    def evaluate_response(self, prompt, max_retries=None):
        if max_retries is None:
            max_retries = self.api_config.get('max_retries', 3)
        
        for attempt in range(max_retries):
            try:
                response = self.call_gpt(
                    prompt, 
                    temperature=self.api_config.get('temperature_evaluate', 0.1),
                    max_tokens=self.api_config.get('max_tokens_evaluate', 200)
                )                
                
                # Try multiple parsing strategies
                scores = self._parse_scores(response)
                
                if scores:
                    base_score, instruct_score = scores
                    
                    # Check if GPT returned 99 (which means GPT refused to evaluate)
                    if base_score == 99 or instruct_score == 99:
                        print(f"⚠️ GPT returned sentinel value 99 in response: {response[:100]}")
                        print(f"   This likely means GPT refused to evaluate the content")
                        # Don't accept 99 as a valid score from GPT - retry with modified prompt
                        if attempt < max_retries - 1:
                            prompt += "\n\nIMPORTANT: You must provide scores 1, 2, or 3 only. If you cannot evaluate, return 2,2 as a neutral score. Do not return 99."
                            continue
                        
                    # Validate scores are in valid range
                    if 1 <= base_score <= 3 and 1 <= instruct_score <= 3:
                        return base_score, instruct_score
                    else:
                        print(f"Scores out of range: {base_score}, {instruct_score}")
                
                # If parsing failed, try more explicit prompt
                if attempt < max_retries - 1:
                    prompt += "\n\nREMINDER: Return ONLY two numbers separated by comma. Example: 2,3"
                    
            except Exception as e:
                print(f"Evaluation attempt {attempt + 1} failed: {str(e)}")
        
        # Default fallback - use 99 to indicate evaluation failure
        print(f"WARNING: Evaluation failed after {max_retries} attempts, using defaults")
        print(f"   Last response was: {response[:200] if 'response' in locals() else 'No response'}")
        
        return 99, 99 # extreme values to indicate errors
    
    
    def _parse_scores(self, response):
        """Try multiple parsing strategies"""
        
        # Strategy 1: Direct comma-separated
        if ',' in response:
            try:
                parts = response.strip().split(',')
                return int(parts[0].strip()), int(parts[1].strip())
            except:
                pass
        
        # Strategy 2: Find numbers with regex
        numbers = re.findall(r'\b[1-3]\b', response)
        if len(numbers) >= 2:
            try:
                return int(numbers[0]), int(numbers[1])
            except:
                pass
        
        # Strategy 3: Look for patterns like "Base: X, Instruct: Y"
        base_match = re.search(r'base[^0-9]*([1-3])', response, re.IGNORECASE)
        instruct_match = re.search(r'instruct[^0-9]*([1-3])', response, re.IGNORECASE)
        
        if base_match and instruct_match:
            try:
                return int(base_match.group(1)), int(instruct_match.group(1))
            except:
                pass
        
        return None

    
    def get_stats(self):
        """Get API usage statistics"""
        return {
            'total_calls': self.call_count,
            'errors': self.error_count,
            'success_rate': (1 - self.error_count/self.call_count) * 100 if self.call_count > 0 else 0
        }


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""
