from dataset import load_movielens_100k, load_movielens_1m, to_tensor
import model
import tensorflow as tf
slim = tf.contrib.slim

flags = tf.app.flags
FLAGS = flags.FLAGS

if __name__ == '__main__':
	with tf.Graph().as_default():
		tf.logging.set_verbosity(tf.logging.INFO)
		
		trainset, testset = load_movielens_1m()
		fullset = trainset + testset
		X = to_tensor(trainset)
		y = to_tensor(fullset)
		logits, _ = model.AE(X, is_training=False)

		names_to_values, names_to_updates = model.error_metrics(logits, y)
		
		logdir = 'trainAE.log'
		checkpoint_path = tf.train.latest_checkpoint(logdir)
		metric_values = slim.evaluation.evaluate_once(
			master='',
			checkpoint_path=checkpoint_path,
			logdir=logdir,
			eval_op=list(names_to_updates.values()),
			final_op=list(names_to_values.values()))

		names_to_values = dict(zip(list(names_to_values.keys()), metric_values))
		for name in names_to_values:
			print('%s: %f' % (name, names_to_values[name]))
