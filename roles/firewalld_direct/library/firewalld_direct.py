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

    from firewall.client import FirewallClient
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
            table=dict(required=False, default='filter'),
            chain=dict(required=True),
            priority=dict(required=False, default=0, type='int'),
            args=dict(required=True),
            type=dict(choices=['ipv4', 'ipv6', 'eb'], default='ipv4'),
            permanent=dict(type='bool', required=False, default=None),
            state=dict(choices=['present', 'absent'], required=True),
        ),
        supports_check_mode=True
    )

    if not HAVE_FIREWALLD:
        module.fail_json(msg='firewalld and the python module are required '
                             'for this module')

    if not FIREWALLD_RUNNING:
        module.fail_json(msg='firewalld is not running, and offline operations'
                             ' are not supported yet')

    table = module.params['table']
    chain = module.params['chain']
    priority = module.params['priority']
    args = module.params['args'].split(' ')
    address_type = module.params['type']
    permanent = module.params['permanent']
    state = module.params['state']

    if permanent:
        fw = FirewallClient().config().direct()
    rules = fw.getRules(ipv=address_type, table=table, chain=chain)

    changed = False
    if state == 'present':
        if (priority, args) not in rules:
            fw.addRule(ipv=address_type, table=table, chain=chain,
                       priority=priority, args=args)
            changed = True
    else:
        if (priority, args) in rules:
            fw.removeRule(ipv=address_type, table=table, chain=chain,
                          priority=priority, args=args)
            changed = True
    result = dict(changed=changed)
    module.exit_json(**result)

if __name__ == '__main__':
    main()
