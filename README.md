# Lektor Image Auto-Resize Plugin

This plugin automatically resizes image attachments for pages when you build your site.

## Installation

Add `lektor-image-resize` to your project from the command line:

```
lektor plugins add lektor-image-resize
```

See [the Lektor documentation for more instructions on installing plugins](https://www.getlektor.com/docs/plugins/).

## Configuration

Set these options in `configs/image-resize.ini`:

### `max_width`

Required. Maximum width in pixels for resized images:

```ini
max_width = 2048
```

Wider images are proportionally scaled down to `max_width`. Narrower images not resized.

If you need `max_height` as well, submit a pull request!

### `models`

Optional list of datamodels:

```
models = blog-post, page
```

If `models` is configured, then only images attached to these models are resized. The rest are copied from the source to the build directory unaltered.
