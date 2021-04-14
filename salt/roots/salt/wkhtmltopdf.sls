wkhtmltopdf:
  pkg.installed:
    - pkgs:
      - wkhtmltopdf: 0.12.2.4*
      - xvfb: 2:1.18.4*
# Weasyprint
      - build-essential
      - python3-dev
      - python3-pip
      - python3-setuptools
      - python3-wheel
      - python3-cffi
      - libcairo2
      - libpango-1.0-0
      - libpangocairo-1.0-0
      - libgdk-pixbuf2.0-0
      - libffi-dev
      - shared-mime-info
