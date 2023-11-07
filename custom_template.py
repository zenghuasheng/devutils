from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator
from langchain.agents import mrkl

class CustomPromptTemplate(StringPromptTemplate, BaseModel):
    """A custom prompt template."""

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """Validate the input variables."""
        # Add validation logic if needed
        return v

    def format(self, **kwargs) -> str:
        # Generate the prompt using the input variables
        # Add your prompt generation logic here
        return "Your formatted prompt"

    def _prompt_type(self):
        return "custom-prompt"



custom_template = CustomPromptTemplate(input_variables=["variable1", "variable2"])

# Generate a prompt using the custom template
prompt = custom_template.format(variable1="value1", variable2="value2")
print(prompt)