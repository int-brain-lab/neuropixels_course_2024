"""Add IBL cluster metrics to display"""

import logging
import numpy as np
from phy import IPlugin
import pandas as pd
from pathlib import Path

logger = logging.getLogger('phy')

try:
    import brainbox.metrics.single_units as su
    COMPUTE = True
except ImportError:
    logger.warning('Failed to import ibllib.brainbox')
    COMPUTE = False


class IBLMetricsPlugin(IPlugin):
    def attach_to_controller(self, controller):
        """Note that this function is called at initialization time, *before* the supervisor is
        created. The `controller.cluster_metrics` items are then passed to the supervisor when
        constructing it."""

        clusters_file = Path(controller.dir_path.joinpath('clusters.metrics.pqt'))
        if clusters_file.exists():
            self.metrics = pd.read_parquet(clusters_file)
            self.metrics['cluster_idx'] = self.metrics.index
        else:
            self.metrics = None
            return

        def get_metric(cluster_id, metric_name, metric_function):
            try:
                val = self.metrics.loc[self.metrics['cluster_idx'] == cluster_id, metric_name]
                if len(val) == 0 and COMPUTE:
                    metric_val = metric_function(cluster_id)
                    self.metrics.loc[self.metrics.shape[0] + 1, 'cluster_idx'] = cluster_id
                    self.metrics.loc[self.metrics['cluster_idx'] == cluster_id, metric_name] = metric_val
                elif np.isnan(val.values[0]) and COMPUTE:
                    metric_val = metric_function(cluster_id)
                    self.metrics.loc[self.metrics['cluster_idx'] == cluster_id, metric_name] = metric_val
                else:
                    metric_val = val.values[0]
            except Exception as err:
                metric_val = np.nan
                logger.warning(f'Failed to get metric {metric_name} for {cluster_id}: {err}')

            return metric_val

        def amp_median(cluster_id):

            return get_metric(cluster_id, 'amp_median', compute_amp_median) * 1e6

        def compute_amp_median(cluster_id):
            amps = controller.get_amplitudes(cluster_id, load_all=True)
            amps_log = 20 * np.log10(amps)
            return 10 ** (np.median(amps_log) / 20)

        def noise_cutoff(cluster_id):

            return get_metric(cluster_id, 'noise_cutoff', compute_noise_cutoff)

        def compute_noise_cutoff(cluster_id):
            amps = controller.get_amplitudes(cluster_id, load_all=True)
            _, cutoff, _ = su.noise_cutoff(amps, **su.METRICS_PARAMS['noise_cutoff'])
            return cutoff

        def max_confidence(cluster_id):

            return get_metric(cluster_id, 'max_confidence', compute_max_confidence)

        def compute_max_confidence(cluster_id):
            times = controller.get_spike_times(cluster_id)
            res = su.metrics.slidingRP(times, conf_thres=90, cont_thresh=10, rp_reject=0.0005, sampleRate=30000,
                                       binSizeCorr=1/30000)
            return res[0]

        def label(cluster_id):
            return get_metric(cluster_id, 'label', compute_label)

        def compute_label(cluster_id):
            metrics = self.metrics.loc[self.metrics['cluster_idx'] == cluster_id]
            labels = np.c_[metrics['max_confidence'].values[0] >= su.METRICS_PARAMS['RPmax_confidence'],
                           metrics['noise_cutoff'].values[0] < su.METRICS_PARAMS['noise_cutoff']['nc_threshold'],
                           metrics['amp_median'].values[0] > su.METRICS_PARAMS['med_amp_thresh_uv'] / 1e6]
            return np.mean(labels, axis=1).astype(np.float64)

        controller.cluster_metrics['amp_median'] = controller.context.memcache(amp_median)
        controller.cluster_metrics['noise_cutoff'] = controller.context.memcache(noise_cutoff)
        controller.cluster_metrics['max_confidence'] = controller.context.memcache(max_confidence)
        controller.cluster_metrics['label'] = controller.context.memcache(label)

