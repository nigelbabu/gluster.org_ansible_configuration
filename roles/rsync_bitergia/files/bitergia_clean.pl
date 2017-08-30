#!/usr/bin/perl
use strict;
use warnings;

use Digest::MD5;

my $DIR = '/srv/bitergia/logs/httpd';
chdir($DIR) or die "Can't change dir to $DIR";

foreach (<$DIR/*>) {
    #skip access_log   
    next if $_ !~ m/^\S+-\d{4}/;
    
    next if $_ =~ m/.*.gz$/;
    if( -f $_ . ".gz") {
        my $ctx = Digest::MD5->new;
        open(my $FILE, $_) or die "can't open $_\n";
        $ctx->addfile($FILE);
        my $md5sum = $ctx->hexdigest();

        my $ctx_gz = Digest::MD5->new;
        open(my $FILE_GZ, "zcat $_.gz |") or die "can't open $_.gz";
        $ctx_gz->addfile($FILE_GZ);
        my $md5sum_gz = $ctx_gz->hexdigest();

        if ($md5sum_gz eq $md5sum) {
            unlink($_) or die "Couldn't remove $_";
        } else {
            print "Something fishy happened on $_, removing for recompression\n";
            unlink("$_.gz") or die "Couldn't remove $_";
        }
    } else {
        `gzip $_`;
    }
}
