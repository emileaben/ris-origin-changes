#!/usr/bin/env python3
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import arrow
import sys
import glob

x=[]
yo=[]
ya=[]
yr=[]

aa=[]
ar=[]
ac=[]
a_all=[]

processed_ts = set() ## skip if it is already processed
start_time = arrow.get('2019-12-01').timestamp
for fname in sorted( glob.glob("netdiff.*.csv") ):
  with open(fname) as inf:
    for line in inf:
        line = line.rstrip('\n')
        f = line.split(",")
        ts = f[0]
        ar_ts = arrow.get( int(ts) )
        if int(ts) < start_time:
            continue
        if ts in processed_ts: # skip if already processed (there are duplicates potentially)
            continue
        processed_ts.add( ts )
        pfx_cnt = int( f[1] )
        pfx_add_cnt = int( f[2] )
        pfx_rem_cnt = int( f[3] )
        org_cng_cnt = int( f[4] )

        asn_add_cnt = int( f[5] )
        asn_rem_cnt = int( f[6] )
        asn_cng_cnt = int( f[7] )
        all_asn_cnt = int( f[8] )

        #x.append( ts )
        x.append( ar_ts.datetime )
        yo.append( org_cng_cnt )
        yr.append( pfx_rem_cnt )
        ya.append( pfx_add_cnt )

        ## asns
        aa.append( asn_add_cnt )
        ar.append( asn_rem_cnt )
        ac.append( asn_cng_cnt )
        a_all.append( all_asn_cnt )


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n



fig,ax = plt.subplots(figsize=[20,5])
fig.suptitle('BGP prefix changes', fontsize=20 )
ax.xaxis.set_major_locator( mdates.WeekdayLocator() )
ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d') )
ax.xaxis.set_minor_locator( mdates.DayLocator() )
ax2 = ax.twinx()
plt.ylabel('Volume')
plt.xlabel('Time')
#ax.set_xticks(map(lambda x: x*86400, range(0,7) ) )
#ax.set_xticklabels( ('Mon','Tue','Wed','Thu','Fri','Sat','Sun') )
#for wknr in sorted( time_by_wk.keys() ):
#    lab = wknr_to_lab( wknr )
#ax.plot(time_by_wk[ wknr ], vals_by_wk[ wknr ], c=toclr( wknr, wn_max ), alpha=0.8, label=lab )
ax.plot(x,ya, label='additions')
ax.plot(x,yr, label='removals')
ax2.plot(x,yo, label='changes', c='green')
plt.grid(axis='x')
plt.legend()
fig.savefig("orig_change.png")
ax.set_yscale('log')
ax2.set_yscale('log')
fig.savefig("orig_changes.log.png")

fig,ax = plt.subplots(figsize=[20,5])
ax.xaxis.set_major_locator( mdates.WeekdayLocator() )
ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d') )
ax.xaxis.set_minor_locator( mdates.DayLocator() )
ax.set_ylim([0,1000])
fig.suptitle('ASNs with BGP prefix changes', fontsize=20, backgroundcolor= 'silver')
plt.ylabel('Nr of ASNs')
plt.xlabel('Time')
ax.plot(x,aa, label='added prefixes', linewidth=2.0)
ax.plot(x,ar, label='removed prefixes', linewidth=2.0)
ax.plot(x,ac, label='origin changes', linewidth=2.0)
plt.legend()
fig.autofmt_xdate()
plt.grid(axis='x')
plt.tight_layout()
fig.savefig("nets_w_orig_change_details.png")

fig,ax = plt.subplots(figsize=[20,5])
ax.xaxis.set_major_locator( mdates.WeekdayLocator() )
ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d') )
ax.xaxis.set_minor_locator( mdates.DayLocator() )
ax.set_ylim([0,1000])
fig.suptitle('ASNs with BGP prefix changes', fontsize=20, backgroundcolor= 'silver')
plt.ylabel('Nr of ASNs')
plt.xlabel('Time')
ax.plot(x,a_all, c='red', linewidth=1.0, label='raw')
ax.plot(x[2:],moving_average(a_all), c='green', linewidth=3.0, label='avg (daily)')
weekends = list(map(lambda d: d.weekday() in (6,0), x))
print(len( weekends ))
print(len( x ))
ax.fill_between(x, 0, 1000, where=weekends, facecolor='grey', alpha=0.4)
plt.legend()
fig.autofmt_xdate()
plt.grid(axis='y')
plt.tight_layout()
fig.savefig("nets_w_orig_change.png")
#ax.set_yscale('log')
#ax2.set_yscale('log')
#fig.savefig("nets_w_orig_changes.log.png")


