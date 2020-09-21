---
title: QRadar Troubleshooting
type: docs
---

# QRadar Troubleshooting

Here you can find multiple topics that we have learned from in the past and that were noting down.

## Wincollect Agents not responding

TBD

## CRE Performance tuning

This typically pops up after some rule has been modified or created, or a bunch of new logsources has been added. The rule becomes a bottleneck in the CRE pipeline and starts hogging CPU cycles.

1. [Check Threadtop]({{< relref "#check-threadtop" >}}) on the **Event Processor** to see if it is still ongoing ( It could be a temporary hickup). The most efficient syntax i could come up with: `/opt/qradar/support/threadTop.sh -p 7799 -e ".*CRE Processor.*"`
2.  Create an expensive rule report: `/opt/qradar/support/findExpensiveCustomRules.sh -D /tmp`. This will generate a tarball (.tar.gz) in the /tmp directory.
3. Evaluate rule performance
    1. Sort the AverageExecutionTime column and AverageTestTime column to look for large values. This identifies which rules, on average, take more time to run than others. Expensive rules are sorted to the top and typically be a magnitude in size larger than rules running efficiently. Look for values that are 0.01 or larger; these are considered potentially expensive rules that require review.
    2. Review the TotalExecutionTime column to find rules taking much longer to complete than other rules.

Based on this outcome modify the rules that pop-up, typically it will be because of regular expressions being to high up in the filter, positioning is important. Use the rules of thumb defined [here]({{< relref "rules/#how-to-create-a-good-rule" >}}) to fix the rule(s).

## DSM Performance tuning

DSM parsing performance may drop due to a poorly written regular expression in a custom DSM or logsource extension. As with CRE performance drops, this may not be visible until the load increases on a specific parsing property. 

1. [Check Threadtop]({{< relref "#check-threadtop" >}}) on the **Event Collector** that is showing slow performance: `/opt/qradar/support/threadTop.sh -p 7777 -e ".*Event Parser.*"`. This should (currently) show you 8 threads with about 200 ms per thread.
2. Create an expensive custom properties report: `/opt/qradar/support/findExpensiveCustomProperties.sh -D /tmp`. This will generate a tarball (.tar.gz) in the /tmp directory.
3. Evaluate the performance of the custom properties:
    1. Sort on longest match: the longer the matches can be, the longer the CPU will need to process the regular expression.
    2. Sort on average: determines the average processing time required per hit. The higher this is, the longer it will take to complete parsing, thus hogging the parsing queue

## Check Threadtop

IBM Support has an entire folder full of goodies to use, this script will connect to the JMX port of the qradar Java Process, and allows you to see the threads that take up the most MSecs. 

You can run the script without any parameters, and it will collect information from all Processes at once. The downside of doing this is that it is pretty slow.
Below an example from our Consoles (Which also function as Event processors -> AIO):

```shell
[root@qradar]#  /opt/qradar/support/threadTop.sh
System Time: 10/09/2020 at 09:39:42.617
Server          ID     MSecs  Name
--------------  -----  -----  ------------------------------------------
ecs-ec-ingress     81   2231  pool-2-thread-1
ariel_proxy       281    607  hour_idx_46
ariel_proxy       262    571  hour_idx_36
ariel_proxy       216    404  hour_idx_12
ariel_proxy       241    368  hour_idx_31
ariel_proxy       220    335  hour_idx_15
ariel_proxy       265    307  hour_idx_39
hostcontext       163    300  ConfigChangeObserver Timer[1]
ariel_proxy       228    292  hour_idx_21
ecs-ep            220    285  CRE Processor [11]
ariel_proxy       227    282  hour_idx_20
ecs-ep            212    279  CRE Processor [3]
ariel_proxy       240    278  hour_idx_30
ariel_proxy       128    267  hour_idx_2
ariel_proxy       129    264  hour_idx_3
ecs-ep            222    262  CRE Processor [13]
ecs-ep            219    261  CRE Processor [10]
ecs-ep            218    256  CRE Processor [9]
ecs-ep            210    255  CRE Processor [1]
ecs-ep            205    252  CRE Processor [0]
--------------  -----  -----  ------------------------------------------
                        8356  Total (8356/2000)
```

Important to notice is that different roles in QRadar are running as different Java Processes. 
It may be more interesting to pick a specific process that you want to investigate:

* ecs-ep --> event processing ( rule evaluation)
* hostcontext --> event collection
* ariel_query_server and proxy --> search performance

As the ports bound to these processes may change in the future, here's a command (and output) with which you can find all components and JMX ports for those components:

```shell
[root@qradar]# grep -s JMXPORT /opt/qradar/systemd/env/*
/opt/qradar/systemd/env/accumulator:JMXPORT="7791"
/opt/qradar/systemd/env/accumulator_rollup:JMXPORT="7795"
/opt/qradar/systemd/env/arc_builder:JMXPORT=7792
/opt/qradar/systemd/env/ariel_proxy_server.ariel_proxy:JMXPORT="7782"
/opt/qradar/systemd/env/ariel_query_server.ariel:JMXPORT="7782"
/opt/qradar/systemd/env/assetprofiler:JMXPORT=7780
/opt/qradar/systemd/env/data_export:JMXPORT=7794
/opt/qradar/systemd/env/dataNode:JMXPORT=7794
/opt/qradar/systemd/env/ecs-ec:JMXPORT="7777"
/opt/qradar/systemd/env/ecs-ec-ingress:JMXPORT="7787"
/opt/qradar/systemd/env/ecs-ep:JMXPORT="7799"
/opt/qradar/systemd/env/ha_manager:JMXPORT=7788
/opt/qradar/systemd/env/historical_correlation_server:JMXPORT=7783
/opt/qradar/systemd/env/hostcontext:JMXPORT=7778
/opt/qradar/systemd/env/masterdaemon:JMXPORT="7700"
/opt/qradar/systemd/env/offline_forwarder:JMXPORT=7793
/opt/qradar/systemd/env/qvmhostedscanner:JMXPORT="8990"
/opt/qradar/systemd/env/qvmprocessor:JMXPORT="8989"
/opt/qradar/systemd/env/qvmscanner:#    JMXPORT="8989"
/opt/qradar/systemd/env/qvmscanner:JMXPORT="8989"
/opt/qradar/systemd/env/reporting_executor:JMXPORT=7781
/opt/qradar/systemd/env/tomcat:JMXPORT=7779
/opt/qradar/systemd/env/tomcat-forensics:JMXPORT=7788
/opt/qradar/systemd/env/tomcat-rm:JMXPORT=5791
/opt/qradar/systemd/env/vis:JMXPORT=7790
```
