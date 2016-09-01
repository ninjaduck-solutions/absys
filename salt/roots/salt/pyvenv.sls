include:
  - python3

pyvenv:
  cmd.run:
    - name: python3 -m venv {{ pillar['project']['home'] }}/pyvenv
    - runas: {{ pillar['project']['user'] }}
    - require:
      - sls: python3
