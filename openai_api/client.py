import openai

client = openai.OpenAI(api_key="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")

def generate_course_description(course_name):
    #promt_pronto = f'Crie uma descrição detalhada do curso "{course_name}". Inclua os objetivos do curso, tópicos abordados, e o público-alvo.'
    prompt = f"Descreva de forma atrativa o curso chamado '{course_name}':"
    
    try:
        # Chamada para a API OpenAI     
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ou "gpt-4" se você tiver acesso
            messages=[
                {"role": "system", "content": "Você é um redator de cursos criativo."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar descrição do curso: {e}")
        return "Descrição não disponível no momento."