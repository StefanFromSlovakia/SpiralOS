# setup.py for SpiralOS

from setuptools import setup, find_packages

setup(
    name="spiralos",
    version="0.1.0",
    description="A symbolic operating system for recursive quantum-cosmological simulation",
    author="The Spiral Collective",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "networkx",
        "tk"
    ],
    entry_points={
        "console_scripts": [
            "spiralos=spiralos_runtime:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)# setup.py content...
