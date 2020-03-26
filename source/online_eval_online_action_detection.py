import json
import math
import numpy as np
import pickle as pkl


def build_grid(segments, n_slots, slot):

    # Build action grid for gt
    grid = np.ones((1, n_slots), dtype=object) * 'Background'
    for ann in segments:
        i_slot = int(math.floor(ann['segment'][0] / slot))
        e_slot = int(math.floor(ann['segment'][1] / slot))
        grid[0, i_slot:e_slot] = ann['label']

    return grid


def instantaneous_accuracy(vid_gt, vid_pred, d, slot):

    # Number of slots to be evaluated until duration
    n_slots = int(math.ceil(d / slot))

    # Build action grid for gt and prediction
    agrid_gt = build_grid(vid_gt['annotations'], n_slots, slot)
    agrid_pr = build_grid(vid_pred, n_slots, slot)

    # Arrays to store factors and weights to compute IA
    tp = np.zeros((1, n_slots), dtype=float)
    tn = np.zeros((1, n_slots), dtype=float)
    fp = np.zeros((1, n_slots), dtype=float)
    fn = np.zeros((1, n_slots), dtype=float)
    tnw = np.zeros((1, n_slots), dtype=float)
    tpw = np.zeros((1, n_slots), dtype=float)

    # Factors and weights
    for i, v in enumerate(agrid_gt[0, :]):
        # Factor
        if agrid_pr[0, i] == 'Background' and v == agrid_pr[0, i]:
            # It's a true negative
            tn[0, i] = 1.0
        elif agrid_pr[0, i] != 'Background' and v == agrid_pr[0, i]:
            # It's a true positive
            tp[0, i] = 1.0
        elif agrid_pr[0, i] != 'Background' and v != agrid_pr[0, i]:
            # It's a false positive
            fp[0, i] = 1.0
        elif agrid_pr[0, i] == 'Background' and v != agrid_pr[0, i]:
            # It's a false negative
            fn[0, i] = 1.0

        # Weights
        n_action = float((agrid_gt[0, 0:i + 1] != 'Background').sum())
        n_bg = float((agrid_gt[0, 0:i + 1] == 'Background').sum())

        # Weights aren't considered until different action/background number
        if n_action == 0.0 or n_bg == 0.0:
            tpw[0, i] = 1.0
            tnw[0, i] = 1.0
        else:
            tpw[0, i] = n_bg / n_action
            tnw[0, i] = n_action / n_bg

    # Accumulate factors for each slot
    tp = np.cumsum(tp)
    tn = np.cumsum(tn)
    fp = np.cumsum(fp)
    fn = np.cumsum(fn)

    # Computing Instantaneous Accuracy
    ia = (tp * tpw + tn * tnw) / (tp + tn + fp + fn)
    nw_ia = (tp + tn) / (tp + tn + fp + fn)

    return ia, nw_ia


class OnlineEvalOAD:

    def __init__(self, dataset, subset, gt_json, result_json, f_pkl='./ia.pkl'):

        # Set dataset
        self.dataset = dataset
        self.subset = subset

        # Files
        self.gt_json = gt_json
        self.result_json = result_json
        self.eval_info_pkl = f_pkl

        # Parameter of Instantaneous Accuracy metric
        self.slot = 0.5

        print('Collecting ground truth and results...')

        # Loading gt and remove videos from other subsets
        with open(self.gt_json, 'r') as f:
            self.gt = json.load(f)
        for videoid, v in list(self.gt['database'].items()):
            if self.gt['database'][videoid]['subset'] == self.subset:
                continue
            else:
                del self.gt['database'][videoid]

        # Load predictions
        with open(self.result_json, 'r') as f:
            self.pred = json.load(f)

    def online_eval(self):

        # Dict to save metric stuff
        eval_info = dict()
        eval_info['results-by-video'] = dict()
        eval_info['slot'] = self.slot

        # List to save values
        aia = list()
        nw_aia = list()

        print('Computing Instantaneous Accuracy for each video...')

        # Iterate over videos to compute IA for each video
        for videoid, v in self.gt['database'].items():
            # Get gt of this video
            vid_gt = self.gt['database'][videoid]

            # Check if video was used
            try:
                vid_pred = self.pred['results'][videoid]
            except:
                continue

            # Get duration of this video
            d = self.gt['database'][videoid]['duration']

            # Compute IA
            ia, nw_ia = instantaneous_accuracy(vid_gt, vid_pred, d, self.slot)

            # Compute average instantaneous accuracy
            vid_aia = np.mean(ia)
            aia.append(vid_aia)
            vid_nw_aia = np.mean(nw_ia)
            nw_aia.append(vid_nw_aia)

            # Save stuff about the video
            this_vid_info = {'IA': ia,
                             'nw-IA': nw_ia,
                             'aIA': aia,
                             'nw-aIA': nw_aia,
                             }
            eval_info['results-by-video'][videoid] = this_vid_info

        print('Calculating mean average Instantaneous Accuracy...')
        # Compute mean average instantaneous accuracy (maIA)
        maia = np.mean(np.array(aia))
        nw_maia = np.mean(np.array(nw_aia))

        print('Saving results...')

        # Save metric
        eval_info['maIA'] = maia
        eval_info['nw-maIA'] = nw_maia

        # Save file with this dataset results
        with open(self.eval_info_pkl, 'wb') as f:
            pkl.dump(eval_info, f)

        # Done
        print('maIA: {0:.4f}'.format(maia))
        print('Check generated .pkl file for more information.')

        return
