# inspired by https://nigelb.me/2015-08-26-mailman-attacks.html
def list_bans(m):
    try:
        m.Lock()
        for i in m.ban_list:
            print i
    finally:
        m.Unlock()
    print ''
