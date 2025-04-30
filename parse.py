import google.generativeai as genai
import os
from dotenv import load_dotenv

def parse_with_gemini(dom_chunks, parse_description):
    load_dotenv()

    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-2.0-flash-exp")

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = (
            f"You are tasked with extracting specific information from the following text content:\n\n"
            f"{chunk}\n\n"
            f"Please follow these instructions carefully:\n"
            f"1. Extract only the information that directly matches this description: {parse_description}\n"
            f"2. No Extra Content: Do not include additional text, comments, or explanations.\n"
            f"3. Empty Response: If nothing matches, return an empty string ('').\n"
            f"4. Direct Data Only: Respond only with the extracted data (no formatting).\n"
        )
        response = model.generate_content(prompt)
        parsed_results.append(response.text.strip())

        print(f"Parsed batch {i} of {len(dom_chunks)}")
    
    return "\n".join(parsed_results)
