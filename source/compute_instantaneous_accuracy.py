import argparse
from online_eval_online_action_detection import OnlineEvalOAD


def parse_input_args():

    description = ('Online evaluation for Online Action Detection. This '
                   'script evaluates the performance of a method for Online '
                   'Action Detection.')

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-d', default='Noname', help='Dataset name.')
    parser.add_argument('-gt', help='Ground Truth file.')
    parser.add_argument('-subset', default='Test', help='Dataset subset.')
    parser.add_argument('-pred', help='Prediction file.')
    parser.add_argument('-pkl', default='../pkl/ia.pkl', help='File to store' 
                                                              'info about '
                                                              'evaluation.')

    return parser.parse_args()


if __name__ == '__main__':
    # Get input arguments
    dataset, gt, subset, pred, info_pkl = vars(parse_input_args()).values()

    # Online Action Detection Evaluation class
    eval_oad = OnlineEvalOAD(dataset, subset, gt, pred, info_pkl)

    # Start online evaluation for each video
    eval_oad.online_eval()
