from t_init import *

output = crack_captcha_cnn()
saver = tf.train.Saver()


def crack_captcha(imgname='c.jpg'):
    #with tf.Session() as sess: CPU版
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        saver.restore(sess, MODELS_PATH)
        predict = tf.argmax(tf.reshape(output, [-1, CAPTCHA_LEN, CHAR_SET_LEN]), 2)
        batch_x = zeros([1, IMAGE_HEIGHT * IMAGE_WIDTH])
        img = Image.open(imgname)
        img = img.convert("L")
        image_array = array(img)[:IMAGE_HEIGHT, :IMAGE_WIDTH]
        x = image_array.flatten() / 255
        batch_x[0, :] = x
        text = sess.run(predict, feed_dict={X: batch_x, keep_prob: 1})
        res = ''
        for e in text[0, :]:
            res += alphabet[int(e)]
        sess.close()
    return res


