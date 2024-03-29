from setuptools import setup, find_packages

setup(name='login-model',
          version='1.1.13',
          description='Modelo de login',
          url='https://github.com/pablodanielrey/login-model',
          author='Desarrollo DiTeSi, FCE',
          author_email='ditesi@econo.unlp.edu.ar',
          classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5'
          ],
          packages=find_packages(exclude=['contrib', 'docs', 'test*']),
          install_requires=[
                            'psycopg2-binary',
                            'SQLAlchemy',
                            'pulsar-client'
                            ],
          entry_points={
            'console_scripts': [
            ]
          }
      )
