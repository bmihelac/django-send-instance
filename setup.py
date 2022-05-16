from setuptools import setup, find_packages
import os


VERSION = __import__("send_instance").__version__

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Programming Language :: Python :: 3',
]

setup(
    name="django-send-instance",
    description="Easily send model instances as e-mails",
    long_description=open(os.path.join(os.path.dirname(__file__), 
        'README.rst')).read(),
    version=VERSION,
    author="Informatika Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://github.com/bmihelac/django-send-instance",
    packages=find_packages(exclude=["example", "example.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=3.2,<4',
    ],
)

