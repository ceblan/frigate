---
id: plus
title: BIS-IA+
---

For more information about how to use BIS-IA+ to improve your model, see the [BIS-IA+ docs](/plus/).

## Setup

### Create an account

Free accounts can be created at [https://plus.bisia.video](https://plus.bisia.video).

### Generate an API key

Once logged in, you can generate an API key for BIS-IA in Settings.

![API key](/img/plus-api-key-min.png)

### Set your API key

In BIS-IA, you can use an environment variable or a docker secret named `PLUS_API_KEY` to enable the `BIS-IA+` buttons on the Explore page. Home Assistant App users can set it under Settings > Apps > BIS-IA > Configuration > Options (be sure to toggle the "Show unused optional configuration options" switch).

:::warning

You cannot use the `environment_vars` section of your BIS-IA configuration file to set this environment variable. It must be defined as an environment variable in the docker config or Home Assistant App config.

:::

## Submit examples

Once your API key is configured, you can submit examples directly from the Explore page in BIS-IA. From the More Filters menu, select "Has a Snapshot - Yes" and "Submitted to BIS-IA+ - No", and press Apply at the bottom of the pane. Then, click on a thumbnail and select the Snapshot tab.

You can use your keyboard's left and right arrow keys to quickly navigate between the tracked object snapshots.

:::note

Snapshots must be enabled to be able to submit examples to BIS-IA+

:::

![Submit To Plus](/img/plus/submit-to-plus.jpg)

### Annotate and verify

You can view all of your submitted images at [https://plus.bisia.video](https://plus.bisia.video). Annotations can be added by clicking an image. For more detailed information about labeling, see the documentation on [annotating](../plus/annotating.md).

![Annotate](/img/annotate.png)

## Use Models

Once you have [requested your first model](../plus/first_model.md) and gotten your own model ID, it can be used with a special model path. No other information needs to be configured for BIS-IA+ models because it fetches the remaining config from BIS-IA+ automatically.

You can either choose the new model from the BIS-IA+ pane in the Settings page of the BIS-IA UI, or manually set the model at the root level in your config:

```yaml
detectors: ...

model:
  path: plus://<your_model_id>
```

:::note

Model IDs are not secret values and can be shared freely. Access to your model is protected by your API key.

:::

Models are downloaded into the `/config/model_cache` folder and only downloaded if needed.

If needed, you can override the labelmap for BIS-IA+ models. This is not recommended as renaming labels will break the Submit to BIS-IA+ feature if the labels are not available in BIS-IA+.

```yaml
model:
  path: plus://<your_model_id>
  labelmap:
    3: animal
    4: animal
    5: animal
```
