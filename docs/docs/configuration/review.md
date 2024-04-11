---
id: review
title: Review
---

Review items are saved as periods of time where frigate detected events. After watching the preview of a review item it is marked as reviewed.

## Restricting alerts to specific object types

By default a review item will only be marked as an alert if a person or car is detected. This can be configured using the following config:

```yaml
# can be overridden at camera level
objects:
  alert:
    - car
    - cat
    - dog
    - person
```

## Restricting alerts to specific zones

By default a review item will be marked as an alert if any `objects -> alert` is detected anywhere in the camera frame. You will likely want to configure review items to only be marked as an alert when the object enters an area of interest, [see the zone docs for more information](./zones.md#restricting-alerts-to-specific-zones)
