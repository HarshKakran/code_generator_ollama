import ollama

def code_snippet_generator(task_description:str, model_name: str = 'deepseek-coder:6.7b'):
    prompt = """
    You are a coding assistant that can generate code snippets based on the task description and programming language provided. The task description is as follows: "{task_description}".
    Provide only the code, without any additional explanation or markdown formatting unless it's part of the code itself (e.g., comments).
    """.format(task_description=task_description, model_name=model_name)

    print(f"\nSending the prompt to the model...")
    print(prompt)
    print("---------------------------------------")

    full_response_content = []

    try:
        generated_code: str
        stream = ollama.generate(
            model=model_name,
            prompt=prompt,
            stream=True,
            options={
                "temperature": 0.9
            }
        )
        
        for chunks in stream:
            if 'response' in chunks:
                token = chunks['response']
                print(token, end='', flush=True)
                full_response_content.append(token)
            if chunks.get('done'):
                if chunks.get('total_duration'):
                     print(f"\nGeneration complete. Total duration: {chunks['total_duration']/1E9:.2f}s")
                else:
                    print("\nGeneration complete.")

        generated_code = "".join(full_response_content).strip()

        if generated_code.startswith("```"): # Generic ```
            generated_code = generated_code.split("\n", 1)[1]
            if generated_code.endswith("```"):
                generated_code = generated_code[:-3].strip()


        print("\n--- Generated Code ---")
        print(generated_code)
        print("----------------------")
        return generated_code
    except Exception as e:
        print(f"\nError occurred while generating code:\n{e}")
        return None
    
if __name__ == "__main__":
    model_name = input("Enter the name of the model to use (default: 'deepseek-coder:6.7b'): ") or "deepseek-coder:6.7b"
    task_description = input("Please describe the task you want me to perform:\n")

    code_snippet_generator(task_description, model_name)

