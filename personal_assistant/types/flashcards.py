from pydantic import BaseModel


class Flashcard(BaseModel):
    question: str
    answer: str

if __name__ == "__main__":
    import outlines.models as models
    import outlines.text as text
    import outlines.text.generate as generate

    @text.prompt
    def prompt_with_result_format(question, response_model):
        """{{ question }}

        Please reply in the following format:

        {{ response_model | schema}}

        """

    model_name = "nomic-ai/gpt4all-j"
    revision = "v1.2-jazzy"
    model = models.transformers(model_name,  revision=revision)
    prompt = prompt_with_result_format("Write a question/answer pair about Napoleon Bonaparte.", Flashcard)
    sequence = generate.json(model, Flashcard)(prompt)
