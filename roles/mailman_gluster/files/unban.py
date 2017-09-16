# adapted from https://nigelb.me/2015-08-26-mailman-attacks.html
def unban(m, address):
    try:
        m.Lock()
        if address in m.ban_list:
            m.ban_list.remove(address)
        m.Save()
    finally:
        m.Unlock()
