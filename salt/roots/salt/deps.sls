general-pkgs:
  pkg.installed:
    - pkgs:
      - build-essential: 12*
      - gettext: 0.19.8*

postgresql-pkgs:
  pkg.installed:
    - pkgs:
      - libpq-dev: 12.6*

lxml-pkgs:
  pkg.installed:
    - pkgs:
      - libxslt1-dev: 1.1.34*

pillow-pkgs:
  pkg.installed:
    - pkgs:
      - libtiff5-dev: 4.1.0*
      - libjpeg-dev: 8c*
      - zlib1g-dev: 1:1.2.11*
      - libfreetype6-dev: 2.10.1*
      - liblcms2-dev: 2.9*
      - libwebp-dev: 0.6.1*
