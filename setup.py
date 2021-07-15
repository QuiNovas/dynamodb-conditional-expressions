import setuptools
import io

setuptools.setup(
    name="dynamodb-ce",
    version="0.0.5",
    description="A compiler for DynamoDB conditional expressions that returns an executable truthy function",
    author="Joseph Wortmann",
    author_email="jwortmann@quinovas.com",
    url="https://github.com/QuiNovas/dynamodb-conditional-expressions",
    license="Apache 2.0",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=["dynamodb_ce"],
    install_requires=["simplejson", "sly", "boto3"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
)
