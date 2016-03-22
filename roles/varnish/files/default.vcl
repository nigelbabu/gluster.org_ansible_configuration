# Configuration file managed by salt
# Do not edit directly on the server, as salt will revert it
# 
backend default {
  .host = "127.0.0.1";
  .port = "8080";
}

sub vcl_recv {
    # Deny access to the WordPress XML-RPC API
    if (req.url == "/xmlrpc.php") {
        error 404 "Not Found.";
    }

    # Bypass the cache for these things
    if (req.http.host == "blog.gluster.org" 
        || req.http.host == "planet.gluster.org"
        || ( req.url ~ "^/community/documentation" && ! req.url ~ "^/community/documentation/skins/gluster" )
        || req.url ~ "^/mailman"
       ) {
        return (pass);
    }

    # Everything else gets cached.  Strip cookies from request to prevent duplicates in cache.
    unset req.http.cookie;
}

sub vcl_fetch {
    # Expire cached objects after one hour
    set beresp.ttl = 3600s;
}
