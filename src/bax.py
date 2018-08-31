import matplotlib.pyplot as plt 
from matplotlib import gridspec
import matplotlib.ticker as ticker

class BrokenYAxesProxy:
    def __init__(self, ylims=None, num_twiny_axes=2):

        # Geometry

        self.ylims  = ylims
        self.fig = plt.figure(figsize=(6, 8))
        self.gridspecs = gridspec.GridSpec(
            len(ylims) if ylims else 1,
            1,
            height_ratios=list(reversed([ylim[1] - ylim[0] for ylim in ylims]))
        )
        self.axes = list(self.create_axes())
        self.twiny_axes = [
            [ax.twiny() for ax in self.axes] for i in range(num_twiny_axes)
        ]
        for ax, ylim in zip(self.axes, list(reversed(ylims))):
            ax.set_ylim(*ylim)
        # for twinx_axes in self.twinx_axes:
        #     for ax, ylim in zip(twinx_axes, list(reversed(ylims))):
        #         ax.set_ylim(*ylim)
 
        # Axes
        #for ax in self.axes[:-1] + self.twin_axes[:-1]:
        for ax in self.axes[:-1] + [ax for twiny_axes in self.twiny_axes for ax in twiny_axes[:-1] ]:
            #ax.spines['bottom'].set_visible(False)
            ax.spines['bottom'].set_linewidth(.5)
            #ax.spines['bottom'].set_alpha(.5)
            ax.spines['bottom'].set_linestyle('dotted')
            ax.tick_params(
                labelbottom=False,
                bottom=False,
                which='major'
            ) 
            ax.tick_params(
                labelbottom=False,
                bottom=False,
                which='minor'
            ) 
 
        for ax in self.axes[1:] + [ax for twiny_axes in self.twiny_axes for ax in twiny_axes[1:]]:
            #ax.spines['top'].set_visible(False)
            ax.spines['top'].set_linewidth(.5)
            #ax.spines['top'].set_alpha(.5)
            ax.spines['top'].set_linestyle('dotted')
            ax.tick_params(
                labeltop=False,
                top=False,
                which='major'
            )
            ax.tick_params(
                labeltop=False,
                top=False,
                which='minor'
            )

        for ax in self.axes + [ax for twiny_axes in self.twiny_axes for ax in twiny_axes]:
        #for ax in self.axes + self.twin_axes:
            ax.tick_params(
                direction='in',
                which='major'
            )
            ax.tick_params(
                direction='in',
                which='minor'
            )
            ax.yaxis.set_major_locator(ticker.MultipleLocator(.1))
            ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
            ax.set_axisbelow(True)
        for ax in self.axes:
            ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
            ax.grid(ls='-', which='major', lw=1, c='k', alpha=.2)
            ax.grid(ls='-', which='minor', lw=.5, c='k', alpha=.1)
        self.create_diag(.008, .015)

        # sub_ticks

    def create_axes(self):
        main_ax = None
        for gs in self.gridspecs:
            if main_ax:
                yield plt.subplot(gs, sharex=main_ax if main_ax else None)
            else:
                main_ax = plt.subplot(gs)
                yield main_ax
    
    def plot(self, *args, **kwargs):
        return [
            ax.plot(*args, **kwargs) for ax in self.axes
        ]
    def scatter(self, *args, **kwargs):
        kwargs['alpha'] = .5
        return [
            ax.scatter(*args, **kwargs) for ax in self.axes
        ]
    def set_xlabel(self, *args, **kwargs):
        return self.axes[-1].set_xlabel(*args, **kwargs)
    def set_xlim(self, *args, **kwargs):
        for ax in [ax for twiny_axes in self.twiny_axes for ax in twiny_axes]:
            ax.set_xlim(*args, **kwargs)
        return self.axes[0].set_xlim(*args, **kwargs)
    def create_diag(self, w, h):
        for idx, (ax, ylim) in enumerate(zip(self.axes, self.ylims)):
            y_range = ylim[1] - ylim[0]
            if idx != len(self.axes) - 1:
                ax.plot((0 - w, 0 + w), (0 - h * y_range, 0 + h * y_range),   transform=ax.transAxes, color='k', clip_on=False)
                ax.plot((1 - w, 1 + w), (0 - h * y_range, 0 + h * y_range),   transform=ax.transAxes, color='k', clip_on=False)
            if idx != 0:
                ax.plot((0 - w, 0 + w), (1 - h * y_range, 1 + h * y_range),   transform=ax.transAxes, color='k', clip_on=False)
                ax.plot((1 - w, 1 + w), (1 - h * y_range, 1 + h * y_range),   transform=ax.transAxes, color='k', clip_on=False)

    def set_twin_ax_ticks(self, axis_id: int, ticks, labels, minor_ticks=None, axis_label=None, color='k', xmin=None, xmax=None, inside=False):
        for ax in self.twiny_axes[axis_id]:
            ax.set_xticks(ticks)
            ax.set_xticklabels(labels)
            ax.get_xaxis().set_ticks_position('top')
            ax.get_xaxis().set_label_position('top')
            ax.grid(ls='-', which='major', lw=1, c=color, alpha=.2)
            ax.grid(ls='-', which='minor', lw=.5, c=color, alpha=.1)
            if minor_ticks is not None:
                ax.set_xticks(minor_ticks, minor=True)

        self.twiny_axes[axis_id][0].tick_params(
            labeltop=True,
            top=True,
            color=color,
            labelcolor=color,
            which='major',
            direction='in' if inside else 'out',
            pad= -17 if inside else 0
        )

        if minor_ticks is not None:
            self.twiny_axes[axis_id][0].tick_params(
                labeltop=True,
                top=True,
                color=color,
                labelcolor=color,
                which='minor',
                direction='in' if inside else 'out',
            )

        if axis_label is not None:
            self.twiny_axes[axis_id][0].set_xlabel(
                axis_label,
                labelpad=-34 if inside else 4,
                color = color
            )
        
        # Hide ticks and labels

        for ax in self.axes[:-1] + [ax for twiny_axes in self.twiny_axes for ax in twiny_axes[:-1] ]:
            #ax.spines['bottom'].set_visible(False)
            ax.spines['bottom'].set_linewidth(.5)
            #ax.spines['bottom'].set_alpha(.5)
            ax.spines['bottom'].set_linestyle('dotted')
            ax.tick_params(
                labelbottom=False,
                bottom=False,
                which='major'
            ) 
            ax.tick_params(
                labelbottom=False,
                bottom=False,
                which='minor'
            ) 
 
        for ax in self.axes[1:] + [ax for twiny_axes in self.twiny_axes for ax in twiny_axes[1:]]:
            #ax.spines['top'].set_visible(False)
            ax.spines['top'].set_linewidth(.5)
            #ax.spines['top'].set_alpha(.5)
            ax.spines['top'].set_linestyle('dotted')
            ax.tick_params(
                labeltop=False,
                top=False,
                which='major'
            )
            ax.tick_params(
                labeltop=False,
                top=False,
                which='minor'
            )
