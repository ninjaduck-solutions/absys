git:
  pkg.installed:
    - version: 1:2.7.4*

git-flow:
  pkg.installed:
    - version: 1.9.1*

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
    - version: 2.0.2*

git-push-default:
  git.config_set:
    - name: push.default
    - value: simple
    - user: {{ pillar['project']['user'] }}
    - global: True
