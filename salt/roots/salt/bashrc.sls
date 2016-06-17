user-bashrc:
  file.blockreplace:
    - name: {{ pillar['project']['home'] }}/.bashrc
    - marker_start: "# START managed configuration -DO-NOT-EDIT-"
    - marker_end: "# END managed configuration"
    - content: |
        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8
        export LANGUAGE=en_US.UTF-8
        export EDITOR=vim
        source ${HOME}/pyvenv/bin/activate
        if hash thefuck 2>/dev/null; then
            eval $(thefuck --alias)
        fi
        git config --get user.name >/dev/null
        if [ $? -ne 0 ]; then
            echo -n "Bitte Git Benutzernamen eingeben: "
            read USERNAME
            git config --global user.name "${USERNAME}"
        fi
        git config --get user.email >/dev/null
        if [ $? -ne 0 ]; then
            echo -n "Bitte Git E-Mail Adresse eingeben: "
            read EMAIL
            git config --global user.email "${EMAIL}"
        fi
    - template: jinja
    - append_if_not_found: True
