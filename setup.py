import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

REPO_NAME = "Conversational_AI_Agent"
AUTHOR_USER_NAME = "Group 9"
SRC_REPO = "src"
AUTHOR_EMAIL = "hopjetair@gmail.com"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A project for Convo_AI App",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "black>=23.12.0",
        "boto3>=1.39.4",
        "botocore>=1.39.4",
        "faiss-cpu>=1.11.0",
        "fastapi>=0.109.0",
        "httpx>=0.28.1",
        "isort>=5.13.0",
        "joblib>=1.5.1",
        "langchain>=0.1.0",
        "langchain-community>=0.3.26",
        "langgraph>=0.0.20",
        "langsmith>=0.0.69",
        "mypy>=1.8.0",
        "openai>=1.90.0",
        "peft>=0.15.2",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.9.1",
        "pymupdf>=1.26.1",
        "pytest>=7.4.0",
        "python-dotenv>=1.0.0",
        "sentence-transformers>=4.1.0",
        "streamlit>=1.31.0",
        "torch>=2.1.0",
        "transformers>=4.36.0",
        "typing-extensions>=4.14.0",  # ✅ NOT `typing`
        "uvicorn>=0.27.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust if needed
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
