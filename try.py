from paperqa import Settings, ask

local_llm_config = dict(
    model_list=[
        dict(
            model_name="moren",
            litellm_params=dict(
                model="deepseek/deepseek-chat",
                api_base="https://api.deepseek.com",
                api_key="sk-027ac6afb5bc4cfb8ccb0b51fc3c5b26",
                temperature=0.1,
                frequency_penalty=1.5,
                max_tokens=512,
                set_verbose=True,  # Add this line to enable verbose mode
            ),
        )
    ]
)

answer = ask(
    "What manufacturing challenges are unique to bispecific antibodies?",
    settings=Settings(
        llm="moren",
        llm_config=local_llm_config,
        summary_llm="moren",
        summary_llm_config=local_llm_config,
        embedding="text-embedding-3-small",
    ),
)
