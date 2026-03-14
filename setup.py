from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="task-management-system",
    version="1.0.0",
    author="Victor",
    author_email="victor@example.com",
    description="A comprehensive task management system with CLI, API, and web interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/victorcode/task-management-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "schedule>=1.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "notifications": [
            "win10toast>=0.9",
        ],
        "email": [
            "secure-smtplib>=0.1.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "task-manager=main:main",
            "task-cli=cli:main",
            "task-api=api:run_api",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.css", "*.js", "*.json"],
    },
    project_urls={
        "Bug Reports": "https://github.com/victorcode/task-management-system/issues",
        "Source": "https://github.com/victorcode/task-management-system",
        "Documentation": "https://github.com/victorcode/task-management-system/wiki",
    },
    keywords="task management productivity cli api dashboard",
    zip_safe=False,
)
