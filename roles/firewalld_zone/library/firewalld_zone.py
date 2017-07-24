#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Michael Scherer (misc@zarb.org)

#TODO DOCUMENTATION, example, license

from ansible.module_utils.basic import AnsibleModule

HAVE_FIREWALLD = True
FIREWALLD_RUNNING = True
try:
    import firewall.config
    FW_VERSION = firewall.config.VERSION

    from firewall.client import FirewallClient, FirewallClientZoneSettings
    try:
        fw = FirewallClient()
        fw.getDefaultZone()
    except AttributeError:
        FIREWALLD_RUNNING = False
except ImportError:
    HAVE_FIREWALLD = False


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            state=dict(choices=['present', 'absent'], required=True),
            no_reload=dict(type='bool', default='no'),
        ),
        supports_check_mode=False
    )

    if not HAVE_FIREWALLD:
        module.fail_json(msg='firewalld and the python module are required '
                             'for this module')

    if not FIREWALLD_RUNNING:
        module.fail_json(msg='firewalld is not running, and offline operations'
                             ' are not supported yet')

    name = module.params['name']
    state = module.params['state']
    no_reload = module.params['no_reload']

    fw = FirewallClient().config()
    zones = fw.getZoneNames()

    changed = False
    if state == 'present':
        if name not in zones:
            fw.addZone(name, FirewallClientZoneSettings())
            changed = True
    else:
        if name in zones:
            z = fw.getZoneByName(name)
            z.remove()
            changed = True
    if changed and not no_reload:
        FirewallClient().reload()

    result = dict(changed=changed)
    module.exit_json(**result)

if __name__ == '__main__':
    main()
