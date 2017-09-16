# taken from https://nigelb.me/2015-08-26-mailman-attacks.html
def ban(m, address):
    try:
        m.Lock()
        if address not in m.ban_list:
            m.ban_list.append(address)
        m.Save()
    finally:
        m.Unlock()
