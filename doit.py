#!/usr/bin/env python3
#import subprocess ## < FCK THIS screws up my stdin beyond repair
import os
import os.path
import arrow
import sys
import json

af = 4

start = arrow.get("2020-07-01T00:00:00Z")
end =   arrow.get("2020-07-08T00:00:00Z")

# json output
jout = open("netdiff.%s.%s.v%s.jsonf" % (start.timestamp, end.timestamp, af) ,'w')
# csv output
outf = open("netdiff.%s.%s.v%s.csv" % (start.timestamp,end.timestamp,af), 'w', buffering=1)

def che_che_che_changes( ts, t1, t2):

    d = {'ts': ts} # data struct that we put to json

    p1 = set( t1.keys() )
    p2 = set( t2.keys() )

    drop_set = p2 - p1 # prefixes
    add_set  = p1 - p2 # prefixes

    d['dropped_pfxes'] = sorted( list( drop_set ) )
    d['added_pfxes'] = sorted( list( add_set ) )

    drop_asn_set = set()
    add_asn_set = set()

    for dpfx in drop_set:
        for a in t2[dpfx]: # set of origins
            drop_asn_set.add( a )
        
    for apfx in add_set:
        for a in t1[apfx]: # set of origins 
            add_asn_set.add( a )

    d['asns_dropped_pfxes'] = sorted( list( drop_asn_set ) )
    d['asns_added_pfxes'] = sorted( list( add_asn_set ) )
    
    intersection = p1 & p2
    change_cnt = 0
    change_asn_set = set()
    change_pfx_set = set()
    for pfx in intersection:
        if t1[pfx] != t2[pfx]:
            change_pfx_set.add( pfx )
            for a in t1[pfx]:
                change_asn_set.add( a )
            for a in t2[pfx]:
                change_asn_set.add( a )
            change_cnt += 1
    d['asns_changed_pfxes'] = sorted( list( change_asn_set ) )
    d['changed_pfxes'] = sorted( list( change_pfx_set ) )

    json.dump( d, jout ) # per line
    print("", file=jout) # per line
    return len( drop_set), len( add_set ), change_cnt, len( drop_asn_set ), len( add_asn_set ), len( change_asn_set ), len( add_asn_set | drop_asn_set | change_asn_set )

now = start
p2o_now = {}
p2o_last = {}

while now <= end:
    ts = now.timestamp
    fname = "./data/tbl.%s" % (ts,)
    cmd = "echo '+dc RIS_RIB_V +xt %s -M 0/0 +S +M +T +minpwr 50' | nc inrdb-1.ripe.net 5555 > %s" % ( ts, fname) # 50 to reduce multi origin
    ###DEBUG cmd = "/Users/emile/bin/ido +dc RIS_RIB_V +xt %s -M 193/8 +S +M +T +minpwr 50 > ./data/tbl.%s" % ( ts, ts ) # 50 to reduce multi origin
    print( now,ts,cmd , file=sys.stderr )
    ###### process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if not os.path.isfile(fname):
        os.system( cmd )
    with open("./data/tbl.%s" % ts) as inf:
    #while True:
    #        output = process.stdout.readline()
    #        if output == '' and process.poll() is not None:
    #            break
    #        if output:
    #            output = str( output )
    #
        for output in inf:
                if output == '\n':
                    continue
                line = output.rstrip('\n')
                f = line.split('|')
                if len(f) < 4:
                    if len(f) > 1:
                        print( "WAH?", f, file=sys.stderr )
                    continue
                pfx = f[2]
                asn = f[3]
                p2o_now.setdefault( pfx, set() )
                p2o_now[ pfx ].add( asn )
    ### rc = process.poll()
    #print rc
    #print >>sys.__stderr__, " pflast:%s pfnow: %s" % ( len( p2o_last.keys() ), len( p2o_now.keys() ) )
    pfx_cnt = len( p2o_now.keys() )
    if len( p2o_last.keys() ) > 0:
        output = che_che_che_changes( ts, p2o_last, p2o_now )
        print("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (ts, pfx_cnt, output[0], output[1], output[2], output[3], output[4], output[5], output[6]), file=outf)
    now = now.shift(hours=+8)
    p2o_last = p2o_now
    p2o_now = {}
