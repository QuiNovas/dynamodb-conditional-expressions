import setuptools
import io

setuptools.setup(
    name='dynamodb-ce',
    version='0.0.1',
    description='A parser for DynamoDB conditional expressions that returns a truthy function',
    author='Joseph Wortmann',
    author_email='jwortmann@quinovas.com',
    url='https://github.com/QuiNovas/dynamodb-conditional-expressions',
    license='Apache 2.0',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    packages = ['dynamodb_ce'],
    install_requires = [ 'sly', 'boto3' ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
)
