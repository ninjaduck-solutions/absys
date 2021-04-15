git:
  pkg.installed:
    - version: 1:2.25.1*

git-flow:
  pkg.installed:
    - version: 1.12.3*

git-flow-init:
  cmd.run:
    - name: git flow init -d
    - runas: {{ pillar['project']['user'] }}
    - cwd: /vagrant
    - unless: grep "^\[gitflow" /vagrant/.git/config >/dev/null
    - require:
      - pkg: git-flow

tig:
  pkg.installed:
    - version: 2.4.1*

git-push-default:
  git.config_set:
    - name: push.default
    - value: simple
    - user: {{ pillar['project']['user'] }}
    - global: True
