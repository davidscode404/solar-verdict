import os
from groq import Groq

def llama_prompt(prompt):
    """
    Process the given prompt using the Groq API.
    
    Args:
        prompt (str): The prompt text to process
        
    Returns:
        str: The AI response
    """
    try:
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Error processing prompt: {str(e)}"

if __name__ == "__main__":
    # For testing purposes
    test_prompt = "This location has an annual average of 17.34 air temperature, 214.83 DNI and 186.17 GHI. VERY BRIEFLY, how much money and energy could one save by installing solar panels?"
    print(llama_prompt(test_prompt))