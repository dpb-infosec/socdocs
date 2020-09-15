---
bookCollapseSection: true
weight: 10
---

# Introduction

This subdirectory contains all rules.

Rules trigger actions or alert on specific events  and may consist out of building blocks, or may 

# How to Create a good rule

The best way to build a good rule is first define:
* What is good behavior?
* What is bad behavior?
* Which log sources can adequately provide the information I need to determine this behavior?
* Where does this map within the MaGMa Framework?

From there on, create logical blocks of reusable code (aka Building Blocks)
Keep in mind that the way you construct the building block impacts the performance of the CRE (custom rule engine) 
* Start off with filters that eliminate lots of events (e.g. QID filters, Log Source filters, Log Source Type Filters). 
* Try to work with indexed fields as much as possible
* All regular expressions go last.

For the rule itself make sure to add a description and a changelog. Copy-Paste the block below as a template to let it generate nicely in our documentation.

```
<Description goes here>

## Changelog

|Date|Description|Username|
|------------|----------------------|----------|
|<YYYY/MM/DD>|<Describe your change>|<Username>|
|<YYYY/MM/DD>|<Describe your change>|<Username>|
|<YYYY/MM/DD>|<Describe your change>|<Username>|

```

## How to tune out exceptions

It is unavoidable that some rules will have exceptions. Use the same rules as above to define this known good behavior, but make sure it is as precise as possible. After all, excluding too many may lead to false negatives. As a general rule of thumb:
* Create a Building block for the exception
* Use a reference set/map/table in the building block if multiple exceptions are needed.