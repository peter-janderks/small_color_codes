from setuptools import setup, find_packages

setup(
    name="d3_color_codes",
    version="0.1.0",
    description="A Python package for color code simulation and analysis.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.7",
)
