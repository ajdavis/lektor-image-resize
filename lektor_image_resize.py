# -*- coding: utf-8 -*-
import re
from warnings import warn

import click
from lektor.build_programs import AttachmentBuildProgram, buildprogram
from lektor.context import get_ctx
from lektor.db import Image
from lektor.imagetools import computed_height, get_image_info, resize_image
from lektor.pluginsystem import Plugin
from werkzeug.utils import cached_property


@buildprogram(Image)
class ResizedImageBuildProgram(AttachmentBuildProgram):
    def build_artifact(self, artifact):
        ctx = get_ctx()
        plugin = ctx.env.plugins['image-resize']
        max_width = plugin.max_width

        if max_width is None or not plugin.should_resize(artifact):
            # Not configured.
            AttachmentBuildProgram.build_artifact(self, artifact)
            return

        source_img = artifact.source_obj.attachment_filename

        with open(source_img, 'rb') as f:
            _, w, h = get_image_info(f)
            if w <= max_width:
                # Don't resize.
                AttachmentBuildProgram.build_artifact(self, artifact)
                return

        height = computed_height(source_img, max_width, w, h)
        artifact.ensure_dir()
        resize_image(ctx, source_img, artifact.dst_filename, max_width, height)


class ImageResizePlugin(Plugin):
    name = u'image-resize'
    description = u'Add your description here.'
    image_exts = ['png', 'jpg', 'jpeg', 'gif']

    def on_setup_env(self, **extra):
        if self.max_width is None:
            msg = 'Add "max_width = <number>" to "configs/%s.ini"' % self.id
            click.echo(click.style('W', fg='red') + ' ' + msg)

    @cached_property
    def max_width(self):
        return self.get_config().get_int('max_width')

    @cached_property
    def models(self):
        models = self.get_config().get('models')
        if not models:
            return None

        return re.findall(r"[\w\-]+", models)

    def should_resize(self, artifact):
        """Is this an attachment of a model included in "models" in config?"""
        if not self.models:
            # All models allow auto-resize.
            return True

        model = artifact.source_obj.parent.datamodel.id
        return model in self.models
