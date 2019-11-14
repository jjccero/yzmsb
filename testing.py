from t_init import *

import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"




def crack_captcha(imgname='c.jpg'):
    saver = tf.train.Saver()
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        saver.restore(sess, MODELS_PATH)
        batch_x = zeros([1, IMAGE_HEIGHT * IMAGE_WIDTH])
        img = Image.open(imgname)
        img = img.convert("L")
        image_array = array(img)[:IMAGE_HEIGHT, :IMAGE_WIDTH]
        x = image_array.flatten() / 255
        batch_x[0, :] = x
        text = sess.run(ix, feed_dict={X: batch_x, keep_prob: 1})
        res = ''
        for e in text[0, :]:
            res += alphabet[int(e)]
        sess.close()
    return res

# for f in os.listdir('images'):
#     x=crack_captcha('images/'+f)
#     y=f[0:4]
#     if x!=y:
#         print(x,y)

