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


def change_cpu(module, name, model, feature, add):
    virt_xml_path = module.get_bin_path('virt-xml', True)

    cmd = [virt_xml_path, name, '--edit', '--cpu']
    if add:
        feature = model + ',+' + feature
    else:
        feature = model + ',-' + feature

    cmd.extend([feature])
    (rc, out, err) = module.run_command(cmd)
    if rc != 0:
        module.fail_json(
            msg="virt-xml failed", stderr=err, stdout=out
        )

    return {'changed': True}


def main():

    module = AnsibleModule(argument_spec=dict(
        name=dict(required=True, aliases=['guest']),
        feature=dict(required=True),
        model=dict(default=''),
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
    feature = module.params.get('feature')
    model = module.params.get('model')
    state = module.params.get('state')

    conn = libvirt.open(uri)
    vm = conn.lookupByName(name)
    xmldesc = vm.XMLDesc(0)
    root = ElementTree.fromstring(xmldesc)
    if model == '':
        model = root.findall('cpu/model')[0].text

    has_feature = len(root.findall("cpu/feature[@name='%s']" % feature)) > 0
    result = {
        'feature': len(root.findall("cpu/feature[@name='%s']" % feature)),
        'feature_': feature,
        'changed': False,
    }

#    if state == 'present' and not has_feature:
#        result = change_cpu(module, name, model, feature, True)
#    elif state == 'absent' and has_feature:
#        result = change_cpu(module, name, model, feature, False)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
