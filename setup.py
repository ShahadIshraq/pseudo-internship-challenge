from setuptools import find_packages, setup

setup(
    name="email-automation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.3",
        "pytest-mock>=3.12.0",
        "google-auth>=2.23.4",
        "google-auth-oauthlib>=1.1.0",
        "google-auth-httplib2>=0.1.1",
        "google-api-python-client>=2.108.0",
        "email-validator>=2.1.0",
    ],
    python_requires=">=3.8",
)
