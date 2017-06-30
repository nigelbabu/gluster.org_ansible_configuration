#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from xml.etree import ElementTree
try:
    import libvirt
except ImportError:
    HAS_VIRT = False
else:
    HAS_VIRT = True


def change_interface(module, name, bridge, add):
    virt_xml_path = module.get_bin_path('virt-xml', True)

    cmd = [virt_xml_path, name]
    if add:
        cmd.append('--add-device')
    else:
        cmd.append('--remove-device')
    cmd.extend(['-w', 'bridge=%s' % bridge, '--update'])
    (rc, out, err) = module.run_command(cmd)
    if rc != 0:
        module.fail_json(
            msg="virt-xml failed", stderr=err, stdout=out
        )

    return {'changed': True}


def main():

    module = AnsibleModule(argument_spec=dict(
        name=dict(required=True, aliases=['guest']),
        bridge=dict(required=True),
        state=dict(default='present', choices=['present', 'absent']),
        uri=dict(default='qemu:///system'),
    ))

    if not HAS_VIRT:
        module.fail_json(
            msg='The libvirt module is not importable.\
                 Check the requirements.'
        )

    uri = module.params.get('uri')
    name = module.params.get('name')
    bridge = module.params.get('bridge')
    state = module.params.get('state')

    conn = libvirt.open(uri)
    vm = conn.lookupByName(name)
    xmldesc = vm.XMLDesc(0)
    root = ElementTree.fromstring(xmldesc)
    has_interface = len(root.findall("devices/interface[@type='bridge']/source[@bridge='%s']" % bridge)) > 0

    result = {
        'changed': False,
    }

    if state == 'present' and not has_interface:
        result = change_interface(module, name, bridge, True)
    elif state == 'absent' and has_interface:
        result = change_interface(module, name, bridge, False)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
