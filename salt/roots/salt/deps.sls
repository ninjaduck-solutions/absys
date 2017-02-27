general-pkgs:
  pkg.installed:
    - pkgs:
      - build-essential: 12*
      - gettext: 0.19.7*

postgresql-pkgs:
  pkg.installed:
    - pkgs:
      - libpq-dev: 9.5.*

lxml-pkgs:
  pkg.installed:
    - pkgs:
      - libxslt1-dev: 1.1.28*

pillow-pkgs:
  pkg.installed:
    - pkgs:
      - libtiff5-dev: 4.0.6*
      - libjpeg-dev: 8c*
      - zlib1g-dev: 1:1.2.8*
      - libfreetype6-dev: 2.6.1*
      - liblcms2-dev: 2.6*
      - libwebp-dev: 0.4.4*
