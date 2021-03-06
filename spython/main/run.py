
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot
from spython.utils import stream_command
import json

def run(self, 
        image = None,
        args = None,
        app = None,
        sudo = False,
        writable = False,
        contain = False,
        bind = None,
        stream = False,
        nv = False):

    '''
        run will run the container, with or withour arguments (which
        should be provided in a list)
    
        Parameters
        ==========
        image: full path to singularity image
        args: args to include with the run 
        app: if not None, execute a command in context of an app
        writable: This option makes the file system accessible as read/write
        contain: This option disables the automatic sharing of writable
                 filesystems on your host
        bind: list or single string of bind paths.
              This option allows you to map directories on your host system to
              directories within your container using bind mounts
        stream: if True, return <generator> for the user to run
        nv: if True, load Nvidia Drivers in runtime (default False)
    '''
    from spython.utils import check_install
    check_install()

    cmd = self._init_command('run')
   
    # nv option leverages any GPU cards
    if nv is True:
        cmd += ['--nv']

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    # If an instance is provided, grab it's name
    if isinstance(image, self.instance):
        image = image.get_uri()

    # Does the user want to use bind paths option?
    if bind is not None:
        cmd += self._generate_bind_list(bind)

    # Does the user want to run an app?
    if app is not None:
        cmd = cmd + ['--app', app]

    cmd = cmd + [image]

    # Conditions for needing sudo
    if writable is True:
        sudo = True
        
    if args is not None:        
        if not isinstance(args, list):
            args = args.split(' ')
        cmd = cmd + args

    if stream is False:
        result = self._run_command(cmd, sudo=sudo)
    else:
        return stream_command(cmd, sudo=sudo)

    if result:
        result = result.strip('\n')

        try:
            result = json.loads(result)
        except:
            pass
        return result
