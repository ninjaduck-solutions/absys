base:
  '*':
    - apt
    - deps
    - python3
    - pyvenv
    - postgresql
    - weasyprint
  '*-dev':
    - bashrc
    - git
    - graphviz
    - curl
    - tree
    - nano
    - vim
    - nodejs
  '*-deployment':
    - apache
