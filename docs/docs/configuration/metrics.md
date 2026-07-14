---
id: metrics
title: Metrics
---

# Metrics

BIS-IA exposes Prometheus metrics at the `/api/metrics` endpoint that can be used to monitor the performance and health of your BIS-IA instance.

## Available Metrics

### System Metrics
- `bisia_cpu_usage_percent{pid="", name="", process="", type="", cmdline=""}` - Process CPU usage percentage
- `bisia_mem_usage_percent{pid="", name="", process="", type="", cmdline=""}` - Process memory usage percentage
- `bisia_gpu_usage_percent{gpu_name=""}` - GPU utilization percentage
- `bisia_gpu_mem_usage_percent{gpu_name=""}` - GPU memory usage percentage

### Camera Metrics
- `bisia_camera_fps{camera_name=""}` - Frames per second being consumed from your camera
- `bisia_detection_fps{camera_name=""}` - Number of times detection is run per second
- `bisia_process_fps{camera_name=""}` - Frames per second being processed
- `bisia_skipped_fps{camera_name=""}` - Frames per second skipped for processing
- `bisia_detection_enabled{camera_name=""}` - Detection enabled status for camera
- `bisia_audio_dBFS{camera_name=""}` - Audio dBFS for camera
- `bisia_audio_rms{camera_name=""}` - Audio RMS for camera

### Detector Metrics
- `bisia_detector_inference_speed_seconds{name=""}` - Time spent running object detection in seconds
- `bisia_detection_start{name=""}` - Detector start time (unix timestamp)

### Storage Metrics
- `bisia_storage_free_bytes{storage=""}` - Storage free bytes
- `bisia_storage_total_bytes{storage=""}` - Storage total bytes
- `bisia_storage_used_bytes{storage=""}` - Storage used bytes
- `bisia_storage_mount_type{mount_type="", storage=""}` - Storage mount type info

### Service Metrics
- `bisia_service_uptime_seconds` - Uptime in seconds
- `bisia_service_last_updated_timestamp` - Stats recorded time (unix timestamp)
- `bisia_device_temperature{device=""}` - Device Temperature

### Event Metrics
- `bisia_camera_events{camera="", label=""}` - Count of camera events since exporter started

## Configuring Prometheus

To scrape metrics from BIS-IA, add the following to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'bisia'
    metrics_path: '/api/metrics'
    static_configs:
      - targets: ['bisia:5000']
    scrape_interval: 15s
```

## Example Queries

Here are some example PromQL queries that might be useful:

```promql
# Average CPU usage across all processes
avg(bisia_cpu_usage_percent)

# Total GPU memory usage
sum(bisia_gpu_mem_usage_percent)

# Detection FPS by camera
rate(bisia_detection_fps{camera_name="front_door"}[5m])

# Storage usage percentage
(bisia_storage_used_bytes / bisia_storage_total_bytes) * 100

# Event count by camera in last hour
increase(bisia_camera_events[1h])
```

## Grafana Dashboard

You can use these metrics to create Grafana dashboards to monitor your BIS-IA instance. Here's an example of metrics you might want to track:

- CPU, Memory and GPU usage over time
- Camera FPS and detection rates
- Storage usage and trends
- Event counts by camera
- System temperatures

A sample Grafana dashboard JSON will be provided in a future update.

## Metric Types

The metrics exposed by BIS-IA use the following Prometheus metric types:

- **Counter**: Cumulative values that only increase (e.g., `bisia_camera_events`)
- **Gauge**: Values that can go up and down (e.g., `bisia_cpu_usage_percent`)
- **Info**: Key-value pairs for metadata (e.g., `bisia_storage_mount_type`)

For more information about Prometheus metric types, see the [Prometheus documentation](https://prometheus.io/docs/concepts/metric_types/).
