# -*- coding: utf-8 -*-

import ast
import io
import re
from setuptools import setup


def _get_version():
    """Extract version from up2minio.py."""
    version_re = re.compile(r"__version__\s+=\s+(.*)")

    with open("up2minio.py", "r", encoding="utf-8") as fh:
        version = ast.literal_eval(version_re.search(fh.read()).group(1))
    return str(version)


def _get_author():
    """Extract author name and email from up2minio.py."""
    author_re = re.compile(r"__author__\s+=\s+(.*)")
    mail_re = re.compile(r"(.*)\s<(.*)>")

    with open("up2minio.py", "r", encoding="utf-8") as fh:
        author = ast.literal_eval(author_re.search(fh.read()).group(1))

    match = mail_re.match(author)
    return (match.group(1), match.group(2)) if match else (author, None)


def _get_readme():
    """Read the README.rst file as the long description."""
    with io.open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


version = _get_version()
(author, email) = _get_author()

setup(
    name="up2minio",
    version=version,
    license="Apache 2.0",
    author=author,
    author_email=email,
    description="将图片上传至 Minio 的扩展模块",
    long_description=_get_readme(),
    long_description_content_type="text/x-rst",  # 显式指定 README 文件类型
    url="https://www.dfql.io",
    py_modules=["up2minio"],
    zip_safe=False,
    install_requires=["minio>=7.1.10"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Graphics",
    ],
    keywords="sapic minio storage hook",
    python_requires=">=3.6",  # 指定最低 Python 版本
)
