git:
  pkg:
    - installed

git-flow:
  pkg:
    - installed

git-flow-init:
  cmd.run:
    - name: git-flow init -d
    - runas: {{ pillar['project']['user'] }}
    - require:
      - pkg: git-flow

tig:
  pkg:
    - installed

git-push-default:
  git.config_set:
    - name: push.default
    - value: simple
    - user: {{ pillar['project']['user'] }}
    - global: True
