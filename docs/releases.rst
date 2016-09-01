********
Releases
********

Since `git-flow <https://github.com/nvie/gitflow/>`_ is used to organize the
work in feature branches it will also be used to create the releases. Before
you start a new release make sure all feature branches you want to be part of
the release have been merged into the ``develop`` branch.

Start a new release branch
==========================

Let's assume all features for the next release are merged into the ``develop``
branch and the next release should be version ``1.0.0``.

So the first step is to start a new release branch:

::

    $ git flow release start 1.0.0

After that you will be on the newly created ``release/1.0.0`` branch.

Prepare the release branch
==========================

The next thing to do is to update the version numbers using
`bumpversion <https://github.com/peritus/bumpversion>`_. Since this is a new
major release we need to pass the ``major`` keyword to :program:`bumpversion`.
Other possible keyword for the version number part are ``patch`` for bugfix
releases (example: ``0.8.2``) and ``minor`` for minor releases (example
``0.9.0``).

::

    $ bumpversion major

Also update the model graphs:

::

    $ make modelgraph

Now run the test suite to make sure everything works as expected:

::

    $ make clean test-all

Fix any errors or failures that occur directly in the release branch.

Finish the release branch
=========================

Now you can finish the release branch:

::

    $ git flow release finish 1.0.0

Now you change to the ``master`` branch and push it together with the new tag
``1.0.0`` to the Git remote:

::

    $ git checkout master
    $ git push origin master
    $ git push origin master --tags

After that create the distribution:

::

    $ git checkout 1.0.0
    $ make dist

Finally change back to the ``develop`` branch and push it to the Git remote:

::

    $ git checkout develop
    $ git push origin develop

