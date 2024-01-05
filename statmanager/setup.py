# Copyright (C) 2023 Changseok Lee 


from setuptools import setup, find_packages

with open(r'statmanager\README.md', encoding='utf-8') as f:
    description_markdown = f.read()

setup(
    name='statmanager-kr',
    version='1.8.1.4',
    license='MIT',
    long_description=description_markdown,
    long_description_content_type='text/markdown',
    description='Open-source statistical package in Python based on the Pandas',
    author='ckdckd145',
    author_email='ckdckd145@gmail.com',
    url='https://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4',
    download_url='https://github.com/ckdckd145/statmanager-kr',
    install_requires=['pandas', 'scipy', 'statsmodels', 'matplotlib', 'seaborn', 'XlsxWriter'],
    packages=find_packages(),
    keywords=['statistic', 'socialscience', 'stats',],
    python_requires='>=3.0',
    package_data={
        'statmanager' : ['*.csv', '*.png'],
        },
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.13',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: MacOS', 
        'Natural Language :: Korean',
        'Natural Language :: English',        
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',
    ],
)