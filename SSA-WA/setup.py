from setuptools import find_packages, setup

setup(
    name="EsquemaBasico",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",  # Agrega otras dependencias según el archivo requirements.txt
    ],
    entry_points={
        "console_scripts": [
            "esquemabasico=EsquemaBasico.dbEsquemabasico:app.run",  # Cambia según tu archivo de entrada principal
        ]
    },
    author="Tu Nombre",
    author_email="tuemail@example.com",
    description="Descripción del paquete Flask",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
    ],
    python_requires=">=3.6",
)